from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_config import SessionLocal
from models import Player, Objective

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/players/", response_model=dict)
def get_player(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    if not players:
        raise HTTPException(status_code=404, detail="Nenhum jogador encontrado.")
    return {"players": players}


@router.post("/players/", response_model=dict)
def create_player(name: str, color: str, db: Session = Depends(get_db)):
    if db.query(Player).filter(Player.color == color).first():
        raise HTTPException(status_code=400, detail="A cor já foi escolhida por outro jogador.")
    
    player = Player(name=name, color=color)
    db.add(player)
    db.commit()
    db.refresh(player)
    
    return {"id": player.id, "name": player.name, "color": player.color}

@router.post("/objectives/{player_id}", response_model=dict)
def assign_objective(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
    
    while True:
        objective = db.query(Objective).filter(Objective.assigned == False).first()
        if not objective:
            raise HTTPException(status_code=404, detail="Não há objetivos disponíveis.")
        
        if not objective.player_id:
            objective.player_id = player_id
            objective.assigned = True
            db.commit()
            db.refresh(objective)
            return {"player_id": player_id, "objective": objective.description}

