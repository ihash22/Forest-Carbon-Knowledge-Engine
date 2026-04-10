import fitz  # PyMuPDF
import json
import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Ensure output directory exists
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def parse_and_chunk_pdf(pdf_path):
    print(f"📄 Processing: {pdf_path.name}")
    
    # 1. Open the PDF
    doc = fitz.open(pdf_path)
    
    # 2. Configure the Text Splitter
    # We use 1000 characters per chunk, with a 200 character overlap 
    # to ensure context isn't lost if a sentence crosses a chunk boundary.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    all_chunks = []
    
    # 3. Extract text page-by-page to preserve metadata
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        
        # Skip empty pages
        if not text.strip():
            continue
            
        # Split the page text into chunks
        chunks = text_splitter.split_text(text)
        
        # Tag each chunk with crucial metadata
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "source": pdf_path.name,
                    "page": page_num + 1 # +1 because enumerate starts at 0
                }
            })
            
    return all_chunks

def main():
    # Find all PDFs in the raw directory
    pdf_files = list(RAW_DATA_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDFs found in data/raw/")
        return

    all_registry_data = []

    # Process each PDF
    for pdf_path in pdf_files:
        document_chunks = parse_and_chunk_pdf(pdf_path)
        all_registry_data.extend(document_chunks)
        
    # Save the master chunked dataset as a JSON file
    output_file = PROCESSED_DATA_DIR / "registry_knowledge_base.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_registry_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Success! {len(all_registry_data)} total chunks saved to {output_file}")

if __name__ == "__main__":
    main()