from src.db_config import engine, Base, SessionLocal
from src.models import Color, Objective, Territory, TerritoryNeighbor, Army, Player

def initialize_database():
    # Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        colors = ["vermelho", "azul", "verde", "amarelo", "preto", "branco"]
        for color in colors:
            db.add(Color(color=color))
        
        objectives = [
            {"id": 1, "description": "Conquistar Sul"},
            {"id": 2, "description": "Conquistar Norderste"},
            {"id": 3, "description": "Conquistar Centro-Oeste"},
            {"id": 4, "description": "Conquistar Note"},
            {"id": 5, "description": "Conquistar Sudeste"},
            {"id": 6, "description": "15 territorios"}
        ]
        
        for obj in objectives:
            db.add(Objective(id=obj['id'], description=obj["description"]))
        
        territories = [
            ("Acre", "Norte"),
            ("Alagoas", "Nordeste"),
            ("Amazonas", "Norte"),
            ("Bahia", "Nordeste"),
            ("Ceará", "Nordeste"),
            ("Distrito Federal", "Centro-Oeste"),
            ("Espírito Santo", "Sudeste"),
            ("Goiás", "Centro-Oeste"),
            ("Maranhão", "Nordeste"),
            ("Mato Grosso", "Centro-Oeste"),
            ("Mato Grosso do Sul", "Centro-Oeste"),
            ("Minas Gerais", "Sudeste"),
            ("Pará", "Norte"),
            ("Paraíba", "Nordeste"),
            ("Paraná", "Sul"),
            ("Pernambuco", "Nordeste"),
            ("Piauí", "Nordeste"),
            ("Rio de Janeiro", "Sudeste"),
            ("Rio Grande do Norte", "Nordeste"),
            ("Rio Grande do Sul", "Sul"),
            ("Rondônia", "Norte"),
            ("Roraima", "Norte"),
            ("Santa Catarina", "Sul"),
            ("São Paulo", "Sudeste"),
            ("Sergipe", "Nordeste"),
            ("Tocantins", "Norte")
        ]
        
        for name, region in territories:
            db.add(Territory(name=name, region=region))
        
        neighbors = [
            (1, 3),(1, 21),(2, 16),(2, 25),(2, 4),(3, 1),(3, 21),(3, 10),(3, 13),(3, 22),(4, 2),(4, 25),(4, 16),(4, 17),
            (4, 8),(4, 12),(5, 19),(5, 14),(5, 16),(5, 17),(6, 8),(6, 12),(7, 12),(7, 18),(7, 4),(8, 10),(8, 6),(8, 12),
            (8, 4),(8, 11),(9, 17),(9, 26),(9, 13),(10, 3),(10, 21),(10, 26),(10, 8),(10, 11),(11, 10),(11, 8),(11, 12),
            (11, 15),(12, 11),(12, 8),(12, 6),(12, 7),(12, 4),(12, 18),(13, 9),(13, 26),(13, 3),(14, 5),(14, 19),(14, 16)
            ,(15, 11),(15, 23),(16, 14),(16, 5),(16, 2),(16, 4),(17, 9),(17, 5),(17, 4),(18, 12),(18, 7),(18, 24),(19, 5),
            (19, 14),(20, 23),(21, 1),(21, 3),(21, 10),(22, 3),(23, 20),(23, 15),(24, 18),(24, 12),(24, 15),(25, 2),(25, 4)
            ,(26, 9),(26, 13),(26, 10)
        ]

        
        for territory_id, neighbor_id in neighbors:
            db.add(TerritoryNeighbor(territory_id=territory_id, neighbor_id=neighbor_id))
        
        territories = db.query(Territory).all()
        for territory in territories:
            db.add(Army(player_id=None, territory_id=territory.id, count=1))
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        db.close()
