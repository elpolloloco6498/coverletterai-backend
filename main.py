from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import generation, parsing, users

origins = ["http://localhost:8080", "https://coverletterai-e2226.web.app"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation.router)
app.include_router(parsing.router)
app.include_router(users.router)



