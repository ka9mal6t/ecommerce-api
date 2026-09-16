from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.connection.router import router as connection_router

app = FastAPI()

app.include_router(connection_router)


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


