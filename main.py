import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()  # reads your .env file
print("KEY FOUND:", os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")
model = genai.GenerativeModel("gemini-3.6-flash")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = model.generate_content(request.message)
    return {"reply": response.text}

class Message(BaseModel):
    role: str
    content: str

class OpenAIChatRequest(BaseModel):
    messages: list[Message]

@app.post("/v1/chat/completions")
def openai_chat(request: OpenAIChatRequest):
    last_user_message = request.messages[-1].content
    response = model.generate_content(last_user_message)
    return {
        "choices": [
            {"message": {"role": "assistant", "content": response.text}}
        ]
    }