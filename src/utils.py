import os
import csv
import time
import logging
import smtplib
import requests
from datetime import datetime
import pytz
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

IST = pytz.timezone('Asia/Kolkata')

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_genai_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    return genai.Client(api_key=api_key)

def is_market_open(client):
    """Real-time check for Indian market sessions (NSE/BSE)."""
    date_str = datetime.now(IST).strftime("%d %B %Y")
    prompt = f"Is the Indian stock market (NSE/BSE) open for a live trading session today, {date_str}? Consider potential holidays or special sessions. Reply with only 'OPEN' or 'CLOSED'."
    config = types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
    try:
        response = client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt, config=config)
        return "OPEN" in response.text.upper()
    except Exception as e:
        logger.error(f"Error checking market status: {e}")
        return False

def generate_ai_content(client, prompt, use_search=False, temperature=0.7, max_retries=3):
    """Generate AI content with retry logic and exponential backoff."""
    tools = [types.Tool(google_search=types.GoogleSearch())] if use_search else []
    config = types.GenerateContentConfig(tools=tools, temperature=temperature)
    
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest", 
                contents=prompt, 
                config=config
            )
            return response.text.replace("```html", "").replace("```", "").strip()
        except Exception as e:
            logger.error(f"AI Generation Error (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                wait_time = 2 ** (attempt - 1)  # 1s, 2s, 4s
                logger.info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
    
    logger.error("All retry attempts exhausted for AI content generation.")
    return None

def get_active_subscribers():
    csv_url = os.environ.get("SUBSCRIBERS_CSV_URL")
    default_bcc = ["priyaag202@gmail.com", "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", "tkinfotechs@gmail.com", "bhandarijimmy@gmail.com", "chandanaishwarya@gmail.com"]
    
    if not csv_url:
        logger.warning("SUBSCRIBERS_CSV_URL not set in environment. Falling back to default list.")
        return default_bcc

    try:
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        lines = response.text.splitlines()
        reader = csv.reader(lines)
        headers = next(reader, None)  # Skip header
        
        subscriptions = {}
        for row in reader:
            if len(row) >= 3: # Timestamp, Email, Action are the first three
                email = row[1].strip().lower()
                action = row[2].strip().lower()
                
                # The latest entry defines the subscription status because rows are chronological
                if 'subscribe' in action and 'unsubscribe' not in action:
                    subscriptions[email] = True
                elif 'unsubscribe' in action:
                    subscriptions[email] = False
                    
        active_list = [email for email, is_active in subscriptions.items() if is_active]
        # Enforce maximum of 90 active email subscriptions
        active_list = active_list[:90]
        
        logger.info(f"Fetched {len(active_list)} active subscribers from Google Sheets.")
        return active_list if active_list else default_bcc
    except Exception as e:
        logger.error(f"Failed to fetch or parse CSV from Google Sheets: {e}")
        return default_bcc

def send_email(content, subject, from_addr=None):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    
    if not sender or not password:
        logger.warning("Email credentials not set. Skipping email.")
        return

    bcc = get_active_subscribers()
    to_addr = "tbhavar@gmail.com"
    
    now_ist = datetime.now(IST)
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_addr
    msg['Subject'] = f"{subject} {now_ist.strftime('%d %b %Y')}"
    
    msg.attach(MIMEText(content, 'html'))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(sender, password)
            s.sendmail(sender, [to_addr] + bcc, msg.as_string())
        logger.info(f"Email sent successfully: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def send_error_notification(report_type, error_msg):
    """Send a failure notification email to the admin."""
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    
    if not sender or not password:
        logger.warning("Cannot send error notification — email credentials not set.")
        return

    to_addr = "tbhavar@gmail.com"
    
    now_ist = datetime.now(IST)
    msg = MIMEMultipart()
    msg['From'] = f"Market Bot Alert <{sender}>"
    msg['To'] = to_addr
    msg['Subject'] = f"⚠️ Report Failed: {report_type} — {now_ist.strftime('%d %b %Y')}"
    
    error_html = f"""
    <div style="font-family: system-ui, sans-serif; padding: 20px; max-width: 600px;">
        <h2 style="color: #d32f2f;">⚠️ Report Generation Failed</h2>
        <table style="border-collapse: collapse; width: 100%;">
            <tr><td style="padding: 8px; border: 1px solid #e0e0e0; font-weight: bold;">Report Type</td>
                <td style="padding: 8px; border: 1px solid #e0e0e0;">{report_type}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #e0e0e0; font-weight: bold;">Time</td>
                <td style="padding: 8px; border: 1px solid #e0e0e0;">{now_ist.strftime('%d %b %Y, %I:%M %p')} IST</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #e0e0e0; font-weight: bold;">Error</td>
                <td style="padding: 8px; border: 1px solid #e0e0e0; color: #d32f2f;">{error_msg}</td></tr>
        </table>
        <p style="color: #64748b; font-size: 13px; margin-top: 20px;">This is an automated alert from your Market Briefing Bot.</p>
    </div>
    """
    
    msg.attach(MIMEText(error_html, 'html'))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(sender, password)
            s.sendmail(sender, [to_addr], msg.as_string())
        logger.info(f"Error notification sent for: {report_type}")
    except Exception as e:
        logger.error(f"Failed to send error notification: {e}")
