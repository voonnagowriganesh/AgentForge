from app.rag.retriever import retrieve_documents

docs = retrieve_documents("third-party integrations")

print(docs)
