import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

# --- 1. AI Configuration with Real-time Search ---
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_realtime_report():
    date_today = datetime.now().strftime("%d %B, %Y")
    
    # Prompting with Google Search Grounding enabled
    prompt = f"""
    Search for the most recent Indian stock market data as of 9:15 AM IST today, {date_today}.
    Provide a professional briefing including:
    1. Live Nifty 50 and Sensex opening figures.
    2. Top 5 headlines from Moneycontrol and CNBC TV18.
    3. Sentiment analysis from r/IndiaInvestments on Reddit and financial experts on X (Twitter).
    4. Market Outlook: Specific sectors to watch today.
    
    Format the response as HTML body content (no <html>/<body> tags).
    Use Navy Blue (#1a237e) for headers and a clean card-based layout.
    """

    # Enable Google Search Tool
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        temperature=0.2
    )

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=config
    )
    
    ai_content = response.text.replace("```html", "").replace("```", "")
    
    # Branded Template
    full_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f6;">
        <div style="max-width: 650px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e0e0e0;">
            <div style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); padding: 35px; text-align: center; color: white;">
                <h1 style="margin:0; font-size: 24px;">MARKET INTELLIGENCE REPORT</h1>
                <p style="margin:5px 0; opacity:0.8;">{date_today} | Post-Opening Analysis</p>
                <div style="margin-top:20px; border-top: 1px solid rgba(255,255,255,0.2); padding-top:15px; font-weight: bold;">
                    CA Tanmay R Bhavar <br>
                    <span style="font-weight:normal; font-size:12px; opacity:0.8;">Chartered Accountant & Strategic Consultant</span>
                </div>
            </div>
            <div style="padding: 30px; line-height: 1.6; color: #333;">
                {ai_content}
            </div>
            <div style="background-color: #f9f9f9; padding: 25px; border-top: 1px solid #eeeeee; font-size: 11px; color: #7f8c8d; text-align: justify;">
                <strong>DISCLAIMER:</strong> This report is authored by <strong>CA Tanmay R Bhavar</strong>. It is for informational purposes only and not financial advice. Market investments are subject to risk. Verify all data with SEBI-registered professionals.
                <p style="text-align:center; margin-top:10px;">&copy; {datetime.now().year} CA Tanmay R Bhavar</p>
            </div>
        </div>
    </body>
    </html>
    """
    return full_html

# --- 2. Email Dispatch ---
def send_email(html_content):
    sender = os.environ["EMAIL_SENDER"]
    to_email = "tbhavar@gmail.com"
    bcc_emails = [
        "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", 
        "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", 
        "tkinfotechs@gmail.com"
    ]
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"📈 Market Update: {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(html_content, 'html'))
    
    all_recipients = [to_email] + bcc_emails
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, os.environ["EMAIL_PASSWORD"])
        server.sendmail(sender, all_recipients, msg.as_string())

if __name__ == "__main__":
    report = generate_realtime_report()
    send_email(report)
