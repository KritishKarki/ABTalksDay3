import chromadb

# Initialize a persistent client saved in a local folder
client = chromadb.PersistentClient(path="./chroma_db")

#Create (or get) the collection
collection = client.get_or_create_collection(name="coverage_kb")

print("Collection created or retrieved successfully.", collection.name)