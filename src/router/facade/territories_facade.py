import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models import Player, Territory, TerritoryNeighbor

class TerritorieController():
    def __init__(self) -> None:
        pass

    def get_territories(self, db: Session):
        Territories = db.query(Territory).all()
        return Territories

    def get_neighbors(self, territory_id, db: Session):
        neighbor = db.query(TerritoryNeighbor).filter(TerritoryNeighbor.territory_id == territory_id).all()
        if not neighbor:
            raise HTTPException(status_code=404, detail="Nenhum vizinho encontrado.")
        return neighbor

    def distribute_territories(self, db: Session):
        players = db.query(Player).all()
        territories = db.query(Territory).all()

        if not players:
            raise ValueError("Nenhum jogador encontrado.")
        if not territories:
            raise ValueError("Nenhum território encontrado.")

        random.shuffle(territories)

        num_players = len(players)
        
        if num_players <= 3:
            territories_per_player = 5
        else:
            territories_per_player = 4

        for i in range(territories_per_player):
            for idx, player in enumerate(players):
                if not territories:  
                    break
                territory = territories.pop(0)
                territory.owner_id = player.id
        db.commit()


    def get_player_territories(self, db: Session):
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
    
    def get_territories_with_owners_and_armies(self, db: Session):
        territories = db.query(Territory).all()
        result = []

        for territory in territories:
            owner_name = territory.owner.name if territory.owner else "Sem dono"
            army_count = sum(army.count for army in territory.armies)

            result.append({
                "territory": territory.name,
                "owner": owner_name,
                "army_count": army_count
            })

        return result
    
    def get_attackable_territories(self, db: Session, player_id: int):
        player = db.query(Player).filter(Player.id == player_id).first()
        
        if not player:
            raise ValueError("Jogador não encontrado.")

        attackable_territories = set()

        player_territories = player.territories

        for territory in player_territories:
            if territory.armies:  #
                for neighbor in territory.neighbors:
                    if neighbor.owner and neighbor.owner.id != player_id:
                        attackable_territories.add(neighbor)

        result = [
            {
                "territory": territory.name,
                "owner": territory.owner.name if territory.owner else "Sem dono"
            }
            for territory in attackable_territories
        ]

        return result

