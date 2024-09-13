from db_config import engine, Base, SessionLocal
from models import Color, Objective, Territory, TerritoryNeighbor, Army, Player

def initialize_database():
    # Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        colors = ["vermelho", "azul", "verde", "amarelo", "preto", "branco"]
        for color in colors:
            db.add(Color(color=color))
        
        objectives = [
            {"description": "Conquistar 3 territórios"},
            {"description": "Eliminar um exército inimigo"},
            {"description": "Conquistar 2 territórios e ocupar com dois exércitos cada"},
            {"description": "Conquistar o nordeste brasileiro"},
            {"description": "Eliminar um exército inimigo"},
            {"description": "Conquistar o sul do Brasil"}
        ]
        for obj in objectives:
            db.add(Objective(description=obj["description"]))
        
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
            (1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 10), 
            (9, 11), (10, 12), (11, 13), (12, 14), (13, 15), (14, 16), (15, 17),
            (16, 18), (17, 19), (18, 20), (19, 21), (20, 22), (21, 23), (22, 24),
            (23, 25), (24, 26), (25, 27), (26, 28)
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
