# from app.core.logger import logger

# MEMORY = {}


# def save_messages(
#     session_id: str,
#     role: str,
#     content: str,
# ):

#     if session_id not in MEMORY:
#         logger.info(
#             f"Session ID not found so creating a record for that : {session_id}"
#         )
#         MEMORY[session_id] = []

#     MEMORY[session_id].append({"role": role, "content": content})

#     logger.info(f"Content {content} saved successfully to the memory")

#     MEMORY[session_id] = MEMORY[session_id][-10:]


# def get_messages(session_id: str):

#     logger.info(
#         f"Memory retrived from the function get messages for the session id : {session_id}"
#     )

#     return MEMORY.get(session_id, [])


from app.db.database import get_connection
from app.core.logger import logger


def save_messages(
    session_id: str,
    role: str,
    content: str,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_memory
        (session_id, role, content)
        VALUES (?, ?, ?)
        """,
        (session_id, role, content),
    )

    conn.commit()
    conn.close()

    logger.info(
        "memory_saved",
        session_id=session_id,
        role=role,
    )


def get_messages(session_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM conversation_memory
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (session_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    memory = [
        {
            "role": row["role"],
            "content": row["content"],
        }
        for row in rows
    ]

    logger.info(
        "memory_retrieved",
        session_id=session_id,
        count=len(memory),
    )

    return memory


def search_messages(
    session_id: str,
    query: str,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT role, content
    FROM conversation_memory
    WHERE session_id = ?
    AND content LIKE ?
    ORDER BY id DESC
    LIMIT 5
    """,
        (session_id, f"%{query}%"),
    )

    rows = cursor.fetchall()

    conn.close()

    results = [
        {
            "role": row["role"],
            "content": row["content"],
        }
        for row in rows
    ]

    logger.info(
        "memory_search_completed",
        session_id=session_id,
        query=query,
        count=len(results),
    )

    return results
