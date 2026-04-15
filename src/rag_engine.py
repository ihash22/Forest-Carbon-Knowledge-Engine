import os
from pathlib import Path
from dotenv import load_dotenv
import mlflow # 🚨 NEW IMPORT

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"

def setup_rag_chain():
    # 🚨 NEW: Enable MLflow Tracing for LangChain
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    mlflow.set_experiment("Forest_Carbon_RAG")
    mlflow.langchain.autolog()

    print("🔌 Connecting to ChromaDB...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_DIR), 
        embedding_function=embeddings,
        collection_name="forest_carbon_registry"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    SYSTEM_TEMPLATE = """
    You are an expert Forest Carbon Analyst. You answer questions based ONLY on the provided context from official registry documents.
    
    Context:
    {context}
    
    Rules:
    1. If the answer is not in the context, say "I cannot answer this based on the provided registry documents." Do not guess.
    2. Always cite your sources at the end of your answer using the format: [Source: Document Name, Page X].
    3. Keep your answers concise and professional.
    
    Question: {question}
    """
    
    prompt = ChatPromptTemplate.from_template(SYSTEM_TEMPLATE)

    def format_docs(docs):
        formatted = []
        for d in docs:
            source = d.metadata.get("source", "Unknown")
            page = d.metadata.get("page", "Unknown")
            formatted.append(f"[Source: {source}, Page {page}]\n{d.page_content}")
        return "\n\n".join(formatted)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain