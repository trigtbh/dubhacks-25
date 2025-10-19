from fastapi import APIRouter, Request
from api.mongo import cursor



user_router = APIRouter(prefix="/users", tags=["User Management"])


