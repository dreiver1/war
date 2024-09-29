from fastapi import FastAPI
from src.db_config import SessionLocal
from src.initialize_db import initialize_database

from src.router.player_route import router as player_route
from src.router.objectives_route import router as objectives_route
from src.router.territories_router import router as player_territories_router
from src.router.army_route import router as army_route

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

app.include_router(player_route, prefix="/players", tags=["Jogadores"])
app.include_router(objectives_route, prefix="/objectives", tags=["Objetivos"])
app.include_router(player_territories_router, prefix="/territories", tags=["Territórios"])
app.include_router(army_route, prefix="/army", tags=["Exercitos"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo ao jogo War!"}
