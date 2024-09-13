from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db_config import SessionLocal
from models import Player, Objective
from initialize_db import initialize_database

from router.player_route import router as player_route
from router.objectives_route import router as objectives_route
from router.player_territories_router import router as player_territories_router
from router.army_route import router as army_route

app = FastAPI(
    title="Jogo War API",
    description="API para gerenciar o jogo War, incluindo jogadores, objetivos e territórios.",
    version="1.0.0",
)

initialize_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(objectives_route, prefix="/objectives", tags=["Objetivos"])
app.include_router(player_route, prefix="/players", tags=["Jogadores"])
app.include_router(player_territories_router, prefix="/player-territories", tags=["Territórios dos Jogadores"])
app.include_router(army_route, prefix="/army", tags=["Exercito e Ataque"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo ao jogo War!"}
