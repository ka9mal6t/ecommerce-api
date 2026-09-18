from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.connection.router import router as connection_router
from app.users.router import router as user_router
import app.models as models

app = FastAPI()

app.include_router(connection_router)
app.include_router(user_router)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # Cookie for front end
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"]
)


