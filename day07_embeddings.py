import json
import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

# 1. Initialize the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text: str) -> np.ndarray:
    """Generate a 384-dimensional dense vector representation for the given text."""
    return model.encode(text)


def process_and_visualize():
    kb_path = "knowledge_base.jsonl"
    texts = []
    sections = []

    # 2. Read knowledge_base.jsonl
    with open(kb_path, "r", encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)
            texts.append(chunk["text"])
            sections.append(chunk["metadata"]["section"])

    print(f"Loaded {len(texts)} chunks from {kb_path}.")

    # 3. Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # 4. Save embeddings.npy
    np.save("embeddings.npy", embeddings)
    print("Saved embeddings to embeddings.npy")

    # 5. PCA Reduction to 2D
    print("Reducing dimensions using PCA...")
    pca = PCA(n_components=2)
    embeddings_2d = pca.fit_transform(embeddings)

    # 6. Plot by section
    plt.figure(figsize=(10, 7))
    unique_sections = list(set(sections))

    for section in unique_sections:
        # Get indices for this section
        idx = [i for i, s in enumerate(sections) if s == section]
        plt.scatter(
            embeddings_2d[idx, 0],
            embeddings_2d[idx, 1],
            label=section,
            alpha=0.7,
            edgecolors="k",
        )

    plt.title("2D PCA Visualization of Knowledge Base Embeddings")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(title="Sections")
    plt.grid(True, linestyle="--", alpha=0.5)

    # 7. Save plot
    output_png = "embeddings_2d.png"
    plt.savefig(output_png, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved visualization plot to {output_png}!")


if __name__ == "__main__":
    process_and_visualize()