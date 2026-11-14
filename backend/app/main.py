from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.schemas import (
    AssistantMode,
    ChatRequest,
    ChatResponse,
    SourceCitation,
)

app = FastAPI(
    title="AfriCareEdu AI API",
    description="Unified RAG-powered AI engine for Preventive Health Awareness and Accessible Education.",
    version="0.1.0",
)

# Enable CORS for frontend local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDICAL_DISCLAIMER = (
    "Disclaimer: AfriCareEdu AI provides general preventive health awareness and educational "
    "information only. It is not a substitute for professional medical diagnosis or treatment. "
    "Always consult a licensed healthcare provider for medical advice."
)


@app.get("/health", tags=["System"])
def health_check():
    """Verify that the API service is online and healthy."""
    return {
        "status": "ok",
        "service": "AfriCareEdu AI Backend",
        "version": "0.1.0",
    }


@app.post("/api/v1/chat", response_model=ChatResponse, tags=["AI Assistant"])
def chat_endpoint(payload: ChatRequest):
    """
    Unified chat endpoint switching between Health Awareness Mode and Learning Assistant Mode.
    """
    if payload.mode == AssistantMode.HEALTH:
        answer = (
            f"[Health Awareness Mode] Here is verified preventive health guidance regarding: "
            f"'{payload.query}'. (RAG vector retrieval & LLM synthesis will connect here.)"
        )
        sources = [
            SourceCitation(
                title="WHO Preventive Health & Community Hygiene Guidelines",
                category="health",
                source_url="https://www.who.int",
            )
        ]
        disclaimer = MEDICAL_DISCLAIMER
    else:
        answer = (
            f"[Learning Assistant Mode] Let's break down '{payload.query}' step by step. "
            f"(Curriculum RAG retrieval & tutor prompt will connect here.)"
        )
        sources = [
            SourceCitation(
                title="AfriCareEdu Foundational STEM & Literacy Modules",
                category="education",
            )
        ]
        disclaimer = None

    return ChatResponse(
        mode=payload.mode,
        answer=answer,
        sources=sources,
        safety_disclaimer=disclaimer,
    )