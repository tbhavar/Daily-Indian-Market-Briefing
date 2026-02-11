import os
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types, errors

# --- 1. AI Configuration ---
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def check_and_generate_ipo_report():
    date_today = datetime.now().strftime("%d %B, %Y")
    
    prompt = f"""
    Search for active MAINBOARD IPOs in India open for subscription as of {date_today}.
    
    If NONE are open, respond ONLY with "NONE".
    If active, provide a CA-level briefing in HTML. 
    Include: Subscription % (QIB/NII/Retail), GMP trends, P/E vs Peers, and Broker Consensus.
    
    STRICT: Perform as few searches as possible to save quota. Combine queries.
    """

    # Config with Search
    search_config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        temperature=0.1
    )

    # Config WITHOUT Search (The Fallback)
    fallback_config = types.GenerateContentConfig(temperature=0.1)

    # --- 2. High-Resiliency Call Logic ---
    max_retries = 3
    response = None

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}: Generating report with Search...")
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=search_config
            )
            break 
        except errors.ClientError as e:
            err_str = str(e).upper()
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                if attempt < max_retries - 1:
                    time.sleep(60 * (attempt + 1))
                else:
                    print("⚠️ Search Quota Empty. Attempting Fallback (No Search)...")
                    try:
                        # Final attempt: Rely on internal training data
                        response = client.models.generate_content(
                            model="gemini-2.0-flash",
                            contents=prompt + " (Note: Use your internal knowledge if search fails)",
                            config=fallback_config
                        )
                    except:
                        return None
            else:
                raise e

    if not response or not response.text:
        return None

    report_text = response.text.strip()

    # --- 3. Gatekeeper Logic ---
    clean_text = report_text.upper()
    if clean_text.startswith("NONE") or len(clean_text) < 100:
        print(f"[{date_today}] No active Mainboard IPOs identified.")
        return None 
    
    ai_content = report_text.replace("```html", "").replace("```", "")
    
    # Branded Template
    full_html = f"""
    <html>
    <body style="font-family: Arial; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: #fff; border: 1px solid #d4af37; border-radius: 8px; overflow: hidden;">
            <div style="background: #1a237e; color: #fff; padding: 20px; text-align: center;">
                <h2 style="margin:0;">IPO INTELLIGENCE BRIEF</h2>
                <p style="margin:5px 0 0; font-size:12px;">CA Tanmay R Bhavar | {date_today}</p>
            </div>
            <div style="padding: 20px; line-height: 1.6;">
                {ai_content}
            </div>
            <div style="font-size: 10px; color: #777; padding: 20px; text-align: center; border-top: 1px solid #eee;">
                © {datetime.now().year} TRB & Co. | For Educational Purposes Only.
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
    bcc_emails = ["tanmay.bhavar@mail.ca.in"] # Add others as needed
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"🚀 IPO Alert: {datetime.now().strftime('%d %b %Y')}"
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [to_email] + bcc_emails, msg.as_string())
    print("Email sent successfully.")

if __name__ == "__main__":
    report = check_and_generate_ipo_report()
    if report:
        send_email(report)
