# 📈 Indian Market Intelligence Automation

An AI-powered automation engine that scrapes live Indian stock market data, processes sentiment via **Gemini 3 Flash**, and dispatches a professional HTML briefing to stakeholders every morning at **09:20 AM IST**.

## 🚀 Overview
This system bypasses the need for manual research by aggregating news from top-tier financial sources and social platforms, using LLMs to extract actionable insights.

### Key Features:
* **AI Synthesis:** Uses Gemini 3 Flash for rapid context extraction and professional formatting.
* **Multi-Source Scraping:** Aggregates data from Moneycontrol, CNBC TV18, and NSE.
* **Sentiment Analysis:** Scans social metrics from X, Reddit, and LinkedIn.
* **Serverless Execution:** Runs entirely on GitHub Actions (No hosting costs).
* **Multi-Recipient Support:** Sends reports to an entire team simultaneously.

---

## 🛠️ Setup Instructions

### 1. Repository Secrets
Navigate to `Settings > Secrets and variables > Actions` and add the following **New repository secrets**:

| Secret Name | Description | Example |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google AI Studio API Key | `AIzaSy...` |
| `EMAIL_SENDER` | The Gmail account sending the mail | `bot@gmail.com` |
| `EMAIL_PASSWORD` | Gmail **App Password** (16 digits) | `abcd efgh ijkl mnop` |
| `EMAIL_RECEIVER` | List of emails (Comma separated) | `user1@me.com,user2@firm.in` |

### 2. Google AI Studio
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Generate an API Key for **Gemini 3 Flash**.
3. Ensure you have the `flash` model enabled for low-latency processing.

### 3. Gmail App Password
To allow the script to send emails:
1. Go to your Google Account Security settings.
2. Enable **2-Factor Authentication**.
3. Search for **App Passwords**.
4. Create a new one named "Market Bot" and copy the 16-character code.

---

## 📅 Schedule
The automation is configured via `.github/workflows/daily_briefing.yml` to run on the following cron schedule:
* **Time:** `50 3 * * 1-5` (03:50 AM UTC / 09:20 AM IST)
* **Days:** Monday through Friday (Market Days).

---

## 📂 File Structure
* `report_bot.py`: The core logic for scraping and AI processing.
* `.github/workflows/daily_briefing.yml`: The automation engine.
* `requirements.txt`: Python dependencies (`google-generativeai`, `requests`, `beautifulsoup4`).

---

## ⚖️ Disclaimer
*This project is for educational and informational purposes only. The automated reports do not constitute financial advice. Always verify data with a SEBI-registered advisor before trading.*
