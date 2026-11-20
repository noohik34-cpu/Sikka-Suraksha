
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ============================================
# SIKKA SURAKSHA - GROQ AI FINANCIAL GUARDIAN
# ============================================

load_dotenv()

st.set_page_config(
    page_title="Sikka Suraksha",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()

# ---------------- SESSION STATE ----------------

defaults = {
    "history": [],
    "last_result": None,
    "message_input": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- PROFESSIONAL DESIGN ----------------

st.markdown("""
<style>
/* Main page */
.stApp {
    background: #f3f6fb;
    color: #172b4d;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071b49 0%, #123d75 100%) !important;
}

[data-testid="stSidebar"] > div {
    background: transparent !important;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Remove white alert boxes from sidebar */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #123d75 !important;
    border: 1px solid #5b8bb9 !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] p,
[data-testid="stSidebar"] [data-testid="stAlert"] div,
[data-testid="stSidebar"] [data-testid="stAlert"] span {
    color: #ffffff !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #087ca7 !important;
    color: #ffffff !important;
    border: 1px solid #59b9df !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #0b5f91 !important;
    border-color: #ffffff !important;
}

/* Sidebar inputs */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #123d75 !important;
    color: white !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #6b8eb7 !important;
}

/* Hero */
.hero {
    background: linear-gradient(110deg, #071b49, #087ca7);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 22px;
    color: white;
}

.hero h1 {
    color: white !important;
    font-size: 34px;
    margin-bottom: 8px;
}

.hero p {
    color: #e0f2fe !important;
    margin-bottom: 5px;
}

/* Dashboard metrics */
.metric-card {
    background: #ffffff;
    border: 1px solid #dce6f1;
    border-radius: 15px;
    padding: 20px;
    min-height: 110px;
    box-shadow: 0 3px 12px rgba(7, 27, 73, 0.05);
}

.metric-label {
    color: #64748b;
    font-size: 14px;
}

.metric-value {
    color: #0b2855;
    font-size: 27px;
    font-weight: 750;
}

/* Main buttons */
.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 42px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 600;
}

/* Expanders */
[data-testid="stExpander"] {
    border-radius: 12px;
    border: 1px solid #dce6f1;
}

/* Progress */
.stProgress > div > div {
    border-radius: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    padding: 15px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SCAM DETECTION ----------------

SCAM_PATTERNS = {
    "Fake KYC": [
        "kyc expired", "update kyc", "kyc blocked",
        "account blocked", "verify pan",
        "kyc verification", "bank account blocked",
        "update your kyc"
    ],

    "UPI Collect Fraud": [
        "collect request", "approve request",
        "receive money", "enter your upi pin",
        "payment pending", "approve payment",
        "upi collect", "receive payment"
    ],

    "Remote Access App": [
        "anydesk", "teamviewer", "quick support",
        "remote access", "screen sharing",
        "install this app", "share access code"
    ],

    "OTP / Password Theft": [
        "share otp", "send otp", "otp required",
        "share password", "banking password",
        "tell me your otp"
    ],

    "Suspicious Link": [
        "click this link", "claim reward",
        "free gift", "lottery winner",
        "bit.ly", "tinyurl", "http://"
    ],

    "Threat / Urgency": [
        "account will be closed", "immediately",
        "within 24 hours", "urgent action",
        "police case", "legal action",
        "account suspended", "last warning"
    ],

    "Fake Reward / Lottery": [
        "you have won", "claim your prize",
        "won a lottery", "cash prize",
        "free iphone", "congratulations winner"
    ]
}


def detect_scam(message, already_clicked=False):
    text = message.lower()
    matched = []

    for category, phrases in SCAM_PATTERNS.items():
        if any(phrase in text for phrase in phrases):
            matched.append(category)

    score = 10 if not matched else min(15 + len(matched) * 15, 95)

    if already_clicked:
        score = min(score + 15, 100)

    if score >= 70:
        level = "HIGH RISK"
    elif score >= 40:
        level = "MEDIUM RISK"
    else:
        level = "LOW DETECTED RISK"

    return {
        "score": score,
        "level": level,
        "matched": matched
    }


# ---------------- GROQ AI ENGINE ----------------

def ask_groq(message, detection, already_clicked):

    if not API_KEY:
        return None, "GROQ_API_KEY missing. Check your .env file."

    try:
        client = Groq(
            api_key=API_KEY,
            timeout=25.0,
            max_retries=1
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
You are Sikka Suraksha, an Indian digital financial safety assistant.

Analyze suspicious SMS, WhatsApp messages and emails.

Use simple Hindi or Hinglish.

Give these sections:
1. Verdict
2. Warning signs
3. Why it may be suspicious
4. Recommended action
5. Safety tip

Rules:
- Never ask for OTP, UPI PIN or passwords.
- Never claim certainty without evidence.
- A UPI PIN authorizes payments, not receiving money.
- Explain how to verify messages safely.
- If the user clicked a link or shared information,
  recommend contacting their bank immediately.
- If money was lost to cyber fraud in India,
  mention helpline 1930 and cybercrime.gov.in.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Message:
{message}

Rule-based risk score: {detection['score']}/100
Detected patterns: {detection['matched']}
User already clicked/shared information: {already_clicked}

Give a concise, practical analysis.
"""
                }
            ],
            temperature=0.3,
            max_tokens=800
        )

        answer = response.choices[0].message.content

        if not answer:
            return None, "AI returned an empty response."

        return answer, None

    except Exception as error:
        return None, f"{type(error).__name__}: {str(error)[:400]}"


