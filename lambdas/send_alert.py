import boto3
from dotenv import load_dotenv
import os

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