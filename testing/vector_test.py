from app.memory.embedding_service import (
    embedding_service,
)

from app.memory.store import (
    search_similar_memories,
)

query_embedding = embedding_service.generate_embedding("where do i work")

results = search_similar_memories(
    "voonna1",
    query_embedding,
)

print(results)
