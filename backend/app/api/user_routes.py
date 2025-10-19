from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

from app.api.vectorization_routes import UserAttributes
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["User Management"], dependencies=[Depends(get_current_user)])

# ============================================================================
# Pydantic Models
# ============================================================================

class CreateUserRequest(BaseModel):
    """Request to create a new user"""
    user_attributes: UserAttributes = Field(..., description="User attributes for the new user")

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
# In-Memory Storage (Replace with database in production)
# ============================================================================

_users_store: Dict[str, UserAttributes] = {}

# ============================================================================
# User Management Endpoints
# ============================================================================

@router.post("", response_model=CreateUserResponse)
async def create_user(request: CreateUserRequest):
    """
    Create a new user with the given attributes.

    This endpoint creates a new user and stores their attributes for future
    vectorization and clustering operations.

    Args:
        request: CreateUserRequest containing user attributes

    Returns:
        CreateUserResponse with created user information
    """
    try:
        uuid = request.user_attributes.uuid

        # Check if user already exists
        if uuid in _users_store:
            raise HTTPException(status_code=409, detail=f"User with ID '{uuid}' already exists")

        # Store the user
        _users_store[uuid] = request.user_attributes

        return CreateUserResponse(
            uuid=uuid,
            user_attributes=request.user_attributes,
            timestamp=datetime.now().isoformat(),
            message=f"User '{uuid}' created successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
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
    try:
        if uuid not in _users_store:
            raise HTTPException(status_code=404, detail=f"User with ID '{uuid}' not found")

        return GetUserResponse(
            uuid=uuid,
            user_attributes=_users_store[uuid],
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
        users = list(_users_store.values())

        return ListUsersResponse(
            users=users,
            total_count=len(users),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list users: {str(e)}")