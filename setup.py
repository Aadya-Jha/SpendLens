import boto3
import json
import zipfile
import os
import time

def get_account_id(session):
    sts = session.client('sts')
    return sts.get_caller_identity()['Account']

def setup_spendlens():
    print("\n🔍 SpendLens Setup\n")
    print("This will deploy SpendLens to your AWS account in a few minutes.")
    print("You need AWS credentials configured (run 'aws configure' first)\n")

    # get user inputs
    email = input("Enter your email for alerts: ").strip()
    region = input("Enter AWS region (default us-east-1): ").strip() or "us-east-1"
    groq_key = input("Enter your Groq API key: ").strip()

    print("\n Setting up AWS resources...\n")

    session = boto3.Session(region_name=region)
    account_id = get_account_id(session)

    # 1. create dynamodb table
    print("Creating DynamoDB table...")
    dynamodb = session.client('dynamodb')
    try:
        dynamodb.create_table(
            TableName='spendlens-alerts',
            KeySchema=[{'AttributeName': 'anomaly_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'anomaly_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        time.sleep(3)
        print("  DynamoDB table created")
    except dynamodb.exceptions.ResourceInUseException:
        print("  DynamoDB table already exists, skipping")

    # 2. create SNS topic
    print("Creating SNS topic...")
    sns = session.client('sns')
    topic = sns.create_topic(Name='spendlens-alerts-topic')
    topic_arn = topic['TopicArn']
    sns.subscribe(TopicArn=topic_arn, Protocol='email', Endpoint=email)
    print(f"  SNS topic created — check {email} for confirmation email")

    # 3. create IAM role for Lambda
    print("Creating IAM role...")
    iam = session.client('iam')
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    try:
        role = iam.create_role(
            RoleName='spendlens-lambda-role',
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role['Role']['Arn']

        # attach policies
        policies = [
            'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
            'arn:aws:iam::aws:policy/CloudWatchLogsFullAccess',
        ]
        for p in policies:
            iam.attach_role_policy(RoleName='spendlens-lambda-role', PolicyArn=p)

        # inline policy for Cost Explorer and SNS
        iam.put_role_policy(
            RoleName='spendlens-lambda-role',
            PolicyName='spendlens-inline',
            PolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["ce:GetAnomalies", "sns:Publish"],
                    "Resource": "*"
                }]
            })
        )
        print("  IAM role created")
        time.sleep(10)  # wait for role to propagate
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = f"arn:aws:iam::{account_id}:role/spendlens-lambda-role"
        print("  IAM role already exists, skipping")

    # 4. create lambda zip
    print("Packaging Lambda function...")
    with zipfile.ZipFile('spendlens_lambda.zip', 'w') as z:
        for f in os.listdir('lambdas'):
            if f.endswith('.py'):
                z.write(f'lambdas/{f}', f)
    print("  Lambda packaged")

    # 5. create Lambda function
    print("Creating Lambda function...")
    lambda_client = session.client('lambda')
    with open('spendlens_lambda.zip', 'rb') as f:
        zip_bytes = f.read()

    try:
        lambda_client.create_function(
            FunctionName='spendlens-daily',
            Runtime='python3.12',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_bytes},
            Timeout=30,
            MemorySize=128,
            Environment={
                'Variables': {
                    'GROQ_API_KEY': groq_key,
                    'SNS_TOPIC_ARN': topic_arn
                }
            }
        )
        print("  Lambda function created")
    except lambda_client.exceptions.ResourceConflictException:
        print("  Lambda already exists, skipping")

    # 6. create EventBridge schedule
    print("Creating EventBridge schedule...")
    events = session.client('events')
    events.put_rule(
        Name='spendlens-daily-trigger',
        ScheduleExpression='cron(0 8 * * ? *)',
        State='ENABLED'
    )
    lambda_arn = f"arn:aws:lambda:{region}:{account_id}:function:spendlens-daily"
    events.put_targets(
        Rule='spendlens-daily-trigger',
        Targets=[{'Id': 'spendlens', 'Arn': lambda_arn}]
    )
    print("  EventBridge schedule created")

    print("\n✅ SpendLens deployed successfully!")
    print(f"\n  Check {email} and confirm the SNS subscription")
    print(f"  SpendLens will run daily at 8AM UTC")
    print(f"  View logs: CloudWatch → /aws/lambda/spendlens-daily")
    print("\n  Setup complete!\n")

if __name__ == "__main__":
    setup_spendlens()