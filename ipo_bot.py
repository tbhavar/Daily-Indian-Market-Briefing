import os
import requests
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

# --- 1. Configuration ---
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
IPOALERTS_KEY = os.environ.get("IPOALERTS_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

def get_live_ipo_data():
    """Fetches open IPO data using ipoalerts API to save Google Search quota."""
    url = "https://api.ipoalerts.in/ipos?status=open"
    headers = {"X-API-KEY": IPOALERTS_KEY}
    
    try:
        print("Fetching data from ipoalerts...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # If the API returns no IPOs, it usually has an empty list or specific meta count
            if not data.get('ipos'):
                return "NONE"
            return data
        else:
            print(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Fetch failed: {e}")
        return None

def generate_report_with_ai(raw_data):
    """Formats raw data into a CA-branded briefing using Gemini 2.0 Flash."""
    date_today = datetime.now().strftime("%d %B, %Y")
    
    if raw_data == "NONE":
        return "NONE"

    # Prompt designed to use the provided JSON data only (0 Search Grounding used)
    prompt = f"""
    You are an expert IPO Analyst for TRB & Co. 
    Below is the raw JSON data for currently open Mainboard IPOs in India:
    {raw_data}

    TASK:
    1. Extract Company Name, Price Band, Open/Close Dates, and Subscription status if available.
    2. Format this into a high-end investment briefing in HTML.
    3. Include a 'CA Tanmay's Take' section for each IPO discussing the valuation (P/E) vs Peer average based on your internal knowledge of these companies.
    4. Use a professional theme: Navy Blue (#1a237e) and Gold (#D4AF37).
    5. Use HTML tables for the IPO details.
    
    CRITICAL: If the JSON data appears to have no active mainboard issues, respond ONLY with 'NONE'.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return None

def send_email(html_content):
    date_str = datetime.now().strftime("%d %b %Y")
    sender = os.environ["EMAIL_SENDER"]
    password = os.environ["EMAIL_PASSWORD"]
    to_email = "tbhavar@gmail.com"
    
    bcc_emails = [
        "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", 
        "priyaag202@gmail.com", "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", 
        "jadhavsanket77@gmail.com", "tkinfotechs@gmail.com", "bhandarijimmy@gmail.com", 
        "chandanaishwarya@gmail.com"
    ]
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"🚀 IPO Alert: Mainboard Intelligence - {date_str}"
    
    # Cleaning AI output tags
    clean_html = html_content.replace("```html", "").replace("```", "")
    
    # Final Branded Wrapper
    full_body = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8f9fa;">
        <div style="max-width: 700px; margin: 20px auto; background-color: #ffffff; border: 1px solid #d4af37; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <div style="background: linear-gradient(135deg, #1a237e 0%, #d4af37 100%); padding: 35px 20px; text-align: center; color: #ffffff;">
                <h1 style="margin: 0; font-size: 24px; letter-spacing: 1.5px; text-transform: uppercase;">IPO Intelligence Brief</h1>
                <p style="margin: 5px 0 0; opacity: 0.85; font-size: 14px;">Market Insight by CA Tanmay R Bhavar</p>
                <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px; font-size: 13px;">
                    <strong>TRB & Co</strong> | Nashik, Maharashtra
                </div>
            </div>
            <div style="padding: 30px; color: #333333; line-height: 1.8;">
                {clean_html}
            </div>
            <div style="background-color: #fdfae6; padding: 20px; border-top: 1px solid #faebcc; color: #8a6d3b; font-size: 11px; text-align: justify;">
                <p><strong>PROFESSIONAL DISCLAIMER:</strong> This briefing is for informational purposes only and does not constitute financial advice. IPO investments are subject to market risks. Please consult your financial advisor before making any investment decisions.</p>
                <p style="text-align: center; margin-top: 10px; font-weight: bold;">© {datetime.now().year} CA Tanmay R Bhavar</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(full_body, 'html'))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, [to_email] + bcc_emails, msg.as_string())
        print("Advisory email dispatched successfully.")
    except Exception as e:
        print(f"Email failed: {e}")

if __name__ == "__main__":
    raw_data = get_live_ipo_data()
    if raw_data:
        report = generate_report_with_ai(raw_data)
        if report and "NONE" not in report.upper():
            send_email(report)
        else:
            print("No active Mainboard IPOs found today. No email sent.")
    else:
        print("Failed to retrieve data. Exiting.")
