import argparse
import os
from datetime import datetime

from src.utils import get_genai_client, is_market_open, generate_ai_content, send_email
from src.prompts import MORNING_PROMPT, CLOSING_PROMPT, IPO_PROMPT
from src.data_fetcher import get_live_ipo_data

def read_template(template_name):
    # Determine absolute path to templates directory relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'templates', f'{template_name}.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def run_bot(report_type):
    client = get_genai_client()
    date_str = datetime.now().strftime("%d %B, %Y")
    
    # Placeholder for the google form link the user created
    form_url = os.environ.get("GOOGLE_FORM_URL", "#enter-your-google-form-url-in-secrets")
    
    if report_type in ['morning', 'closing']:
        print(f"Running {report_type} bot...")
        if not is_market_open(client):
            print("Market is closed. No email sent.")
            return

        if report_type == 'morning':
            prompt = MORNING_PROMPT.format(date_str=date_str)
            ai_content = generate_ai_content(client, prompt, use_search=True, temperature=0.1)
            subject = "📈 Market Briefing:"
        else:
            prompt = CLOSING_PROMPT.format(date_str=date_str)
            ai_content = generate_ai_content(client, prompt, use_search=True, temperature=0.7)
            subject = "📉 Market Closing:"

        if ai_content:
            template = read_template(report_type)
            final_html = template.format(date_str=date_str, ai_content=ai_content, form_url=form_url)
            send_email(final_html, subject)

    elif report_type == 'ipo':
        print("Running IPO bot...")
        raw_data = get_live_ipo_data()
        
        if raw_data and raw_data != "NONE":
            prompt = IPO_PROMPT.format(raw_data=raw_data)
            ai_content = generate_ai_content(client, prompt, use_search=False, temperature=0.7)
            
            if ai_content and "NONE" not in ai_content.upper():
                if "{" in ai_content and "}" in ai_content:
                    print("Safety Block: Report contains raw JSON. Review prompt.")
                else:
                    template = read_template('ipo')
                    final_html = template.format(date_str=date_str, ai_content=ai_content, form_url=form_url)
                    send_email(final_html, "🚀 IPO Intelligence:")
            else:
                print("No active IPOs found based on AI response.")
        else:
            print("No active IPOs found or failed to fetch IPO data.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Indian Market Briefing Bots")
    parser.add_argument('--type', choices=['morning', 'closing', 'ipo'], required=True, help="Type of report to generate")
    args = parser.parse_args()
    
    run_bot(args.type)
