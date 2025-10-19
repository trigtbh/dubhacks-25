from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import os

from api.mongo import cursor
import random


client_kwargs={
        'scope': 'openid email profile'
    }

import fastapi

from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

base = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base, "names.txt"), "r") as f:
    NAMES = [line.strip() for line in f.readlines() if line.strip()]


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
    print(redirect_uri)
    return await google.authorize_redirect(request, redirect_uri)


@auth_router.get('/callback', name='auth_callback')
async def auth(request: Request):
    token = await google.authorize_access_token(request)
    user = token['userinfo']

    user = {
        k: v for k, v in user.items()
        if k in {"sub", "name", "email"}
    }

    user["current_mission"] = {}
    user["previous_missions"] = []

    user["uuid"] = user["sub"]
    user["_id"] = user["sub"]

    user["agent"] = "Agent " + " ".join(random.sample(NAMES, 2))

    if not cursor["users"].find_one({"sub": user["sub"]}):
        cursor["users"].insert_one(user)

    redirect_response = RedirectResponse(url=os.getenv('HOST'), status_code=303)
    redirect_response.set_cookie("userid", user["sub"])
    return redirect_response
