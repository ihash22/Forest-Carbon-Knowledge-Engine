# 🌲 Forest Carbon Knowledge Engine

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Terraform](https://img.shields.io/badge/Terraform-AWS_Fargate-7B42BC)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Passing-brightgreen)

An AI-powered application designed to retrieve and synthesize complex information from forest carbon registry documents (e.g., Verra, ACR, CAR). This production-grade Retrieval-Augmented Generation (RAG) system allows users to ask natural language questions and receive concise, grounded answers with explicit source citations.

Beyond the core AI, this repository demonstrates **enterprise MLOps and Cloud-Native best practices**, featuring automated prompt tracing, statistical output evaluation, containerization, and Infrastructure as Code (IaC).

## 🚀 Features
* **Semantic Search:** Quickly find exact methodology rules across tens of thousands of pages.
* **Source-Grounded AI:** Powered by GPT-4o-mini and constrained strictly to registry context to prevent hallucinations.
* **REST API:** Built with FastAPI for interactive querying via Swagger UI.
* **MLOps Observability:** MLflow for prompt tracing and Evidently AI for statistical NLP evaluation.
* **Cloud-Native Architecture:** Containerized via Docker and deployable as a microservice.
* **Infrastructure as Code (IaC):** Serverless AWS Fargate deployment blueprint codified with Terraform.
* **Continuous Integration:** GitHub Actions automatically tests Docker builds and IaC formatting on every push.

## 🛠️ Tech Stack
* **AI & Data:** LangChain, OpenAI API, ChromaDB (Vector Store), PyMuPDF
* **Backend API:** FastAPI, Uvicorn, Pydantic
* **MLOps:** MLflow (Tracing), Evidently AI (Text Evaluation)
* **DevOps & Cloud:** Docker, Docker Compose, Terraform, AWS (ECS/Fargate), GitHub Actions

## 📁 Project Structure

```text
├── .github/workflows/
│   └── ci-cd.yml           # GitHub Actions CI/CD pipeline
├── data/
│   ├── raw/                # Source PDFs (Verra, ACR, CAR)
│   └── chroma_db/          # Local vector database
├── docs/reports/           # Evidently AI evaluation dashboards
├── src/
│   ├── api.py              # FastAPI application entry point
│   ├── build_vector_db.py  # Document ingestion & embedding script
│   ├── rag_engine.py       # LangChain pipeline w/ optional MLflow tracing
│   └── evaluate_rag.py     # Evidently AI test suite
├── terraform/
│   └── main.tf             # AWS infrastructure blueprint
├── .dockerignore           # Container build exclusions
├── .env                    # Environment variables (Git-ignored)
├── docker-compose.yml      # Local container orchestration
├── Dockerfile              # API container definition
├── requirements.txt        # Production API dependencies
└── README.md
```

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Docker Desktop
- Terraform CLI & AWS CLI (for infrastructure deployment)
- OpenAI API Key

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/forest-carbon-knowledge-engine.git](https://github.com/yourusername/forest-carbon-knowledge-engine.git)
cd forest-carbon-knowledge-engine
```

### 2. Set up environment variables
Create a `.env` file in the root directory:
```bash
touch .env
```
Add your OpenAI key to the `.env` file:
```env
OPENAI_API_KEY="sk-your-openai-api-key"
```

### 3. Run the API (Choose one method)

**Method A: Production Mode (Docker)** Run the fully isolated, cloud-ready container. *Note: MLflow tracing is gracefully disabled in Docker to keep the container lightweight.*
```bash
docker-compose up --build
```

**Method B: Development Mode (Local/Conda)** Run locally with full MLflow tracking and evaluation tools.
```bash
# Create and activate environment
conda create -n carbon_llm_prod python=3.10
conda activate carbon_llm_prod

# Install all dependencies (including dev tools)
pip install -r requirements.txt
pip install mlflow evidently jupyter

# Launch the FastAPI server
uvicorn src.api:app --reload
```

Once running, access the interactive API interface at: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 📊 Evaluation & MLOps

This engine includes an automated suite to monitor the health and behavior of the LLM outputs.

To run the evaluation pipeline:
```bash
python -m src.evaluate_rag
```
This queries the RAG engine against a golden dataset, extracts the results, and compiles an interactive HTML dashboard using **Evidently AI** (saved to `docs/reports/rag_evaluation_report.html`). It tracks response length, generation failures, and acts as a proxy for answer toxicity/sentiment.

## ☁️ Infrastructure as Code (IaC)

The application infrastructure is codified using Terraform, targeting AWS Fargate for serverless container hosting. 

To preview the cloud infrastructure blueprint:
```bash
cd terraform
terraform init
terraform plan
```
This provisions a dedicated VPC, Public Subnet, ECS Cluster, Fargate Task Definitions, and Security Groups required to host the Dockerized API securely.

## 🔮 Future Work
- **LLM-as-a-Judge:** Upgrading the Evidently AI evaluation suite to grade answers explicitly on *Faithfulness* and *Relevance* to programmatically prevent hallucinations.
- **Dynamic Document Ingestion:** Adding a POST endpoint to upload, chunk, and vectorize new registry PDFs directly through the API.