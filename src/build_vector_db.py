import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# 1. Load environment variables (your API key)
load_dotenv()

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"

def main():
    # Verify API key exists
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file.")
        return

    # 2. Load the chunked JSON data
    json_path = PROCESSED_DATA_DIR / "registry_knowledge_base.json"
    if not json_path.exists():
        print(f"❌ ERROR: Could not find {json_path}")
        return

    print(f"📂 Loading text chunks from {json_path.name}...")
    with open(json_path, "r", encoding="utf-8") as f:
        raw_chunks = json.load(f)

    # 3. Convert JSON dictionaries into LangChain Document objects
    documents = []
    for chunk in raw_chunks:
        doc = Document(
            page_content=chunk["text"],
            metadata=chunk["metadata"]
        )
        documents.append(doc)

    print(f"✅ Successfully loaded {len(documents)} documents.")

    # 4. Initialize the Embedding Model
    print("🧠 Initializing OpenAI Embeddings (text-embedding-3-small)...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 5. Build and persist the Vector Database
    print(f"💾 Building ChromaDB at {CHROMA_DB_DIR}... (This may take a minute)")
    
    # This command automatically embeds the text and saves the database to your hard drive
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR),
        collection_name="forest_carbon_registry"
    )

    print("✅ Vector Database successfully built and saved to disk!")

    # 6. Quick Sanity Check!
    test_query = "What is the baseline scenario for the project?"
    print(f"\n🔍 Running test similarity search: '{test_query}'")
    
    # Search the database for the top 2 most relevant chunks
    results = vectorstore.similarity_search(test_query, k=2)
    
    for i, res in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {res.metadata.get('source')} | Page: {res.metadata.get('page')}")
        print(f"Snippet: {res.page_content[:250]}...")

if __name__ == "__main__":
    main()