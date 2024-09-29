import random
from src.models import Player, Objective, Territory, TerritoryNeighbor, Army
from src.db_config import SessionLocal
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import random
from .army_facade import ArmyController



class AttackRequest(BaseModel):
    attacker_id: int
    attacker_territory_id: int
    defender_territory_id: int


class PlayerController:
    def __init__(self) -> None:
        pass

    def get_player(self, db: Session):
        players = db.query(Player).all()
        if not players:
            raise HTTPException(status_code=404, detail="Nenhum jogador encontrado.")
        return {"players": players}
    
    def create_player(self, name: str, color: str, db: Session):
        if db.query(Player).filter(Player.color == color).first():
            raise HTTPException(status_code=400, detail="A cor já foi escolhida por outro jogador.")
        
        player = Player(name=name, color=color)
        db.add(player)
        db.commit()
        db.refresh(player)
        
        return {"id": player.id, "name": player.name, "color": player.color}
            

    def attack_territory(self, db: Session, attacker_id: int, attacker_territory_id: str, defender_territory_id: str):
        attacker = db.query(Player).filter(Player.id == attacker_id).first()
        
        if not attacker:
            raise ValueError("Jogador atacante não encontrado.")

        attacker_territory = db.query(Territory).filter(Territory.id == attacker_territory_id, Territory.owner_id == attacker.id).first()
        
        if not attacker_territory:
            raise ValueError("Território atacante não encontrado ou não pertence ao jogador.")

        defender_territory = db.query(Territory).filter(Territory.id == defender_territory_id).first()
        
        if not defender_territory or defender_territory.owner_id == attacker.id:
            raise ValueError("Território defensor não encontrado ou pertence ao atacante.")

        attacker_armies = sum(army.count for army in attacker.armies if army.territory_id == attacker_territory.id)
        if attacker_armies < 2:
            raise ValueError("O jogador deve ter pelo menos 2 exércitos para atacar.")

        defender_armies = sum(army.count for army in defender_territory.armies)

        if attacker_armies > defender_armies:
            victory_chance = 2/3
        else:
            victory_chance = 1/3

        attack_result = random.random() < victory_chance

        if attack_result:
            defender_territory.owner_id = attacker.id
            
            defender_armies = sum(army.count for army in defender_territory.armies)
            
            for army in defender_territory.armies:
                db.delete(army)
            
            db.add(Army(player_id=attacker.id, territory_id=defender_territory.id, count=defender_armies))

            db.commit()
            return f"{attacker.name} conquistou {defender_territory_id}!"

        else:
        
            armies_lost = attacker_armies - 1  
            for army in attacker.armies:
                if army.territory_id == attacker_territory.id and armies_lost > 0:
                    if army.count > armies_lost:
                        army.count -= armies_lost
                        armies_lost = 0
                    else:
                        armies_lost -= army.count
                        db.delete(army)

            db.commit()
            return f"{attacker.name} atacou {defender_territory_id} e perdeu a batalha."

    def new_round(self, db: Session): 
        ArmyController.aditional_armies(db)
        return {"message": "Nova rodada iniciada, exercitos distribuidos"}