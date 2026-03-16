
import os
import sys
from datetime import datetime
import pytz

# Add current directory to path so we can import src
sys.path.append(os.getcwd())

from src.utils import get_genai_client, is_market_open

IST = pytz.timezone('Asia/Kolkata')

def test_market_status():
    print(f"Current IST Time: {datetime.now(IST)}")
    client = get_genai_client()
    print("Checking market status...")
    status = is_market_open(client)
    print(f"Market Open: {status}")

if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not set")
    else:
        test_market_status()
