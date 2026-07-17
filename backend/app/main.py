from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.databases.database import Base, engine
from app.api.transactions import router as transactions

from app.config import settings

app = FastAPI()

origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions)

@app.get("/")
def home():
    return {"message": "Finance Tracker API"}