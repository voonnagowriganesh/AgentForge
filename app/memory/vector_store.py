import chromadb
from app.core.logger import logger

client = chromadb.PersistentClient(path="./chroma_db")

logger.error("Memory->vector_store.py file is executing please checl")

collection = client.get_or_create_collection(name="conversation_memory")
