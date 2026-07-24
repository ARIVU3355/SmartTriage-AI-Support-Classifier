"""
Labeled support ticket dataset.
Each entry: (subject, body, category)
Categories: Billing, Technical, HR, General
"""

TICKETS = [
    # ── BILLING ──────────────────────────────────────────────────────────────
    ("Invoice not received", "I completed my order last week but have not received my invoice yet. Please send it to my email.", "Billing"),
    ("Incorrect charge on my account", "I was charged $149 but my plan is only $99 per month. Please refund the difference.", "Billing"),
    ("Double payment issue", "I see two identical charges on my credit card for the same subscription. Please reverse one of them.", "Billing"),
    ("Subscription cancellation refund", "I cancelled my subscription 3 days ago and would like to know when the refund will be processed.", "Billing"),
    ("Payment method update", "My credit card expired. I need to update my payment details to continue the service.", "Billing"),
    ("Cannot pay - card declined", "My card is being declined every time I try to pay for the Pro plan. My bank says there is no issue on their end.", "Billing"),
    ("Annual plan discount", "I want to switch from monthly to annual billing. Can you apply the 20% discount I saw advertised?", "Billing"),
    ("VAT invoice needed", "We are a VAT-registered business and need a VAT invoice for our latest payment for tax purposes.", "Billing"),
    ("Overcharged this month", "My bill this month is $50 higher than last month but I did not change my plan or add any services.", "Billing"),
    ("Free trial charged unexpectedly", "I signed up for the free trial but I see a charge of $29 on my statement. This was not disclosed.", "Billing"),
    ("Promo code not applied", "I entered the promo code SAVE20 at checkout but the discount was not applied to my total.", "Billing"),
    ("Request for billing statement", "Can you please send me a complete billing statement for the past 12 months for our accounting records?", "Billing"),
    ("Subscription renewal price changed", "My subscription auto-renewed at a higher price than last year. I was not notified of a price increase.", "Billing"),
    ("Billing address update", "I have moved to a new office and need to update my billing address on the account.", "Billing"),
    ("Unclear fee on invoice", "There is a line item called 'Platform fee - $15' on my invoice that I do not recognize or remember agreeing to.", "Billing"),

    # ── TECHNICAL ────────────────────────────────────────────────────────────
    ("App crashes on startup", "Every time I open the application on my Windows 11 laptop it immediately crashes with an error code 0x80073CF3.", "Technical"),
    ("Cannot login to portal", "I am entering the correct credentials but keep getting 'Invalid username or password'. I have already reset my password twice.", "Technical"),
    ("API rate limit exceeded", "Our integration is hitting a 429 Too Many Requests error even though we are well below the documented rate limit of 1000 req/min.", "Technical"),
    ("Data export broken", "When I click Export CSV on the reports page, the download starts but the file is empty. This started happening after the last update.", "Technical"),
    ("Slow loading times", "The dashboard is taking over 30 seconds to load. This is severely impacting our team's productivity.", "Technical"),
    ("Integration with Slack not working", "The Slack integration stopped posting notifications 2 days ago. I have reconnected it three times with no success.", "Technical"),
    ("File upload size limit error", "I keep getting an error saying the file is too large when trying to upload a 5MB PDF, even though the limit is listed as 25MB.", "Technical"),
    ("Password reset email not arriving", "I requested a password reset 4 times today and none of the emails have arrived. Checked spam folder as well.", "Technical"),
    ("Mobile app sync issue", "Changes I make on the web app are not syncing to my iOS mobile app. My colleague has the same problem.", "Technical"),
    ("Two-factor authentication locked out", "I got a new phone and lost access to my 2FA authenticator app. I cannot log in to my account.", "Technical"),
    ("Webhook not firing", "Our webhook endpoint is not receiving events. The webhook log in the dashboard shows all events as 'delivered' which is incorrect.", "Technical"),
    ("Database connection timeout", "Our cloud database is timing out intermittently during peak hours. Connections drop after exactly 30 seconds.", "Technical"),
    ("Search feature not returning results", "The search bar returns no results for any query. It was working fine yesterday before the maintenance window.", "Technical"),
    ("PDF report generation failing", "When I generate a monthly report in PDF format the system shows a spinner for 5 minutes and then times out.", "Technical"),
    ("Browser extension broken on Chrome", "Your Chrome extension stopped working after the latest Chrome update (version 125). Getting console errors about manifest v3.", "Technical"),
    ("Email notifications stopped", "I am no longer receiving any email notifications for new assignments even though notifications are enabled in settings.", "Technical"),

    # ── HR ───────────────────────────────────────────────────────────────────
    ("Leave balance discrepancy", "My leave balance shows 5 days remaining but I have only taken 3 days this year and started with 15. Please correct this.", "HR"),
    ("Payslip not accessible", "I cannot access my payslips from the employee portal. It shows a blank page after I click on Payslips.", "HR"),
    ("Work from home policy question", "I wanted to understand the current work from home policy. Can someone clarify how many days per week are allowed?", "HR"),
    ("Onboarding documents not received", "I start on Monday but have not received any onboarding documents or instructions from HR yet.", "HR"),
    ("Performance review schedule", "When will the Q2 performance reviews be scheduled? I need to plan my availability for the coming weeks.", "HR"),
    ("Benefit enrollment deadline", "I missed the open enrollment window for health benefits. Is there any way to enroll now or do I have to wait?", "HR"),
    ("Salary increment query", "I was told my salary review would happen in April but it is now June and I have not heard anything.", "HR"),
    ("Maternity leave request", "I am expecting in September and would like to formally apply for maternity leave and understand my entitlements.", "HR"),
    ("Employee ID card replacement", "My ID card was lost during travel. Can HR issue a replacement? What is the process and is there a fee?", "HR"),
    ("Relocation assistance inquiry", "I have been offered a transfer to the New York office. Can you outline what relocation assistance the company provides?", "HR"),
    ("Harassment complaint", "I would like to report a workplace harassment incident confidentially. Please let me know the proper escalation procedure.", "HR"),
    ("Reference letter request", "I need an official employment verification letter for my mortgage application. Can HR provide this?", "HR"),
    ("Training and development program", "I am interested in enrolling in the leadership development program. How do I apply and who approves it?", "HR"),
    ("Exit interview scheduling", "My last day is July 31st. Can someone from HR schedule an exit interview and explain the offboarding process?", "HR"),
    ("Overtime pay not reflected", "I worked 15 extra hours last month but my paycheck does not include overtime pay at the 1.5x rate.", "HR"),

    # ── GENERAL ──────────────────────────────────────────────────────────────
    ("Product roadmap inquiry", "I would like to know what features are planned for the next quarter. Is there a public roadmap available?", "General"),
    ("How to use bulk import feature", "I have 200 records to import. Is there a bulk import feature and where can I find documentation for it?", "General"),
    ("Partnership opportunity", "Our company would like to explore a partnership or reseller arrangement with your organization. Who should I contact?", "General"),
    ("Feedback on recent update", "The new dashboard layout is much harder to navigate than the old one. I would like to share detailed feedback.", "General"),
    ("Compliance and data residency", "We operate in the EU and need to confirm where our data is stored to ensure GDPR compliance.", "General"),
    ("Office hours and support availability", "What are your support hours? I need to know when I can reach a live agent for urgent issues.", "General"),
    ("Feature request - dark mode", "Could you please add a dark mode option to the web application? Several of my team members have requested this.", "General"),
    ("Account team introduction", "We recently upgraded to Enterprise. Who is our assigned account manager and how do we get in touch?", "General"),
    ("Accessibility compliance question", "Is your platform WCAG 2.1 AA compliant? We need this confirmation before our company can proceed with procurement.", "General"),
    ("Service status page", "Is there a status page I can check for service outages? We experienced downtime yesterday and want to be kept informed.", "General"),
    ("Training webinar schedule", "Do you offer onboarding or training webinars for new users? If so, when is the next session?", "General"),
    ("Custom domain setup", "I want to set up a custom domain for my workspace. Is this a supported feature and where do I configure it?", "General"),
    ("Data migration assistance", "We are moving from a competitor and have 3 years of data to migrate. Do you offer migration assistance?", "General"),
    ("White-label options", "We are evaluating your product for potential white-labeling. Can you share the white-label terms and pricing?", "General"),
    ("Company name change on account", "Our company rebranded. How do I update the organization name across all my billing and account details?", "General"),
]
