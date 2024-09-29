# tests/test_routes.py

import pytest

def test_create_player(client):
    response = client.post("/players/", json={"name": "Jogador", "color": "Azul"})
    assert response.status_code == 200

def test_get_player(client):
    response = client.get("/players")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "Jogador 1"
    assert response.json()["color"] == "Azul"

def test_attack_territory(client):
    # Criar dois jogadores
    client.post("/players", json={"name": "Atacante", "color": "Vermelho"})
    client.post("/players", json={"name": "Defensor", "color": "Azul"})
    
    # Testar o ataque entre territórios
    response = client.post("/players/attack", json={
        "attacker_id": 1,
        "attacker_territory_id": "Territorio 1",
        "defender_territory_id": "Territorio 2"
    })
    
    print(response.json())  # Para depuração
    assert response.status_code in (200, 400)  # Ajuste conforme necessário para os erros de ataque

def test_new_round(client):
    response = client.get("/players/new_round")
    assert response.status_code == 200
