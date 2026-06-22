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
from app.memory.embedding_service import embedding_service

import json
import numpy as np


def save_messages(
    session_id: str,
    role: str,
    content: str,
    metadata: dict = None,
):

    if metadata is None:
        metadata = {}

    conn = get_connection()
    cursor = conn.cursor()

    # cursor.execute(
    #     """
    #     INSERT INTO conversation_memory
    #     (session_id, role, content)
    #     VALUES (?, ?, ?)
    #     """,
    #     (session_id, role, content),
    # )

    BAD_PATTERNS = [
        "not explicitly stated",
        "tool results",
        "confidence score",
        "without additional information",
        "the question is",
    ]

    if role == "assistant":

        content_lower = content.lower()

        if any(pattern in content_lower for pattern in BAD_PATTERNS):

            logger.info(
                "assistant_memory_skipped",
                reason="low_quality_response",
            )

            return

    cursor.execute(
        """
        SELECT 1
        FROM conversation_memory
        WHERE session_id = ?
        AND role = ?
        AND content = ?
        LIMIT 1
        """,
        (
            session_id,
            role,
            content,
        ),
    )

    existing = cursor.fetchone()

    if existing:
        logger.info(
            "duplicate_memory_skipped",
            role=role,
            content_preview=content[:100],
        )
        conn.close()
        return

    embedding = json.dumps(embedding_service.generate_embedding(content))
    logger.info(
        "embedding_generated",
        text=content[:50],
        dimensions=len(json.loads(embedding)),
    )

    cursor.execute(
        """
    INSERT INTO conversation_memory
    (
        session_id,
        role,
        content,
        memory_type,
        memory_value,
        embedding
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            session_id,
            role,
            content,
            metadata.get("memory_type"),
            metadata.get("memory_value"),
            embedding,
        ),
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
        SELECT role, content, memory_type, memory_value
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
            "memory_type": row["memory_type"],
            "memory_value": row["memory_value"],
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


def get_memory_by_type(
    session_id: str,
    memory_type: str,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT memory_value
        FROM conversation_memory
        WHERE session_id = ?
        AND memory_type = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (session_id, memory_type),
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["memory_value"]

    return None


def get_all_memories(session_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT memory_type, memory_value
        FROM conversation_memory
        WHERE session_id = ?
        AND memory_type IS NOT NULL
        ORDER BY id DESC
        """,
        (session_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    memories = {}

    for row in rows:

        memory_type = row["memory_type"]

        if memory_type not in memories:
            memories[memory_type] = row["memory_value"]

    logger.info(
        "all_memories_retrieved",
        session_id=session_id,
        count=len(memories),
    )

    return memories


def get_all_user_memories(
    session_id: str,
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT memory_type,memory_value
        FROM user_memory
        WHERE session_id = ?
        ORDER BY id DESC
        """,
        (session_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    result = {}

    for row in rows:

        if row["memory_type"] not in result:

            result[row["memory_type"]] = row["memory_value"]

    logger.info(
        "all_user_memories_retrieved",
        session_id=session_id,
        count=len(result),
    )

    return result


def upsert_user_memory(
    session_id: str,
    memory_type: str,
    memory_value: str,
):

    conn = get_connection()

    cursor = conn.cursor()

    existing = cursor.execute(
        """
        SELECT id
        FROM user_memory
        WHERE session_id = ?
        AND memory_type = ?
        """,
        (
            session_id,
            memory_type,
        ),
    ).fetchone()

    if existing:

        cursor.execute(
            """
            UPDATE user_memory
            SET memory_value=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,
            (
                memory_value,
                existing["id"],
            ),
        )

        logger.info(
            "user_memory_updated",
            session_id=session_id,
            memory_type=memory_type,
            memory_value=memory_value,
        )

    else:

        cursor.execute(
            """
            INSERT INTO user_memory
            (
                session_id,
                memory_type,
                memory_value
            )
            VALUES (?, ?, ?)
            """,
            (
                session_id,
                memory_type,
                memory_value,
            ),
        )

        logger.info(
            "user_memory_inserted",
            session_id=session_id,
            memory_type=memory_type,
            memory_value=memory_value,
        )

    conn.commit()
    conn.close()


def save_user_memory(
    session_id: str,
    memory_type: str,
    memory_value: str,
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_memory
        (
            session_id,
            memory_type,
            memory_value
        )
        VALUES (?, ?, ?)
        """,
        (
            session_id,
            memory_type,
            memory_value,
        ),
    )

    conn.commit()
    conn.close()

    logger.info(
        "user_memory_saved",
        session_id=session_id,
        memory_type=memory_type,
        memory_value=memory_value,
    )


def delete_user_memory(
    session_id,
    memory_type,
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM user_memory
        WHERE session_id = ?
        AND memory_type = ?
        """,
        (
            session_id,
            memory_type,
        ),
    )

    conn.commit()

    conn.close()

    logger.info(
        "user_memory_deleted",
        session_id=session_id,
        memory_type=memory_type,
    )


def get_user_memory(
    session_id: str,
    memory_type: str,
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT memory_value
        FROM user_memory
        WHERE session_id = ?
        AND memory_type = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            session_id,
            memory_type,
        ),
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        logger.info(
            "user_memory_found",
            session_id=session_id,
            memory_type=memory_type,
        )

        return row["memory_value"]

    logger.info(
        "user_memory_not_found",
        session_id=session_id,
        memory_type=memory_type,
    )

    return None


def get_memory_profile(session_id: str):

    # return {
    #     "name": get_user_memory(session_id, "name"),
    #     "location": get_user_memory(session_id, "location"),
    #     "company": get_user_memory(session_id, "company"),
    #     "profession": get_user_memory(session_id, "profession"),
    #     "favorite_color": get_user_memory(
    #         session_id,
    #         "favorite_color",
    #     ),
    # }

    return {
        "name": get_user_memory(session_id, "name"),
        "location": get_user_memory(session_id, "location"),
        "company": get_user_memory(session_id, "company"),
        "profession": get_user_memory(session_id, "profession"),
        "favorite_color": get_user_memory(session_id, "favorite_color"),
        "skills": get_user_memory(session_id, "skills"),
        "education": get_user_memory(session_id, "education"),
        "hobbies": get_user_memory(session_id, "hobbies"),
    }


def delete_memory(
    session_id: str,
    memory_type: str,
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM conversation_memory
        WHERE session_id = ?
        AND memory_type = ?
        """,
        (
            session_id,
            memory_type,
        ),
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    logger.info(
        "memory_deleted",
        session_id=session_id,
        memory_type=memory_type,
        deleted=deleted,
    )

    return deleted


def search_similar_memories(
    session_id,
    query_embedding,
    top_k=5,
):

    logger.info(
        "vector_search_started",
        session_id=session_id,
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role,
               content,
               embedding
        FROM conversation_memory
        WHERE session_id = ?
        AND embedding IS NOT NULL
        """,
        (session_id,),
    )

    rows = cursor.fetchall()

    logger.info(
        "vector_search_memories_loaded",
        session_id=session_id,
        count=len(rows),
    )

    conn.close()

    SIMILARITY_THRESHOLD = 0.3

    results = []

    for row in rows:

        if not row["embedding"]:
            continue

        content = row["content"].strip()

        if content.endswith("?"):
            continue

        memory_embedding = np.array(json.loads(row["embedding"]))

        similarity = np.dot(
            query_embedding,
            memory_embedding,
        ) / (np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding))

        logger.info(
            "memory_similarity_score",
            content=row["content"][:50],
            score=float(similarity),
        )

        results.append(
            (
                similarity,
                row["role"],
                row["content"],
            )
        )

    # results.sort(reverse=True, key=lambda x: x[0])
    results.sort(reverse=True, key=lambda x: x[0])

    # filtered_results = [
    #     (score, role, content)
    #     for score, role, content in results
    #     if score >= SIMILARITY_THRESHOLD
    # ]

    filtered_results = [
        (score, role, content)
        for score, role, content in results
        if (score >= SIMILARITY_THRESHOLD and role == "assistant")
    ]

    BAD_MEMORY_PATTERNS = [
        "no_name_found",
        "no_location_found",
        "no_company_found",
        "no_profession_found",
        "no_color_found",
        "name stored successfully",
        "location stored successfully",
    ]

    filtered_results = [
        (score, role, content)
        for score, role, content in filtered_results
        if not any(pattern in content.lower() for pattern in BAD_MEMORY_PATTERNS)
    ]

    # assistant_results = [item for item in filtered_results if item[1] == "assistant"]

    # if assistant_results:
    #     filtered_results = assistant_results

    filtered_results.sort(reverse=True, key=lambda x: x[0])

    # filtered_results = [
    #     (score, memory, content)
    #     for score, memory, content in results
    #     if score >= SIMILARITY_THRESHOLD
    # ]

    logger.info(
        "similarity_filter_applied",
        threshold=SIMILARITY_THRESHOLD,
        before_count=len(results),
        after_count=len(filtered_results),
    )

    logger.info(
        "vector_search_results",
        # results_preview=str(results[:5]),
        results_preview=str(filtered_results[:8]),
    )

    for score, role, content in filtered_results[:5]:

        logger.info(
            "memory_candidate",
            score=float(score),
            role=role,
            content=content[:100],
        )

    return filtered_results[:top_k]

    # return results[:top_k]
