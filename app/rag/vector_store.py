import chromadb
from app.core.logger import logger

client = chromadb.PersistentClient(path="./chroma_db")

logger.info("Rag folder is executing ")


memory_collection = client.get_or_create_collection(name="conversation_memory")

rag_collection = client.get_or_create_collection(name="rag_documents")
