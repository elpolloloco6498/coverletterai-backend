from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import generation, parsing, users

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation.router)
app.include_router(parsing.router)
app.include_router(users.router)



