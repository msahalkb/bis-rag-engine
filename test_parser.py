from src.ingestion.parser import extract_text

text = extract_text("data/raw/dataset.pdf")
print(text[:5000])