## Features

### Core
- **Automated anomaly detection** — polls AWS Cost Explorer daily for unexpected spend spikes, no manual checks needed
- **AI-powered explanations** — feeds raw anomaly data to Claude and gets back a plain-English root cause analysis, not just a number
- **Actionable fix recommendations** — every alert includes 2–3 concrete steps to resolve or prevent the anomaly
- **Email alerts via SNS** — formatted alert delivered directly to your inbox the moment an anomaly is found

### Reliability
- **Deduplication** — DynamoDB tracks seen anomaly IDs so you never get spammed with the same alert twice
- **Graceful degradation** — if Claude API is unavailable, the alert still sends with raw anomaly data rather than silently failing
- **Configurable threshold** — minimum cost delta (default $5) filters out noise from tiny fluctuations

### Security
- **Secrets Manager integration** — API keys are never hardcoded or stored in environment variables
- **Least-privilege IAM** — Lambda role has only the exact permissions it needs, nothing more
- **No sensitive data in logs** — CloudWatch logs contain only anomaly IDs and service names, never cost details or keys

### Observability
- **CloudWatch logging** — every execution is fully logged with timestamps and execution status
- **TTL on DynamoDB records** — alert history auto-expires after 90 days, keeping the table clean and cost-free
- **CloudWatch alarm** — fires if SNS publish fails consecutively, so you know if alerts stop working

---