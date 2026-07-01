print("Script Started")
import json
from pathlib import Path


RAW_PATH = Path("data/raw/shl_product_catalog.json")
PROCESSED_PATH = Path("data/processed/assessments.json")


def load_catalog():
    with open(RAW_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_assessment(item):
    return {
        "id": item.get("entity_id", ""),
        "name": item.get("name", ""),
        "url": item.get("link", ""),
        "description": item.get("description", ""),
        "job_levels": item.get("job_levels", []),
        "languages": item.get("languages", []),
        "duration": item.get("duration", ""),
        "remote": item.get("remote", ""),
        "adaptive": item.get("adaptive", ""),
        "categories": item.get("keys", [])
    }


def process_catalog(catalog):
    processed = []

    for assessment in catalog:
        processed.append(normalize_assessment(assessment))

    return processed


def save_catalog(processed_catalog):
    with open(PROCESSED_PATH, "w", encoding="utf-8") as file:
        json.dump(processed_catalog, file, indent=4)


def main():
    catalog = load_catalog()

    processed_catalog = process_catalog(catalog)

    save_catalog(processed_catalog)

    print(f"✅ Processed {len(processed_catalog)} assessments")
    print(f"📁 Saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    main()