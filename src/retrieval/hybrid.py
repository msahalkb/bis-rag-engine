class HybridRetriever:
    def __init__(self, bm25_retriever, dense_retriever):
        self.bm25 = bm25_retriever
        self.dense = dense_retriever

    def retrieve(self, query, top_k=5):
        bm25_results = self.bm25.retrieve(query, top_k=top_k)
        dense_results = self.dense.retrieve(query, top_k=top_k)

        combined = bm25_results + dense_results

        # remove duplicates while preserving order
        unique_results = []
        seen = set()
        for item in combined:
            if item not in seen:
                unique_results.append(item)
                seen.add(item)

        return unique_results[:top_k]