# ---------------- FALLBACK ENGINE ----------------

def fallback_explanation(detection, already_clicked):

    explanations = {
        "Fake KYC":
            "This message may impersonate a bank to steal KYC or personal information.",

        "UPI Collect Fraud":
            "An unknown UPI collect request can authorize a payment. Never enter your UPI PIN to receive money.",

        "Remote Access App":
            "Remote access applications may allow another person to view or control your device.",

        "OTP / Password Theft":
            "OTP and banking passwords are confidential. Never share them with anyone.",

        "Suspicious Link":
            "This link may lead to a fake website designed to steal personal information.",

        "Threat / Urgency":
            "Scammers often use urgency and threats to pressure people into acting quickly.",

        "Fake Reward / Lottery":
            "Unexpected prize messages may be used to collect money or personal details."
    }

    if detection["matched"]:
        details = "\n\n".join(
            f"- **{item}:** {explanations[item]}"
            for item in detection["matched"]
        )
    else:
        details = (
            "No known scam pattern was detected. "
            "This does not guarantee that the message is genuine."
        )

    if detection["score"] >= 70:
        verdict = "🚨 High risk. Avoid interacting with this message."
    elif detection["score"] >= 40:
        verdict = "⚠️ Medium risk. Verify the sender first."
    else:
        verdict = "Potentially low risk. Verify independently."

    if already_clicked:
        action = (
            "Contact your bank immediately if credentials may be compromised. "
            "If money was lost to cyber fraud in India, call 1930."
        )
    else:
        action = (
            "Do not click unknown links or share OTP, UPI PIN or passwords."
        )

    return f"""
### Verdict
{verdict}

### Detected Warning Signs
{details}

### Recommended Action
{action}

### Safety Tip
A UPI PIN is used to authorize payments, not to receive money.
"""


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🛡️ SIKKA SURAKSHA")
    st.caption("Your Financial Safety Companion")

    st.divider()

    st.markdown("### System Status")

    if API_KEY:
        st.markdown(
            '<div style="background:#123d75;border:1px solid #48a878;'
            'padding:12px;border-radius:10px;color:white;">'
            '🟢 Groq API key loaded</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div style="background:#123d75;border:1px solid #d69e36;'
            'padding:12px;border-radius:10px;color:white;">'
            '🟡 API key missing - fallback active</div>',
            unsafe_allow_html=True
        )

    st.write("")
    st.caption(f"Model: {MODEL}")
    st.caption("Detection: Rule-based + AI")

    if st.button("🔌 Test Groq Connection", use_container_width=True):

        if not API_KEY:
            st.error("Add GROQ_API_KEY to your .env file.")
        else:
            try:
                client = Groq(
                    api_key=API_KEY,
                    timeout=15.0,
                    max_retries=0
                )

                test = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "user", "content": "Reply only: Connected"}
                    ],
                    max_tokens=30
                )

                st.markdown(
                    '<div style="background:#123d75;border:1px solid #48a878;'
                    'padding:10px;border-radius:10px;color:white;">'
                    '✅ ' + (test.choices[0].message.content or "Connected")
                    + '</div>',
                    unsafe_allow_html=True
                )

            except Exception as error:
                st.error(f"{type(error).__name__}: {str(error)[:300]}")

    st.divider()

    st.markdown("### Safety Reminders")
    st.markdown("""
- Never share OTP or UPI PIN.
- Never approve unknown collect requests.
- Never install unknown remote access apps.
- Verify suspicious messages independently.
- Contact your bank through official channels.
""")

    st.divider()
    st.caption("Sikka Suraksha | Financial Safety")


