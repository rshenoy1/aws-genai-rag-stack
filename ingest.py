
import os
import json
import boto3

ENV_MODE = os.getenv("ENV_MODE", "LOCAL")

def lambda_handler(event=None, context=None):
    print(f"[BOOT] Initializing Ingestion Engine in [{ENV_MODE}] mode...")
    
    if ENV_MODE == "PRODUCTION":
        # Live AWS Infrastructure Configuration
        s3 = boto3.client("s3")
        bedrock = boto3.client("bedrock-runtime")
        
        # Pull bucket data dynamically from the S3 upload event trigger
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"]
        
        print(f"[S3 TRIGGER] Fetching object s3://{bucket_name}/{file_key}")
        s3_object = s3.get_object(Bucket=bucket_name, Key=file_key)
        text_content = s3_object["Body"].read().decode("utf-8")
        
        # Real Amazon Bedrock Titan Embeddings API Call
        chunks = [c.strip() for c in text_content.split(". ") if c.strip()]
        for chunk in chunks:
            body = json.dumps({"inputText": chunk})
            response = bedrock.invoke_model(
                body=body, 
                modelId="amazon.titan-embed-text-v1", 
                accept="application/json", 
                contentType="application/json"
            )
            response_body = json.loads(response.get("body").read())
            embedding = response_body.get("embedding")
            print(f"[BEDROCK EMBED] Successfully generated vector array of size {len(embedding)}")
            # (Production Action: Insert embedding vector variable into real OpenSearch Index here)
            
    else:
        # Offline Local Simulation Configuration
        source_file = "./data_lake/company_policy.txt"
        db_file = "./vector_db/index.json"
        
        with open(source_file, "r") as f:
            text_content = f.read()

        chunks = [c.strip() for c in text_content.split(". ") if c.strip()]
        with open(db_file, "w") as f:
            json.dump({"chunks": chunks}, f, indent=4)
            
        print(f"[SUCCESS Local] OpenSearch Index updated with {len(chunks)} chunks.")

if __name__ == "__main__":
    lambda_handler()

