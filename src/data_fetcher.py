import os
import logging
import requests

logger = logging.getLogger(__name__)

def get_live_ipo_data():
    url = "https://api.ipoalerts.in/ipos?status=open"
    ipo_api_key = os.environ.get("IPOALERTS_API_KEY")
    headers = {"X-API-KEY": ipo_api_key} if ipo_api_key else {}
    
    try:
        logger.info("Fetching data from ipoalerts...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data if data.get('ipos') else "NONE"
        logger.warning(f"IPO API returned status code: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Fetch failed: {e}")
        return None
