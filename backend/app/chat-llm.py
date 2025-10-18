from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, List, Any
from google import genai
from google.genai import types

import os

# ---------- CONFIG ----------
model_name = "gemini-2.5-flash"  # @param ["gemini-2.5-flash-lite", "gemini-2.5-flash-lite-preview-09-2025", "gemini-2.5-flash", "gemini-2.5-flash-preview-09-2025", "gemini-2.5-pro"] {"allow-input":true}

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="Mission Control Onboarding API")

# ---------- MODELS ----------
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    interests_logged: List[str] = []

# ---------- MEMORY STORE ----------
user_sessions: Dict[str, List[Dict[str, Any]]] = {}

# ---------- FUNCTION: log_interest ----------
def log_interest(interest_summary: str):
    """
    Record user interests, hobbies, or traits as structured intel 
    """
    print(f"[INTEL LOGGED] {interest_summary}")
    return interest_summary


# ---------- GEMINI SETUP ----------
system_prompt = """
### SYSTEM PROMPT — “Mission Control Onboarding AI”

You are MISSION CONTROL, the AI operator for a covert organization known only as The Network.
[... full prompt from user here ...]
"""

model_name = "gemini-2.5-flash"  # @param ["gemini-2.5-flash-lite", "gemini-2.5-flash-lite-preview-09-2025", "gemini-2.5-flash", "gemini-2.5-flash-preview-09-2025", "gemini-2.5-pro"] {"allow-input":true}

chat = client.chats.create(
    model=model_name,
    config=types.GenerateContentConfig(
        tools=[log_interest],
        system_instruction=COFFEE_BOT_PROMPT,
    ),
)

# ---------- MAIN ENDPOINT ----------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    user_id = req.user_id
    message = req.message

    # Initialize conversation if new
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    # Add user message
    user_sessions[user_id].append({"role": "user", "content": message})

    # Generate response from Gemini
    chat = model.start_chat(history=user_sessions[user_id])
    response = chat.send_message(message)

    # Handle possible function calls
    interests_logged = []
    for part in response.candidates[0].content.parts:
        if part.function_call:
            fn_name = part.function_call.name
            fn_args = part.function_call.args
            if fn_name == "log_interest":
                logged = log_interest(fn_args.get("interest_summary", ""))
                interests_logged.append(logged)

    # Extract final model text
    text = ""
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text"):
            text += part.text + "\n"

    # Append assistant reply to history
    user_sessions[user_id].append({"role": "assistant", "content": text.strip()})

    return ChatResponse(response=text.strip(), interests_logged=interests_logged)
