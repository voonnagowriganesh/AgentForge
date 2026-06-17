from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os

from app.rag.retriever import rag_collection

from app.core.logger import logger
from app.core.logger_tracing import console_log
from app.graph.workflow import graph
from app.schemas.request import ChatRequest
from app.schemas.response import AgentResponse
from app.rag.ingestion import ingest_document

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


@router.post("/chat")
async def chat(request: ChatRequest):
    console_log(f"Received chat request: {request.query}")
    logger.info("chat_request_received", query=request.query)

    result = await graph.ainvoke(
        {
            "query": request.query,
            "session_id": request.session_id,
            "memory_context": [],
            "step_results": [],
            "execution_trace": [],
        }
    )

    logger.info(
        "chat_request_completed",
        query=request.query,
        route=result.get("route"),
        response_length=len(str(result.get("final_response", ""))),
    )

    return AgentResponse(
        query=result["query"],
        route=result["route"],
        final_response=result["final_response"],
        execution_trace=result["execution_trace"],
    )


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename,
    )

    with open(
        file_path,
        "wb",
    ) as f:

        content = await file.read()

        f.write(content)

    chunks_count = ingest_document(file_path)

    chunks_count = ingest_document(file_path)

    logger.info(
        "rag_documents_count",
        count=rag_collection.count(),
    )

    return {
        "status": "success",
        "file": file.filename,
        "chunks": chunks_count,
    }
