import pandas as pd
import os
from evidently import Dataset, DataDefinition, Report # 🚨 Import Dataset and DataDefinition
from evidently.presets import TextEvals
from evidently.descriptors import TextLength
from src.rag_engine import setup_rag_chain

def main():
    print("🌲 Initializing Evaluation Suite...")
    rag_chain = setup_rag_chain()
    
    # 1. Define a "Golden" Test Set
    test_queries = [
        "What is the baseline scenario for the Sharp Bingham project?",
        "What methodology is used for the IFM projects?",
        "Are there any specific harvesting prohibitions?"
    ]
    
    results = []
    
    # 2. Run the RAG chain on the test set
    print("⏳ Generating answers for evaluation...")
    for query in test_queries:
        print(f"   -> Querying: {query}")
        response = rag_chain.invoke(query)
        results.append({
            "question": query,
            "generated_answer": response
        })
        
    # 3. Convert to a Pandas DataFrame
    df = pd.DataFrame(results)
    
    # 🚨 4. NEW: Create an Evidently Dataset and attach Descriptors
    print("📊 Compiling Evidently AI GenAI Report...")
    
    # We tell Evidently to calculate TextLength specifically on the 'generated_answer' column
    eval_dataset = Dataset.from_pandas(
        df, 
        data_definition=DataDefinition(),
        descriptors=[
            TextLength("generated_answer", alias="Answer Length")
        ]
    )
    
    # 5. Generate the Report using the TextEvals preset
    report = Report(metrics=[
        TextEvals() # It automatically finds and charts the descriptors we attached above!
    ])
    
    eval_snapshot = report.run(reference_data=None, current_data=eval_dataset)
    
    # 6. Save the report
    output_dir = "docs/reports"
    os.makedirs(output_dir, exist_ok=True)
    report_path = f"{output_dir}/rag_evaluation_report.html"
    
    eval_snapshot.save_html(report_path)
    
    print(f"✅ Evaluation complete! Open {report_path} in your browser to view the dashboard.")

if __name__ == "__main__":
    main()