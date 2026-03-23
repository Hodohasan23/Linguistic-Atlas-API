from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv
import os

from anthropic import Anthropic
from sqlmodel import Session

from app.db.session import get_session
from app.analytics import service

load_dotenv()

router = APIRouter(prefix="/ask", tags=["Ask the Atlas"])


def get_anthropic_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY missing")
    return Anthropic(api_key=api_key)


class AskRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "How similar are Swahili and Zulu? Are they from the same family?",
            }
        }
    )
    question: str


class AskResponse(BaseModel):
    answer: str


# tools the AI can call (mapped to your backend)
TOOLS = [
    {
        "name": "get_similarity",
        "description": "Compare two languages and return similarity score.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lang1": {"type": "string"},
                "lang2": {"type": "string"},
            },
            "required": ["lang1", "lang2"],
        },
    },
    {
        "name": "compare_sets",
        "description": "Compare two language sets and return overlap statistics.",
        "input_schema": {
            "type": "object",
            "properties": {
                "set1_id": {"type": "integer"},
                "set2_id": {"type": "integer"},
            },
            "required": ["set1_id", "set2_id"],
        },
    },
]


def run_tool(tool_name: str, tool_input: dict, session: Session):
    if tool_name == "get_similarity":
        return service.get_similarity(
            session,
            tool_input["lang1"],
            tool_input["lang2"],
        )

    if tool_name == "compare_sets":
        return service.compare_language_sets(
            session,
            tool_input["set1_id"],
            tool_input["set2_id"],
        )

    raise ValueError(f"Unknown tool: {tool_name}")


@router.post("", response_model=AskResponse, summary="Ask the Atlas anything")
def ask(request: AskRequest, session: Session = Depends(get_session)):
    client = get_anthropic_client()

    system_prompt = """
You are an assistant for a Linguistic Analytics API.

Rules:
- Use tools when the question involves comparing languages or sets.
- Never invent data.
- Keep answers clear and concise.
"""

    try:
        messages = [{"role": "user", "content": request.question}]

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            system=system_prompt,
            tools=TOOLS,
            messages=messages,
        )

        while response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input, session)

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        }
                    )

            messages.append(
                {
                    "role": "assistant",
                    "content": response.content,
                }
            )

            messages.append(
                {
                    "role": "user",
                    "content": tool_results,
                }
            )

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                system=system_prompt,
                tools=TOOLS,
                messages=messages,
            )

        final_text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()

        return AskResponse(answer=final_text or "No response generated.")

    except Exception:
        q = request.question.lower()

        if "compare" in q or "similar" in q:
            words = q.split()
            ids = [w for w in words if len(w) > 6]

            if len(ids) >= 2:
                result = service.get_similarity(session, ids[0], ids[1])
                if result:
                    return AskResponse(answer=str(result))

            return AskResponse(
                answer="Try comparing two languages like: Compare guri1248 and engl1234"
            )

        if "set" in q and "compare" in q:
            return AskResponse(
                answer="Use /analytics/compare-sets with set IDs to compare language sets."
            )

        return AskResponse(
            answer="AI service unavailable, but core analytics endpoints are still working."
        )
