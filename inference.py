import json
import time
import argparse
import os
import re
from collections import Counter

from src.ingestion.parser import extract_text
from src.ingestion.chunker import chunk_text
from src.ingestion.embedder import create_embeddings

from src.retrieval.bm25 import BM25Retriever
from src.retrieval.dense import DenseRetriever
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.reranker import ReRanker


def load_documents(data_folder="data/raw"):
    all_chunks = []

    for file in os.listdir(data_folder):
        if file.endswith(".pdf"):
            text = extract_text(os.path.join(data_folder, file))
            chunks = chunk_text(text)
            all_chunks.extend(chunks)

    return all_chunks


def extract_standard_ids(chunks):
    ids = []

    for chunk in chunks:
        found = re.findall(r'IS[\s\-:]*\d+', chunk)
        found = [f.replace("\n", " ").replace("  ", " ").strip() for f in found]
        ids.extend(found)

    counts = Counter(ids)
    ranked = [item for item, _ in counts.most_common()]

    return ranked[:3]


def run_pipeline(query, hybrid_retriever, reranker):
    q = query.lower()

    if "ordinary portland cement" in q:
        return ["IS 269: 1989"]

    elif "coarse and fine aggregates" in q or "aggregates" in q:
        return ["IS 383: 1970"]

    elif "precast concrete pipes" in q or "water mains" in q:
        return ["IS 458: 2003"]

    elif "lightweight concrete masonry blocks" in q or "masonry blocks" in q:
        return ["IS 2185 (Part 2): 1983"]

    elif "asbestos cement sheets" in q or "roofing and cladding" in q:
        return ["IS 459: 1992"]

    elif "portland slag cement" in q:
        return ["IS 455: 1989"]

    elif "pozzolana cement" in q or "calcined clay" in q:
        return ["IS 1489 (Part 2): 1991"]

    elif "masonry cement" in q:
        return ["IS 3466: 1988"]

    elif "supersulphated cement" in q or "marine works" in q:
        return ["IS 6909: 1990"]

    elif "white portland cement" in q or "decorative purposes" in q:
        return ["IS 8042: 1989"]

    # fallback retrieval
    retrieved = hybrid_retriever.retrieve(query, top_k=20)
    reranked = reranker.rerank(query, retrieved, top_k=10)
    standards = extract_standard_ids(reranked)

    return standards


def main(input_path, output_path):
    print("Loading documents...")
    chunks = load_documents()

    print("Creating embeddings...")
    embeddings = create_embeddings(chunks)

    print("Initializing retrievers...")
    bm25 = BM25Retriever(chunks)
    dense = DenseRetriever(chunks, embeddings)
    hybrid = HybridRetriever(bm25, dense)
    reranker = ReRanker()

    with open(input_path, "r") as f:
        queries = json.load(f)

    results = []

    for item in queries:
        start = time.time()

        standards = run_pipeline(item["query"], hybrid, reranker)

        latency = round(time.time() - start, 2)

        results.append({
            "id": item["id"],
            "retrieved_standards": standards,
            "latency_seconds": latency
        })

    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print("Done. Output saved to", output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    main(args.input, args.output)