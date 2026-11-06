import json
import boto3
import os

ENV_MODE = os.getenv("ENV_MODE", "LOCAL")

def trigger_production_squad_execution(macro_objective):
    print(f"[ENTRY POINT] Initializing request tracking pipeline in [{ENV_MODE}] mode...")
    
    payload = {
        "objective": macro_objective,
        "request_metadata": {
            "origin": "corporate_portal",
            "security_tier": "tier_1"
        }
    }
    
    if ENV_MODE == "PRODUCTION":
        sfn_client = boto3.client("stepfunctions", region_name="us-east-1")
        state_machine_arn = "arn:aws:states:us-east-1:123456789012:stateMachine:enterprise-multi-agent-squad-orchestrator"
        
        print(f"[AWS API] Triggering live execution state machine loop: {state_machine_arn}")
        
        response = sfn_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(payload)
        )
        
        print(f"[SUCCESS Live] Execution started! Execution ARN: {response['executionArn']}")
        return response['executionArn']
    else:
        print("[LOCAL MOCK] Simulating Step Function trigger payload handoff...")
        print(f" -> Forwarded payload parameter mapping string to mock state context engine: {json.dumps(payload)}")
        print("[SUCCESS Local] State machine entry parameters validated.")
        return "mock-execution-arn-12345"

if __name__ == "__main__":
    trigger_production_squad_execution("Research copper price spikes and compute a 15% overhead increase.")
