from app.rag.retriever import retrieve_documents
from app.rag.hybrid_retriever import hybrid_retrieve
from app.rag.clean_document import clean_document


def document_search(query: str):

    # results = retrieve_documents(
    #     query=query,
    #     top_k=5,
    # )

    results = hybrid_retrieve(
        query=query,
        top_k=5,
    )

    # documents = results["documents"]

    # return "\n\n".join(documents)

    documents = results["documents"]

    documents = [clean_document(doc) for doc in documents]
    scores = results["scores"]

    # formatted_results = []

    # for i, (doc, score) in enumerate(
    #     zip(documents, scores),
    #     start=1,
    # ):

    #     formatted_results.append(f"""
    # Document {i}
    # Relevance Score: {score}

    # {doc}
    # """)

    # return "\n\n".join(formatted_results)

    formatted_results = []

    doc_no = 1

    for doc, score in zip(documents, scores):

        # Skip irrelevant documents
        if score < 0:
            continue

        formatted_results.append(f"""
    Document {doc_no}
    Relevance Score: {score:.4f}

    {doc}
    """)

        doc_no += 1

    if not formatted_results:
        return "No relevant documents found."

    return "\n\n".join(formatted_results)
