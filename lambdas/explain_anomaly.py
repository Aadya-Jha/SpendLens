from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_anomaly(anomaly):
    prompt = f"""
You are a cloud cost expert. Analyze this AWS cost anomaly and explain it clearly.

Anomaly Details:
- Service: {anomaly['service']}
- Expected Spend: ${anomaly['expected_spend']}
- Actual Spend: ${anomaly['actual_spend']}
- Extra Cost: ${anomaly['total_impact']}
- Date Range: {anomaly['start_date']} to {anomaly['end_date']}
- Severity Score: {anomaly['severity_score']} out of 1.0

Respond in exactly this format:

SUMMARY:
One sentence explaining what happened in plain English.

ROOT CAUSE:
Most likely reason this spike occurred.

RECOMMENDATIONS:
1. First action to take
2. Second action to take
3. Third action to take
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# test it
from fetch_anomalies import fetch_anomalies, get_mock_anomaly, parse_anomaly

anomalies = fetch_anomalies()
if not anomalies:
    anomalies = get_mock_anomaly()

parsed = [parse_anomaly(a) for a in anomalies]

for p in parsed:
    explanation = explain_anomaly(p)
    print(explanation)