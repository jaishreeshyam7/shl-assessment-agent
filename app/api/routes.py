from fastapi import APIRouter

from app.core.llm import (
    generate_response,
    generate_comparison
)
from app.core.conversation_manager import ConversationManager
from app.retrieval.retriever import search
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation
)

router = APIRouter()

manager = ConversationManager()


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # -----------------------------
    # Step 1: Read conversation
    # -----------------------------
    history = [message.model_dump() for message in request.messages]

    # -----------------------------
    # Step 2: Out of Scope Detection
    # -----------------------------
    if manager.is_out_of_scope(history):

        return ChatResponse(
            reply="I'm designed to help with SHL assessment recommendations. Please ask about hiring, roles, skills, or assessments.",
            recommendations=[],
            end_of_conversation=True
        )

    # -----------------------------
    # Step 3: Build Search Query
    # -----------------------------
    user_query = " ".join(
        message.content
        for message in request.messages
        if message.role == "user"
    )

    # -----------------------------
    # Step 4: Compare Request
    # -----------------------------
    if manager.is_compare_request(history):

        results = search(user_query, top_k=5)

        recommendations = []

        for assessment in results:

            recommendations.append(
                Recommendation(
                    name=assessment["name"],
                    url=assessment["url"]
                )
            )

        llm_reply = generate_comparison(
            user_query,
            results
        )

        return ChatResponse(
            reply=llm_reply,
            recommendations=recommendations,
            end_of_conversation=True
        )

    # -----------------------------
    # Step 5: Clarification
    # -----------------------------
    analysis = manager.analyze(history)

    if analysis["status"] == "clarify":

        return ChatResponse(
            reply=analysis["reply"],
            recommendations=[],
            end_of_conversation=False
        )

    # -----------------------------
    # Step 6: Retrieve Assessments
    # -----------------------------
    results = search(user_query, top_k=5)

    # -----------------------------
    # Step 7: Convert to Response Model
    # -----------------------------
    recommendations = []

    for assessment in results:

        recommendations.append(
            Recommendation(
                name=assessment["name"],
                url=assessment["url"]
            )
        )

    # -----------------------------
    # Step 8: Gemini Recommendation
    # -----------------------------
    llm_reply = generate_response(
        user_query,
        results
    )

    # -----------------------------
    # Step 9: Return Response
    # -----------------------------
    return ChatResponse(
        reply=llm_reply,
        recommendations=recommendations,
        end_of_conversation=True
    )