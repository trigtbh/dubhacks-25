from fastapi import APIRouter, Request
from api.mongo import cursor
from api.vectorization_service import classify

user_router = APIRouter(prefix="/users", tags=["User Management"])

@user_router.get("/{uuid}")
async def get_your_user(uuid: str, request: Request):
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


    cursor["users"].update_one({"_id": uuid}, {"$set": {"category": classify(" ".join(user["inputs"]))}})

    return {"message": "Inputs added successfully.", "total_inputs": len(user["inputs"])}
