from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.models import Army, Player, Territory
from pydantic import BaseModel
from src.db_config import SessionLocal


class AttackRequest(BaseModel):
    attacker_id: int
    attacker_territory_id: int
    defender_territory_id: int
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ArmyController:
    def __init__(self) -> None:
        pass

    def distribute_armies(self, db: Session): 
        players = db.query(Player).all()
        
        if not players:
            raise ValueError("Nenhum jogador encontrado.")

        for player in players:
            player_territories = db.query(Territory).filter_by(owner_id=player.id).all()

            if not player_territories:
                raise ValueError(f"O jogador {player.name} não possui territórios.")

            for territory in player_territories:
                new_army = Army(
                    territory_id=territory.id,
                    player_id=player.id,
                    count=1 
                )
                db.add(new_army)
        db.commit()

    def aditional_armies(db: Session):
        players = db.query(Player).all()
        for player in players:
            player_territories = db.query(Territory).filter_by(owner_id=player.id).all()
            for i in range(2):
                if player_territories:
                    new_army_free = Army(
                        territory_id=player_territories[0].id,
                        player_id=player.id,
                        count=1
                    )
                    db.add(new_army_free)
        db.commit()

    def distribute_armies_for_all_players(self, db: Session):
        self.distribute_armies(db)
        self.aditional_armies(db)
        return {"message": "Rodada iniciada, exercitos distribuidos"}


    def get_player_armies(self, db: Session, player_id):
        player = db.query(Player).filter(Player.id == player_id).first()
        return player.armies

    def move_army(self, db: Session, fromTerritory: int, toTerritory: int, player_id: int):

        territory1 = db.query(Territory).filter_by(id = fromTerritory).first()
        print(type(territory1.owner_id))
        print(type(player_id))
        print(territory1.owner_id)
        if territory1.owner_id != player_id:
            raise ValueError("Teritorio não pertence ao jogador")

        territory2 = db.query(Territory).filter_by(id = toTerritory).first()
        if territory2.owner_id != player_id:
            raise ValueError("Teritorio não pertence ao jogador")
        
        if len(territory1.armies) < 2 : 
            raise ValueError("Teritorio tem apenas 1 exercito")
        
        army_to_move = territory1.armies[0]

        army_to_move.territory_id = territory2.id

        db.add(army_to_move)
        db.commit()

        return {"message": "Exército movido com sucesso"}


    

