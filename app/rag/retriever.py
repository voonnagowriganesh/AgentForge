from app.rag.vector_store import rag_collection

from app.memory.embedding_service import embedding_service

# def retrieve_documents(
#     query: str,
#     top_k: int = 5,
# ):

#     query_embedding = embedding_service.generate_embedding(query)

#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=top_k,
#     )

#     return results


# def retrieve_documents(
#     query,
#     top_k=5,
# ):

#     query_embedding = embedding_service.generate_embedding(query)

#     results = rag_collection.query(
#         query_embeddings=[query_embedding],
#         n_results=top_k,
#     )

#     #documents = results["documents"][0]

#     return {
#         "documents": results["documents"][0],
#         "distances": results["distances"][0],
#     }


from app.rag.hybrid_retriever import (
    hybrid_retrieve,
)


def retrieve_documents(
    query,
    top_k=5,
):

    results = hybrid_retrieve(
        query=query,
        top_k=top_k,
    )

    return {
        "documents": results["documents"],
        "distances": [],
    }
