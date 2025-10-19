from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/challenges", tags=["challenges"], dependencies=[Depends(get_current_user)])

# ============================================================================
# Pydantic Models
# ============================================================================

class Challenge(BaseModel):
    """Challenge model for user challenges"""
    uuids: List[str] = Field(..., description="List of all user IDs participating in the challenge")
    name: str = Field(..., description="Name/title of the challenge")
    due_timestamp: str = Field(..., description="ISO timestamp for when the challenge is due")
    individual_challenges: Dict[str, str] = Field(..., description="Map of uuid -> individual challenge description")

class ChallengeRequest(BaseModel):
    """Request to create or update a challenge"""
    challenge: Challenge = Field(..., description="The challenge to create or update")

class ChallengeResponse(BaseModel):
    """Response for challenge operations"""
    challenge: Challenge
    challenge_id: str
    timestamp: str

class CreateChallengeFromUsersRequest(BaseModel):
    """Request to create a challenge from a list of users"""
    uuids: List[str] = Field(..., description="List of user IDs to include in the challenge")
    name: str = Field(..., description="Name/title of the challenge")
    due_timestamp: str = Field(..., description="ISO timestamp for when the challenge is due")

class AddChallengeRequest(BaseModel):
    """Request to add a new challenge to an existing challenge"""
    challenge_id: str = Field(..., description="ID of the challenge to add to")
    uuid: str = Field(..., description="User ID to add challenge for")
    challenge_description: str = Field(..., description="Description of the individual challenge")

# ============================================================================
# In-Memory Storage (Replace with database in production)
# ============================================================================

_challenges_store: Dict[str, Challenge] = {}

# ============================================================================
# Challenge Endpoints
# ============================================================================

@router.post("/create-from-users", response_model=ChallengeResponse)
async def create_challenge_from_users(request: CreateChallengeFromUsersRequest):
    """
    Create a new challenge from a list of users.
    Individual challenges will be generated automatically.
    """
    # TODO: Implement challenge creation from user list
    # This should:
    # 1. Validate uuids exist
    # 2. Generate individual challenges based on user profiles
    # 3. Create the challenge object
    # 4. Store it and return response

    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.post("/add-challenge", response_model=ChallengeResponse)
async def add_individual_challenge(request: AddChallengeRequest):
    """
    Add a new individual challenge to an existing challenge.
    """
    # TODO: Implement adding individual challenge
    # This should:
    # 1. Validate challenge_id exists
    # 2. Validate uuid is in the challenge
    # 3. Add/update the individual challenge
    # 4. Return updated challenge

    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.post("", response_model=ChallengeResponse)
async def create_challenge(request: ChallengeRequest):
    """
    Create a new challenge with individual challenges for each user.

    This endpoint creates a challenge with personalized challenges for each participating user.

    Args:
        request: ChallengeRequest containing the challenge details

    Returns:
        ChallengeResponse with the created challenge and ID
    """
    try:
        challenge = request.challenge

        # Validate that all uuids have individual challenges
        missing_challenges = []
        for uuid in challenge.uuids:
            if uuid not in challenge.individual_challenges:
                missing_challenges.append(uuid)

        if missing_challenges:
            raise HTTPException(
                status_code=400,
                detail=f"Missing individual challenges for users: {missing_challenges}"
            )

        # Generate a simple challenge ID
        challenge_id = f"challenge_{len(_challenges_store) + 1}_{int(datetime.now().timestamp())}"

        # Store the challenge
        _challenges_store[challenge_id] = challenge

        return ChallengeResponse(
            challenge=challenge,
            challenge_id=challenge_id,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create challenge: {str(e)}")

@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(challenge_id: str):
    """
    Retrieve a challenge by its ID.

    Args:
        challenge_id: The ID of the challenge to retrieve

    Returns:
        ChallengeResponse with the challenge details
    """
    try:
        if challenge_id not in _challenges_store:
            raise HTTPException(status_code=404, detail="Challenge not found")

        challenge = _challenges_store[challenge_id]

        return ChallengeResponse(
            challenge=challenge,
            challenge_id=challenge_id,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve challenge: {str(e)}")

@router.get("", response_model=Dict[str, Any])
async def list_challenges():
    """
    List all challenges.

    Returns:
        Dictionary with challenge IDs and their basic info
    """
    try:
        challenges_info = {}
        for challenge_id, challenge in _challenges_store.items():
            challenges_info[challenge_id] = {
                "name": challenge.name,
                "user_count": len(challenge.uuids),
                "due_timestamp": challenge.due_timestamp,
                "created_at": datetime.now().isoformat()  # In production, store creation timestamp
            }

        return {
            "challenges": challenges_info,
            "total_count": len(challenges_info),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list challenges: {str(e)}")