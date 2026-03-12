import os
import logging
import requests

logger = logging.getLogger(__name__)

def get_live_ipo_data():
    url = "https://api.ipoalerts.in/ipos?status=open"
    ipo_api_key = os.environ.get("IPOALERTS_API_KEY")
    # Only use key if it's set and doesn't look like a placeholder
    headers = {}
    if ipo_api_key:
        api_key_clean = ipo_api_key.strip()
        # Handle cases where users might accidentally paste "X-API-KEY: your_key" into the secret
        if ":" in api_key_clean and ("x-api-key" in api_key_clean.lower()):
            api_key_clean = api_key_clean.split(":")[-1].strip()
            
        if len(api_key_clean) > 5 and api_key_clean.lower() not in ["none", "null", "undefined"]:
            headers["x-api-key"] = api_key_clean
            ipo_api_key = api_key_clean # For logging below
    
    try:
        logger.info(f"Fetching data from ipoalerts... (Key length: {len(ipo_api_key) if ipo_api_key else 0})")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data if data.get('ipos') else "NONE"
        
        # Log response body on failure for better debugging (truncate if too long)
        error_body = response.text[:200]
        logger.warning(f"IPO API returned status code: {response.status_code}. Response: {error_body}")
        
        # If 401, check if key might have invisible characters
        if response.status_code == 401 and ipo_api_key:
            if ipo_api_key != ipo_api_key.strip():
                logger.warning("Warning: IPOALERTS_API_KEY has leading/trailing whitespace.")
        
        return None
    except Exception as e:
        logger.error(f"Fetch failed: {e}")
        return None
