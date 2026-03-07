import os
import csv
import smtplib
import requests
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
from google.genai import types

def get_genai_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    return genai.Client(api_key=api_key)

def is_market_open(client):
    """Real-time check for Indian market sessions (NSE/BSE)."""
    date_str = datetime.now().strftime("%d %B Y")
    prompt = f"Is the Indian stock market (NSE/BSE) open for a live trading session today, {date_str}? Consider potential holidays or special sessions. Reply with only 'OPEN' or 'CLOSED'."
    config = types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
    try:
        response = client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt, config=config)
        return "OPEN" in response.text.upper()
    except Exception as e:
        print(f"Error checking market status: {e}")
        return False

def generate_ai_content(client, prompt, use_search=False, temperature=0.7):
    tools = [types.Tool(google_search=types.GoogleSearch())] if use_search else []
    config = types.GenerateContentConfig(tools=tools, temperature=temperature)
    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest", 
            contents=prompt, 
            config=config
        )
        return response.text.replace("```html", "").replace("```", "").strip()
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return None

def get_active_subscribers():
    csv_url = os.environ.get("SUBSCRIBERS_CSV_URL")
    default_bcc = ["priyaag202@gmail.com", "amolgothi@gmail.com", "ggbirade@gmail.com", "tanmay.bhavar@mail.ca.in", "jadhavsayi01@gmail.com", "aaryanbee@gmail.com", "jadhavsanket77@gmail.com", "tkinfotechs@gmail.com", "bhandarijimmy@gmail.com", "chandanaishwarya@gmail.com"]
    
    if not csv_url:
        print("SUBSCRIBERS_CSV_URL not set in environment. Falling back to default list.")
        return default_bcc

    try:
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        lines = response.text.splitlines()
        reader = csv.reader(lines)
        headers = next(reader, None)  # Skip header
        
        subscriptions = {}
        for row in reader:
            if len(row) >= 3: # Assuming Timestamp, Email, Action are the first three
                email = row[1].strip().lower()
                action = row[2].strip().lower()
                
                # The latest entry defines the subscription status because rows are chronological
                if 'subscribe' in action and 'unsubscribe' not in action:
                    subscriptions[email] = True
                elif 'unsubscribe' in action:
                    subscriptions[email] = False
                    
        active_list = [email for email, is_active in subscriptions.items() if is_active]
        return active_list if active_list else default_bcc
    except Exception as e:
        print(f"Failed to fetch or parse CSV from Google Sheets: {e}")
        return default_bcc

def send_email(content, subject, from_addr=None):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    
    if not sender or not password:
        print("Email credentials not set. Skipping email.")
        return

    bcc = get_active_subscribers()
    to_addr = "tbhavar@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = f"CA Tanmay R Bhavar <{sender}>"
    msg['To'] = to_addr
    msg['Subject'] = f"{subject} {datetime.now().strftime('%d %b %Y')}"
    
    msg.attach(MIMEText(content, 'html'))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(sender, password)
            s.sendmail(sender, [to_addr] + bcc, msg.as_string())
        print(f"Email sent successfully: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")
