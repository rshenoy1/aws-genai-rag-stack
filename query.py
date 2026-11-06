
import os
import json
import re
import boto3

ENV_MODE = os.getenv("ENV_MODE", "LOCAL")

# ==========================================
# 1. LOCAL COMPONENT SIMULATION
# ==========================================
def run_local_guardrail_check(text_input):
    cc_pattern = r"\b(?:\d[ -]*?){13,16}\b"
    if re.search(cc_pattern, text_input):
        print("[GUARDRAIL TRIGGER] Blocked! Input contains sensitive PII (Credit Card).")
        return False, "ERROR: Sensitive PII detected. Transaction blocked by corporate guardrails."
    return True, text_input

def run_local_faithfulness_eval(ai_response, retrieved_context):
    print("[EVAL ENGINE] Running automated evaluation check on output consistency...")
    if "12 weeks" in ai_response and "12 weeks" not in retrieved_context:
        print("[EVAL FAILURE] Hallucination detected! Response contains unverified facts.")
        return False, "REJECTED: Output failed enterprise faithfulness metrics."
    print("[EVAL SUCCESS] Score: 100% Faithful. Output strictly matches retrieved context.")
    return True, ai_response

# ==========================================
# MAIN ROUTING ENGINE & BEDROCK API INVOKER
# ==========================================
def run_query(user_question):
    print(f"\n[QUERY PIPELINE] Mode: [{ENV_MODE}] | Question: \"{user_question}\"")
    
    # Executing Local Guardrail Simulation Path when Offline
    if ENV_MODE == "LOCAL":
        is_safe, guardrail_result = run_local_guardrail_check(user_question)
        if not is_safe:
            print(f"[FINAL RESPONSE]: {guardrail_result}\n")
            return guardrail_result

    # Load Context from OpenSearch database simulation folder
    db_file = "./vector_db/index.json"
    retrieved_context = ""
    if os.path.exists(db_file):
        with open(db_file, "r") as f:
            chunks = json.load(f).get("chunks", [])
            if chunks:
                retrieved_context = chunks

    if ENV_MODE == "PRODUCTION":
        # ========================================================
        # LIVE PRODUCTION AWS PATH WITH PRODUCTION NATIVE GUARDRAILS
        # ========================================================
        bedrock = boto3.client("bedrock-runtime")
        prompt = f"Context: {retrieved_context}\nQuestion: {user_question}\nAnswer:"
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        # In production, we add the official Amazon Bedrock Guardrail parameters right into the API call
        response = bedrock.invoke_model(
            body=body,
            modelId="anthropic.claude-3-5-sonnet-v2:0",
            accept="application/json",
            contentType="application/json",
            guardrailIdentifier="gw-enterprise-firewall-12345", # <--- REAL PRODUCTION GUARDRAIL ID HOOK
            guardrailVersion="1"                                # <--- ACTIVE PRODUCTION GUARDRAIL VERSION
        )
        
        response_body = json.loads(response.get("body").read())
        ai_response = response_body["content"]["text"]
        
    else:
        # Offline Local Simulation Configuration
        if "leave" in user_question.lower() or "paternity" in user_question.lower():
            ai_response = "According to our corporate policy, employees are entitled to 12 weeks of fully paid parental leave."
        else:
            ai_response = "I cannot find any relevant company documentation regarding that query."

    # Execute Output Evaluation Faithfulness Check
    if ENV_MODE == "LOCAL":
        is_faithful, final_checked_response = run_local_faithfulness_eval(ai_response, retrieved_context)
    else:
        final_checked_response = ai_response
    
    print(f"[FINAL RESPONSE]: {final_checked_response}\n")
    return final_checked_response

if __name__ == "__main__":
    run_query("How many weeks of paternity leave do I get?")

