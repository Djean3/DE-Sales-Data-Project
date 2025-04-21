# 🫘 DE-Sales-Data-Project

A fully serverless, event-driven ETL pipeline for processing and analyzing sales data on AWS.

Built to simulate realistic transaction data, transform it automatically, and make it queryable using Amazon Athena — all with zero manual effort. Ideal for scalable, cost-efficient data pipelines in cloud-native environments.

---

## 🔧 Tech Stack

- **AWS Lambda** – Serverless compute for ETL logic  
- **Amazon S3** – Data lake storage for raw and processed files  
- **AWS Glue Catalog** – Schema registration for Athena  
- **Amazon Athena** – Serverless SQL querying  
- **Terraform** – Infrastructure as code  
- **Serverless Framework** – Lambda + EventBridge deployment  
- **Docker + Poetry** – Dependency management and packaging  
- **Power BI** – Optional visualization layer  

---

## 🛠️ Key Features

- Synthetic sales data generation using Faker  
- Automated ETL with Lambda triggered on file drop  
- Date-partitioned Parquet outputs for optimized querying  
- Daily scheduled runs via EventBridge cron job  
- Athena integration via Glue Catalog for instant querying  
- Modular infrastructure managed with Terraform  
- Zero-devops deployment with Serverless Framework  

---

## 📦 Project Structure

```bash
DE-Sales-Data-Project/
├── data_pipeline/
│   ├── generate_data.py           # Faker-based sales data generator
│   ├── process_sales_function.py  # Lambda ETL logic
│   └── run_local.py               # Local test harness
├── infrastructure/
│   ├── main.tf                    # Terraform config (S3, IAM, Glue, Athena)
│   ├── serverless.yml             # Serverless framework config
│   └── variables.tf
├── Dockerfile                     # Lambda container packaging
├── pyproject.toml                 # Poetry dependencies
├── Makefile                       # Build & deploy shortcuts
└── README.md

