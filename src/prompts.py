MORNING_PROMPT = """
Act as a Senior Market Strategist for CA Tanmay R Bhavar. 
Search for live Nifty 50 and Sensex opening levels for {date_str}.
Provide:
1. Opening levels and % change.
2. 5 major headlines from Moneycontrol and CNBC TV18.
3. Live sentiment from X (Twitter) and Reddit (r/IndiaInvestments).
Format as professional HTML using <h3> tags for headers, and clean, styled HTML <table> tags with borders and padding to present the data (levels, headlines, sentiment) in a structured tabular format instead of paragraphs or lists.
Explicitly color code positive changes/sentiments in green (#2e7d32) and negative ones in red (#d32f2f).
Do not include <html> or <body> tags.
"""

CLOSING_PROMPT = """
Analyze the Indian market closing for {date_str}. 
Include:
1. Closing levels for Nifty 50 and Bank Nifty.
2. Top 3 gainers and losers with reasons.
3. Technical Outlook: Next trading day's strategy based on today's price action.
Format as professional HTML using <h3> tags for headers, <ul> for lists, and <p> for paragraphs. 
Explicitly color code positive changes/sentiments in green (#2e7d32) and negative ones in red (#d32f2f).
Do not include <html> or <body> tags.
"""

IPO_PROMPT = """
Convert this IPO JSON into a professional HTML report for CA Tanmay R Bhavar: {raw_data}. 
Include:
1. IPO Name and Dates.
2. Subscription Status and GMP (if available).
3. Final Verdict for investors.
Format as professional HTML using <h3> tags for headers, <ul> for lists, and <p> for paragraphs.
Explicitly color code positive premiums/subscriptions in green (#2e7d32) and negative/neutral ones in red (#d32f2f) or grey.
Do not include <html> or <body> tags.
"""
