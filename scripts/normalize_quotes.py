import json, uuid 
from pathlib import Path

INPUT_FILE = Path("data/quotes.json")
OUTPUT_FILE = Path("data/quotes_normalized.json")

def clean_text(text: str) -> str:
  """
  Normalize quote text:
  - Strip smart quotes and regular quotes
  - Normalize whitespace
  """

  if not text:
    return ""
  
  return text.strip().strip('“”"\'').replace("\n", " ").strip()


def normalize_quotes(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8") as f:
        quotes = json.load(f)

    normalized = []

    for quote in quotes:
        normalized.append(
            {
                "id": str(uuid.uuid4()),
                "text": clean_text(quote.get("text", "")),
                "author": quote.get("author") or "Unknown",
                "tags": quote.get("tags", []),
                "source": "quotes.toscrape.com",
            }
        )

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print(f"Normalized {len(normalized)} quotes → {output_path}")


if __name__ == "__main__":
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    normalize_quotes(INPUT_FILE, OUTPUT_FILE)