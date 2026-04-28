from src.ingestion.parser import extract_text
import re

text = extract_text("data/raw/dataset.pdf")

matches = re.findall(r'IS[\s\-:]*\d+', text)

print(matches[:20])