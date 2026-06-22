import json
import os

from rank_bm25 import BM25Okapi

from app.core.logger import logger


class BM25Retriever:

    def __init__(self):

        self.chunk_path = "data/rag_chunks.json"

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        if not os.path.exists(self.chunk_path):

            logger.warning("bm25_chunk_store_missing")

            return []

        with open(
            self.chunk_path,
            "r",
            encoding="utf-8",
        ) as f:

            chunks = json.load(f)

        corpus = [x["text"] for x in chunks]

        tokenized_corpus = [doc.lower().split() for doc in corpus]

        bm25 = BM25Okapi(tokenized_corpus)

        scores = bm25.get_scores(query.lower().split())

        ranked = sorted(
            zip(corpus, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        results = []

        for doc, score in ranked[:top_k]:

            results.append(
                {
                    "document": doc,
                    "score": float(score),
                }
            )

        logger.info(
            "bm25_retrieval_completed",
            count=len(results),
        )

        return results


bm25_retriever = BM25Retriever()
