from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_config import SessionLocal
from models import  Objective
from pydantic import BaseModel
from typing import List, Optional


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ObjectiveResponse(BaseModel):
    id: int
    description: str
    player_id: Optional[int] = None  # Pode ser None
    assigned: Optional[bool] = None

    class Config:
        orm_mode = True


@router.get("/objectives/", response_model=List[ObjectiveResponse])
def get_objectives(db: Session = Depends(get_db)):
    objectives = db.query(Objective).all()
    if not objectives:
        raise HTTPException(status_code=404, detail="Nenhum objetivo encontrado.")
    return objectives