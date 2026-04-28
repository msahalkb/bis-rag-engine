import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_recommendation(query, retrieved_chunks):
    context = "\n".join(retrieved_chunks)

    prompt = f"""
You are a BIS standards expert.

Product Description:
{query}

Relevant document excerpts:
{context}

Return only top 3 BIS Standard IDs like:
IS 456
IS 1786
IS 383
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    text = response.text
    ids = re.findall(r'IS\s?\d+', text)

    return ids[:3]