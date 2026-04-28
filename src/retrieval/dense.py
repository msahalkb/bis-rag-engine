import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class DenseRetriever:
    def __init__(self, chunks, embeddings):
        self.chunks = chunks
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))

    def retrieve(self, query, top_k=5):
        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.chunks[i] for i in indices[0]]