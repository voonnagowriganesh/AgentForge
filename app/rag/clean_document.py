import re


def clean_document(text: str):

    # Remove isolated page numbers
    text = re.sub(r"\b\d+\b", "", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()
