from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException, Depends
from .facade.territories_facade import TerritorieController
from sqlalchemy.orm import Session
from src.db_config import get_db

router = APIRouter()

controller = TerritorieController()

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


class TerritoryNeighborsResponse(BaseModel):
    id: int
    name: str
    neighbors: list

    class Config:
        orm_mode = True


@router.get("/")
def get_territories(db: Session = Depends(get_db)):
    return controller.get_territories(db)

@router.get("/neighbors/{territory_id}")
def get_neighbors(territory_id: int, db: Session = Depends(get_db)):
    try:
        return controller.get_neighbors(territory_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao distribuir territórios.")


@router.post("/distribute-territories/")
def distribute_territories_route(db: Session = Depends(get_db)):
    try:
        controller.distribute_territories(db)
        return {"message": "Territórios distribuídos com sucesso."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao distribuir territórios.")

@router.get("/players/", response_model=List[PlayerTerritoriesResponse])
def get_player_territories(db: Session = Depends(get_db)):
    return controller.get_player_territories(db)