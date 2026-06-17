from app.rag.retriever import retrieve_documents


def document_search(query: str):

    results = retrieve_documents(
        query=query,
        top_k=5,
    )

    documents = results["documents"]

    return "\n\n".join(documents)
