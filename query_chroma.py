import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Connect to local ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="coverage_kb")

# 2. Embed the Step 4 test query
model = SentenceTransformer("all-MiniLM-L6-v2")
query_text = "Is physical therapy covered under the Silver plan?"
query_embedding = model.encode(query_text).tolist()

# 3. Query ChromaDB for top 5 results (without filter for now)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("--- Step 4: Raw Query Results ---")
for i, (doc, meta, dist) in enumerate(zip(results["documents"][0], results["metadatas"][0], results["distances"][0])):
    print(f"\nResult {i+1} (Distance: {dist:.4f}):")
    print(f"Metadata: {meta}")
    print(f"Text Snippet: {doc[:150]}...")