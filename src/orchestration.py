import os
import requests
import subprocess
from prefect import task, flow, get_run_logger

# --- TASK 1: Check and Download ---
@task(retries=2, retry_delay_seconds=10)
def fetch_new_registry_pdfs():
    logger = get_run_logger()
    logger.info("🔍 Checking ACR/Verra public endpoints for new methodology updates...")
    
    # We use a sample PDF here to simulate the download process for the portfolio
    sample_pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    output_dir = "data/raw"
    output_path = os.path.join(output_dir, "new_mock_methodology.pdf")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Simulate logic: If we don't already have this file, download it.
    if not os.path.exists(output_path):
        logger.info(f"📥 New methodology found! Downloading to {output_path}...")
        response = requests.get(sample_pdf_url)
        with open(output_path, "wb") as f:
            f.write(response.content)
        logger.info("✅ Download complete.")
        return True
    else:
        logger.info("💤 No new PDFs found. System is up to date.")
        return False

# --- TASK 2: Vectorize ---
@task
def update_vector_db(new_docs_downloaded: bool):
    logger = get_run_logger()
    
    if not new_docs_downloaded:
        logger.info("⏭️ Skipping database rebuild.")
        return
    
    logger.info("⚙️ Triggering vector database rebuild...")
    
    try:
        # This calls your existing script from Phase 1 to process the new PDFs
        # Assuming you have a build_vector_db.py in your src/ folder
        subprocess.run(["python", "src/build_vector_db.py"], check=True)
        logger.info("✅ Vector database successfully updated with new embeddings!")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to rebuild vector database: {e}")
        raise e

# --- THE DAG (Flow) ---
@flow(name="Weekly Carbon Registry Sync")
def registry_sync_pipeline():
    """
    This is the main Directed Acyclic Graph (DAG).
    It defines the exact order of operations.
    """
    logger = get_run_logger()
    logger.info("🚀 Starting the automated Forest Carbon update pipeline...")
    
    # 1. Fetch data
    has_new_data = fetch_new_registry_pdfs()
    
    # 2. Update DB (only if new data exists)
    update_vector_db(has_new_data)
    
    logger.info("🏁 Pipeline execution finished.")

if __name__ == "__main__":
    # This block turns the script into a long-running scheduler.
    # The cron string "0 0 * * 0" means: Run at minute 0, hour 0, every Sunday.
    registry_sync_pipeline.serve(
        name="weekly-production-sync",
        cron="0 0 * * 0",
        tags=["data-engineering", "production"]
    )