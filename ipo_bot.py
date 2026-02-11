import os
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types, errors

# --- 1. Configuration ---
# Ensure GEMINI_API_KEY, EMAIL_SENDER, and EMAIL_PASSWORD are in your GitHub Secrets
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def check_and_generate_ipo_report():
    date_today = datetime.now().strftime("%d %B, %Y")
    
    # Refined CA-Professional Prompt
    prompt = f"""
    Search for active MAINBOARD IPOs in India currently open for subscription as of {date_today}. 
    (Exclude SME IPOs. If today is the closing date of an IPO, include it).

    CRITICAL INSTRUCTION: 
    - If there are NO Mainboard IPOs currently open, respond ONLY with the word: NONE.
    - If active IPOs exist, generate a professional investment briefing in HTML.

    For each active IPO, include:
    1. Key Highlights: Price Band, Lot Size, and Fresh Issue vs. OFS mix.
    2. Subscription Velocity: Current status for QIB, NII, and Retail.
    3. Grey Market intelligence: Current GMP and estimated listing gain %.
    4. Financial Perspective: P/E Ratio vs. Peer Average and 3-year Revenue CAGR.
    5. Advisory Sentiment: Consensus from top brokerages and social sentiment.

    Design: Use Navy Blue (#1a237e) and Gold (#D4AF37) theme with tables for data.
    """

    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        temperature=0.1
    )

    # --- 2. High-Resiliency AI Call ---
    max_retries = 3
    response = None

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}: Generating IPO report...")
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=config
            )
            break 
        except errors.ClientError as e:
            err_str = str(e).upper()
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 60  # Wait 60s, then 120s
                    print(f"Quota reached. Sleeping for {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print("Daily search quota fully exhausted. Stopping script.")
                    return None
            else:
                print(f"API Error: {e}")
                raise e

    if not response or not response.text:
        return None

    report_text = response.text.strip()

    # --- 3. Gatekeeper Logic ---
    clean_text = report_text.upper().strip()
    if clean_text.startswith("NONE") or (len(clean_text) < 50 and "NONE" in clean_text):
        print(f"[{date_today}] No active Mainboard IPOs found. Skipping email.")
        return None 
    
    # Clean up AI output for HTML
    ai_content = report_text.replace("```html", "").replace("```", "")
    
    # Branded Template for TRB & Co / CA Tanmay Bhavar
    full_html = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <div style="max-width: 650px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #d4af37;">
            <div style="background: linear-gradient(135deg, #1a237e 0%, #d4af37 100%); padding: 30px; text-align: center; color: #ffffff;">
                <h1 style="margin: 0; font-size: 22px; letter-spacing: 1px;">IPO INTELLIGENCE BRIEF</h1>
                <p style="margin: 5px 0 0; font-size: 14px; opacity: 0.9;">{date_today} | Market Insights</p>
                <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px;">
                    <span style="font-weight: bold; font-size: 16px;">CA Tanmay R Bhavar</span><br>
                    <span style="font-size: 11px;">Proprietor, TRB & Co | Nashik</span>
                </div>
            </div>
            <div style="padding: 25px; line-height: 1.6; color: #333333;">
                {ai_content}
            </div>
            <div style="background-color: #fcf8e3; padding: 20px; border-top: 1px solid #faebcc; color: #8a6d3b; font-size: 10px; text-align: justify;">
                <p><strong>DISCLAIMER:</strong> This report is for informational purposes only. GMP is speculative. Please consult a SEBI-registered investment advisor before investing.</p>
                <p style="text-align: center; margin-top: 10px;">© {datetime.now().year} CA Tanmay R Bhavar</p>
            </div>
        </div>
    </body>
    </html>
    """
    return full_html

def send_email(html_content):
    sender = os.environ["EMAIL_SENDER"]
    password = os.environ["EMAIL_PASSWORD"]
    to_email = "tbhavar@gmail.com"
    
    # List of recipients for BCC
    bcc_emails = [
        "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", 
        "priyaag202@gmail.com", "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", 
        "jadhavsanket77@gmail.com", "tkinfotechs@gmail.com", "bhandarijimmy@gmail.com", 
        "chandanaishwarya@gmail.com"
    ]
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"🚀 IPO Alert: Mainboard Intelligence - {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(html_content, 'html'))
    
    all_recipients = [to_email] + bcc_emails
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, all_recipients, msg.as_string())
        print("Email sent successfully to all recipients.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    try:
        report = check_and_generate_ipo_report()
        if report:
            send_email(report)
        else:
            print("Process finished with no report to send.")
            sys.exit(0)
    except Exception as e:
        print(f"Critical script failure: {e}")
        sys.exit(1)
