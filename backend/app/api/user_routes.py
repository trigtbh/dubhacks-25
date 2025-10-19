from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

from app.api.auth_routes import parse_user
from app.api.user_schemas import UserAttributes
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["User Management"], dependencies=[Depends(get_current_user)])

from app.api.mongo import cursor

# ============================================================================
# Pydantic Models
# ============================================================================

class CreateUserResponse(BaseModel):
    """Response for user creation"""
    uuid: str
    user_attributes: UserAttributes
    timestamp: str
    message: str

class GetUserResponse(BaseModel):
    """Response for getting a user"""
    uuid: str
    user_attributes: UserAttributes
    timestamp: str

class ListUsersResponse(BaseModel):
    """Response for listing all users"""
    users: List[UserAttributes]
    total_count: int
    timestamp: str



# ============================================================================
# User Management Endpoints
# ============================================================================
import os

base = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base, "names.txt"), "r") as f:
    AAAAA, BBBBB, CCCCC = f.read().split("\n\n")
    a = AAAAA.split("\n")
    b = BBBBB.split("\n")
    c = CCCCC.split("\n")

    a = [name.title() for name in a if name.strip()]
    b = [name.title() for name in b if name.strip()]
    c = [name.title() for name in c if name.strip()]

import random

def generate_agent_name():
    n = random.choice(a) + " " + random.choice(b) + "-" + random.choice(c)
    while cursor["users"].find_one({"agent": n}):
        n = random.choice(a) + " " + random.choice(b) + "-" + random.choice(c)
    return n

@router.get("/whoami")
async def whoami(request: Request):
    return request.session.get("user")




@router.post("/create", response_model=CreateUserResponse)
async def create_user(request: UserAttributes):
    """
    Create a new user with the given attributes.

    This endpoint creates a new user and stores their attributes for future
    vectorization and clustering operations.

    Args:
        request: CreateUserRequest containing user attributes

    Returns:
        CreateUserResponse with created user information
    """
    print(cursor)
    try:
        uuid = request.uuid

        # Check if user already exists
        print(cursor)
        # if uuid in _users_store:
        if cursor["users"].find_one({"_id": uuid}):
            raise HTTPException(status_code=409, detail=f"User with ID '{uuid}' already exists")

        


        # Store the user
        # _users_store[uuid] = request.user_attributes
        user_dict = {
            "uuid": uuid,
            "_id": uuid,
            "specialty": request.specialty,
            "fields": request.fields,
            "interests_and_hobbies": request.interests_and_hobbies,
            "vibe": request.vibe,
            "comfort": request.comfort,
            "availability": request.availability,
            "name": request.name,
            "handle": request.handle,
            "agent": generate_agent_name()
        }

        cursor["users"].insert_one(user_dict)

        return CreateUserResponse(
            uuid=uuid,
            user_attributes=user_dict,
            timestamp=datetime.now().isoformat(),
            message=f"User '{uuid}' created successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise e
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


@router.get("/{uuid}", response_model=GetUserResponse)
async def get_user(uuid: str):
    """
    Get a specific user by their ID.

    Args:
        uuid: The ID of the user to retrieve

    Returns:
        GetUserResponse with user information
    """
    print(cursor)
    try:
        if not cursor["users"].find_one({"_id": uuid}):
            raise HTTPException(status_code=404, detail=f"User with ID '{uuid}' not found")

        return GetUserResponse(
            uuid=uuid,
            user_attributes=cursor["users"].find_one({"_id": uuid}),
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")


@router.get("", response_model=ListUsersResponse)
async def list_users():
    """
    List all users in the system.

    Returns:
        ListUsersResponse with all users
    """
    try:
        users = list(cursor["users"].find_many({}))

        return ListUsersResponse(
            users=users,
            total_count=len(users),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list users: {str(e)}")