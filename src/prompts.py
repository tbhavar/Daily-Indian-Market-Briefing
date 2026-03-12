MORNING_PROMPT = """
Act as a Senior Market Strategist for CA Tanmay R Bhavar. 
Search for live Nifty 50 and Sensex opening levels for {date_str}.
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
3. <h3>💬 Live Sentiment Analysis</h3> -> Table with Platform, Sentiment Summary, Outlook (Negative/Neutral/Positive).
4. <h3>📊 Sectoral Performance</h3> -> Table with Rank, Sector, Trend (Gaining/Losing), Brief Reason.
"""

CLOSING_PROMPT = """
Analyze the Indian market closing for {date_str}.
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
"""

IPO_PROMPT = """
Convert this IPO JSON into a professional HTML report: {raw_data}.
Provide the response ONLY in professional HTML format.
Use <h3> tags for headers and <table> tags.

### HTML Requirements:
1. Tables MUST have: border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; margin-bottom: 20px; border-color: #e2e8f0; font-size: 14px;"
2. Use Green (#2e7d32) for High GMP/Subscription and Red (#d32f2f) for low interest.
3. Do NOT include markdown blocks or <html>/<body> tags.

### Structure:
1. <h3>🚀 IPO Details & Status</h3> -> Table with IPO Name, Dates, Subscription Status, GMP.
2. <h3>💡 Final Verdict for Investors</h3> -> Concise reasoning and decision (Apply/Avoid).
"""

WEEKLY_PROMPT = """
Compile a comprehensive weekly market recap for the week ending {date_str}.
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
