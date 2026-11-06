
import os
import json
import boto3
import time
from query import run_query

ENV_MODE = os.getenv("ENV_MODE", "LOCAL")

def process_queue_traffic():
    if ENV_MODE == "PRODUCTION":
        # Live AWS Infrastructure Configuration
        sqs = boto3.client("sqs")
        queue_url = "https://amazonaws.com"
        
        print(f"[AWS SQS] Polling messages from production queue: {queue_url}")
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )
        
        messages = response.get("Messages", [])
        print(f"[AWS SQS] Pulled {len(messages)} items out of queue.")
        for msg in messages:
            body_data = json.loads(msg["Body"])
            user_question = body_data.get("question")
            
            # Route processing downstream
            run_query(user_question)
            
            # Delete message from SQS to acknowledge complete processing loop
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
            
    else:
        # Offline Local Simulation Configuration
        mock_sqs_queue = ["How many weeks of paternity leave do I get?"]
        print(f"[LOCAL SQS MOCK] Processing buffered message queue array safely...")
        for msg in mock_sqs_queue:
            run_query(msg)
            time.sleep(0.5)

if __name__ == "__main__":
    process_queue_traffic()

