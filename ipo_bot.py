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
    url = "https://api.ipoalerts.in/ipos?status=open"
    headers = {"X-API-KEY": IPOALERTS_KEY}
    try:
        print("Step 1: Fetching data from ipoalerts...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data if data.get('ipos') else "NONE"
        return None
    except Exception as e:
        print(f"Fetch failed: {e}")
        return None

def generate_report_with_ai(raw_data):
    if raw_data == "NONE": return "NONE"
    
    date_today = datetime.now().strftime("%d %B, %Y")
    prompt = f"Convert this IPO JSON into a CA-branded HTML report: {raw_data}. Use Navy/Gold theme."

    # --- ATTEMPTING LITE MODEL TO BYPASS QUOTA ---
    try:
        print("Step 2: Generating report with Flash-Lite...")
        response = client.models.generate_content(
            model="gemini-2.5-pro", # Using Lite model for better quota availability
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"AI Quota Error: {e}")
        print("CRITICAL: Returning raw data summary as fallback.")
        return f"Raw Data Alert: {raw_data}" # Fallback text

def send_email(html_content):
    # [Keep your existing send_email function code here]
    # (The one with MIMEMultipart, bcc_emails, and smtplib)
    pass

if __name__ == "__main__":
    raw_data = get_live_ipo_data()
    if raw_data:
        report = generate_report_with_ai(raw_data)
        # Final safety check before sending
        if report and "NONE" not in report.upper():
            # Ensure we don't send raw JSON to clients
            if "{" in report and "}" in report:
                print("Safety Block: Report contains raw JSON. Review prompt.")
            else:
                # Replace this with your actual send_email(report) call
                print("Report ready for dispatch.")
