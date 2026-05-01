# SpendLens  
## AI-Powered AWS Cost Anomaly Explainer  

### System Workflow Document • v1.0  

---

## System Overview

SpendLens monitors an AWS account for unexpected cost spikes, identifies the service or resource responsible, and delivers a plain-English explanation with actionable recommendations automatically. :contentReference[oaicite:0]{index=0}  

### Core Problem Being Solved

AWS bills can spike unexpectedly, and engineers often spend hours investigating Cost Explorer to identify the cause. SpendLens automates this process and provides clear explanations without manual effort. :contentReference[oaicite:1]{index=1}  

---

## End-to-End Workflow

### Step 1 — Scheduled Trigger

EventBridge triggers the system daily at 08:00 UTC.

- Trigger: EventBridge Scheduler (cron expression)  
- Frequency: Daily (configurable)  
- Target: SpendLens Lambda function via IAM role  

---

### Step 2 — Cost Anomaly Detection

Lambda fetches anomalies using the AWS Cost Explorer API.

- API: `cost_explorer.get_anomalies()`  
- Lookback window: 7 days  
- Filter: anomalies above $5 threshold (configurable)  
- Output: anomaly objects with service, account, cost delta, date range  

---

### Step 3 — Deduplication Check

Prevents duplicate alerts using DynamoDB.

- Table: `spendlens-alerts`  
- Key: `anomaly_id`  
- If exists: skip  
- If new: process and mark as seen  

---

### Step 4 — AI Analysis via Claude API

Each anomaly is analyzed using Claude.

- Model: `claude-sonnet-4-20250514`  
- Input: service, cost delta, time range, usage data  
- Output:
  - One-line summary  
  - Root cause explanation  
  - 2–3 actionable recommendations  

---

### Step 5 — Store to DynamoDB

Stores anomaly data and analysis.

- Table: `spendlens-alerts`  
- TTL: 90 days  
- Fields:
  - anomaly_id  
  - service  
  - cost_delta  
  - analysis  
  - timestamp  
  - status  

---

### Step 6 — Alert Delivery via SNS

Delivers alerts to subscribers.

- SNS Topic: `spendlens-alerts-topic`  
- Default subscriber: email  
- Format: plain-text summary, explanation, recommendations  
- Extensible to Slack, PagerDuty, etc.  

---

## Data Flow Summary

| Step | Component | Action | Output |
|------|----------|--------|--------|
| 1 | EventBridge | Trigger scheduled job | Lambda invocation |
| 2 | Lambda + Cost Explorer | Fetch anomalies | List of anomalies |
| 3 | Lambda + DynamoDB | Deduplicate | New anomalies only |
| 4 | Lambda + Claude API | Analyze anomalies | Explanation |
| 5 | Lambda + DynamoDB | Store records | Persisted data |
| 6 | Lambda + SNS | Send alerts | Email delivered |

---

## AWS Services Used

| Service | Purpose | Free Tier |
|--------|--------|----------|
| AWS Lambda | Runs core logic | 1M requests/month |
| Amazon EventBridge | Scheduling | Free for cron |
| AWS Cost Explorer API | Fetch anomalies | ~$0.01 per call |
| Amazon DynamoDB | Storage | 25GB free |
| Amazon SNS | Alerts | 1000 emails/month |
| Claude API | AI analysis | $5 free credits |
| AWS IAM | Permissions | Always free |

---

## Error Handling and Edge Cases

- No anomalies: exit gracefully, no alert  
- Cost Explorer failure: retry once, log error  
- Claude failure: send alert without AI analysis  
- DynamoDB failure: log error, still send alert  
- SNS failure: CloudWatch alarm triggers  

---

## Security Considerations

- Least-privilege IAM roles  
- Claude API key stored in AWS Secrets Manager  
- DynamoDB restricted to Lambda role  
- SNS publish restricted to Lambda role  
- No sensitive cost data logged  

---

## Extensibility

- Add Slack alerts via SNS subscriber without code changes  
- Add new anomaly sources (Trusted Advisor, GuardDuty) via additional triggers  
- Update Claude prompt independently of infrastructure  

---