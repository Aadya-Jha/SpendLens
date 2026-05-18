import json
import boto3
import os
from dotenv import load_dotenv
from fetch_anomalies import fetch_anomalies, get_mock_anomaly, parse_anomaly
from store_anomaly import store_anomaly
from explain_anomaly import explain_anomaly
from send_alert import send_alert

load_dotenv()

def lambda_handler(event, context):
    print("SpendLens started")
    
    anomalies = fetch_anomalies()
    if not anomalies:
        print("No real anomalies, using mock data")
        anomalies = get_mock_anomaly()
    
    parsed = [parse_anomaly(a) for a in anomalies]
    print(f"Processing {len(parsed)} anomalies")
    
    processed = 0
    skipped = 0
    
    for anomaly in parsed:
        stored = store_anomaly(anomaly)
        
        if not stored:
            skipped += 1
            continue
        
        explanation = explain_anomaly(anomaly)
        
        send_alert(anomaly, explanation)
        
        processed += 1
    
    print(f"Done — processed: {processed}, skipped: {skipped}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed': processed,
            'skipped': skipped
        })
    }

if __name__ == "__main__":
    lambda_handler({}, {})