SYSTEM_PROMPT = """
You are Sentaur AI — a calm, highly intelligent assistant.
You think step-by-step, explain your reasoning clearly, and avoid mistakes.
You never guess; you analyze.
You keep answers concise but insightful.
You maintain context from the conversation.
"""

from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from .database import Base, engine, get_db, SessionLocal
from .auth import router as auth_router, get_current_user
from .ai import chat_with_centaur
from .tools import get_due_reminders, mark_reminder_sent, send_email
from pydantic import BaseModel

# Create DB tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Session middleware (required for OAuth)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET", "dev-secret"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routes
app.include_router(auth_router)

# Chat request/response models
class ChatIn(BaseModel):
    message: str

class ChatOut(BaseModel):
    response: str

# Chat endpoint
@app.post("/chat", response_model=ChatOut)
def chat(req: ChatIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    answer = chat_with_centaur(db, user, req.message)
    return ChatOut(response=answer)

# Reminder scheduler job
def reminder_job():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        due = get_due_reminders(db, now)
        for r in due:
            if r.user and r.user.email:
                send_email(
                    to_email=r.user.email,
                    subject="Sentaur reminder",
                    body=r.text,
                )
            mark_reminder_sent(db, r)
    finally:
        db.close()

# Start scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(reminder_job, "interval", minutes=1)
scheduler.start()

# Serve frontend static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")