# SpendLens  
## AI-Powered AWS Cost Anomaly Explainer  

### Build Timeline • v2.0  

---

## Project Summary

SpendLens is a **solo build targeting placement readiness**. Each week has a clear deliverable so progress is always visible.  

The project is structured to be **fully functional by the end of Week 3**, with **Week 4 dedicated to the dashboard and API layer**, and **Week 5 for polish, documentation, and portfolio presentation**.

---

## Weekly Overview

| Week | Focus | Deliverable |
|------|------|------------|
| Week 1 | AWS Foundations + Lambda | ✅ Scheduled Lambda running and logging to CloudWatch |
| Week 2 | Data Layer | Real anomaly data fetched and stored in DynamoDB |
| Week 3 | AI Integration + Alerts | Full pipeline: anomaly → Claude → email alert |
| Week 4 | Dashboard + API | Flask REST API + frontend dashboard deployed |
| Week 5 | Polish + Portfolio | README, architecture diagram, demo video |

---

# ✅ Week 1 — AWS Foundations & Lambda (DONE)

### Goal
Get comfortable with **Lambda and IAM**. Lambda running on a daily schedule with CloudWatch logs.

### Completed
- IAM user `spendlens-dev` created with AdministratorAccess
- Zero-spend budget alert active
- Lambda function `spendlens-daily` created (Python 3.12)
- EventBridge cron trigger set (daily 8 AM UTC)
- CloudWatch logs verified
- Boto3 basics done — listed S3 buckets from Lambda

---

# Week 2 — Data Layer

### Goal
Fetch AWS cost anomaly data and store it in DynamoDB with deduplication.

### Days 1–2: Cost Explorer API
- Read anomaly detection docs
- Start with **mocked data**
- Create sample anomaly JSON
- Extract:
  - service
  - cost delta
  - date range

### Days 3–4: DynamoDB Integration
- Create table: `spendlens-alerts`
- Partition key: `anomaly_id`
- Add IAM permissions
- Implement:
  - Deduplication check
  - Insert new anomalies
- Add TTL (90 days expiry)

### Days 5–7: Real API Call
- Replace mock data with real Cost Explorer API call
- Handle empty responses
- Set up VSCode locally with AWS CLI + Boto3
- Test full flow end to end

### Week 2 Checkpoint
- Real/mocked anomaly data fetched  
- Stored in DynamoDB  
- No duplicates  
- Code pushed to GitHub  

---

# Week 3 — AI Integration & Alerts

### Goal
Full pipeline working:
**Anomaly → Claude → Email alert**

### Days 1–2: Claude API
- Get Anthropic API key
- Learn Messages API
- Build standalone script
- Prompt should return:
  - 1-line summary
  - root cause
  - 2–3 fix recommendations
- Format clean output

### Days 3–4: SNS Alerts
- Create SNS topic: `spendlens-alerts-topic`
- Subscribe email
- Add publish permissions
- Send alert from Lambda
- Test email delivery

### Days 5–7: Secrets + Testing
- Store Claude API key in Secrets Manager
- Fetch at runtime
- Run full pipeline test
- Debug via CloudWatch
- Validate alert formatting

### Week 3 Checkpoint
- End-to-end pipeline working  
- AI explanation generated  
- Email alerts received  
- Full flow: EventBridge → Lambda → Cost Explorer → DynamoDB → Claude → SNS → Email  

---

# Week 4 — Dashboard + API Layer

### Goal
Make SpendLens a **visible, demoable product** — not just a backend script.

### Days 1–2: Flask REST API
- Build Flask app with these endpoints:
  - `GET /anomalies` — list all stored anomalies
  - `GET /anomalies/<id>` — get one anomaly + Claude explanation
  - `GET /health` — basic health check
- Connect Flask to DynamoDB
- Test endpoints locally

### Days 3–4: API Gateway
- Deploy Flask API via API Gateway on AWS
- Wire it to Lambda
- Test live endpoints from browser

### Days 5–7: Frontend Dashboard
- Simple HTML/CSS/JS dashboard (no framework needed)
- Shows:
  - List of recent anomalies
  - Claude's explanation per anomaly
  - Basic cost trend chart (Chart.js)
- Host as S3 static website

### Week 4 Checkpoint
- REST API live and returning real data  
- Dashboard accessible via browser  
- Can demo the full product visually  

---

# Week 5 — Polish & Portfolio

### Goal
Make the project **resume + interview ready**

### Days 1–2: README
Include:
- Problem statement
- Architecture diagram
- Services used + why each one
- Setup instructions
- Example alert screenshot
- Link to live dashboard

### Days 3–4: Architecture Diagram + Blog Post
- Draw architecture in Excalidraw or draw.io
- Flow: EventBridge → Lambda → Cost Explorer → DynamoDB → Claude → SNS → Email + Dashboard
- Use AWS icons, export PNG, embed in README
- Write a Medium post: "How I built an AI-powered AWS cost monitor as a college student"
  - This alone will get you recruiter attention

### Days 5–7: Demo + Edge Cases
- Record 2-min demo video (Loom is free)
- Handle edge cases:
  - No anomalies → no email sent
  - Claude API failure → fallback plain-text alert
  - DynamoDB failure → log and continue
- Tag release `v1.0` on GitHub

### Week 5 Checkpoint
- Clean GitHub repo  
- Demo video ready  
- Medium post published  
- Fully explainable in interview  

---

# Interview Talking Points

| Question | What It Tests |
|---------|-------------|
| Why did you build SpendLens? | Problem understanding |
| Explain the architecture | System design clarity |
| Why DynamoDB over RDS? | Tech decision making |
| How does deduplication work? | Stateful logic |
| How does the API layer work? | Backend engineering |
| Why serverless over a regular server? | Cloud awareness |
| What would you add next? | Scalability thinking |
| Hardest part? | Debugging + honesty |

---

# Time Estimate

| Week | Hours/Day | Total | Risk |
|------|----------|------|------|
| Week 1 | 1.5 hrs | ~10 hrs | ✅ Done |
| Week 2 | 2 hrs | ~14 hrs | IAM + API complexity |
| Week 3 | 2 hrs | ~14 hrs | Prompt engineering |
| Week 4 | 2.5 hrs | ~17 hrs | Frontend + deployment |
| Week 5 | 1.5 hrs | ~10 hrs | Scope creep |

### Total: ~65 hours

---

## Notes
- Week 3 is the hardest — allocate buffer time  
- Use mocked data in Week 2 first, real API after  
- Dashboard is your most important demo asset — don't skip it  
- The Medium post takes one evening and is worth more than you think  
- Keep scope tight — don't over-engineer  

---

## Final Outcome

By the end, you will have:
- A **full stack cloud project** with a real UI
- A **live REST API** backed by AWS
- Strong **backend + cloud fundamentals**
- A **resume-worthy system design story**
- A **Medium post** that shows up when recruiters Google you