import os, sys, smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Use the same is_market_open() function as above
def is_market_open():
    date_str = datetime.now().strftime("%d %B 2026")
    prompt = f"Is the NSE/BSE stock market open for a live session today, {date_str}? Reply only 'OPEN' or 'CLOSED'."
    config = types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
    response = client.models.generate_content(model="gemini-flash-latest", contents=prompt, config=config)
    return "OPEN" in response.text.upper()

def generate_closing_report():
    date_str = datetime.now().strftime("%d %B, %Y")
    prompt = f"""
    Analyze the Indian market closing for {date_str}. 
    Include:
    1. Closing levels for Nifty 50 and Bank Nifty.
    2. Top 3 gainers and losers with reasons.
    3. Technical Outlook: Next trading day's strategy based on today's price action.
    Format as professional HTML for CA Tanmay R Bhavar using a Slate Grey (#2c3e50) and Gold (#D4AF37) theme. 
    Do not include <html> or <body> tags.
    """
    config = types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt, config=config)
    
    ai_content = response.text.replace("```html", "").replace("```", "")
    
    return f"""
    <div style="max-width: 650px; margin: 20px auto; font-family: 'Segoe UI', Arial; border: 1px solid #d4af37; border-radius: 8px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #2c3e50 0%, #000000 100%); padding: 30px; text-align: center; color: #D4AF37;">
            <h1 style="margin: 0; font-size: 24px;">CLOSING BELL ANALYSIS</h1>
            <p style="margin: 5px 0 0; color: white; opacity: 0.8;">{date_str} | Market Wrap-Up</p>
            <div style="margin-top: 15px; border-top: 1px solid rgba(212,175,55,0.3); padding-top: 10px; font-weight: bold;">
                CA Tanmay R Bhavar | <span style="font-weight: normal; color: white;">Next Day Strategy</span>
            </div>
        </div>
        <div style="padding: 25px; line-height: 1.6; color: #333;">{ai_content}</div>
        <div style="background: #f9f9f9; padding: 20px; font-size: 11px; color: #777; text-align: justify;">
            <strong>DISCLAIMER:</strong> Authored by CA Tanmay R Bhavar. Market investments are subject to risk.
        </div>
    </div>
    """

# Use the same send_email() logic as in report_bot.py
def send_email(content, subject_prefix="Closing"):
    sender = os.environ["EMAIL_SENDER"]
    bcc = ["amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", "tkinfotechs@gmail.com"]
    msg = MIMEMultipart(); msg['From'] = f"CA Tanmay R Bhavar <{sender}>"; msg['To'] = "tbhavar@gmail.com"
    msg['Subject'] = f"📉 Market {subject_prefix}: {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(content, 'html'))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(sender, os.environ["EMAIL_PASSWORD"])
        s.sendmail(sender, ["tbhavar@gmail.com"] + bcc, msg.as_string())

if __name__ == "__main__":
    if is_market_open():
        send_email(generate_closing_report(), "Closing Bell")
