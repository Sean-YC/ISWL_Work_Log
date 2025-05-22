from fastapi import FastAPI
from .database import SessionLocal
from .routers import users, logs
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is working ✅"}

app.include_router(users.router)
app.include_router(logs.router)

# === TEMPORARY: Create all tables if they do not exist ===
models.Base.metadata.create_all(bind=engine)

