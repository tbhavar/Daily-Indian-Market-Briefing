import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

# --- 1. AI Configuration ---
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_ipo_report():
    date_today = datetime.now().strftime("%d %B, %Y")
    
    # Prompting Gemini for live IPO tracking (Mainboard Only)
    prompt = f"""
    Act as an IPO Research Expert. Search for active MAINBOARD IPOs (exclude SME IPOs) in India as of today {date_today}.
    For each active IPO, provide:
    1. Current Subscription Status (QIB, NII, Retail, and Total) from opening date till now.
    2. Grey Market Premium (GMP) trends from Chittorgarh, IPOWatch, and IPOPremium.
    3. Sentiment Analysis: Summarize recent discussions from Reddit (r/IndianStockMarket) and LinkedIn.
    
    Format the output in professional HTML. Use a Gold (#D4AF37) and Navy Blue (#1a237e) theme.
    If no mainboard IPO is active, provide a list of 'Upcoming Mainboard IPOs' to watch.
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
    
    ai_content = response.text.replace("```html", "").replace("```", "")
    
    # Your Branded Consultancy Template
    full_html = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #fdfdfd;">
        <div style="max-width: 650px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #d4af37; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            
            <div style="background: linear-gradient(135deg, #1a237e 0%, #d4af37 100%); padding: 40px 20px; text-align: center; color: #ffffff;">
                <h1 style="margin: 0; font-size: 24px; letter-spacing: 2px;">IPO INTELLIGENCE BRIEF</h1>
                <p style="margin: 8px 0 0; opacity: 0.9; font-size: 14px;">{date_today} | 08:00 AM Daily Update</p>
                <div style="margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 15px;">
                    <span style="font-weight: bold; font-size: 18px;">CA Tanmay R Bhavar</span><br>
                    <span style="font-weight: normal; font-size: 12px; opacity: 0.9;">Strategic Consultant & IPO Analyst</span>
                </div>
            </div>

            <div style="padding: 30px; line-height: 1.7; color: #333333; font-size: 15px;">
                {ai_content}
            </div>

            <div style="background-color: #fcf8e3; padding: 25px; border-top: 1px solid #faebcc; color: #8a6d3b; font-size: 11px; text-align: justify;">
                <p style="margin-top: 0;"><strong>DISCLAIMER:</strong> This IPO report is authored by the office of <strong>CA Tanmay R Bhavar</strong>. It is for informational purposes only. IPO investments are subject to market risks. GMP is an unofficial market estimate and should not be the sole basis for investment.</p>
                <p style="text-align: center; margin-top: 15px;">
                    © {datetime.now().year} CA Tanmay R Bhavar. All Rights Reserved.
                </p>
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
    bcc_emails = [
        "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", 
        "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", 
        "tkinfotechs@gmail.com"
    ]
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"🚀 IPO Alert: Daily Mainboard Briefing - {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(html_content, 'html'))
    
    all_recipients = [to_email] + bcc_emails
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, all_recipients, msg.as_string())

if __name__ == "__main__":
    report_body = generate_ipo_report()
    send_email(report_body)
