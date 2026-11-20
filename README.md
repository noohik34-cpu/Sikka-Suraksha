# 🛡️ Sikka Suraksha
### Your Financial Safety Companion

Every rupee deserves protection.

Sikka Suraksha is a smart financial safety application designed to help users identify suspicious financial messages, understand potential UPI scams, and build safer digital payment habits.

## 🚨 Problem Statement

Digital payment fraud, fake KYC messages, phishing links and UPI scams are increasing. Many users struggle to identify fraudulent messages before losing their money.

Sikka Suraksha aims to make digital payments safer through scam detection and financial awareness.

## ✨ Key Features

### 1. 🔍 Smart Scam Detection
- Detects suspicious SMS, WhatsApp and email messages.
- Identifies Fake KYC attempts.
- Detects UPI Collect fraud patterns.
- Identifies OTP and password theft attempts.
- Detects suspicious links and remote access app requests.
- Generates a risk score.

### 2. 🤖 AI-Powered Explanation
- Uses Groq API for AI-based message analysis.
- Explains potential scam indicators.
- Provides practical financial safety recommendations.
- Includes a rule-based fallback when the API is unavailable.

### 3. 💰 Smart Budget Planner
- Calculates monthly income and expenses.
- Shows remaining balance.
- Helps users understand their spending.

### 4. 🛡️ Financial Safety Score
- Evaluates digital payment safety habits.
- Generates a score out of 100.
- Provides safety awareness feedback.

### 5. 📜 Activity History
- Stores previous message analyses during the app session.
- Displays detected warning categories and risk scores.

## 🛠️ Technologies Used

- Python
- Streamlit
- Groq API
- Groq Python SDK
- python-dotenv
- Rule-Based Detection Engine

## ⚙️ Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd Sikka-Suraksha
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Get your API key from:

https://console.groq.com/keys

Never upload your `.env` file to GitHub.

### Step 5: Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Security Note

- Never share OTP or UPI PIN.
- Never approve unknown UPI collect requests.
- Verify suspicious messages through official bank channels.
- Do not expose API keys or personal banking information.

## ⚠️ Disclaimer

Sikka Suraksha provides an initial risk assessment and financial safety awareness. It does not guarantee fraud detection or replace professional banking and cybersecurity support.

## 👩‍💻 Project

**Project Name:** Sikka Suraksha

**Theme:** AI for Finance

**Hackathon:** Arthaton 2026

Stay Alert. Stay Safe. Protect Your Money. 🛡️
