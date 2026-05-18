import boto3
from dotenv import load_dotenv
import os
from fetch_anomalies import fetch_anomalies, get_mock_anomaly, parse_anomaly
from explain_anomaly import explain_anomaly

load_dotenv()

def send_alert(anomaly, explanation):
    sns = boto3.client('sns', region_name='us-east-1')

    topic_arn = os.getenv("SNS_TOPIC_ARN")

    subject = f"SpendLens Alert: {anomaly['service']} cost spike detected"

    message = f"""
SpendLens Cost Anomaly Alert
=============================

Service:        {anomaly['service']}
Date Range:     {anomaly['start_date']} to {anomaly['end_date']}
Expected Spend: ${anomaly['expected_spend']}
Actual Spend:   ${anomaly['actual_spend']}
Extra Cost:     ${anomaly['total_impact']}
Severity:       {anomaly['severity_score']} / 1.0

AI Analysis
-----------
{explanation}

---
Powered by SpendLens
"""

    sns.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message
    )

    print(f"Alert sent for: {anomaly['service']}")

anomalies = fetch_anomalies()
if not anomalies:
    anomalies = get_mock_anomaly()

parsed = [parse_anomaly(a) for a in anomalies]

for p in parsed:
    explanation = explain_anomaly(p)
    result = send_alert(p, explanation)