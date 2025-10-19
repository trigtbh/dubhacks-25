import dotenv
dotenv.load_dotenv()

import fastapi
from starlette.middleware.sessions import SessionMiddleware



app = fastapi.FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

from api.auth import auth_router

app.include_router(auth_router)



@app.get("/")
async def homepage():
    return {"message": "Welcome to the homepage"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, forwarded_allow_ips="*")
