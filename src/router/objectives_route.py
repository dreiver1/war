from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db_config import get_db
from pydantic import BaseModel
from typing import List, Optional
from src.router.facade.objective_facade import objectiveController

controller = objectiveController()
router = APIRouter()

class ObjectiveResponse(BaseModel):
    id: int
    description: str
    player_id: Optional[int] = None 
    assigned: Optional[bool] = None

    class Config:
        orm_mode = True


@router.get("/", response_model=List[ObjectiveResponse])
def get_objectives(db: Session = Depends(get_db)):
    return controller.get_objectives(db)

@router.post("/{player_id}", response_model=dict)
def assign_objective(player_id: int, db: Session = Depends(get_db)):
    return controller.assign_objective(player_id, db)

@router.get("/{player_id}")
def get_player_objective(player_id: int, db: Session = Depends(get_db)):
    return controller.get_player_objective(player_id, db)

@router.get('/verify/{player_id}')
def verify_objective(player_id: int, db: Session = Depends(get_db)):
    return controller.verify_objective(player_id, db)
