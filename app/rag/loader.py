from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)

from pathlib import Path


def load_document(file_path: str):

    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(file_path)

    elif suffix == ".docx":
        loader = Docx2txtLoader(file_path)

    elif suffix == ".txt":
        loader = TextLoader(file_path)

    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return loader.load()
