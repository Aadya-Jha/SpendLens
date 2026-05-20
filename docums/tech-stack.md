#  Tech Stack & Features

## Tech Stack

### AWS Services

| Service | Role |
|---|---|
| **AWS Lambda** | Core execution engine — runs all business logic serverlessly |
| **Amazon EventBridge** | Daily cron scheduler that triggers the Lambda function |
| **AWS Cost Explorer API** | Detects and fetches cost anomalies from your AWS account |
| **Amazon DynamoDB** | Stores alert history and handles deduplication |
| **Amazon SNS** | Delivers formatted email alerts to subscribers |
| **AWS Secrets Manager** | Securely stores the Claude API key at runtime |
| **AWS IAM** | Least-privilege permissions between every service |
| **Amazon CloudWatch** | Logging, monitoring, and error tracking |

### External

| Tool | Role |
|---|---|
| **Claude API (Anthropic)** | Generates plain-English explanations and fix recommendations |
| **Python 3.12** | Lambda runtime and all business logic |
| **Boto3** | AWS SDK — used to call Cost Explorer, DynamoDB, SNS, Secrets Manager |

---

