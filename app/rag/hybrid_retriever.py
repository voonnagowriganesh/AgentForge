from app.rag.vector_store import rag_collection

from app.memory.embedding_service import (
    embedding_service,
)

from app.rag.bm25_retriever import (
    bm25_retriever,
)

from app.rag.rrf import reciprocal_rank_fusion
from app.rag.reranker import rerank_documents

from app.core.logger import logger


def hybrid_retrieve(
    query: str,
    top_k: int = 5,
):

    #
    # Vector Search
    #

    embedding = embedding_service.generate_embedding(query)

    vector_results = rag_collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
    )

    vector_docs = vector_results["documents"][0]

    #
    # BM25 Search
    #

    bm25_results = bm25_retriever.retrieve(
        query=query,
        top_k=top_k,
    )

    bm25_docs = [item["document"] for item in bm25_results]

    #
    # Merge + Deduplicate
    #

    # combined = []

    # seen = set()

    # for doc in vector_docs + bm25_docs:

    #     if doc not in seen:

    #         combined.append(doc)

    #         seen.add(doc)

    # return {"documents": combined[:top_k]}
    # combined = []
    # scores = []

    # seen = set()

    # for rank, doc in enumerate(vector_docs + bm25_docs):

    #     if doc not in seen:

    #         combined.append(doc)

    #         # temporary score
    #         scores.append(1 / (rank + 1))

    #         seen.add(doc)

    fused_results = reciprocal_rank_fusion(
        vector_docs,
        bm25_docs,
    )

    top_documents = []
    top_scores = []

    # for doc, score in fused_results[:top_k]:

    #     top_documents.append(doc)
    #     top_scores.append(score)

    candidate_docs = [doc for doc, _ in fused_results[:10]]

    reranked = rerank_documents(query=query, documents=candidate_docs, top_k=top_k)

    # top_documents = []
    # top_scores = []

    # for doc, score in reranked:

    #     top_documents.append(doc)
    #     top_scores.append(float(score))

    top_documents = []
    top_scores = []

    for doc, score in reranked:

        if float(score) <= 0:
            continue

        if "table of contents" in doc.lower():
            continue

        top_documents.append(doc)
        top_scores.append(float(score))

    logger.info(
        "hybrid_retrieval_completed with rrf",
        vector_count=len(vector_docs),
        bm25_count=len(bm25_docs),
    )

    return {
        "documents": top_documents,
        "scores": top_scores,
    }

    # logger.info(
    #     "hybrid_retrieval_completed",
    #     vector_count=len(vector_docs),
    #     bm25_count=len(bm25_docs),
    #     final_count=len(combined[:top_k]),
    # )

    # return {
    #     "documents": combined[:top_k],
    #     "scores": scores[:top_k],
    # }
