import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel
import json

def check_pricing(plan: str):
    """Get pricing details for a plan.

    Args:
        plan: The name of the plan (basic, pro, or enterprise)
    """
    with open("pricing.json") as f:
        pricing = json.load(f)
    plan = plan.lower()
    if plan in pricing:
        return pricing[plan]
    return {"error": f"No plan named '{plan}' found"}

def escalate_to_human(reason: str, summary: str):
    """Escalate the conversation to a human when the AI can't help further.

    Args:
        reason: why this needs a human (e.g. 'angry customer', 'complex custom pricing')
        summary: a short summary of the conversation so far, for the human to read
    """
    with open("leads.json") as f:
        leads = json.load(f)
    leads.append({"reason": reason, "summary": summary})
    with open("leads.json", "w") as f:
        json.dump(leads, f, indent=2)
    return {"status": "escalated", "message": "A team member will follow up shortly."}

def update_confidence(field: str):
    """Mark a qualification field as confirmed during the conversation.

    Args:
        field: one of 'budget', 'team_size', 'timeline', 'authority'
    """
    if field in confidence_state:
        confidence_state[field] = True
        return {"status": "updated", "field": field}
    return {"error": f"Unknown field '{field}'"}

load_dotenv()
print("KEY FOUND:", os.getenv("GEMINI_API_KEY"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

confidence_state = {
    "budget": False,
    "team_size": False,
    "timeline": False,
    "authority": False
}

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=request.message,
        config=types.GenerateContentConfig(tools=[check_pricing, escalate_to_human, update_confidence]),
    )
    return {"reply": response.text}

def build_gemini_history(messages: list["Message"]):
    gemini_contents = []
    for msg in messages:
        if msg.role == "system":
            continue
        role = "model" if msg.role == "assistant" else "user"
        gemini_contents.append(
            types.Content(role=role, parts=[types.Part(text=msg.content)])
        )
    return gemini_contents

class Message(BaseModel):
    role: str
    content: str

class OpenAIChatRequest(BaseModel):
    messages: list[Message]

@app.post("/v1/chat/completions")
def openai_chat(request: OpenAIChatRequest):
    gemini_contents = build_gemini_history(request.messages)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=gemini_contents,
        config=types.GenerateContentConfig(tools=[check_pricing, escalate_to_human, update_confidence]),
    )
    return {
        "choices": [
            {"message": {"role": "assistant", "content": response.text}}
        ]
    }

@app.get("/score")
def get_score():
    filled = sum(confidence_state.values())
    total = len(confidence_state)
    return {
        "budget": confidence_state["budget"],
        "teamSize": confidence_state["team_size"],
        "timeline": confidence_state["timeline"],
        "authority": confidence_state["authority"],
        "score": filled / total
    }