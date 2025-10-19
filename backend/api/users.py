from fastapi import APIRouter, Request
from api.mongo import cursor
from api.vectorization_service import classify
from google import genai
from google.genai import types
import os

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(agent_name: str, category: int, user_inputs: list) -> str:
    inputs_text = " ".join(user_inputs)
    
    prompt = f"""
    Based on the following user inputs and their personality category, generate a brief, engaging summary for this agent:
    
    Agent Name: {agent_name}
    Personality Category: {category}
    User Inputs: {inputs_text}
    
    Create a 2-3 sentence summary that captures their personality and interests in a spy/agent theme. Always start with "[Name], or [Agent Name] is..."
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=150
            )
        )
        return response.text.strip()
    except Exception as e:
        # Fallback summary if Gemini fails
        raise e
        return f"{agent_name} is a mysterious agent with category {category} who has shared {len(user_inputs)} insights."

user_router = APIRouter(prefix="/users", tags=["User Management"])

@user_router.get("/@me")
async def get_your_user(request: Request):
    data = await request.json()
    uuid = data.get("uuid")
    return cursor["users"].find_one({"_id": uuid})

@user_router.post("/inputs")
async def add_user_inputs(request: Request):
    data = await request.json()
    uuid = data.get("uuid")
    inputs = data.get("inputs")

    if not uuid or not inputs:
        return {"error": "uuid and inputs are required."}

    user = cursor["users"].find_one({"_id": uuid})
    if not user:
        return {"error": "User not found."}

    if "inputs" not in user:
        user["inputs"] = []

    user["inputs"].extend(inputs)
    cursor["users"].update_one({"_id": uuid}, {"$set": {"inputs": user["inputs"]}})


    # Update category based on user inputs
    category = classify(" ".join(user["inputs"]))
    cursor["users"].update_one({"_id": uuid}, {"$set": {"category": category}})

    # Generate summary using Gemini
    agent_name = user.get("agent", "Unknown Agent")
    summary = generate_summary(agent_name, category, user["inputs"])

    # Update user with generated summary
    cursor["users"].update_one({"_id": uuid}, {"$set": {"summary": summary}})


    

    return {"message": "Inputs added successfully.", "total_inputs": len(user["inputs"])}
