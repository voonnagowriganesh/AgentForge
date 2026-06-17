import uuid

from app.rag.loader import load_document
from app.rag.chunker import chunk_documents

from app.rag.vector_store import rag_collection

from app.memory.embedding_service import (
    embedding_service,
)


def ingest_document(file_path: str):

    docs = load_document(file_path)

    chunks = chunk_documents(docs)

    for chunk in chunks:

        text = chunk.page_content

        embedding = embedding_service.generate_embedding(text)

        # collection.add(
        #     ids=[str(uuid.uuid4())],
        #     documents=[text],
        #     embeddings=[embedding],
        #     metadatas=[{"source": file_path}],
        # )

        rag_collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": file_path,
                    "chunk_length": len(text),
                }
            ],
        )

    return len(chunks)
