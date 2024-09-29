from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db_config import get_db
from .facade.army_facade import ArmyController

router = APIRouter()
controller = ArmyController()

@router.post("/distribute/")
def distribute_armies_for_all_players(db: Session = Depends(get_db)):
    return controller.distribute_armies_for_all_players(db)

@router.get('player/{player_id}')
def get_player_armies(player_id, db: Session = Depends(get_db)):
    return controller.get_player_armies(db, player_id)

@router.put("/move/")
def move_army(fromTerritory: int, toTerritory: int, player_id: int, db: Session = Depends(get_db)):
    return controller.move_army(db, fromTerritory, toTerritory, player_id)



