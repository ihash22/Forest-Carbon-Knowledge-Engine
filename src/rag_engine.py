import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"

def setup_rag_chain():
    # 1. Re-initialize the Vector Database connection
    print("🔌 Connecting to ChromaDB...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_DIR), 
        embedding_function=embeddings,
        collection_name="forest_carbon_registry"
    )
    
    # 2. Create the Retriever 
    # (Fetch the top 5 most relevant chunks for any question)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # 3. Initialize the LLM (GPT-4o-mini is fast, cheap, and highly capable)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 4. Engineer the Strict System Prompt
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

    # 5. Helper function to format the retrieved documents into a single string
    def format_docs(docs):
        formatted = []
        for d in docs:
            source = d.metadata.get("source", "Unknown")
            page = d.metadata.get("page", "Unknown")
            formatted.append(f"[Source: {source}, Page {page}]\n{d.page_content}")
        return "\n\n".join(formatted)

    # 6. Build the actual LCEL (LangChain Expression Language) Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def main():
    print("🌲 Initializing Forest Carbon Knowledge Engine...")
    chain = setup_rag_chain()
    
    print("\n✅ System Ready. Type 'quit' to exit.")
    print("-" * 50)
    
    while True:
        question = input("\n🤔 Ask a question about the carbon projects: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        print("\n⏳ Searching registries and generating answer...\n")
        
        # Invoke the chain with the user's question
        response = chain.invoke(question)
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()