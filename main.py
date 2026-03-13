import argparse
import os
import json
import logging
from datetime import datetime
import pytz

# Timezone helper
IST = pytz.timezone('Asia/Kolkata')

from src.utils import get_genai_client, is_market_open, generate_ai_content, send_email, send_error_notification
from src.prompts import MORNING_PROMPT, CLOSING_PROMPT, IPO_PROMPT, WEEKLY_PROMPT
from src.data_fetcher import get_live_ipo_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

REPORTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports.json')
NOTIFIED_IPOS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notified_ipos.json')

def get_notified_ipos():
    """Load the list of IPO names that have already been reported."""
    if os.path.exists(NOTIFIED_IPOS_FILE):
        try:
            with open(NOTIFIED_IPOS_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except Exception as e:
            logger.error(f"Error reading notified IPOs: {e}")
            return set()
    return set()

def save_notified_ipos(notified_set):
    """Save the list of notified IPO names to prevent re-sending."""
    try:
        # Sort for consistent git diffs
        with open(NOTIFIED_IPOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sorted(list(notified_set)), f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save notified IPOs: {e}")

def read_template(template_name):
    # Determine absolute path to templates directory relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'templates', f'{template_name}.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def is_valid_html(content):
    """Basic validation that the AI response is HTML and not garbled text."""
    if not content:
        return False
    return "<" in content and ">" in content

def save_to_archive(report_type, subject, ai_content):
    """Save the report to a rolling JSON archive (last 7 per type)."""
    try:
        if os.path.exists(REPORTS_FILE):
            with open(REPORTS_FILE, 'r', encoding='utf-8') as f:
                archive = json.load(f)
        else:
            archive = {}
        
        if report_type not in archive:
            archive[report_type] = []
        
        now = datetime.now(IST)
        archive[report_type].insert(0, {
            "date": now.strftime("%d %b %Y"),
            "time": now.strftime("%I:%M %p"),
            "subject": subject,
            "content": ai_content
        })
        
        # Keep only last 7 reports per type
        archive[report_type] = archive[report_type][:7]
        
        with open(REPORTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(archive, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report archived: {report_type}")
    except Exception as e:
        logger.error(f"Failed to save report to archive: {e}")

def run_bot(report_type):
    client = get_genai_client()
    now_ist = datetime.now(IST)
    date_str = now_ist.strftime("%d %B, %Y")
    
    # Placeholder for the google form link the user created
    form_url = os.environ.get("GOOGLE_FORM_URL", "#enter-your-google-form-url-in-secrets")
    
    if report_type in ['morning', 'closing']:
        logger.info(f"Running {report_type} bot...")
        if not is_market_open(client):
            logger.info("Market is closed. No email sent.")
            return

        if report_type == 'morning':
            prompt = MORNING_PROMPT.format(date_str=date_str)
            ai_content = generate_ai_content(client, prompt, use_search=True, temperature=0.1)
            subject = "📈 Market Briefing:"
        else:
            prompt = CLOSING_PROMPT.format(date_str=date_str)
            ai_content = generate_ai_content(client, prompt, use_search=True, temperature=0.1)
            subject = "📉 Market Closing:"

        if ai_content and is_valid_html(ai_content):
            # Extract sentiment section if markers exist
            sentiment_analysis = ""
            if "[SENTIMENT_START]" in ai_content and "[SENTIMENT_END]" in ai_content:
                parts = ai_content.split("[SENTIMENT_START]")
                main_body = parts[0]
                sentiment_part = parts[1].split("[SENTIMENT_END]")[0]
                ai_content = main_body.strip()
                
                # Wrap sentiment in a premium styled container
                bg_color = "#f0f7ff" if report_type == 'morning' else "#f0fdf4"
                border_color = "#bae6fd" if report_type == 'morning' else "#bbf7d0"
                sentiment_analysis = f"""
                <div style="margin: 0 25px 25px; padding: 20px; background-color: {bg_color}; border-radius: 12px; border: 1px solid {border_color};">
                    {sentiment_part.strip()}
                </div>
                """
            
            template = read_template(report_type)
            final_html = template.format(
                date_str=date_str, 
                ai_content=ai_content, 
                sentiment_analysis=sentiment_analysis,
                form_url=form_url
            )
            send_email(final_html, subject)
            save_to_archive(report_type, subject, ai_content + sentiment_analysis)
        else:
            error_msg = "AI returned empty or non-HTML content" if not ai_content else "AI response failed HTML validation"
            logger.error(f"{report_type.title()} report failed: {error_msg}")
            send_error_notification(report_type, error_msg)

    elif report_type == 'ipo':
        logger.info("Running IPO bot...")
        raw_data = get_live_ipo_data()
        
        if raw_data and raw_data != "NONE":
            # Filter out IPOs that have already been notified
            notified_set = get_notified_ipos()
            new_ipos = []
            for ipo in raw_data['ipos']:
                name = ipo.get('name', '').strip().upper()
                if name and name not in notified_set:
                    new_ipos.append(ipo)
            
            if not new_ipos:
                logger.info("No new IPOs found. All active IPOs have already been notified.")
                return

            # Only pass new IPOs to the prompt
            raw_data['ipos'] = new_ipos
            prompt = IPO_PROMPT.format(raw_data=raw_data)
            # Enable search for IPOs to fetch GMP and subscription status from the web
            ai_content = generate_ai_content(client, prompt, use_search=True, temperature=0.1)
            
            if ai_content and "NONE" not in ai_content.upper():
                # Check if the response is raw JSON instead of formatted HTML
                stripped = ai_content.strip()
                if stripped.startswith("{") or stripped.startswith("["):
                    logger.warning("Safety Block: Report contains raw JSON. Review prompt.")
                    send_error_notification("ipo", "AI returned raw JSON instead of formatted HTML.")
                elif not is_valid_html(ai_content):
                    logger.error("IPO report failed HTML validation.")
                    send_error_notification("ipo", "AI response failed HTML validation.")
                else:
                    template = read_template('ipo')
                    # Consistent placeholder passing
                    final_html = template.format(date_str=date_str, ai_content=ai_content, form_url=form_url, sentiment_analysis="")
                    send_email(final_html, "🚀 IPO Intelligence:")
                    save_to_archive("ipo", "🚀 IPO Intelligence:", ai_content)
                    
                    # Mark these IPOs as notified (normalize names)
                    for ipo in new_ipos:
                        notified_set.add(ipo.get('name', '').strip().upper())
                    save_notified_ipos(notified_set)
            else:
                logger.info("No active IPOs found based on AI response.")
        else:
            logger.info("No active IPOs found or failed to fetch IPO data.")

    elif report_type == 'weekly':
        logger.info("Running Weekly Recap bot...")
        prompt = WEEKLY_PROMPT.format(date_str=date_str)
        ai_content = generate_ai_content(client, prompt, use_search=True, temperature=0.1)

        if ai_content and is_valid_html(ai_content):
            template = read_template('weekly')
            # Consistent placeholder passing
            final_html = template.format(date_str=date_str, ai_content=ai_content, form_url=form_url, sentiment_analysis="")
            send_email(final_html, "📊 Weekly Market Recap:")
            save_to_archive("weekly", "📊 Weekly Market Recap:", ai_content)
        else:
            error_msg = "AI returned empty or non-HTML content" if not ai_content else "AI response failed HTML validation"
            logger.error(f"Weekly report failed: {error_msg}")
            send_error_notification("weekly", error_msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Indian Market Briefing Bots")
    parser.add_argument('--type', choices=['morning', 'closing', 'ipo', 'weekly'], required=True, help="Type of report to generate")
    args = parser.parse_args()
    
    run_bot(args.type)
