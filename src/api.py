from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import the RAG chain setup from your existing script
from src.rag_engine import setup_rag_chain

# 1. Initialize the FastAPI app
app = FastAPI(
    title="Forest Carbon Knowledge API",
    description="A RAG-powered API for querying official ACR/Verra registry documents.",
    version="1.0.0"
)

# Global variable to hold our RAG chain in memory
rag_chain = None

# 2. Define the Data Schemas using Pydantic
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

# 3. Load the RAG engine when the server starts
@app.on_event("startup")
async def startup_event():
    global rag_chain
    print("🌲 Booting up the Forest Carbon RAG Engine...")
    rag_chain = setup_rag_chain()
    print("✅ Engine connected and ready for requests!")

# 4. Define the POST endpoint
@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    if not rag_chain:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized.")
    
    try:
        # Pass the user's question to the LLM chain
        answer = rag_chain.invoke(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)