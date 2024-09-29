from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db_config import Base

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, unique=True, nullable=False)
    territories = relationship("Territory", back_populates="owner")
    objectives = relationship("Objective", back_populates="player")
    armies = relationship("Army", back_populates="player")

class Territory(Base):
    __tablename__ = "territories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("players.id"))
    owner = relationship("Player", back_populates="territories")
    region = Column(String)
    armies = relationship("Army", back_populates="territory")
    neighbors = relationship(
        "Territory",
        secondary="territory_neighbors",
        primaryjoin="Territory.id == TerritoryNeighbor.territory_id",
        secondaryjoin="Territory.id == TerritoryNeighbor.neighbor_id",
        back_populates="neighbor_of"
    )
    neighbor_of = relationship(
        "Territory",
        secondary="territory_neighbors",
        primaryjoin="Territory.id == TerritoryNeighbor.neighbor_id",
        secondaryjoin="Territory.id == TerritoryNeighbor.territory_id",
        back_populates="neighbors"
    )

class Objective(Base):
    __tablename__ = "objectives"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    player = relationship("Player", back_populates="objectives")
    assigned = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "player_id": self.player_id
        }

class Army(Base):
    __tablename__ = "armies"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    territory_id = Column(Integer, ForeignKey("territories.id"), nullable=False)
    count = Column(Integer, nullable=False, default=1)  # Número de unidades do exército
    
    player = relationship("Player", back_populates="armies")
    territory = relationship("Territory", back_populates="armies")

class TerritoryNeighbor(Base):
    __tablename__ = "territory_neighbors"
    
    id = Column(Integer, primary_key=True, index=True)
    territory_id = Column(Integer, ForeignKey("territories.id"), nullable=False)
    neighbor_id = Column(Integer, ForeignKey("territories.id"), nullable=False)
    
    territory = relationship("Territory", foreign_keys=[territory_id], overlaps="neighbors,neighbor_of")
    neighbor = relationship("Territory", foreign_keys=[neighbor_id], overlaps="neighbors,neighbor_of")

class Color(Base):
    __tablename__ = "colors"
    
    id = Column(Integer, primary_key=True, index=True)
    color = Column(String, index=True)
