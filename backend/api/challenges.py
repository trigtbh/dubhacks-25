import json
import os
import random
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from api.mongo import cursor
from uuid import uuid4

OPERATIONS = [
  "Operation Centerstage",
  "Operation Uplift",
  "Operation Flat World",
  "Operation Grin Keeper",
  "Operation Sustenance",
  "Operation Point Zero",
  "Operation Passageway",
  "Operation Wisdom Gate",
  "Operation Color Code",
  "Operation Terminus"
]

challenges_router = APIRouter(prefix="/challenges", tags=["Challenge Management"])

base = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base, "actions.txt"), "r") as f:
    ACTIONS = [line.strip() for line in f.readlines() if line.strip()]

with open(os.path.join(base, "locations.json"), "r") as f:
    LOCATIONS = json.load(f)

@challenges_router.post("/create")
async def create_all_challenges():
    clusters = {}
    
    for user in cursor["users"].find({}, {"_id": 1, "category": 1}):
        category = user.get("category", "Uncategorized")
        if category not in clusters:
            clusters[category] = set()
        clusters[category].add(user["_id"])

    for category, users in clusters.items():
        challenge_id = str(uuid4())

        c_index = random.randint(0, len(LOCATIONS.items()) - 1)
        print(LOCATIONS, c_index)
        challenge = {
            "challenge_id": challenge_id,
            "category": category,
            "participants": list(users),
            "status": "active",
            "riddle": list(LOCATIONS.items())[c_index][1],
            "action": random.choice(ACTIONS),
            "challenge_name": OPERATIONS[c_index],
            "expiration": time.time() + 600
        }
        cursor["challenges"].insert_one(challenge)

        numbers = set()
        while len(numbers) < len(users):
            numbers.add(random.randint(100, 999))
        numbers = list(numbers)


        for i, user_id in enumerate(users):

            target_user = cursor["users"].find_one({"_id": list(users)[(i + 1) % len(users)]})

            cursor["users"].update_one(
                {"_id": user_id},
                {"$set": {
                    "current_mission": {
                        "challenge_id": challenge_id,
                        "riddle": challenge["riddle"],
                        "action": challenge["action"],
                        "challenge_name": challenge["challenge_name"],
                        "code_offered": numbers[i],
                        "code_needed": numbers[(i + 1) % len(users)],
                        "agent_needed": target_user["agent"],
                        "assigned_at": time()
                    }
                }}
            )


@challenges_router.post("/claim")
async def claim_challenge(body: dict):
    """Claim a challenge by providing your uuid and the code to claim.

    Expected body: { "uuid": "user-id", "code": 123 }

    If the provided code matches the user's current_mission.code_needed,
    remove the current_mission and append the challenge_id to previous_missions.
    """
    # basic validation
    uuid = body.get("uuid")
    code = body.get("code")
    if not uuid or code is None:
        raise HTTPException(status_code=400, detail="uuid and code are required")

    # fetch user
    user = cursor["users"].find_one({"_id": uuid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current = user.get("current_mission")
    if not current:
        raise HTTPException(status_code=400, detail="No active mission for user")

    # prevent claiming if more than 2 minutes (120 seconds) have passed since assignment
    assigned_at = current.get("assigned_at")
    if assigned_at is not None:
        try:
            assigned_at_val = float(assigned_at)
        except Exception:
            assigned_at_val = None

        if assigned_at_val is not None:
            if time() - assigned_at_val > 120:
                raise HTTPException(status_code=400, detail="Claim window expired")

    # code_needed may be stored as int or string; compare loosely
    code_needed = current.get("code_needed")
    try:
        if int(code_needed) != int(code):
            raise HTTPException(status_code=400, detail="Incorrect code")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid code format")

    challenge_id = current.get("challenge_name")

    # update user: unset current_mission and push to previous_missions
    update_result = cursor["users"].update_one(
        {"_id": uuid},
        {
            "$unset": {"current_mission": ""},
            "$push": {"previous_missions": challenge_id}
        }
    )

    if update_result.modified_count == 0:
        # fallback: still consider success but inform
        return {"status": "ok", "message": "Code matched but user record not modified"}

    return {"status": "ok", "message": "Challenge claimed", "challenge_id": challenge_id}
