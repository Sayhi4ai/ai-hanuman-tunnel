from fastapi import APIRouter
from pydantic import BaseModel
from openclaw.tool_registry import TOOLS
from openclaw.guardian import guardian

router = APIRouter()

class ChatRequest(BaseModel):
    agent: str
    messages: list
    tool_choice: str | None = None

@router.post("/chat")
def chat(req: ChatRequest):
    # Simple echo-style agent for now
    last_user_message = req.messages[-1]["content"]

    # Guardian input validation
    ok, err = guardian.validate_input(req.agent, last_user_message)
    if not ok:
        return {"type": "error", "message": err}

    # If tool_choice is provided, run the tool
    if req.tool_choice and req.tool_choice in TOOLS:
        result = TOOLS[req.tool_choice]["run"](text=last_user_message)

        # Guardian output validation
        ok, err = guardian.validate_output(req.agent, str(result))
        if not ok:
            return {"type": "error", "message": err}

        return {
            "type": "tool_result",
            "tool": req.tool_choice,
            "result": result
        }

    # Normal chat response
    response = f"Agent {req.agent} says: {last_user_message}"

    # Guardian output validation
    ok, err = guardian.validate_output(req.agent, response)
    if not ok:
        return {"type": "error", "message": err}

    return {
        "type": "message",
        "content": response
    }
