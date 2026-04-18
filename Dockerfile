# 1. Use a lightweight, official Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (to leverage Docker layer caching)
COPY requirements.txt .

# 4. Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the source code and the vector database into the container
# Note: We do NOT copy the raw PDFs to keep the image small
COPY src/ /app/src/
COPY data/chroma_db/ /app/data/chroma_db/

# 6. Expose the port FastAPI runs on
EXPOSE 8000

# 7. Define the command to boot the API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
