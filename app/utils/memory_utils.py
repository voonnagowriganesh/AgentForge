def extract_memory_metadata(text):

    text_lower = text.lower().strip()

    if text_lower.startswith("my name is"):
        return {
            "memory_type": "name",
            "memory_value": text[11:].strip(),
        }

    if text_lower.startswith("i live in"):
        return {
            "memory_type": "location",
            "memory_value": text[9:].strip(),
        }

    return {
        "memory_type": None,
        "memory_value": None,
    }


def extract_forget_memory(query):

    query_lower = query.lower()

    mapping = {
        "name": "name",
        "location": "location",
        "company": "company",
        "profession": "profession",
        "favorite color": "favorite_color",
    }

    for key, value in mapping.items():

        if key in query_lower:
            return value

    return None
