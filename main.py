from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import generation, parsing, users, payment, letters, resumes

origins = ["*"]

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["filename"],
)

app.include_router(generation.router)
app.include_router(parsing.router)
app.include_router(users.router)
app.include_router(payment.router)
app.include_router(letters.router)
app.include_router(resumes.router)



