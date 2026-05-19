# SpendLens 
> AI-Powered AWS Cost Anomaly Explainer

SpendLens monitors your AWS account for cost anomalies daily, generates plain-English explanations using AI, and emails you actionable fix recommendations — automatically.

AWS's native alerts tell you *that* something spiked. SpendLens tells you *why* and *what to do about it.*

---

## Demo

![SpendLens Dashboard](docs/dashboard.png)

---

## Features

- **Daily automated monitoring** — runs every day at 8AM UTC via EventBridge
- **AI-powered explanations** — plain English root cause analysis with fix recommendations
- **Smart deduplication** — never alerts you about the same anomaly twice
- **Web dashboard** — visualize anomaly history and cost impact by service
- **One-command deploy** — entire AWS stack provisioned automatically
- **Fully serverless** — no servers, no maintenance, costs ~₹1/day to run

---

## Architecture

EventBridge (cron: 8AM UTC)
↓
AWS Lambda
↓
Cost Explorer API ──→ DynamoDB (deduplication + storage)
↓
Groq AI (explanation generation)
↓
SNS (email alert)
↓
Flask API ──→ Dashboard

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Scheduler | AWS EventBridge | Managed cron, no servers needed |
| Compute | AWS Lambda (Python 3.12) | Serverless, pay only per execution |
| Data Source | AWS Cost Explorer API | Native AWS anomaly detection |
| Storage | AWS DynamoDB | Serverless NoSQL, fast key lookups |
| AI | Groq API (Llama 3.3 70B) | Fast inference, free tier available |
| Alerts | AWS SNS | Managed email delivery |
| API | Flask | REST endpoints for dashboard |

---

## Prerequisites

Before you begin make sure you have:

- An AWS account with billing enabled
- AWS CLI installed and configured
- Python 3.12 installed
- A Groq API key — free at [console.groq.com](https://console.groq.com)

---

## Getting Started

### Step 1 — Clone the repo

```bash
git clone https://github.com/yourusername/spendlens.git
cd spendlens
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Configure AWS CLI

If you haven't already, configure your AWS credentials:

```bash
aws configure
```

You'll need:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (recommended: `us-east-1`)
- Default output format: `json`

To verify it's working:
```bash
aws sts get-caller-identity
```

### Step 4 — Run the setup script

```bash
python setup.py
```

The script will ask for:
- Your email address for alerts
- AWS region (press Enter for `us-east-1`)
- Your Groq API key

It will then automatically:
1. Create a DynamoDB table (`spendlens-alerts`)
2. Create an SNS topic and subscribe your email
3. Create an IAM role with required permissions
4. Package and deploy the Lambda function
5. Set up the EventBridge daily schedule

**Important:** After running setup, check your email and confirm the SNS subscription. You won't receive alerts until you confirm.

### Step 5 — Confirm your email subscription

AWS will send a confirmation email to the address you provided. Click **Confirm subscription** in that email.

### Step 6 — Run the dashboard locally

Start the Flask API:
```bash
cd api
python app.py
```

Open `frontend/index.html` in your browser. The dashboard will show all detected anomalies with AI explanations and cost charts.

---

## How It Works

### 1. Anomaly Detection
Every day at 8AM UTC, EventBridge triggers the Lambda function. It calls the AWS Cost Explorer API to fetch any cost anomalies from the past 30 days where the extra spend exceeds $1.

### 2. Deduplication
Before processing, SpendLens checks DynamoDB to see if this anomaly has already been handled. If it has, it skips it — so you never get the same alert twice.

### 3. AI Explanation
New anomalies are sent to the Groq API with a structured prompt. The AI returns:
- A one-line plain English summary
- The most likely root cause
- 3 specific fix recommendations

### 4. Alert
The explanation is emailed to you via SNS and stored in DynamoDB for the dashboard.

---

## Project Structure

```text
spendlens/
├── lambdas/
│   ├── lambda_function.py      # main handler, orchestrates the pipeline
│   ├── fetch_anomalies.py      # Cost Explorer API + mock fallback
│   ├── store_anomaly.py        # DynamoDB storage + deduplication
│   ├── explain_anomaly.py      # Groq AI explanation generation
│   └── send_alert.py           # SNS email delivery
├── api/
│   └── app.py                  # Flask REST API
├── frontend/
│   └── index.html              # web dashboard
├── setup.py                    # automated deployment script
├── requirements.txt            # Python dependencies
└── README.md
```

---

## API Reference

The Flask API runs locally on port 5000.

**GET /health**
```json
{
  "status": "SpendLens API is running"
}
```

**GET /anomalies**
```json
{
  "count": 1,
  "anomalies": [
    {
      "anomaly_id": "abc-123",
      "service": "Amazon EC2",
      "actual_spend": "89.23",
      "expected_spend": "12.50",
      "total_impact": "76.73",
      "severity_score": "0.95",
      "start_date": "2026-05-10",
      "end_date": "2026-05-15",
      "explanation": "...",
      "processed_at": "2026-05-18T16:49:07"
    }
  ]
}
```

---

## Cost to Run

| Service | Monthly Cost |
|---------|-------------|
| AWS Lambda | Free (1M requests/month free tier) |
| AWS DynamoDB | Free (25GB free tier) |
| AWS EventBridge | Free (unlimited scheduled rules) |
| AWS SNS | Free (1000 emails/month free tier) |
| AWS Cost Explorer | ~$0.30/month |
| Groq API | Free tier |
| **Total** | **~₹25/month** |

---

## Troubleshooting

**Not receiving email alerts?**
- Check your spam folder
- Make sure you confirmed the SNS subscription email
- Check CloudWatch logs: `Logs → /aws/lambda/spendlens-daily`

**Lambda timing out?**
- Go to Lambda → Configuration → General → increase timeout to 30 seconds

**Access Denied errors?**
- Check the Lambda execution role has `ce:GetAnomalies`, `sns:Publish`, and `AmazonDynamoDBFullAccess` permissions

**No anomalies showing?**
- Your AWS account may be too new for Cost Explorer to detect patterns
- Cost Explorer needs ~2 weeks of billing history to detect anomalies
- The system falls back to mock data automatically during this period

---

## What's Next

- [ ] Slack notifications alongside email
- [ ] Multi-account support via IAM cross-account roles  
- [ ] Cost forecasting using historical billing data
- [ ] Terraform module for infrastructure as code deployment
- [ ] Docker support for local development

---

## Author

Built by Aadya

---

## License

MIT License — free to use, modify, and deploy to your own AWS account.