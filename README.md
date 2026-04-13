# 🌲 Forest Carbon Knowledge Engine

A specialized MLOps pipeline and Vertical RAG (Retrieval-Augmented Generation) system designed to provide high-fidelity, cited answers regarding Forest Carbon Projects using official registry documentation (ACR/Verra).

## 🚀 Overview
General-purpose LLMs often struggle with hyper-specific technicalities, methodology versions, and vintage-year credit counts found in Forest Carbon registries. This project implements a **Vertical RAG** architecture that anchors LLM responses to "Ground Truth" PDF documents, ensuring every answer is accurate and includes a verifiable source citation.

### Key Features
- **Advanced Document ETL**: Automated parsing and chunking of massive PDF Project Design Documents (PDDs) using `PyMuPDF`.
- **Semantic Search**: Vectorized knowledge base using OpenAI `text-embedding-3-small` and `ChromaDB`.
- **Strict Citation Logic**: Engineered system prompts that force the LLM to cite document names and page numbers, reducing hallucination risk.
- **Production-Ready API**: A FastAPI service designed for containerized deployment and integration with carbon accounting platforms.

---

## 🏗️ System Architecture
1. **Data Ingestion**: Raw ACR/Verra PDFs are placed in the ingestion layer.
2. **Processing**: Documents are parsed and split using `RecursiveCharacterTextSplitter` to preserve semantic context across chunk boundaries.
3. **Vectorization**: Chunks are transformed into 1536-dimensional vectors and stored in a local `ChromaDB` instance.
4. **Retrieval**: User queries trigger a semantic similarity search to fetch the top 5 most relevant context blocks.
5. **Generation**: GPT-4o-mini synthesizes the final answer based *only* on the retrieved context snippets.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10
- **GenAI Framework:** LangChain (LCEL)
- **Vector Database:** ChromaDB
- **LLM/Embeddings:** OpenAI (GPT-4o-mini / text-embedding-3-small)
- **API Framework:** FastAPI + Uvicorn
- **Environment Management:** Conda

---

## 📂 Project Structure
```text
Forest-Carbon-Knowledge-Engine/
├── data/
│   ├── raw/            # Original Registry PDFs (Gitignored)
│   ├── processed/      # Chunked JSON knowledge base
│   └── chroma_db/      # Persisted Vector Database
├── src/
│   ├── parse_registry_docs.py   # PDF ETL Pipeline
│   ├── build_vector_db.py       # Embedding & Indexing logic
│   ├── rag_engine.py            # LangChain Retrieval & Prompt logic
│   └── api.py                   # FastAPI implementation
├── environment.yml              # Conda environment definition
└── .env                         # API Keys (Gitignored)
```

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
git clone [https://github.com/YOUR_USERNAME/Forest-Carbon-Knowledge-Engine.git](https://github.com/YOUR_USERNAME/Forest-Carbon-Knowledge-Engine.git)
cd Forest-Carbon-Knowledge-Engine
conda env create -f environment.yml
conda activate carbon_llm_prod
```

### 2. Configure Secrets
Create a `.env` file in the root directory:
```text
OPENAI_API_KEY=your_api_key_here
```

### 3. Initialize Knowledge Base
Drop your ACR/Verra PDFs into `data/raw/`, then run the pipeline:
```bash
python src/parse_registry_docs.py
python src/build_vector_db.py
```

### 4. Launch the API
```bash
uvicorn src.api:app --reload
```
Access the interactive documentation at `http://localhost:8000/docs`.

---

## 📝 Example Query
**Input:** *"What is the baseline scenario for the Sharp Bingham project?"*

**Output:**
> "The baseline for the Sharp Bingham project includes stricter management regimes than state practices, maximizing Net Present Value (NPV) at a 4% discount rate. It also explicitly prohibits harvesting within specific riparian buffer zones to ensure carbon stock maintenance. **[Source: SharpBingham_GHG_Plan.pdf, Page 21]**"

---

## 🗺️ Roadmap & MLOps Maturity
This project follows an iterative MLOps lifecycle. 
- [x] **Phase 1: Knowledge Engine:** Basic RAG, PDF ETL, and FastAPI integration.
- [ ] **Phase 2: LLMOps:** Integrate **MLflow** for prompt tracing and **Evidently AI** for faithfulness/hallucination metrics.
- [ ] **Phase 3: Cloud Native:** Containerize with Docker and deploy to AWS using Terraform (IaC).
- [ ] **Phase 4: Full Orchestration:** Implement **Apache Airflow** to automatically monitor registries for new filings and trigger re-indexing.