# ---------------- MAIN HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🛡️ Sikka Suraksha</h1>
    <p>Your AI-powered financial safety companion.</p>
    <p>Detect suspicious messages. Protect your money. Build safer habits.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- METRICS ----------------

history = st.session_state.history

history_count = len(history)
high_risk_count = sum(
    1 for item in history if item["score"] >= 70
)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">'
        f'Messages Analysed</div><div class="metric-value">'
        f'{history_count}</div></div>',
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">'
        f'High Risk Alerts</div><div class="metric-value">'
        f'{high_risk_count}</div></div>',
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        '<div class="metric-card"><div class="metric-label">'
        'Protection Mode</div><div class="metric-value" '
        'style="font-size:19px">AI + RULES</div></div>',
        unsafe_allow_html=True
    )

st.write("")


# ---------------- TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Scam Detection",
    "💰 Smart Budget",
    "🛡️ Safety Score",
    "📜 Activity History"
])


# ============================================
# TAB 1 - SCAM DETECTION
# ============================================

with tab1:

    st.subheader("Check a Suspicious Message")

    st.write(
        "Paste an SMS, WhatsApp message or email "
        "to check for potential financial fraud."
    )

    samples = {
        "Fake KYC": (
            "Your bank account will be blocked today. "
            "Update your KYC immediately by clicking this link."
        ),

        "UPI Collect": (
            "Your payment is pending. Approve this UPI collect "
            "request and enter your UPI PIN to receive money."
        ),

        "Remote App": (
            "Install AnyDesk and share your access code "
            "to receive your refund."
        ),

        "Genuine": (
            "Your monthly bank statement is now available. "
            "Please check it through your bank's official app."
        )
    }

    sample_cols = st.columns(4)

    for index, (name, sample) in enumerate(samples.items()):
        with sample_cols[index]:
            if st.button(name, use_container_width=True):
                st.session_state.message_input = sample
                st.rerun()

    with st.form("scam_form"):

        message = st.text_area(
            "Message",
            height=130,
            placeholder="Paste suspicious SMS or WhatsApp message...",
            key="message_input"
        )

        already_clicked = st.checkbox(
            "I already clicked the link or shared sensitive information."
        )

        submitted = st.form_submit_button(
            "🔍 Analyse Message",
            use_container_width=True,
            type="primary"
        )

    if submitted:

        if not message.strip():
            st.warning("Please enter a message first.")

        else:
            with st.spinner("Checking message..."):

                detection = detect_scam(
                    message,
                    already_clicked
                )

                ai_answer, ai_error = ask_groq(
                    message,
                    detection,
                    already_clicked
                )

                if ai_answer:
                    explanation = ai_answer
                    source = "Groq AI"
                else:
                    explanation = fallback_explanation(
                        detection,
                        already_clicked
                    )
                    source = "Rule-Based Fallback"

                result = {
                    "message": message,
                    "score": detection["score"],
                    "level": detection["level"],
                    "matched": detection["matched"],
                    "explanation": explanation,
                    "source": source,
                    "ai_error": ai_error,
                    "already_clicked": already_clicked,
                    "time": datetime.now().strftime("%d-%m-%Y %I:%M %p")
                }

                st.session_state.last_result = result
                st.session_state.history.insert(0, result)

    result = st.session_state.last_result

    if result:

        st.divider()
        st.subheader("Analysis Result")

        score = result["score"]

        if score >= 70:
            st.error(f"🚨 HIGH RISK — {score}/100")
        elif score >= 40:
            st.warning(f"⚠️ MEDIUM RISK — {score}/100")
        else:
            st.success(f"✅ LOW DETECTED RISK — {score}/100")

        st.progress(score / 100)

        if result["matched"]:
            st.markdown("### Warning Signs Detected")
            for warning in result["matched"]:
                st.write(f"⚠️ {warning}")
        else:
            st.info(
                "No known scam pattern detected. "
                "This does not guarantee the message is safe."
            )

        st.markdown("### 🤖 Smart Scam Explanation")
        st.caption(f"Explanation source: {result['source']}")
        st.markdown(result["explanation"])

        if result["ai_error"]:
            with st.expander("AI connection details"):
                st.code(result["ai_error"])

        if result["already_clicked"]:
            st.error(
                "If banking details or credentials were exposed, "
                "contact your bank immediately. If money was lost "
                "to cyber fraud in India, call 1930 promptly."
            )

        st.caption(
            "This is an initial risk assessment, not a guarantee "
            "or a replacement for your bank's fraud team."
        )


