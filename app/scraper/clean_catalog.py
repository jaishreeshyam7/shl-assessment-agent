import json
from pathlib import Path

# Locate the raw catalog
catalog_path = Path("data/raw/shl_product_catalog.json")

# Load the JSON file
with open(catalog_path, "r", encoding="utf-8") as file:
    catalog = json.load(file)

print("=" * 60)
print("SHL Catalog Loaded Successfully!")
print("=" * 60)

print(f"Type of catalog: {type(catalog)}")

# Check if it is a list
if isinstance(catalog, list):
    print(f"\nTotal Assessments: {len(catalog)}")

    print("\nFirst Assessment:\n")
    print(json.dumps(catalog[0], indent=4))

# Otherwise print keys
elif isinstance(catalog, dict):
    print("\nTop-level Keys:")
    print(list(catalog.keys()))