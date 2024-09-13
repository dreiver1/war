from pydantic import BaseModel
from typing import List, Optional, Dict
from models import Player, Territory
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_config import SessionLocal
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TerritoryBase(BaseModel):
    id: int
    name: str
    region: Optional[str] = None

class PlayerTerritoriesResponse(BaseModel):
    player_id: int
    player_name: str
    color: str
    territories: List[TerritoryBase]

    class Config:
        orm_mode = True


class TerritoryBase(BaseModel):
    id: int
    name: str
    region: Optional[str] = None

class PlayerTerritoriesResponse(BaseModel):
    player_id: int
    player_name: str
    color: str
    territories: List[TerritoryBase]

territories = [
    {"id": 1, "name": "Acre", "region": "Norte"},
    {"id": 2, "name": "Alagoas", "region": "Nordeste"},
    {"id": 3, "name": "Amazonas", "region": "Norte"},
    {"id": 4, "name": "Bahia", "region": "Nordeste"},
    {"id": 5, "name": "Ceará", "region": "Nordeste"},
    {"id": 6, "name": "Distrito Federal", "region": "Centro-Oeste"},
    {"id": 7, "name": "Espírito Santo", "region": "Sudeste"},
    {"id": 8, "name": "Goiás", "region": "Centro-Oeste"},
    {"id": 9, "name": "Maranhão", "region": "Nordeste"},
    {"id": 10, "name": "Mato Grosso", "region": "Centro-Oeste"},
    {"id": 11, "name": "Mato Grosso do Sul", "region": "Centro-Oeste"},
    {"id": 12, "name": "Minas Gerais", "region": "Sudeste"},
    {"id": 13, "name": "Pará", "region": "Norte"},
    {"id": 14, "name": "Paraíba", "region": "Nordeste"},
    {"id": 15, "name": "Paraná", "region": "Sul"},
    {"id": 16, "name": "Pernambuco", "region": "Nordeste"},
    {"id": 17, "name": "Piauí", "region": "Nordeste"},
    {"id": 18, "name": "Rio de Janeiro", "region": "Sudeste"},
    {"id": 19, "name": "Rio Grande do Norte", "region": "Nordeste"},
    {"id": 20, "name": "Rio Grande do Sul", "region": "Sul"},
    {"id": 21, "name": "Rondônia", "region": "Norte"},
    {"id": 22, "name": "Roraima", "region": "Norte"},
    {"id": 23, "name": "Santa Catarina", "region": "Sul"},
    {"id": 24, "name": "São Paulo", "region": "Sudeste"},
    {"id": 25, "name": "Sergipe", "region": "Nordeste"},
    {"id": 26, "name": "Tocantins", "region": "Norte"}
]

neighbors = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 5],
    4: [2, 6],
    5: [3, 7],
    6: [4, 8],
    7: [5, 9],
    8: [6, 10],
    9: [7, 11],
    10: [8, 12],
    11: [9, 13],
    12: [10, 14],
    13: [11, 15],
    14: [12, 16],
    15: [13, 17],
    16: [14, 18],
    17: [15, 19],
    18: [16, 20],
    19: [17, 21],
    20: [18, 22],
    21: [19, 23],
    22: [20, 24],
    23: [21, 25],
    24: [22, 26],
    25: [23, 27],
    26: [24, 28]
}

@router.get("/territories", response_model=List[Dict[str, str]])
def get_territories():
    return territories

@router.get("/territories/{territory_id}/neighbors")
def get_neighbors(territory_id: int):
    territory = next((t for t in territories if t["id"] == territory_id), None)
    if not territory:
        raise HTTPException(status_code=404, detail="Território não encontrado")

    neighbor_ids = neighbors.get(territory_id, [])
    neighbor_territories = [t for t in territories if t["id"] in neighbor_ids]
    return {"territory": territory, "neighbors": neighbor_territories}



def distribute_territories(db: Session):
    players = db.query(Player).all()
    territories = db.query(Territory).all()
    
    if not players:
        raise ValueError("Nenhum jogador encontrado.")
    if not territories:
        raise ValueError("Nenhum território encontrado.")
    
    random.shuffle(territories)
    
    num_players = len(players)
    for idx, territory in enumerate(territories):
        player = players[idx % num_players] 
        territory.owner_id = player.id
    
    db.commit()


@router.post("/distribute-territories/")
def distribute_territories_route(db: Session = Depends(get_db)):
    try:
        distribute_territories(db)
        return {"message": "Territórios distribuídos com sucesso."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao distribuir territórios.")

@router.get("/players/territories/", response_model=List[PlayerTerritoriesResponse])
def get_player_territories(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    
    if not players:
        raise HTTPException(status_code=404, detail="Nenhum jogador encontrado.")
    
    player_territories = []
    for player in players:
        territories = db.query(Territory).filter(Territory.owner_id == player.id).all()
        player_territories.append({
            "player_id": player.id,
            "player_name": player.name,
            "color": player.color,
            "territories": [{"id": t.id, "name": t.name, "region": t.region} for t in territories]
        })
    
    return player_territories


