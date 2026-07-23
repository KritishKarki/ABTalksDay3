 # Creating a knowledge base by reading all the .txt files from raw_text/

# Importing necessary libraries
from datetime import datetime, timezone
import json
import os
import sqlite3
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd

#Initializing text splitter with a chunk size of 500 and an overlap of 50
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=50, 
    length_function=len
    )

knowledge_base = []

# Timestamping the ingestion process
def get_iso_timestamp():
    return datetime.now().isoformat()


# Process Unstructured Text Files from raw_text/
unstructured_files = [
    {
        "file": "raw_text/benefits.txt",
        "section": "benefits",
        "plan_type": "all",
    },
    {
        "file": "raw_text/claims_process.txt",
        "section": "claims",
        "plan_type": "all",
    },
    {
        "file": "raw_text/enrollment.txt",
        "section": "enrollment",
        "plan_type": "all",
    },
]

for item in unstructured_files:
    path = item["file"]
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = text_splitter.split_text(text)

        for chunk in chunks:
            knowledge_base.append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "metadata": {
                    "source_file": path,
                    "source_type": "unstructured",
                    "plan_type": item["plan_type"],
                    "section": item["section"],
                    "ingested_at": get_iso_timestamp(),
                },
            })

# Process Structured Database Rows from coverage.db
db_path = "coverage.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)

    # Process Plans Table
    plans_df = pd.read_sql_query("SELECT * FROM plans", conn)
    for _, row in plans_df.iterrows():
        plan_text = (
            f"Plan ID: {row.get('plan_id', 'N/A')} | Plan Name:"
            f" {row.get('plan_name', 'N/A')} | Tier:"
            f" {row.get('tier', 'N/A')} | Deductible:"
            f" ${row.get('deductible', 'N/A')} | Out of Pocket Max:"
            f" ${row.get('out_of_pocket_max', 'N/A')}"
        )
        knowledge_base.append({
            "id": str(uuid.uuid4()),
            "text": plan_text,
            "metadata": {
                "source_file": "coverage.db:plans",
                "source_type": "structured",
                "plan_type": str(row.get("plan_name", "general")).lower(),
                "section": "benefits",
                "ingested_at": get_iso_timestamp(),
            },
        })

    # Process Claims Table
    claims_df = pd.read_sql_query("SELECT * FROM claims", conn)
    for _, row in claims_df.iterrows():
        claim_text = (
            f"Claim ID: {row.get('claim_id', 'N/A')} | Plan ID:"
            f" {row.get('plan_id', 'N/A')} | Service:"
            f" {row.get('service_description', 'N/A')} | Amount:"
            f" ${row.get('amount', 'N/A')} | Status:"
            f" {row.get('status', 'N/A')}"
        )
        knowledge_base.append({
            "id": str(uuid.uuid4()),
            "text": claim_text,
            "metadata": {
                "source_file": "coverage.db:claims",
                "source_type": "structured",
                "plan_type": "all",
                "section": "claims",
                "ingested_at": get_iso_timestamp(),
            },
        })

    conn.close()

 # Export to root knowledge_base.jsonl
output_path = "knowledge_base.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for entry in knowledge_base:
        f.write(json.dumps(entry) + "\n")

print(
    f"Successfully generated {output_path} with {len(knowledge_base)} chunks!"
)