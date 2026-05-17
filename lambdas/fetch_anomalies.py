import boto3
import json
from datetime import datetime, timedelta

def fetch_anomalies():
    client = boto3.client('ce', region_name='us-east-1')

    end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

    response = client.get_anomalies(
        DateInterval={
        'StartDate': start_date,
        'EndDate': end_date,
    },
    TotalImpact={
        'NumericOperator': 'GREATER_THAN_OR_EQUAL',
        'StartValue': 1
    },
    )

    anomalies = response.get('Anomalies', [])
    print(f"Found {len(anomalies)} anomalies")

    for a in anomalies:
        print(json.dumps(a, indent=2, default=str))

    return anomalies


def get_mock_anomaly():
    return [
        {
            "AnomalyId": "mock-anomaly-001",
            "AnomalyStartDate": "2026-05-10",
            "AnomalyEndDate": "2026-05-15",
            "DimensionValue": "Amazon EC2",
            "Impact": {
                "MaxImpact": 45.67,
                "TotalActualSpend": 89.23,
                "TotalExpectedSpend": 12.50,
                "TotalImpact": 76.73
            },
            "MonitorArn": "mock-monitor-arn",
            "Feedback": "YES",
            "AnomalyScore": {
                "MaxScore": 0.95,
                "CurrentScore": 0.85
            }
        }
    ]

def parse_anomaly(anomaly):
    return {
        'anomaly_id': anomaly['AnomalyId'],
        'service': anomaly['DimensionValue'],
        'start_date': anomaly['AnomalyStartDate'],
        'end_date': anomaly['AnomalyEndDate'],
        'expected_spend': anomaly['Impact']['TotalExpectedSpend'],
        'actual_spend': anomaly['Impact']['TotalActualSpend'],
        'total_impact': anomaly['Impact']['TotalImpact'],
        'severity_score': anomaly['AnomalyScore']['MaxScore']
    }

anomalies = fetch_anomalies()
if not anomalies:
    print("No anomalies found, using mock data")
    anomalies = get_mock_anomaly()

print(f"Working with {len(anomalies)} anomalies")

parsed = [parse_anomaly(a) for a in anomalies]
for p in parsed:
    print(json.dumps(p, indent=2))