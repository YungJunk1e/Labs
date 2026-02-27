import os
import time
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import SessionLocal, engine
from models import Base, Item

load_dotenv()

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

APP_VERSION = os.getenv("APP_VERSION", "unknown")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/default")
def root():
    return {"message": "DevOps test app running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": APP_VERSION}


@app.post("/items")
def create_item(name: str, db: Session = Depends(get_db)):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/load")
def simulate_load(delay: int = 2):
    time.sleep(delay)
    return {"message": f"Simulated {delay}s delay"}


# 👇 ВАЖНО: точка входа
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="192.168.1.102",
        port=8000,
        reload=False
    )
