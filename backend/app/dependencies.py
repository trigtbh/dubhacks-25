from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

async def get_current_user(request: Request) -> dict:
    """
    Dependency to get the current authenticated user from session.

    Args:
        request: The FastAPI request object

    Returns:
        User information from session

    Raises:
        HTTPException: If user is not authenticated
    """
    print(request.session)
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Optional user dependency for endpoints that work with or without auth
async def get_current_user_optional(request: Request) -> Optional[dict]:
    """
    Optional dependency to get the current user if authenticated.

    Args:
        request: The FastAPI request object

    Returns:
        User information from session or None if not authenticated
    """
    print(request.session)
    return request.session.get("user")