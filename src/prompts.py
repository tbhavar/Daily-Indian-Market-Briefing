MORNING_PROMPT = """
Act as a Senior Market Strategist for CA Tanmay R Bhavar. 
Search for live Nifty 50 and Sensex opening levels for {date_str}.
Provide:
1. Opening levels and % change.
2. 5 major headlines from Moneycontrol and CNBC TV18.
3. Live sentiment from X (Twitter) and Reddit (r/IndiaInvestments).
Format as professional HTML with Navy Blue (#1a237e) and Emerald Green (#2e7d32) theme. 
Do not include <html> or <body> tags.
"""

CLOSING_PROMPT = """
Analyze the Indian market closing for {date_str}. 
Include:
1. Closing levels for Nifty 50 and Bank Nifty.
2. Top 3 gainers and losers with reasons.
3. Technical Outlook: Next trading day's strategy based on today's price action.
Format as professional HTML for CA Tanmay R Bhavar using a Slate Grey (#2c3e50) and Gold (#D4AF37) theme. 
Do not include <html> or <body> tags.
"""

IPO_PROMPT = """
Convert this IPO JSON into a professional HTML report for CA Tanmay R Bhavar: {raw_data}. 
Use a Navy Blue and Gold theme. 
Include:
1. IPO Name and Dates.
2. Subscription Status and GMP (if available).
3. Final Verdict for investors.
Do not include <html> or <body> tags.
"""
