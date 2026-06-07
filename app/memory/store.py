from app.core.logger import logger

MEMORY = {}


def save_messages(
    session_id: str,
    role: str,
    content: str,
):

    if session_id not in MEMORY:
        logger.info(
            f"Session ID not found so creating a record for that : {session_id}"
        )
        MEMORY[session_id] = []

    MEMORY[session_id].append({"role": role, "content": content})

    logger.info(f"Content {content} saved successfully to the memory")

    MEMORY[session_id] = MEMORY[session_id][-10:]


def get_messages(session_id: str):

    logger.info(
        f"Memory retrived from the function get messages for the session id : {session_id}"
    )

    return MEMORY.get(session_id, [])
