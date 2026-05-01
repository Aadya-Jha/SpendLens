# SpendLens  
## AI-Powered AWS Cost Anomaly Explainer  

### Build Timeline • v1.0  

---

##  Project Summary

SpendLens is a **4-week solo build**. Each week has a clear deliverable so progress is always visible.  

The project is structured to be **fully functional by the end of Week 3**, with **Week 4 dedicated to polish, documentation, and portfolio presentation**. :contentReference[oaicite:0]{index=0}  

---

##  Weekly Overview

| Week | Focus | Deliverable |
|------|------|------------|
| Week 1 | AWS Foundations + Lambda | Scheduled Lambda running and logging to CloudWatch |
| Week 2 | Data Layer | Real anomaly data fetched and stored in DynamoDB |
| Week 3 | AI Integration + Alerts | Full pipeline: anomaly → Claude → email alert |
| Week 4 | Polish + Portfolio | README, architecture diagram, demo |

---

#  Week 1 — AWS Foundations & Lambda

###  Goal
Get comfortable with **Lambda and IAM**. By the end, you should have a scheduled Lambda running daily with logs.

###  Days 1–2: IAM & Lambda Basics
- Learn IAM concepts: roles, policies
- Create your first Lambda (Python runtime)
- Print `"SpendLens is running"` → log to CloudWatch
- View CloudWatch logs
- Understand Lambda execution roles

###  Days 3–4: EventBridge Scheduler
- Create EventBridge rule (cron: daily 8 AM UTC)
- Connect to Lambda
- Manually trigger and verify logs
- Learn environment variables in Lambda

###  Days 5–7: Boto3 Basics
- Learn Boto3 (AWS SDK for Python)
- Call a simple AWS API (e.g., list S3 buckets)
- Understand credentials (local vs Lambda)

###  Week 1 Checkpoint
- Trigger Lambda manually  
- View logs in CloudWatch  
- Daily schedule working  
- IAM basics clear  

---

#  Week 2 — Data Layer

###  Goal
Fetch AWS cost anomaly data and store it in DynamoDB with deduplication.

###  Days 1–2: Cost Explorer API
- Read anomaly detection docs
- Start with **mocked data**
- Create sample anomaly JSON
- Extract:
  - service
  - cost delta
  - date range

###  Days 3–4: DynamoDB Integration
- Create table: `spendlens-alerts`
- Partition key: `anomaly_id`
- Add IAM permissions
- Implement:
  - Deduplication check
  - Insert new anomalies
- Add TTL (90 days expiry)

###  Days 5–7: Real API Call
- Replace mock data with real API
- Handle empty responses
- Test full flow

###  Week 2 Checkpoint
- Real/mocked anomaly data fetched  
- Stored in DynamoDB  
- No duplicates  

---

#  Week 3 — AI Integration & Alerts

###  Goal
Full pipeline working:
**Anomaly → Claude → Email alert**

###  Days 1–2: Claude API
- Get Anthropic API key
- Learn Messages API
- Build standalone script
- Prompt should return:
  - 1-line summary
  - root cause
  - 2–3 recommendations
- Format clean output

###  Days 3–4: SNS Alerts
- Create SNS topic: `spendlens-alerts-topic`
- Subscribe email
- Add publish permissions
- Send alert from Lambda
- Test email delivery

###  Days 5–7: Secrets + Testing
- Store API key in Secrets Manager
- Fetch at runtime
- Run full pipeline test
- Debug via CloudWatch
- Validate alert formatting

###  Week 3 Checkpoint
- End-to-end system working  
- AI explanation generated  
- Email alerts received  

---

#  Week 4 — Polish & Portfolio

###  Goal
Make the project **resume + interview ready**

###  Days 1–2: README
Include:
- Problem statement
- Architecture diagram
- Services used + why
- Setup instructions
- Example alert

###  Days 3–4: Architecture Diagram
- Tools: draw.io / Excalidraw
- Flow:
EventBridge → Lambda → Cost Explorer → DynamoDB → Claude → SNS → Email
- Use AWS icons
- Export PNG and embed

###  Days 5–7: Demo & Edge Cases
- Record 2-min demo video
- Handle edge cases:
- No anomalies → no email
- Claude failure → fallback alert
- DynamoDB failure → log + continue
- Add GitHub Actions (bonus)
- Tag `v1.0`

###  Week 4 Checkpoint
- Clean GitHub repo  
- Demo ready  
- Fully explainable in interview  

---

# Interview Talking Points

| Question | What It Tests |
|---------|-------------|
| Why did you build SpendLens? | Problem understanding |
| Explain architecture | System design clarity |
| Why DynamoDB over RDS? | Tech decision making |
| How does deduplication work? | Stateful logic |
| What would you add next? | Scalability thinking |
| Hardest part? | Debugging + honesty |

---

#  Time Estimate

| Week | Hours/Day | Total | Risk |
|------|----------|------|------|
| Week 1 | 1.5 hrs | ~10 hrs | IAM confusion |
| Week 2 | 1.5 hrs | ~10 hrs | API complexity |
| Week 3 | 2 hrs | ~14 hrs | Prompt engineering |
| Week 4 | 1 hr | ~7 hrs | Scope creep |

###  Total: ~41 hours

---

## Notes
- Week 3 is the hardest — allocate buffer time  
- Use mocked data early to avoid AWS costs  
- Keep scope tight — don’t over-engineer  

---

##  Final Outcome

By the end, you will have:
- A **production-like AWS project**
- Strong **backend + cloud fundamentals**
- A **resume-worthy system design project**

---