import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


# ==========================
# Paths
# ==========================

FAISS_INDEX_PATH = Path("data/faiss/index.faiss")
METADATA_PATH = Path("data/faiss/metadata.pkl")


# ==========================
# Load Everything Once
# ==========================

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index(str(FAISS_INDEX_PATH))

print("Loading assessment metadata...")
with open(METADATA_PATH, "rb") as file:
    metadata = pickle.load(file)

print(f"Loaded {len(metadata)} assessments.\n")


# ==========================
# Embedding Function
# ==========================

def create_query_embedding(query: str):
    """
    Converts a user query into an embedding vector.
    """
    return model.encode([query], convert_to_numpy=True)


# ==========================
# Search Function
# ==========================

def search(query: str, top_k: int = 5):
    """
    Searches the FAISS index and returns the
    top matching SHL assessments.
    """

    query_embedding = create_query_embedding(query)

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:

        # Ignore invalid indices
        if idx == -1:
            continue

        results.append(metadata[idx])

    return results


# ==========================
# Standalone Testing
# ==========================

def main():

    while True:

        query = input("\nEnter your query (or type 'exit'): ")

        if query.lower() == "exit":
            break

        results = search(query)

        print("\nTop Recommendations\n")

        for i, assessment in enumerate(results, start=1):

            print("=" * 60)
            print(f"{i}. {assessment['name']}")
            print(f"Category : {', '.join(assessment['categories'])}")
            print(f"Duration : {assessment['duration']}")
            print(f"Remote   : {assessment['remote']}")
            print(f"Adaptive : {assessment['adaptive']}")
            print(f"URL      : {assessment['url']}")

        print("=" * 60)


if __name__ == "__main__":
    main()