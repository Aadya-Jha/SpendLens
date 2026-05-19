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
- **Infrastructure as code** — entire AWS stack defined in SAM template, deployed in one command
- **Fully serverless** — no servers, no maintenance, costs ~₹25/month to run

---

## Architecture

EventBridge (cron: 8AM UTC)
↓
AWS Lambda
↓
Cost Explorer API ──→ DynamoDB (deduplication + storage)
↓
Groq AI (Llama 3.3 70B)
↓
SNS Email Alert
↓
Flask API ──→ Dashboard

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Scheduler | AWS EventBridge | Managed cron, no servers needed |
| Compute | AWS Lambda (Python 3.11) | Serverless, pay only per execution |
| Data Source | AWS Cost Explorer API | Native AWS anomaly detection |
| Storage | AWS DynamoDB | Serverless NoSQL, fast key lookups |
| AI | Groq API (Llama 3.3 70B) | Fast inference, free tier available |
| Alerts | AWS SNS | Managed email delivery |
| API | Flask | REST endpoints for dashboard |
| IaC | AWS SAM | Infrastructure as code, reproducible deploys |

---

## Prerequisites

Before you begin make sure you have:

- An AWS account with billing enabled
- AWS CLI installed and configured — [Install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- AWS SAM CLI installed — [Install guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.11
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

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`
- Default output format: `json`

Verify it works:
```bash
aws sts get-caller-identity
```

### Step 4 — Build and deploy with SAM

```bash
sam build
sam deploy --guided
```

During guided deploy you'll be asked for:
- **Stack name** — enter `spendlens`
- **AWS Region** — enter `us-east-1`
- **GroqApiKey** — paste your Groq API key
- **AlertEmail** — your email address for alerts
- Accept all other defaults

SAM will automatically create:
- Lambda function with correct IAM permissions
- DynamoDB table for anomaly storage
- SNS topic subscribed to your email
- EventBridge rule for daily scheduling

**Important:** After deploy, check your email and confirm the SNS subscription. You won't receive alerts until you confirm.

### Step 5 — Run the dashboard locally

Start the Flask API:
```bash
cd api
python app.py
```

Open `frontend/index.html` in your browser.

---

## How It Works

### 1. Anomaly Detection
Every day at 8AM UTC, EventBridge triggers the Lambda function. It calls the AWS Cost Explorer API to fetch cost anomalies from the past 30 days where extra spend exceeds $1.

### 2. Deduplication
Before processing, SpendLens checks DynamoDB using the anomaly ID. If already processed, it skips — so you never get the same alert twice.

### 3. AI Explanation
New anomalies are sent to Groq API with a structured prompt. The AI returns:
- A one-line plain English summary
- Most likely root cause
- 3 specific fix recommendations

### 4. Alert + Storage
The explanation is emailed via SNS and stored in DynamoDB for the dashboard to display.

---

## Project Structure

```text
spendlens/
├── lambdas/
│   ├── lambda_function.py      # main handler, orchestrates the pipeline
│   ├── fetch_anomalies.py      # Cost Explorer API + mock fallback
│   ├── store_anomaly.py        # DynamoDB storage + deduplication
│   ├── explain_anomaly.py      # Groq AI explanation generation
│   ├── send_alert.py           # SNS email delivery
│   └── requirements.txt        # Lambda dependencies
├── api/
│   └── app.py                  # Flask REST API
├── frontend/
│   └── index.html              # web dashboard
├── template.yaml               # AWS SAM infrastructure definition
├── samconfig.toml              # SAM deployment configuration
├── setup.py                    # alternative manual deployment script
├── requirements.txt            # local development dependencies
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
| AWS Lambda | Free tier (1M requests/month) |
| AWS DynamoDB | Free tier (25GB storage) |
| AWS EventBridge | Free (unlimited scheduled rules) |
| AWS SNS | Free tier (1000 emails/month) |
| AWS Cost Explorer | ~$0.30/month |
| Groq API | Free tier |
| **Total** | **~₹25/month** |

---

## Troubleshooting

**Not receiving email alerts?**
- Check spam folder
- Confirm the SNS subscription email AWS sent after deploy
- Check CloudWatch logs: `Logs → /aws/lambda/spendlens-daily`

**Lambda timing out?**
- Go to Lambda → Configuration → General → increase timeout to 30 seconds

**Access Denied errors?**
- IAM permissions are managed by SAM — run `sam deploy` again to reset them

**No anomalies showing on dashboard?**
- New AWS accounts need 2+ weeks of billing history for Cost Explorer to detect patterns
- SpendLens falls back to mock data automatically during this period

**Want to redeploy after changes?**
```bash
sam build
sam deploy
```

---

## What's Next

- [ ] Slack notifications alongside email
- [ ] Multi-account support via IAM cross-account roles
- [ ] Cost forecasting using historical billing data
- [ ] Terraform module as alternative IaC option
- [ ] Docker support for local development

---

## Author

Built by Aadya

---

## License

MIT — free to use, modify, and deploy to your own AWS account.