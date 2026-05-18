from flask import Flask, jsonify
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)

def get_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    return dynamodb.Table('spendlens-alerts')

@app.route('/health')
def health():
    return jsonify({'status': 'SpendLens API is running'})

@app.route('/anomalies')
def get_anomalies():
    table = get_table()
    response = table.scan()
    items = response.get('Items', [])
    return jsonify({'anomalies': items, 'count': len(items)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)