from fastapi import APIRouter, Request, Response, HTTPException, status
from authlib.integrations.starlette_client import OAuth
from app.config import settings
from starlette.responses import RedirectResponse
import json

# --- Session Management for Authlib ---
def parse_user(token):
    return {
        "user_id": token["sub"],
        "first_name": token["userinfo"]["given_name"],
        "family_name": token["userinfo"]["family_name"],
        "email": token["userinfo"]["email"],
        "pfp": token["userinfo"]["picture"]
        }


router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/google/login")
async def google_login(request: Request):
    """Initiates the Google OAuth login flow."""
    if not settings.google_sso_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google SSO is not configured."
        )
    try:
        redirect_uri = settings.google_redirect_uri
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initiate Google login: {str(e)}"
            )

@router.get("/google/callback")
async def google_callback(request: Request):
    """Handles the Google OAuth callback."""
    if not settings.google_sso_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google SSO is not configured."
        )
    try:
        token = await oauth.google.authorize_access_token(request)
        request.session["user"] = parse_user(token)

        response = RedirectResponse(url="/")
        return response
    
    except HTTPException:
        raise # Re-raise explicit HTTPExceptions
    except Exception as e:
        # Log the error for debugging
        print(f"Google OAuth callback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google login failed: {str(e)}"
        )
    
@router.get("/logout")
async def logout(request: Request):
    """Logs out the user by clearing the session."""
    request.session.pop("user", None)
    return {"message": "Logged out successfully"}

@router.get("/me")
async def read_current_user(request: Request):
    """Returns the currently logged-in user's information from the session."""
    user = request.session.get("user")
    if user:
        return {"user": user}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
