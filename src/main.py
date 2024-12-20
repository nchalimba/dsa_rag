from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import uvicorn
# from src.models.request_models import QuestionRequest
# from src.services.qa_service import QAService
from dotenv import load_dotenv
from src.controllers.document_controller import router as document_router

load_dotenv()

app = FastAPI(
    title="DSA RAG",
    description="A RAG system for answering questions about Data Structures and Algorithms",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# qa_service = QAService()

app.include_router(document_router, prefix="/process")

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "message": "DSA RAG API is running"
    }

# @app.post("/ask")
# async def ask_question(request: QuestionRequest):
#     """
#     Ask a question and get a streaming response based on the processed documents.
#     """
#     try:
#         return EventSourceResponse(
#             qa_service.get_streaming_response(request.question),
#             media_type="text/event-stream"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "services": {
            "document_processor": "up",
            "qa_service": "up"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
