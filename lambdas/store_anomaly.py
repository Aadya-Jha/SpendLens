import boto3
from datetime import datetime

def is_duplicate(table, anomaly_id):
    response = table.get_item(
        Key = {'anomaly_id' : anomaly_id}
    )
    return 'Item' in response

def store_anomalies(anomaly):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('spendlens-alerts')

    if is_duplicate(table, anomaly['anomaly_id']):
        print(f"Duplicate found, skipping: {anomaly['anomaly_id']}")
        return False

    table.put_item(
        Item={
            'anomaly_id': anomaly['anomaly_id'],
            'service': anomaly['service'],
            'start_date': anomaly['start_date'],
            'end_date': anomaly['end_date'],
            'expected_spend': str(anomaly['expected_spend']),
            'actual_spend': str(anomaly['actual_spend']),
            'total_impact': str(anomaly['total_impact']),
            'severity_score': str(anomaly['severity_score']),
            'processed_at': datetime.utcnow().isoformat()
        }
    )
    print(f"Stored anomaly: {anomaly['anomaly_id']}")
    return True

from fetch_anomalies import fetch_anomalies, get_mock_anomaly, parse_anomaly

anomalies = fetch_anomalies()
if not anomalies:
    anomalies = get_mock_anomaly()

parsed = [parse_anomaly(a) for a in anomalies]

for p in parsed:
    result = store_anomalies(p)
    print(f"Stored: {result}")