from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db_config import get_db
from src.router.facade.player_facade import PlayerController

router = APIRouter()
controller = PlayerController()

class PlayerCreate(BaseModel):
    name: str
    color: str

@router.get("/", response_model=dict)
def get_player(db: Session = Depends(get_db)):
    return controller.get_player(db)

@router.post("/", response_model=dict)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    return controller.create_player(player.name, player.color, db)

@router.post("/attack", response_model=dict)
def attack(attacker_id: int, attacker_territory_id: str, defender_territory_id: str, db: Session = Depends(get_db)):
    return controller.attack_territory(db, attacker_id, attacker_territory_id, defender_territory_id)
@router.get('/new_round')
def new_round(db: Session = Depends(get_db)):
    return controller.new_round(db)