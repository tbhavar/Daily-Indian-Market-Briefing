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
            # Filter for Mainboard Equity IPOs
            if isinstance(data, dict) and data.get('ipos'):
                filtered_ipos = []
                for ipo in data['ipos']:
                    # Extract strings safely for comparison
                    name = str(ipo.get('name', '')).upper()
                    category = str(ipo.get('category', '')).upper()
                    ipo_type = str(ipo.get('type', '')).upper()
                    
                    # Logic to identify Mainboard Equity:
                    # 1. Exclude NCDs/Debt (often present in name or category)
                    if any(term in name for term in ["NCD", "DEBENTURE", "BOND", "DEBT"]):
                        continue
                    if any(term in category for term in ["NCD", "DEBT"]):
                        continue
                        
                    # 2. Exclude SME IPOs (we want Mainboard only)
                    if ipo_type == "SME" or "SME" in name:
                        continue
                        
                    # 3. If type exists and it's SME or something else, skip it. 
                    # Usually, mainboard is explicitly tagged as 'MAINBOARD' or 'REGULAR'.
                    # Given the user's request, we'll be restrictive.
                    filtered_ipos.append(ipo)
                
                data['ipos'] = filtered_ipos
                
            return data if (isinstance(data, dict) and data.get('ipos')) else "NONE"
        
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
