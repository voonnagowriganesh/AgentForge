from app.rag.retriever import retrieve_documents
from app.rag.ingestion import ingest_document

# docs = retrieve_documents("third-party integrations")

# print(docs)
file_path = r"C:\Users\voonn\Agentic_AI_Documents\principles-of-building-ai-agents.pdf"

ingest_document(file_path)
