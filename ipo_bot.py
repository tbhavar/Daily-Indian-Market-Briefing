import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

# --- 1. AI Configuration ---
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def check_and_generate_ipo_report():
    date_today = datetime.now().strftime("%d %B, %Y")
    
    # Pre-check & Report Generation Prompt
    # We explicitly ask the AI to return "NONE" if no Mainboard IPO is active.
    prompt = f"""
    Search for active MAINBOARD IPOs (exclude SME IPOs) in India currently open for subscription as of {date_today}.
    
    CRITICAL INSTRUCTION: 
    - If there are NO Mainboard IPOs currently open for subscription, respond with exactly one word: NONE.
    - If there ARE active IPOs, provide a professional briefing in HTML.
    
    For active IPOs, include:
    1. Current Subscription Status (QIB, NII, Retail, Total).
    2. Grey Market Premium (GMP) trends from Chittorgarh, IPOWatch, and IPOPremium.
    3. Sentiment Analysis from Reddit and LinkedIn.
    
    Use a Gold (#D4AF37) and Navy Blue (#1a237e) theme.
    """

    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        temperature=0.1
    )

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=config
    )
    
    report_text = response.text.strip()

    # --- GATEKEEPER LOGIC ---
    # If the AI starts with NONE or the text is very short and contains NONE, skip.
    clean_text = report_text.upper().strip()
    if clean_text.startswith("NONE") or (len(clean_text) < 50 and "NONE" in clean_text):
        print(f"[{date_today}] No active Mainboard IPOs found. Skipping email dispatch.")
        return None  # Signal to stop execution
    
    ai_content = report_text.replace("```html", "").replace("```", "")
    
    # Branded Template
    full_html = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #fdfdfd;">
        <div style="max-width: 650px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #d4af37; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <div style="background: linear-gradient(135deg, #1a237e 0%, #d4af37 100%); padding: 40px 20px; text-align: center; color: #ffffff;">
                <h1 style="margin: 0; font-size: 24px; letter-spacing: 2px;">IPO INTELLIGENCE BRIEF</h1>
                <p style="margin: 8px 0 0; opacity: 0.9; font-size: 14px;">{date_today} | Active Mainboard Subscription</p>
                <div style="margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 15px;">
                    <span style="font-weight: bold; font-size: 18px;">CA Tanmay R Bhavar</span><br>
                    <span style="font-weight: normal; font-size: 12px; opacity: 0.9;">Strategic Consultant & IPO Analyst</span>
                </div>
            </div>
            <div style="padding: 30px; line-height: 1.7; color: #333333; font-size: 15px;">
                {ai_content}
            </div>
            <div style="background-color: #fcf8e3; padding: 25px; border-top: 1px solid #faebcc; color: #8a6d3b; font-size: 11px; text-align: justify;">
                <p><strong>DISCLAIMER:</strong> This report is for informational purposes. GMP is unofficial. Consult a SEBI-registered advisor.</p>
                <p style="text-align: center; margin-top: 15px;">© {datetime.now().year} CA Tanmay R Bhavar</p>
            </div>
        </div>
    </body>
    </html>
    """
    return full_html

def send_email(html_content):
    if html_content is None:
        return # Do nothing if report is empty

    sender = os.environ["EMAIL_SENDER"]
    password = os.environ["EMAIL_PASSWORD"]
    to_email = "tbhavar@gmail.com"
    bcc_emails = [
        "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", 
        "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", 
        "tkinfotechs@gmail.com", "bhandarijimmy@gmail.com"
    ]
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"🚀 IPO Alert: Active Mainboard Briefing - {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(html_content, 'html'))
    
    all_recipients = [to_email] + bcc_emails
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, all_recipients, msg.as_string())
    print("Email sent successfully.")

if __name__ == "__main__":
    report = check_and_generate_ipo_report()
    if report:
        send_email(report)
    else:
        # Exit gracefully so GitHub Action marks it as 'Success' but nothing happened
        sys.exit(0)
