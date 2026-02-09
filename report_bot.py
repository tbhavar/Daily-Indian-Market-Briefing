import os, sys, smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

# Initialize Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def is_market_open():
    """Real-time check for Indian market sessions (NSE/BSE)."""
    date_str = datetime.now().strftime("%d %B %Y")
    prompt = f"Is the Indian stock market (NSE/BSE) open for a live trading session today, {date_str}? Consider potential holidays or special sessions. Reply with only 'OPEN' or 'CLOSED'."
    config = types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
    try:
        response = client.models.generate_content(model="gemini-flash-latest", contents=prompt, config=config)
        return "OPEN" in response.text.upper()
    except Exception as e:
        print(f"Error checking market status: {e}")
        return False

def generate_opening_report():
    date_str = datetime.now().strftime("%d %B, %Y")
    prompt = f"""
    Act as a Senior Market Strategist for CA Tanmay R Bhavar. 
    Search for live Nifty 50 and Sensex opening levels for {date_str}.
    Provide:
    1. Opening levels and % change.
    2. 5 major headlines from Moneycontrol and CNBC TV18.
    3. Live sentiment from X (Twitter) and Reddit (r/IndiaInvestments).
    Format as professional HTML with Navy Blue (#1a237e) and Emerald Green (#2e7d32) theme. 
    Do not include <html> or <body> tags.
    """
    config = types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())], temperature=0.1)
    response = client.models.generate_content(model="gemini-flash-latest", contents=prompt, config=config)
    
    ai_content = response.text.replace("```html", "").replace("```", "")
    
    # Branded Template
    return f"""
    <div style="max-width: 650px; margin: 20px auto; font-family: 'Segoe UI', Arial; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); padding: 30px; text-align: center; color: white;">
            <h1 style="margin: 0; font-size: 24px;">MORNING MARKET BRIEF</h1>
            <p style="margin: 5px 0 0; opacity: 0.8;">{date_str} | Market Opening 09:15 AM</p>
            <div style="margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px; font-weight: bold;">
                CA Tanmay R Bhavar | <span style="font-weight: normal;">Consultancy</span>
            </div>
        </div>
        <div style="padding: 25px; line-height: 1.6; color: #333;">{ai_content}</div>
        <div style="background: #f9f9f9; padding: 20px; font-size: 11px; color: #777; text-align: justify; border-top: 1px solid #eee;">
            <strong>DISCLAIMER:</strong> Prepared by the office of CA Tanmay R Bhavar. For informational purposes only. Consult a SEBI advisor.
        </div>
    </div>
    """

def send_email(content, subject_prefix="Opening"):
    sender = os.environ["EMAIL_SENDER"]
    bcc = ["priyaag202@gmail.com", "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", "tkinfotechs@gmail.com", "bhandarijimmy@gmail.com", "chandanaishwarya@gmail.com"]
    msg = MIMEMultipart(); msg['From'] = f"CA Tanmay R Bhavar <{sender}>"; msg['To'] = "tbhavar@gmail.com"
    msg['Subject'] = f"📈 Market {subject_prefix}: {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(content, 'html'))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(sender, os.environ["EMAIL_PASSWORD"])
        s.sendmail(sender, ["tbhavar@gmail.com"] + bcc, msg.as_string())

if __name__ == "__main__":
    if is_market_open():
        send_email(generate_opening_report(), "Briefing")
    else:
        print("Market is closed. No email sent.")
