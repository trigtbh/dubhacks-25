import dotenv
dotenv.load_dotenv()

import fastapi
from starlette.middleware.sessions import SessionMiddleware
import asyncio
import traceback

app = fastapi.FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

from api.auth import auth_router
from api.users import user_router
from api.photos import photo_router
from api.leaderboard import lb_router
from api.challenges import challenges_router
from api.challenges import create_all_challenges

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(photo_router)
app.include_router(lb_router)
app.include_router(challenges_router)

@app.get("/")
async def homepage():
    return {"message": "Welcome to the homepage"}


async def _periodic_challenge_creator():
    """Background task that calls create_all_challenges every 15 minutes."""
    while True:
        try:
            await create_all_challenges()
        except asyncio.CancelledError:
            raise
        except Exception as e:
            # don't crash the background task; log and continue
            print("Error running create_all_challenges:")
            traceback.print_exc()
        await asyncio.sleep(15*60)

@app.on_event("startup")
async def _start_background_tasks():
    # schedule background periodic creation
    asyncio.create_task(_periodic_challenge_creator())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, forwarded_allow_ips="*")
