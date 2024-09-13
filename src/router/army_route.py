from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Army, Player, Territory, TerritoryNeighbor
from pydantic import BaseModel
from db_config import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/distribute_armies/")
async def distribute_armies_for_all_players(db: Session = Depends(get_db)):
    players = db.query(Player).all()

    if not players:
        raise HTTPException(status_code=404, detail="No players found")

    for player in players:
        territories = db.query(Territory).filter(Territory.owner_id == player.id).all()
        
        for territory in territories:
            army = Army(territory_id=territory.id, player_id=player.id)
            db.add(army)

    db.commit()
    return {"message": "Armies distributed to all territories for all players"}



@router.put("/armies/{army_id}/move/")
def move_army(army_id: int, new_territory_id: int, db: Session = Depends(get_db)):
    army = db.query(Army).filter(Army.id == army_id).first()
    new_territory = db.query(Territory).filter(Territory.id == new_territory_id).first()
    if not army:
        raise HTTPException(status_code=404, detail="Army not found")
    if not new_territory:
        raise HTTPException(status_code=404, detail="Territory not found")

    army.territory_id = new_territory_id
    db.commit()
    db.refresh(army)
    return army


@router.get("/territories/{territory_id}/armies/")
def get_armies_by_territory(territory_id: int, db: Session = Depends(get_db)):
    territory = db.query(Territory).filter(Territory.id == territory_id).first()
    if not territory:
        raise HTTPException(status_code=404, detail="Territory not found")

    armies = db.query(Army).filter(Army.territory_id == territory_id).all()
    return armies


class AttackRequest(BaseModel):
    attacker_id: int
    attacker_territory_id: int
    defender_territory_id: int

@router.post("/attack", summary="Attack a neighboring territory",
             description="Allows a player to attack a neighboring territory. The player can specify which neighboring territory to attack. The attack will only proceed if the player has enough armies and the territories are valid neighbors.",
             response_description="Returns a message indicating whether the attack was successful or failed.",
             response_model=dict)
def attack(attack_data: AttackRequest, db: Session = Depends(get_db)):
    attacker_id = attack_data.attacker_id
    attacker_territory_id = attack_data.attacker_territory_id
    defender_territory_id = attack_data.defender_territory_id
    
    attacker_territory = db.query(Territory).filter(Territory.id == attacker_territory_id).first()
    defender_territory = db.query(Territory).filter(Territory.id == defender_territory_id).first()
    attacker = db.query(Player).filter(Player.id == attacker_id).first()

    if not attacker_territory or not defender_territory or not attacker:
        raise HTTPException(status_code=404, detail="Territory or Player not found")
    
    is_neighbor = db.query(TerritoryNeighbor).filter(
        TerritoryNeighbor.territory_id == attacker_territory_id,
        TerritoryNeighbor.neighbor_id == defender_territory_id
    ).first()
    
    if not is_neighbor:
        raise HTTPException(status_code=400, detail="Territories are not neighbors")

    attacker_armies_count = db.query(Army).filter(Army.territory_id == attacker_territory_id).count()
    defender_armies_count = db.query(Army).filter(Army.territory_id == defender_territory_id).count()

    if attacker_armies_count < 2:
        raise HTTPException(status_code=400, detail="Not enough armies to attack")

    attack_armies = attacker_armies_count - 1

    if attack_armies > defender_armies_count:
        attacking_armies = db.query(Army).filter(Army.territory_id == attacker_territory_id).limit(attack_armies).all()

        for army in attacking_armies:
            army.territory_id = defender_territory_id
            db.add(army)
        
        db.commit()

        return {"message": "Attack successful"}
    else:
        return {"message": "Attack failed. Defender has more armies or equal"}