MORNING_PROMPT = """
Act as a Senior Market Strategist for CA Tanmay R Bhavar. 
Search for live Nifty 50 and Sensex opening levels specifically for {date_str}.

### ACCURACY REQUIREMENT:
1. Fetch actual real-time opening levels and change data for {date_str}.
2. Cross-verify with multiple sources to ensure precision.
3. If the market hasn't opened yet for {date_str}, use the latest pre-market indications or previous close.

Provide the response ONLY in professional HTML format.
Use <h3> tags for headers and <table> tags for all data. 

### HTML Requirements:
1. Tables MUST have: border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #e2e8f0; font-size: 14px;"
2. Header cells (<th>) style: background-color: #f8fafc; color: #1a237e; text-align: left;
3. Use inline styles for EVERYTHING (no <style> blocks).
4. Color code values: Green (#2e7d32) for positive/gaining, Red (#d32f2f) for negative/losing.
5. Do NOT include markdown blocks (```html) or <html>/<body> tags.

### Content Structure (Use this EXACT structure):
1. <h3>📈 Market Opening Levels</h3> -> Table with Index, Opening Level, Change (Pts), Change (%).
2. <h3>📰 Top Market Headlines</h3> -> Table with Source, Headline Summary.
3. <h3>📊 Sectoral Performance</h3> -> Table with Rank, Sector, Trend (Gaining/Losing), Brief Reason.
4. [SENTIMENT_START]
   <h3>🌐 Social Media Pulse (X & Reddit)</h3>
   Analyze live sentiment from x.com (Twitter) and r/IndiaInvestments on reddit.com specifically for {date_str}.
   Table with: Platform, Top Discussions/Trends, Market Sentiment (Bearish/Bullish/Cautious).
   [SENTIMENT_END]
"""

CLOSING_PROMPT = """
Analyze the Indian market closing for {date_str}. 

### CRITICAL ACCURACY REQUIREMENT:
1. You MUST fetch the actual, real-time closing levels for BSE Sensex, NSE Nifty 50, Nifty Bank, and Nifty Midcap 100 specifically for {date_str}.
2. Check multiple search results to verify the accuracy of the closing levels, change amounts, and percentages. 
3. DO NOT hallucinate or provide placeholder data. If specific data for a sector or stock is unavailable for today, describe the general trend honestly rather than inventing numbers.
4. Precision is paramount. Ensure the "Session Trend" (Positive/Negative) matches the mathematical change.

Provide the response ONLY in professional HTML format.
Use <h3> tags for headers and <table> tags for all data.

### HTML Requirements:
1. Tables MUST have: border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #e2e8f0; font-size: 14px;"
2. Header cells (<th>) style: background-color: #f8fafc; color: #1a237e; text-align: left;
3. Use inline styles for EVERYTHING.
4. Color code values: Green (#2e7d32) for positive, Red (#d32f2f) for negative.
5. Do NOT include markdown blocks (```html) or <html>/<body> tags.

### Content Structure:
1. <h3>📉 Market Closing Snapshot</h3> -> Table with Index, Closing Level, Change (%), Session Trend.
2. <h3>🔥 Market Gainers & Losers</h3> -> Table with Stock Name, Change (%), Reason for Move.
3. <h3>🏦 FII/DII Institutional Activity</h3> -> Table with Category, Net Flow (Cr), Sentiment.
4. <h3>🔮 Technical Outlook & Strategy</h3> -> Table with Key Support, Key Resistance, Strategy for Tomorrow.
5. [SENTIMENT_START]
   <h3>🌐 Social Media Pulse (X & Reddit)</h3>
   Analyze closing sentiment/discussions from x.com and reddit.com (r/IndiaInvestments) specifically for {date_str}.
   Table with: Platform, Key Takeaways, Community Sentiment.
   [SENTIMENT_END]
"""

IPO_PROMPT = """
Act as an IPO Research Analyst focusing EXCLUSIVELY on Indian Mainboard Equity IPOs. 
I will provide a JSON list of live/upcoming market instruments: {raw_data}.

### CRITICAL REQUIREMENT:
Analyze ONLY Mainboard Equity IPOs. 
ABSOLUTELY IGNORE and DISCARD any of the following if present in the data:
- SME IPOs (Small & Medium Enterprises)
- NCDs (Non-Convertible Debentures)
- Gold Bonds or Corporate Bonds
- REITs or InvITs
- Rights Issues or Buybacks

If the provided data contains no Mainboard Equity IPOs, respond ONLY with "NONE".

### YOUR TASK:
For each VALID Mainboard Equity IPO listed in the JSON, perform a live search to find:
1. **Latest GMP (Grey Market Premium)** and expected listing gain.
2. **Current Subscription Status** (Total, Retail, and NII/HNI portions).
3. **Analyst Sentiment**: Key strengths, risks, and a final "Apply" or "Avoid" verdict.

### HTML Requirements:
1. Provide the response ONLY in professional HTML format.
2. Use <h3> tags for headers and <table> tags.
3. Tables MUST have: border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #e2e8f0; font-size: 14px;"
4. Use Green (#2e7d32) for strong GMP/Subscription (>15%) and Red (#d32f2f) for low interest or negative GMP.
5. Do NOT include markdown blocks (```html) or <html>/<body> tags.

### Structure:
1. <h3>🚀 Live IPO Intelligence & GMP</h3> -> Table with IPO Name, Dates, Subscription (Total x), GMP (Pts/%), Expected Listing Gain.
2. <h3>💡 Final Verdict for Investors</h3> -> For each IPO, provide a concise summary of Strengths, Risks, and the Final Verdict.
"""

WEEKLY_PROMPT = """
Compile a comprehensive weekly market recap for the week ending {date_str}.

### CRITICAL ACCURACY REQUIREMENT:
1. You MUST fetch the actual weekly performance data for Indian indices specifically for the week ending {date_str}.
2. Verify weekly gains/losses, top stock movers, and institutional flows (FII/DII) against multiple reliable financial sources.
3. Ensure the summary is factually grounded and matches the weekly trend accurately.

Provide the response ONLY in professional HTML format.
Use <h3> tags for headers and <table> tags for all data.

### HTML Requirements:
1. Tables MUST have: border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #e2e8f0; font-size: 14px;"
2. Color code weekly gains in Green (#2e7d32) and losses in Red (#d32f2f).
3. Do NOT include markdown blocks or <html>/<body> tags.

### Structure:
1. <h3>📉 Weekly Index Performance</h3> -> Table with Index, Open, Close, Weekly Change (%).
2. <h3>🔝 Weekly Top Moves (Stocks)</h3> -> Table with Type (Gainer/Loser), Stock Name, Weekly Change (%), Reason.
3. <h3>🏛 Institutional Activity (FII/DII)</h3> -> Table with Category, Cumulative Flow (Cr), Sentiment.
4. <h3>📊 Sectoral Roadmap</h3> -> Table with Sector, Performance, Key Driving Factor.
5. <h3>📅 Upcoming Week Triggers</h3> -> Table with Event Date, Event Name, Potential Impact.
"""
