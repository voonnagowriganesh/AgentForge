from app.memory.store import get_user_memory


def check_structured_memory(
    session_id: str,
    query: str,
):
    query_lower = query.lower()

    if "my name" in query_lower:

        value = get_user_memory(
            session_id,
            "name",
        )

        if value:
            return value

    if "favorite color" in query_lower:

        value = get_user_memory(
            session_id,
            "favorite_color",
        )

        if value:
            return value

    return None
