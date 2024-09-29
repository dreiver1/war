from src.models import Player, Objective
from src.db_config import SessionLocal
from fastapi import HTTPException
from sqlalchemy.orm import Session


class objectiveController():
    def __init__(self) -> None:
        pass

    def assign_objective(self, player_id: int, db: Session):
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
    
    def get_objectives(db: Session):
        objectives = db.query(Objective).all()
        if not objectives:
            raise HTTPException(status_code=404, detail="Nenhum objetivo encontrado.")
        return objectives
    
    def get_player_objective(self, player_id: int, db: Session):
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise HTTPException(status_code=404, detail="Jogador não encontrado.")
        objective = player.objectives
        if not objective:
            raise HTTPException(status_code=404, detail="Nenhum objetivo encontrado.")
        return objective
    
    def verify_objective(self, player_id: int, db: Session):
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player or not player.objectives:
            return False, "Jogador ou objetivo não encontrado."
        
        objective = player.objectives[0]

        region_to_territories = {
            "Sul": ["Paraná", "Santa Catarina", "Rio Grande do Sul"],
            "Nordeste": ["Bahia", "Pernambuco", "Ceará", "Maranhão", "Paraíba", "Sergipe", "Alagoas", "Rio Grande do Norte", "Piauí"],
            "Centro-Oeste": ["Mato Grosso", "Mato Grosso do Sul", "Goiás", "Distrito Federal"],
            "Norte": ["Amazonas", "Pará", "Acre", "Amapá", "Rondônia", "Roraima", "Tocantins"],
            "Sudeste": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Espírito Santo"]
        }

        objective_description = objective.description.split("Conquistar ")[1].strip()

        player_territories = [territory.name for territory in player.territories]

        required_territories = region_to_territories.get(objective_description, [])
        if all(territory in player_territories for territory in required_territories):
            return True, f"Objetivo '{objective.description}' cumprido!"
        else:
            return False, f"Objetivo '{objective.description}' ainda não foi cumprido."