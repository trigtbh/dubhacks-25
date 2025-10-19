from fastapi import APIRouter, Request
import os


client_kwargs={
        'scope': 'openid email profile'
    }

import fastapi

from authlib.integrations.starlette_client import OAuth

oauth = OAuth()


oauth.register(
    name='google',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    server_metadata_url=os.getenv("SERVER_METADATA_URL"),
    client_kwargs=client_kwargs,
)

google = oauth.create_client('google')



auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await google.authorize_redirect(request, redirect_uri)


@auth_router.get('/callback', name='auth_callback')
async def auth(request: Request):
    token = await google.authorize_access_token(request)
    user = token['userinfo']
    return user
