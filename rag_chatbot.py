import os
from dotenv import load_dotenv
from openai import OpenAI
from retrieval_engine import retrieve

load_dotenv()

# Initialize OpenAI client pointing to Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required string for OpenAI SDK initialization
)

MODEL_NAME = "llama3.1"

SYSTEM_PROMPT = """Answer using ONLY the context below.
If the answer isn't in the context, say you don't know and suggest the member contact support.
This is not medical advice."""

def generate_answer(question: str, context: str) -> str:
    """
    Sends the question and context to the local LLM to generate a grounded answer.
    """
    user_message = f"""Context: {context}

Question: {question}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.0
    )
    
    return response.choices[0].message.content

from retrieval_engine import retrieve

def retrieve_and_answer(question: str) -> dict:
    """
    End-to-end RAG pipeline:
    1. Retrieves relevant context using the retrieval engine.
    2. Formats context into a string.
    3. Generates a grounded response using the LLM.
    """
    retrieved_data = retrieve(question)
    
    # Format retrieved SQL rows and Vector chunks into context text
    context_parts = []
    
    if retrieved_data.get("sql_results"):
        context_parts.append("--- Structured Data (SQL) ---")
        for row in retrieved_data["sql_results"]:
            context_parts.append(str(row))
            
    if retrieved_data.get("vector_results"):
        context_parts.append("--- Policy Text (Vector Search) ---")
        for item in retrieved_data["vector_results"]:
            context_parts.append(f"- {item['text']}")
            
    context_str = "\n".join(context_parts) if context_parts else "No relevant context found."
    
    # Generate grounded answer from LLM
    answer = generate_answer(question, context_str)
    
    return {
        "question": question,
        "classification": retrieved_data.get("classification"),
        "context": context_str,
        "answer": answer
    }



def stream_answer(question: str) -> None:
    """
    Retrieves context and streams the generated LLM response directly to stdout.
    """
    retrieved_data = retrieve(question)
    
    context_parts = []
    if retrieved_data.get("sql_results"):
        context_parts.append("--- Structured Data (SQL) ---")
        for row in retrieved_data["sql_results"]:
            context_parts.append(str(row))
            
    if retrieved_data.get("vector_results"):
        context_parts.append("--- Policy Text (Vector Search) ---")
        for item in retrieved_data["vector_results"]:
            context_parts.append(f"- {item['text']}")
            
    context_str = "\n".join(context_parts) if context_parts else "No relevant context found."

    user_message = f"""Context: {context_str}

Question: {question}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.0,
        stream=True  # Enable streaming
    )

    print(f"\n--- Streaming Answer for: '{question}' ---")
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")


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

    print("=== Running Day 11 Full RAG Pipeline Test Harness ===")

    with open("rag_qa_results.md", "w", encoding="utf-8") as f:
        f.write("# RAG Pipeline Evaluation Log\n\n")

        for idx, q in enumerate(test_questions, 1):
            print(f"Processing Q{idx}: {q}")
            try:
                res = retrieve_and_answer(q)

                f.write(f"### Question {idx}\n")
                f.write(f"- **Question:** {res['question']}\n")
                f.write(f"- **Classification:** {res['classification']}\n")
                f.write(f"- **Retrieved Context Summary:**\n```\n{res['context']}\n```\n")
                f.write(f"- **Generated Answer:**\n{res['answer']}\n\n")
                f.write("---\n\n")
            except Exception as e:
                print(f"Error processing Q{idx}: {e}")
                break

    print("\nFinished running test harness!")

    stream_answer("Is physical therapy covered under the Silver plan?")