import uuid

from app.rag.loader import load_document
from app.rag.chunker import chunk_documents

from app.rag.vector_store import rag_collection

import os
import json

from app.memory.embedding_service import (
    embedding_service,
)


def ingest_document(file_path: str):

    docs = load_document(file_path)

    chunks = chunk_documents(docs)

    chunk_store_path = "data/rag_chunks.json"

    os.makedirs("data", exist_ok=True)

    stored_chunks = []

    if os.path.exists(chunk_store_path):

        with open(chunk_store_path, "r", encoding="utf-8") as f:
            stored_chunks = json.load(f)

    # for chunk in chunks:

    #     text = chunk.page_content

    #     stored_chunks.append(
    #         {
    #             "text": text,
    #             "source": file_path,
    #         }
    #     )

    for chunk in chunks:

        text = chunk.page_content

        text_lower = text.lower()

        if (
            "table of contents" in text_lower
            or "part i" in text_lower
            or "part ii" in text_lower
            or "part iii" in text_lower
            or "part iv" in text_lower
            or "chapter" in text_lower
            or (text.count("\n") > 15 and len(text.split()) < 200)
        ):
            continue

        stored_chunks.append(
            {
                "text": text,
                "source": file_path,
            }
        )

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

    with open(
        chunk_store_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            stored_chunks,
            f,
            ensure_ascii=False,
            indent=2,
        )

    return len(chunks)
