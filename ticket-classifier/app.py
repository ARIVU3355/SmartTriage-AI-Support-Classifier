import streamlit as st
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Set Page Config for beautiful layout and styling
st.set_page_config(
    page_title="SmartTriage AI — Support Ticket Routing System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Custom fonts and core elements */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
    }
    
    /* Header card */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(30, 60, 114, 0.15);
    }
    
    /* Styled visual status boxes */
    .metric-card {
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    
    .result-container {
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        margin-top: 1rem;
    }
    
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .badge-billing { background-color: #ebf8ff; color: #2b6cb0; border: 1px solid #bee3f8; }
    .badge-technical { background-color: #f0fff4; color: #276749; border: 1px solid #c6f6d5; }
    .badge-hr { background-color: #fff5f5; color: #9b2c2c; border: 1px solid #fed7d7; }
    .badge-general { background-color: #fffaf0; color: #dd6b20; border: 1px solid #feebc8; }
    .badge-review { background-color: #edf2f7; color: #4a5568; border: 1px dashed #cbd5e0; }
    
    .badge-priority-high { background-color: #fff5f5; color: #e53e3e; border: 1px solid #fed7d7; }
    .badge-priority-normal { background-color: #f7fafc; color: #4a5568; border: 1px solid #e2e8f0; }

    /* Custom sidebar elements */
    .sidebar-info {
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LAYER -----------------
# Dynamically import tickets dataset from data.py
try:
    from data import TICKETS
except ImportError:
    st.error("Error: Could not import data.py. Please verify it is in the same directory.")
    st.stop()

# ----------------- MODEL TRAINING LAYER -----------------
@st.cache_resource
def train_model():
    # Preprocess text (combine subject + body)
    texts = [subject + " " + body for subject, body, _ in TICKETS]
    labels = [category for _, _, category in TICKETS]
    
    # Stratified Split for robust evaluation on small dataset (20% test size)
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=42, stratify=labels
    )
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Logistic Regression Model (C=1.0)
    # Selected due to well-calibrated class probabilities (essential for confidence scores)
    classifier = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    classifier.fit(X_train_vec, y_train)
    
    # Compute accuracy & metrics
    y_pred = classifier.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    classes = classifier.classes_
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    
    return classifier, vectorizer, acc, report, cm, classes

# Train classifier
model, vectorizer, accuracy, class_report, conf_matrix, model_classes = train_model()

# ----------------- REAL-TIME TRIAGE LAYER -----------------
def classify_ticket(subject, body, confidence_threshold=0.60):
    text_combined = f"{subject} {body}"
    text_clean = text_combined.lower().strip()
    
    # Vectorize
    vec = vectorizer.transform([text_combined])
    
    # Get probabilities
    probs = model.predict_proba(vec)[0]
    max_idx = np.argmax(probs)
    predicted_category = model_classes[max_idx]
    confidence = probs[max_idx]
    
    # Route category based on threshold
    if confidence < confidence_threshold:
        routed_category = "Needs Human Review"
    else:
        routed_category = predicted_category
        
    # Priority Tagging via keyword matches
    urgent_keywords = [
        "down", "urgent", "not working", "fails", "crashing", "emergency", 
        "immediately", "overcharged", "harassment", "lockout", "crashed", 
        "declined", "limit exceeded", "timeout", "broken", "lost", "stolen",
        "refund", "unauthorized", "blank page", "double payment"
    ]
    is_urgent = any(kw in text_clean for kw in urgent_keywords)
    priority = "High" if is_urgent else "Normal"
    
    return predicted_category, confidence, routed_category, priority

# ----------------- 5 NEW SAMPLE TICKETS -----------------
preset_samples = {
    "Select a preset sample...": ("", ""),
    "Sample 1: Billing (Refund Request)": (
        "Unauthorized billing charge",
        "Hello, I notice a charge of $49 on my account yesterday but I did not upgrade. Please refund this amount as soon as possible."
    ),
    "Sample 2: Technical (Extension Crash)": (
        "Chrome extension crashed after update",
        "The extension freezes immediately upon clicking the login button. I am running Chrome version 126. Console shows a runtime manifest error."
    ),
    "Sample 3: HR (Dental Benefits)": (
        "Dental insurance policy details",
        "Could you please share the registration link for our dental plan? I need to enroll my spouse before the end of this month."
    ),
    "Sample 4: General (API Capabilities)": (
        "Bulk export API support",
        "We are evaluating your enterprise plan and need to confirm if your webhooks support bulk exports in JSON format."
    ),
    "Sample 5: Edge Case (Needs Human Review)": (
        "Onboarding system billing issue",
        "Hi, I am having trouble with the email system setup for our billing workspace setup during my employee onboarding."
    )
}

# ----------------- SIDEBAR INFO -----------------
with st.sidebar:
    st.title("🎯 SmartTriage AI")
    st.markdown("### Support Ticket Classification System")
    st.markdown("This AI-powered assistant automatically routes support tickets to the appropriate department, flagging low-confidence cases for manual triage.")
    
    # Model Stats
    st.markdown("---")
    st.markdown("#### 📊 Model Statistics")
    st.metric(label="Validation Accuracy", value=f"{accuracy * 100:.1f}%")
    st.markdown(f"- **Algorithm:** Logistic Regression\n- **Vectorizer:** TF-IDF Bag-of-Words\n- **Total Training Set:** {len(TICKETS)} tickets")
    
    # Reflection notes
    st.markdown("---")
    st.markdown("#### 💡 Reflection Note")
    st.markdown(
        "*With more time and data, we would improve this routing layer by:*\n"
        "1. **Semantic Embeddings:** Use a pre-trained transformer model (e.g. DistilBERT) to understand conversational context beyond keyword matching.\n"
        "2. **Continuous Learning:** Deploy an active learning loop to update the model dynamically when tickets routed to human review are resolved.\n"
        "3. **Dynamic Keywords:** Adapt priority tagging with a trained urgency classifier instead of hardcoded keywords."
    )

# ----------------- MAIN UI -----------------
# Header banner
st.markdown(f"""
<div class="header-container">
    <h1 style="margin: 0; font-size: 2.2rem;">SmartTriage AI Support Classifier</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
        Automated classification and routing for incoming customer emails and system helpdesk requests.
    </p>
</div>
""", unsafe_allow_html=True)

# Define Tabs
tab1, tab2, tab3 = st.tabs(["⚡ Single Ticket Triage", "📁 Batch File Processing", "📈 Model Diagnostics"])

# Tab 1: Single Ticket Triage
with tab1:
    st.subheader("Real-Time Ticket Routing")
    st.write("Type a ticket subject and body or select a preset sample to see how the model routes it in real time.")
    
    # Preset selection dropdown
    selected_preset = st.selectbox("Load a sample ticket:", list(preset_samples.keys()))
    
    # Retrieve preset contents
    default_subject, default_body = preset_samples[selected_preset]
    
    # Form input fields
    subject_input = st.text_input("Ticket Subject", value=default_subject, placeholder="e.g. Invoices not received")
    body_input = st.text_area("Ticket Body", value=default_body, height=140, placeholder="e.g. I did not receive my subscription invoice for last month...")
    
    # Threshold slider
    conf_threshold = st.slider("Confidence Threshold for Auto-Assignment (%)", min_value=0, max_value=100, value=60, step=5) / 100.0
    
    if st.button("Route Ticket", type="primary") or (subject_input and body_input):
        if not subject_input.strip() or not body_input.strip():
            st.warning("Please enter both a subject and body to classify.")
        else:
            # Predict
            predicted_class, score, routed_class, priority = classify_ticket(
                subject_input, body_input, confidence_threshold=conf_threshold
            )
            
            # CSS badge names
            badge_class = "badge-review" if routed_class == "Needs Human Review" else f"badge-{routed_class.lower()}"
            priority_class = f"badge-priority-{priority.lower()}"
            
            # Show Results in beautiful card
            st.markdown(f"""
            <div class="result-container" style="background-color: {'#f7fafc' if routed_class == 'Needs Human Review' else '#ffffff'};">
                <h3 style="margin-top: 0; color: #1a202c;">Triage Decision</h3>
                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1rem;">
                    <div>
                        <span style="font-size: 0.8rem; color: #718096; display: block; margin-bottom: 3px;">ASSIGNED ROUTE</span>
                        <span class="badge {badge_class}">{routed_class}</span>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem; color: #718096; display: block; margin-bottom: 3px;">PRIORITY</span>
                        <span class="badge {priority_class}">{priority}</span>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem; color: #718096; display: block; margin-bottom: 3px;">AI CONFIDENCE</span>
                        <span class="badge" style="background-color: #edf2f7; color: #2d3748;">{score * 100:.1f}%</span>
                    </div>
                </div>
                <div>
                    <h4 style="margin: 1rem 0 0.5rem 0; font-size: 0.95rem; color: #4a5568;">Confidence Distribution</h4>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Plot probability bars
            text_comb = f"{subject_input} {body_input}"
            vec = vectorizer.transform([text_comb])
            probs = model.predict_proba(vec)[0]
            
            prob_df = pd.DataFrame({
                'Department': model_classes,
                'Confidence (%)': probs * 100
            }).sort_values(by='Confidence (%)', ascending=False)
            
            st.bar_chart(prob_df.set_index('Department'))

# Tab 2: Batch File Processing
with tab2:
    st.subheader("Batch File Processing & Triage")
    st.write("Upload a CSV file containing support tickets with `subject` and `body` columns to automatically categorize them in bulk.")
    
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'subject' not in df.columns or 'body' not in df.columns:
                st.error("Invalid File Format. Please ensure the CSV has 'subject' and 'body' columns.")
            else:
                st.info(f"Loaded {len(df)} tickets successfully. Processing...")
                
                # Perform batch predictions
                pred_categories = []
                confidences = []
                routed_categories = []
                priorities = []
                
                for _, row in df.iterrows():
                    pred_cat, conf, routed, prio = classify_ticket(
                        str(row['subject']), str(row['body']), confidence_threshold=0.60
                    )
                    pred_categories.append(pred_cat)
                    confidences.append(f"{conf * 100:.1f}%")
                    routed_categories.append(routed)
                    priorities.append(prio)
                    
                df['Routed Department'] = routed_categories
                df['Confidence'] = confidences
                df['Priority'] = priorities
                df['AI Raw Prediction'] = pred_categories
                
                st.success("Batch classification complete!")
                
                # Display statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Tickets", len(df))
                with col2:
                    manual_count = sum(1 for r in routed_categories if r == "Needs Human Review")
                    st.metric("Needs Human Review", manual_count, delta=f"{manual_count / len(df) * 100:.1f}%", delta_color="inverse")
                with col3:
                    high_prio_count = sum(1 for p in priorities if p == "High")
                    st.metric("High Priority Tagged", high_prio_count)
                
                st.dataframe(df[['subject', 'Routed Department', 'Confidence', 'Priority', 'body']])
                
                # Provide download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Routed Tickets CSV",
                    data=csv,
                    file_name="routed_support_tickets.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Tab 3: Model Diagnostics
with tab3:
    st.subheader("Model Diagnostic Metrics")
    st.write("Below are detailed metrics showing how the classifier performed during validation.")
    
    col_acc, col_desc = st.columns([1, 3])
    with col_acc:
        st.markdown(f"""
        <div style="text-align: center; border: 1px solid #e2e8f0; border-radius: 12px; padding: 2rem; background-color: #f7fafc;">
            <span style="font-size: 1.1rem; font-weight: 600; color: #4a5568; display: block; margin-bottom: 0.5rem;">Test Accuracy</span>
            <span style="font-size: 3.5rem; font-weight: 700; color: #2b6cb0;">{accuracy * 100:.1f}%</span>
            <p style="font-size: 0.85rem; color: #718096; margin-top: 1rem;">Evaluated using a stratified hold-out split from the labeled data.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_desc:
        st.write("**Why Logistic Regression?**")
        st.write(
            "We chose **Logistic Regression** over Multinomial Naive Bayes. While both are highly efficient baselines for TF-IDF vectors, "
            "Naive Bayes often produces overconfident or extreme probability distributions (near 0% or 100%). "
            "Logistic Regression outputs well-calibrated class probabilities, which are necessary to make accurate fallback "
            "routing decisions when confidence is below 60%."
        )
        
    st.markdown("---")
    st.markdown("### Department Performance Metrics")
    
    # Format class report into dataframe
    report_data = []
    for cls in model_classes:
        metrics = class_report[cls]
        report_data.append({
            "Department": cls,
            "Precision": f"{metrics['precision'] * 100:.1f}%",
            "Recall": f"{metrics['recall'] * 100:.1f}%",
            "F1-Score": f"{metrics['f1-score'] * 100:.1f}%",
            "Support Samples": int(metrics['support'])
        })
    st.table(pd.DataFrame(report_data))
    
    st.markdown("---")
    st.markdown("### Confusion Matrix")
    
    # Render Confusion Matrix as standard table
    cm_df = pd.DataFrame(
        conf_matrix, 
        index=[f"Actual {c}" for c in model_classes], 
        columns=[f"Predicted {c}" for c in model_classes]
    )
    st.dataframe(cm_df)
