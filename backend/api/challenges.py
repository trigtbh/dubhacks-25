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

with open(os.path.join(base, "words.txt"), "r") as f:
    WORDS = [line.strip() for line in f.readlines() if line.strip()]

@challenges_router.post("/create")
async def create_all_challenges():
    # First, set all currently active challenges to inactive
    cursor["challenges"].update_many(
        {"status": "active"},
        {"$set": {"status": "inactive"}}
    )
    
    # Clear current_mission for all users
    cursor["users"].update_many(
        {},
        {"$set": {"current_mission": {}}}
    )
    
    # Now build clusters
    clusters = {}
    
    for user in cursor["users"].find({}, {"_id": 1, "category": 1}):
        category = user.get("category", "Uncategorized")
        if category == "Uncategorized": continue
        if category not in clusters:
            clusters[category] = set()
        clusters[category].add(user["_id"])

    print(clusters)


    for category, users in clusters.items():
        challenge_id = str(uuid4())
        if len(users) < 2: continue

        c_index = random.randint(0, len(LOCATIONS.items()) - 1)
        #print(LOCATIONS, c_index)
        challenge = {
            "_id": challenge_id,
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

        # Assign each user a unique random word
        assigned_words = random.sample(WORDS, len(users))

        for i, user_id in enumerate(users):
            cursor["users"].update_one(
                {"_id": user_id},
                {"$set": {
                    "current_mission": {
                        "challenge_id": challenge_id,
                        "riddle": challenge["riddle"],
                        "action": challenge["action"],
                        "challenge_name": challenge["challenge_name"],
                        "secret_word": assigned_words[i],
                        "assigned_at": time.time()
                    }
                }}
            )


@challenges_router.post("/claim")
async def claim_challenge(body: dict):
    """Claim a challenge by providing your uuid and secret words for ALL agents in the challenge.

    Expected body: { 
        "uuid": "user-id", 
        "codes": {
            "agent_name_1": "secret_word_1",
            "agent_name_2": "secret_word_2",
            ...
        }
    }

    All users in the cluster must contribute their respective secret words to complete the challenge.
    """
    # basic validation
    uuid = body.get("uuid")
    codes = body.get("codes")
    if not uuid or not codes:
        raise HTTPException(status_code=400, detail="uuid and codes are required")
    
    if not isinstance(codes, dict):
        raise HTTPException(status_code=400, detail="codes must be a dictionary")

    # fetch user
    user = cursor["users"].find_one({"_id": uuid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current = user.get("current_mission")
    if not current:
        raise HTTPException(status_code=400, detail="No active mission for user")

    # prevent claiming if more than 5 minutes (300 seconds) have passed since assignment
    assigned_at = current.get("assigned_at")
    if assigned_at is not None:
        try:
            assigned_at_val = float(assigned_at)
        except Exception:
            assigned_at_val = None

        if assigned_at_val is not None:
            if time.time() - assigned_at_val > 300:
                raise HTTPException(status_code=400, detail="Claim window expired")

    # Validate all agent codes
    challenge_id = current.get("challenge_id")
    if not challenge_id:
        raise HTTPException(status_code=400, detail="No challenge_id in current mission")
    
    # Get the challenge to find all participants
    challenge = cursor["challenges"].find_one({"challenge_id": challenge_id})
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Get all participants in the challenge
    participants = challenge.get("participants", [])
    
    # Get all agents in the challenge with their secret words
    all_agents = {}
    for participant_id in participants:
        participant = cursor["users"].find_one({"_id": participant_id})
        if participant:
            agent_name = participant.get("agent")
            participant_mission = participant.get("current_mission", {})
            secret_word = participant_mission.get("secret_word")
            if agent_name and secret_word:
                all_agents[agent_name] = secret_word
    
    # Check if all agents' words are provided (excluding the claiming user)
    claiming_user_agent = user.get("agent")
    required_agents = {agent: word for agent, word in all_agents.items() if agent != claiming_user_agent}
    
    if len(codes) != len(required_agents):
        raise HTTPException(
            status_code=400,
            detail=f"Must provide secret words for all {len(required_agents)} other agents in the challenge"
        )
    
    # Verify each provided code against the corresponding agent's secret word
    for agent_name, provided_word in codes.items():
        if agent_name not in required_agents:
            raise HTTPException(
                status_code=400, 
                detail=f"Agent '{agent_name}' is not part of this challenge or is the claiming user"
            )
        
        expected_word = required_agents[agent_name]
        
        # Compare the words (case-insensitive)
        if provided_word.lower() != expected_word.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Incorrect secret word for agent '{agent_name}'"
            )
    
    challenge_name = current.get("challenge_name")

    # update user: unset current_mission and push to previous_missions
    update_result = cursor["users"].update_one(
        {"_id": uuid},
        {
            "$unset": {"current_mission": ""},
            "$push": {"previous_missions": challenge_name}
        }
    )

    if update_result.modified_count == 0:
        # fallback: still consider success but inform
        return {"status": "ok", "message": "All secret words matched but user record not modified"}

    return {
        "status": "ok", 
        "message": "Challenge claimed", 
        "challenge_id": challenge_name,
        "agents_verified": list(codes.keys())
    }
