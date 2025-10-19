from fastapi import APIRouter, UploadFile, File, HTTPException
from api.mongo import cursor

lb_router = APIRouter(prefix="/leaderboard", tags=["Leaderboard Management"])

@lb_router.get("/top-10")
async def get_top_10():
    user_data = cursor["users"].find({}, {"_id": 1, "previous_missions": 1}).sort("score", -1).limit(10)

    return list(user_data)


@lb_router.get("/placement/{user_id}")
async def get_user_placement(user_id: str):
    user = cursor["users"].find_one({"_id": user_id}, {"score": 1})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_score = user.get("score", 0)
    placement = cursor["users"].count_documents({"score": {"$gt": user_score}}) + 1

    return {"user_id": user_id, "placement": placement}
