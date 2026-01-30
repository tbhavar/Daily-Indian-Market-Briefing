import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

# --- 1. AI Configuration (2026 Production SDK) ---
# Ensure GEMINI_API_KEY is set in your GitHub Secrets
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_realtime_report():
    date_today = datetime.now().strftime("%d %B, %Y")
    
    # We use Google Search Grounding to bypass static scraping issues
    prompt = f"""
    Act as a Senior Market Strategist. Search for live Indian stock market data as of 9:15 AM IST today ({date_today}).
    
    Include in the report:
    1. Opening levels for Nifty 50, Bank Nifty, and Sensex.
    2. Top 5 headlines from Moneycontrol and CNBC TV18.
    3. Sentiment summary from X (Twitter) and Reddit (r/IndiaInvestments).
    4. Analyst view on key sectors (e.g., IT, Banking, Energy) for the day.
    
    Format the output as clean HTML body content (do not include <html> or <body> tags).
    Use Navy Blue (#1a237e) for headers and Emerald Green (#2e7d32) for positive highlights.
    """

    # Configuring the Google Search tool for Real-time Analysis
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        temperature=0.1
    )

    response = client.models.generate_content(
        model="gemini-3-flash",
        contents=prompt,
        config=config
    )
    
    # Clean the AI response of any markdown code blocks
    ai_content = response.text.replace("```html", "").replace("```", "")
    
    # Wrap in your Professional Branding Template
    full_html = f"""
    <html>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f0f2f5;">
        <div style="max-width: 650px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #d1d5db; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
            
            <div style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); padding: 40px 20px; text-align: center; color: #ffffff;">
                <h1 style="margin: 0; font-size: 26px; text-transform: uppercase; letter-spacing: 2px;">Market Intelligence Brief</h1>
                <p style="margin: 8px 0 0; opacity: 0.9; font-size: 14px;">{date_today} | Live Post-Opening Analysis</p>
                <div style="margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 15px;">
                    <span style="font-weight: bold; font-size: 18px;">CA Tanmay R Bhavar</span><br>
                    <span style="font-weight: normal; font-size: 12px; opacity: 0.8;">Chartered Accountant & Strategic Consultant</span>
                </div>
            </div>

            <div style="padding: 30px; line-height: 1.7; color: #374151; font-size: 15px;">
                {ai_content}
            </div>

            <div style="background-color: #f9fafb; padding: 25px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 11px; text-align: justify;">
                <p style="margin-top: 0;"><strong>DISCLAIMER:</strong> This briefing is prepared by the consultancy office of <strong>CA Tanmay R Bhavar</strong>. The content provided is strictly for informational and educational purposes only and does not constitute financial, investment, legal, or tax advice. Stock market investments are subject to market risks; please read all related documents carefully before investing.</p>
                <p>Views expressed are based on automated real-time data aggregation and AI synthesis; accuracy is not guaranteed. Always consult with a SEBI-registered investment advisor before making investment decisions.</p>
                <p style="text-align: center; margin-top: 15px; border-top: 1px solid #e5e7eb; padding-top: 15px;">
                    © {datetime.now().year} CA Tanmay R Bhavar. All Rights Reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return full_html

# --- 3. Secure Dispatch to Multiple Recipients ---
def send_email(html_content):
    sender = os.environ["EMAIL_SENDER"]
    password = os.environ["EMAIL_PASSWORD"]
    
    # Primary recipient
    to_email = "tbhavar@gmail.com"
    
    # BCC List for privacy
    bcc_emails = [
        "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", 
        "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", 
        "tkinfotechs@gmail.com"
    ]
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"📈 Daily Market Briefing - {datetime.now().strftime('%d %b %Y')}"
    
    msg.attach(MIMEText(html_content, 'html'))
    
    all_recipients = [to_email] + bcc_emails
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, all_recipients, msg.as_string())
        print(f"Branded report successfully sent to {len(all_recipients)} recipients.")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Execute Real-time Analysis and Email
    report_body = generate_realtime_report()
    send_email(report_body)
