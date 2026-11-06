
# Hybrid AWS Solutions Architect + Generative AI Enterprise RAG Stack

A production-ready, flag-driven **Retrieval-Augmented Generation (RAG)** cloud architecture engineered to securely process enterprise documentation and serve low-latency, context-grounded AI responses. 

This repository features a **dual-mode runtime strategy** allowing developers to simulate the entire serverless infrastructure completely offline using local mocks, or deploy it directly to live AWS clouds via **Terraform IaC** with zero modifications to the core logic.

---

## ?? Key Architectural Highlights

*   **Dual-Mode Engine (`ENV_MODE`):** Uses an environment flag to seamlessly toggle between a localized decoupled architecture and real AWS client configurations (`boto3`).
*   **Load-Leveled Traffic Buffer:** Implements a synchronous/asynchronous decoupling pattern via message queuing (**Amazon SQS**) to protect downstream AI model throttling limits (**Amazon Bedrock TPS Quotas**).
*   **Infrastructure as Code:** Complete **Terraform (`main.tf`)** manifest managing least-privilege IAM execution roles, secure S3 data lakes, and FIFO message buffers.
*   **Isolated Data Perimeter:** Designed around the **AWS Well-Architected Security Pillar** ensuring enterprise corporate documentation is encrypted and never used for model training.

---

## ??? System Blueprint

```text
[ INFRASTRUCTURE MODES ]
 +-- [ENV_MODE=LOCAL]      --? Reads Local Disk JSON + Safe Concept-Matched Emulation
 +-- [ENV_MODE=PRODUCTION] --? Connects to Live S3 + Amazon Bedrock + OpenSearch Cluster

[ REAL-TIME USER QUERY PIPELINE ]
 [User Client] --? [API Gateway] --? [Amazon SQS Queue] --? [Controlled Dequeue]
                                                                    ¦
                                                             [AWS Lambda Engine]
                                                              +-----------+
                                                   (Context)  ?           ?  (Inference)
                                                   [OpenSearch DB]     [Amazon Bedrock]
```

---

## ??? Step-by-Step Local Execution Runbook

### 1. Ingest Data Lake Documents
Processes and segments raw documentation into strategic text data blocks:
```powershell
python ingest.py
```

### 2. Execute Real-Time Prompt Query Engine
Runs the core orchestration handler to query the database and synthesize a secure answer:
```powershell
python query.py
```

### 3. Simulate High-Concurrency Queue Buffering
Simulates a sudden traffic spike of concurrent requests to demonstrate how the SQS buffer executes load-leveling natively:
```powershell
python queue_system.py
```

---

## ?? Production Terraform Deployment (Live Cloud)

To provision this entire cloud matrix securely on a live enterprise AWS account, execute the following IaC runbook:

```bash
# Initialize provider configurations and plugins
terraform init

# Review upcoming infrastructure modifications
terraform plan

# Deploy infrastructure to the live AWS cloud env
terraform apply -auto-approve
```

---

## ?? Technology Manifest
*   **Compute Orchestration:** AWS Lambda / Python 3.12 Core
*   **Generative AI Models:** Amazon Bedrock (Anthropic Claude 3.5 Sonnet & Titan Embeddings)
*   **Traffic Backpressure Buffer:** Amazon SQS (First-In, First-Out Queueing)
*   **Storage Layer:** Amazon S3 Data Lake
*   **Database Store:** Amazon OpenSearch Serverless (Vector Engine)
*   **Infrastructure Automation:** Terraform v1.5+

