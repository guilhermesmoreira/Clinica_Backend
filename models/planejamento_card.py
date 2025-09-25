from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.base import Base

class PlanejamentoCard(Base):
    __tablename__ = "planejamento_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    planejamento_id = Column(Integer, ForeignKey("planejamentos.id"), nullable=False)
    card_id = Column(String(100), nullable=False, index=True)
    coluna_id = Column(String(100), nullable=False)
    dados_card = Column(JSON, nullable=False)  # Todos os dados do card em JSON
    
    # Relacionamentos
    planejamento = relationship("Planejamento", back_populates="cards")
