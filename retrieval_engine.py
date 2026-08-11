import re
import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

def classify_query(query: str) -> str:
    """
    Classifies an incoming user query into:
    - 'structured' (SQL lookup for claims, plan details, deductibles)
    - 'unstructured' (Vector search for policy coverage, benefits wording)
    - 'both' (Requires both personal SQL data and policy text)
    """
    query_lower = query.lower()

    # Keywords for structured data lookups
    structured_keywords = ["claim", "status", "deductible spent", "copay paid", "member id", "balance", "total spent"]
    
    # Keywords for unstructured/policy coverage lookups
    unstructured_keywords = ["covered", "policy", "benefit", "exclusions", "limits", "what is", "is physical therapy"]

    has_structured = any(kw in query_lower for kw in structured_keywords)
    has_unstructured = any(kw in query_lower for kw in unstructured_keywords)

    if has_structured and has_unstructured:
        return "both"
    elif has_structured:
        return "structured"
    elif has_unstructured:
        return "unstructured"
    else:
        # Default fallback to unstructured policy search
        return "unstructured"


# if __name__ == "__main__":
#     # Test classifier on sample questions
#     test_queries = [
#         "What is the status of my claim #123?",
#         "Is physical therapy covered under the Silver plan?",
#         "How much deductible have I paid and what is my plan deductible for physical therapy?"
#     ]

#     for q in test_queries:
#         print(f"Query: '{q}' --> Classification: {classify_query(q)}")


DB_PATH = "coverage.db"

def sql_lookup(question: str) -> list[dict]:
    """
    Queries SQLite database (coverage.db) based on key terms in the question.
    """
    results = []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    question_lower = question.lower()
    
    try:
        if "claim" in question_lower:
            cursor.execute("SELECT * FROM claims LIMIT 5")
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            for row in rows:
                results.append(dict(zip(col_names, row)))
        else:
            cursor.execute("SELECT * FROM plans LIMIT 5")
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            for row in rows:
                results.append(dict(zip(col_names, row)))
    except Exception as e:
        print(f"SQL Lookup Error: {e}")
    finally:
        conn.close()
        
    return results

def vector_lookup(question: str, n_results: int = 5) -> list[dict]:
    """
    Embeds the question and queries ChromaDB for the top-n policy chunks.
    """
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="coverage_kb")
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(question).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    formatted_results = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]
        
        for doc, meta, dist in zip(docs, metas, dists):
            formatted_results.append({
                "text": doc,
                "metadata": meta,
                "distance": dist
            })
            
    return formatted_results

def retrieve(question: str) -> dict:
    """
    Routes the query to sql_lookup, vector_lookup, or both based on classification,
    and merges the retrieved context.
    """
    classification = classify_query(question)
    context = {
        "question": question,
        "classification": classification,
        "sql_results": [],
        "vector_results": []
    }
    
    if classification == "structured":
        context["sql_results"] = sql_lookup(question)
    elif classification == "unstructured":
        context["vector_results"] = vector_lookup(question)
    elif classification == "both":
        context["sql_results"] = sql_lookup(question)
        context["vector_results"] = vector_lookup(question)
        
    return context

if __name__ == "__main__":
    test_questions = [
        "What is my copay?",
        "Is maternity care covered on the Bronze plan?",
        "What is the status of claim C-2031?",
        "Is physical therapy covered under the Silver plan?",
        "How much deductible have I spent so far?",
        "What are the limitations and exclusions for mental health services?",
        "What is my member ID and plan type?",
        "How much deductible spent is remaining and is physical therapy covered under Silver?",
        "What is the out-of-pocket maximum for emergency room visits?",
        "Are prescription drugs covered on the Gold plan?"
    ]

    print("=== Running Step 5 Test Harness (10 Questions) ===\n")
    for idx, q in enumerate(test_questions, 1):
        res = retrieve(q)
        print(f"[{idx}] Question: {q}")
        print(f"    Classification: {res['classification']}")
        print(f"    SQL Hits: {len(res['sql_results'])} | Vector Hits: {len(res['vector_results'])}")
        print("-" * 50)