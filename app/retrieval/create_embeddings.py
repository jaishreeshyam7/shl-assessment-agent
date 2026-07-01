import json
import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


# ---------------------- PATHS ----------------------

PROCESSED_PATH = Path("data/processed/assessments.json")
FAISS_INDEX_PATH = Path("data/faiss/index.faiss")
METADATA_PATH = Path("data/faiss/metadata.pkl")


# ---------------------- FUNCTIONS ----------------------

def load_assessments():
    with open(PROCESSED_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def create_search_text(assessment):
    return f"""
Name: {assessment.get("name","")}

Description:
{assessment.get("description","")}

Categories:
{", ".join(assessment.get("categories", []))}

Job Levels:
{", ".join(assessment.get("job_levels", []))}

Languages:
{", ".join(assessment.get("languages", []))}

Duration:
{assessment.get("duration","")}

Remote:
{assessment.get("remote","")}

Adaptive:
{assessment.get("adaptive","")}
"""


# ---------------------- MAIN ----------------------

def main():

    print("🚀 Step 1 : Loading assessments...")

    assessments = load_assessments()

    print(f"✅ Loaded {len(assessments)} assessments")

    print("\n🚀 Step 2 : Creating search documents...")

    search_documents = [
        create_search_text(assessment)
        for assessment in assessments
    ]

    print(f"✅ Created {len(search_documents)} search documents")

    print("\n🚀 Step 3 : Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("✅ Model Loaded")

    print("\n🚀 Step 4 : Generating embeddings...")

    embeddings = model.encode(
        search_documents,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    print("✅ Embeddings Generated")
    print(f"Shape : {embeddings.shape}")

    print("\n🚀 Step 5 : Creating FAISS Index...")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    with open(METADATA_PATH, "wb") as file:
        pickle.dump(assessments, file)

    print("\n==============================")
    print("✅ SUCCESS")
    print("==============================")
    print(f"Vectors Stored : {index.ntotal}")
    print(f"Dimension      : {dimension}")
    print(f"Index Saved    : {FAISS_INDEX_PATH}")
    print(f"Metadata Saved : {METADATA_PATH}")


if __name__ == "__main__":
    main()