# ============================================
# TAB 2 - SMART BUDGET
# ============================================

with tab2:

    st.subheader("💰 Smart Budget Planner")
    st.write("Plan your monthly income and expenses.")

    with st.form("budget_form"):

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0,
            value=30000,
            step=1000
        )

        col1, col2 = st.columns(2)

        with col1:
            rent = st.number_input("Rent (₹)", min_value=0, value=8000)
            food = st.number_input("Food (₹)", min_value=0, value=5000)

        with col2:
            travel = st.number_input("Travel (₹)", min_value=0, value=2000)
            other = st.number_input("Other Expenses (₹)", min_value=0, value=3000)

        budget_submit = st.form_submit_button(
            "Calculate My Budget",
            use_container_width=True
        )

    if budget_submit:

        expenses = rent + food + travel + other
        balance = income - expenses

        c1, c2, c3 = st.columns(3)

        c1.metric("Monthly Income", f"₹{income:,.0f}")
        c2.metric("Total Expenses", f"₹{expenses:,.0f}")
        c3.metric("Remaining Balance", f"₹{balance:,.0f}")

        if balance > 0:
            st.success(
                f"You have ₹{balance:,.0f} remaining. "
                "Consider saving a portion."
            )
        elif balance == 0:
            st.warning("Your full income is being used.")
        else:
            st.error(
                f"You are spending ₹{abs(balance):,.0f} "
                "more than your income."
            )

        if income > 0:
            st.progress(min(expenses / income, 1.0))
            st.caption(
                f"You are using {expenses / income * 100:.1f}% "
                "of your monthly income."
            )


# ============================================
# TAB 3 - SAFETY SCORE
# ============================================

with tab3:

    st.subheader("🛡️ Financial Safety Score")
    st.write("Answer these questions about your digital payment habits.")

    with st.form("safety_form"):

        q1 = st.radio(
            "1. Do you keep your UPI PIN and OTP private?",
            ["Yes", "No"]
        )

        q2 = st.radio(
            "2. Do you verify payment requests before approving?",
            ["Yes", "No"]
        )

        q3 = st.radio(
            "3. Do you avoid unknown links and apps?",
            ["Yes", "No"]
        )

        q4 = st.radio(
            "4. Do you use your bank's official app or website?",
            ["Yes", "No"]
        )

        q5 = st.radio(
            "5. Do you check your bank transactions regularly?",
            ["Yes", "No"]
        )

        safety_submit = st.form_submit_button(
            "Calculate Safety Score",
            use_container_width=True
        )

    if safety_submit:

        points = sum(
            1 for answer in [q1, q2, q3, q4, q5]
            if answer == "Yes"
        )

        safety_score = points * 20

        st.metric("Your Safety Score", f"{safety_score}/100")
        st.progress(safety_score / 100)

        if safety_score >= 80:
            st.success("Excellent digital safety habits!")
        elif safety_score >= 60:
            st.info("Good start. Improve a few safety habits.")
        else:
            st.warning(
                "Your digital safety habits need improvement."
            )


# ============================================
# TAB 4 - ACTIVITY HISTORY
# ============================================

with tab4:

    st.subheader("📜 Activity History")

    if not st.session_state.history:

        st.info("No messages analysed yet.")

    else:

        for item in st.session_state.history:

            with st.expander(
                f"{item['time']} | {item['level']} | {item['score']}/100"
            ):

                st.write("**Message:**")
                st.write(item["message"])

                st.write("**Warning categories:**")

                if item["matched"]:
                    for warning in item["matched"]:
                        st.write(f"⚠️ {warning}")
                else:
                    st.write("No known patterns detected.")

                st.write("**Explanation source:**", item["source"])
                st.markdown(item["explanation"])

        if st.button("🗑️ Clear Activity History"):

            st.session_state.history = []
            st.session_state.last_result = None
            st.rerun()


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    '<div class="footer">'
    'Sikka Suraksha | AI + Rule-Based Financial Protection'
    '<br>Always verify suspicious activity with your bank.'
    '</div>',
    unsafe_allow_html=True
)
