# 🎯 SmartTriage AI — Support Ticket Classifier

A lightweight Python web app that automatically reads incoming support tickets and routes them to the correct department in real time — built as part of the **Fobes Skill Itech AI/ML Internship Assessment**.

---

## 📌 What it does

Paste a ticket subject and body into the app, and it instantly predicts one of four categories:

| Category | Example |
|---|---|
| 💳 Billing | "I was charged twice this month" |
| 🔧 Technical | "App crashes on startup" |
| 👥 HR | "I need to apply for maternity leave" |
| 💬 General | "Do you have a dark mode option?" |

---

## ✨ Features

- **Real-time classification** — instant prediction as you type
- **Confidence score** — shows how certain the model is (e.g. 87.3%)
- **Human review fallback** — tickets below 60% confidence are flagged for manual triage
- **Priority tagging** — keywords like *crash*, *urgent*, *refund* trigger a 🔴 High priority badge
- **Batch upload** — drag & drop a CSV of tickets and download the results
- **Model diagnostics** — accuracy, precision, recall, F1-score, and confusion matrix

---

## 🛠 Tech Stack

```
Python 3.x
scikit-learn  →  TF-IDF vectoriser + Logistic Regression
Streamlit     →  interactive web UI
Pandas        →  data handling
NumPy         →  probability calculations
```

---

## 📂 Project Structure

```
ticket-classifier/
├── app.py        # Streamlit web application (main entry point)
├── data.py       # Labeled training dataset (60 sample tickets)
└── README.md     # This file
```

---

## 🚀 Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/your-username/ticket-classifier.git
cd ticket-classifier
```

**2. Install dependencies**
```bash
pip install streamlit scikit-learn pandas numpy
```

**3. Run the app**
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🖥 How to Use

**Single Ticket (Tab 1)**
1. Type or paste a ticket subject and body
2. Adjust the confidence threshold slider if needed
3. Click **Route Ticket** → see the department, confidence %, and priority badge

**Batch Upload (Tab 2)**
1. Upload a CSV with `subject` and `body` columns
2. The app classifies all rows and shows a summary table
3. Download the results as a new CSV

**Model Diagnostics (Tab 3)**
- View validation accuracy, per-class metrics, and a confusion matrix

---

## 🧠 Model Details

| Item | Choice | Reason |
|---|---|---|
| Vectoriser | TF-IDF (English stop words) | Converts raw text into numerical features |
| Classifier | Logistic Regression | Outputs calibrated probabilities — needed for the confidence fallback |
| Split | 80 / 20 stratified | Keeps class balance on the small dataset |

---

## 💡 Reflection — What I'd improve with more time

1. **Transformer embeddings** (e.g. DistilBERT) for semantic understanding beyond keywords
2. **Active learning loop** — use human-reviewed tickets to continuously retrain the model
3. **Dynamic priority detection** — replace hardcoded keywords with a trained urgency classifier

---

## 📄 License

MIT — free to use, modify, and distribute.
