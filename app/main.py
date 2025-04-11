"""Starting point of the application"""
from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.database import engine, get_db
from app import models
from app.routers import organizations, contacts
from app.seed import seed_data
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
    "https://pingcrm-clone-react-app.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organizations.router)
app.include_router(contacts.router)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    seed_data(db)
