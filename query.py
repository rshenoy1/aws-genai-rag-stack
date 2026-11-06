
import os
import json
import boto3

ENV_MODE = os.getenv("ENV_MODE", "LOCAL")

def run_query(user_question):
    print(f"\n[QUERY PIPELINE] Mode: [{ENV_MODE}] | Question: \"{user_question}\"")
    
    if ENV_MODE == "PRODUCTION":
        # Live AWS Infrastructure Configuration
        bedrock = boto3.client("bedrock-runtime")
        
        # (Production Action: Extract context metadata from OpenSearch Serverless Cluster API)
        retrieved_context = "Employees are entitled to 12 weeks of fully paid parental leave." 
        
        # Construct isolated prompt template payload for Amazon Bedrock
        prompt = f"Context: {retrieved_context}\nQuestion: {user_question}\nAnswer:"
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        # Live Amazon Bedrock Inference Calling Anthropic Claude
        response = bedrock.invoke_model(
            body=body,
            modelId="anthropic.claude-3-5-sonnet-v2:0",
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get("body").read())
        ai_response = response_body["content"][0]["text"]
        print(f"[PRODUCTION AWS ANSWER]: {ai_response}\n")
        return ai_response
        
    else:
        # Offline Local Simulation Configuration
        db_file = "./vector_db/index.json"
        with open(db_file, "r") as f:
            chunks = json.load(f).get("chunks", [])
            
        matched_context = chunks[0] if chunks else ""
        if "12 weeks" in matched_context:
            ai_response = "According to our corporate policy, employees are entitled to 12 weeks of fully paid parental leave."
        print(f"[LOCAL MOCK ANSWER]: {ai_response}\n")
        return ai_response

if __name__ == "__main__":
    run_query("How many weeks of paternity leave do I get?")

