import os
import smtplib
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- 1. AI Configuration ---
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. Scraping Logic ---
def get_raw_news():
    sources = {
        "Moneycontrol": "https://www.moneycontrol.com/news/business/markets/",
        "CNBC TV18": "https://www.cnbctv18.com/market/"
    }
    aggregated_text = ""
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for name, url in sources.items():
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            # Extracting headlines (generic logic)
            headlines = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])[:10]]
            aggregated_text += f"\nSource {name}:\n" + "\n".join(headlines)
        except Exception as e:
            print(f"Error scraping {name}: {e}")
            
    # Add manual simulated "Social Media Search Metrics"
    aggregated_text += "\nSocial Insights (X/Reddit/LinkedIn): Bullish sentiment on Green Energy, concerns over Crude Oil prices."
    return aggregated_text

# --- 3. Report Generation with Gemini 3 Flash ---
def generate_report(news_content):
    prompt = f"""
    Act as a Senior Financial Analyst for the Indian Market. 
    Compile a professional, colorful, and engaging Daily Briefing report.
    Use HTML tags for formatting. Use a theme of Deep Blue, Emerald Green, and Gold.
    
    Data Input: {news_content}
    
    The report must include:
    1. A 'Market Sentiment' meter (Bullish/Bearish/Neutral).
    2. Top 5 Market-Moving Headlines.
    3. Social Media Buzz (summarized from X, Reddit, and LinkedIn mentions).
    4. An 'Expert Outlook' for the trading day.
    """
    response = model.generate_content(prompt)
    return response.text

# --- 4. Email Dispatch ---
def send_email(html_content):
    msg = MIMEMultipart()
    msg['From'] = os.environ["EMAIL_SENDER"]
    msg['To'] = os.environ["EMAIL_RECEIVER"]
    msg['Subject'] = "📈 Daily Indian Market Intelligence Report"
    
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["EMAIL_SENDER"], os.environ["EMAIL_PASSWORD"])
        server.send_message(msg)

if __name__ == "__main__":
    raw_news = get_raw_news()
    report_html = generate_report(raw_news)
    send_email(report_html)
