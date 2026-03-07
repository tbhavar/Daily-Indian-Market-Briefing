# 📈 Indian Market Intelligence Automation

An AI-powered automation engine that scrapes live Indian stock market data, processes sentiment via **Gemini 2.0 Flash**, and dispatches professional HTML briefings to stakeholders throughout the trading day.

## 🚀 Overview
This system bypasses the need for manual research by aggregating news from top-tier financial sources and social platforms, using LLMs to extract actionable insights. It provides three distinct types of reports: Morning Bell, Closing Bell, and IPO Intelligence.

### Key Features:
* **AI Synthesis:** Uses Gemini 2.0 Flash for rapid context extraction and professional formatting.
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

### 2. Google AI Studio
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Generate an API Key for **Gemini 2.0 Flash**.
3. Ensure you have the `flash` model enabled for low-latency processing.

### 3. Gmail App Password
To allow the script to send emails:
1. Go to your Google Account Security settings.
2. Enable **2-Factor Authentication**.
3. Search for **App Passwords**.
4. Create a new one named "Market Bot" and copy the 16-character code.

---

## 📅 Schedule & Workflow

The automation is split into three main workflows:

| Report Type | Python Script | Cron Schedule (UTC) | IST Time |
| :--- | :--- | :--- | :--- |
| **Morning Briefing** | `main.py --type morning` | `45 3 * * *` | 09:15 AM |
| **Closing Bell** | `main.py --type closing` | `15 10 * * *` | 03:45 PM |
| **IPO Intelligence** | `main.py --type ipo` | `30 2 * * *` | 08:00 AM |

*All workflows run Monday through Friday, synchronized with market days.*

---

## 📂 File Structure
* `main.py`: The single entry point to run any report. (e.g., `python main.py --type morning`)
* `src/`: Core logic:
  * `prompts.py`: Externalized prompts for Gemini LLM.
  * `data_fetcher.py`: Logic to fetch live IPO data from APIs.
  * `utils.py`: Setup for Google GenAI client, email logic, and market status checks.
* `templates/`: Professional HTML shells for the emails.
  * `morning.html`, `closing.html`, `ipo.html`
* `.github/workflows/`: Contains the YAML files for GitHub Actions automation.
* `requirements.txt`: Python dependencies (`google-genai`, `requests`, `beautifulsoup4`).

---

## ⚖️ Disclaimer
*This project is for educational and informational purposes only. The automated reports do not constitute financial advice. Always verify data with a SEBI-registered advisor before trading.*
