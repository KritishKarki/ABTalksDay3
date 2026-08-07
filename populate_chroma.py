import json
import numpy as np
import chromadb

# 1. Initialize Chroma client and get/create collection
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="coverage_kb")

# 2. Load knowledge base chunks
with open("knowledge_base.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# 3. Load generated embeddings
embeddings = np.load("embeddings.npy")

# 4. Prepare data for batch upsert
ids = []
documents = []
metadatas = []
embedding_list = embeddings.tolist()

for idx, chunk in enumerate(chunks):
    # Ensure chunk ID is a string
    chunk_id = str(chunk.get("id", f"chunk_{idx}"))
    ids.append(chunk_id)
    
    # Text content
    documents.append(chunk.get("text", ""))
    
    # Metadata for filtering (extract relevant fields or pass metadata dict)
    metadata = chunk.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {"source": str(metadata)}
    metadatas.append(metadata)

# 5. Upsert into ChromaDB
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embedding_list,
    metadatas=metadatas
)

print(f"Successfully upserted {len(ids)} chunks into 'coverage_kb'.")
print(f"Total count in collection: {collection.count()}")