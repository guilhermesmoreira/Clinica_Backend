from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class PlanejamentoConexao(Base):
    __tablename__ = "planejamento_conexoes"
    
    id = Column(Integer, primary_key=True, index=True)
    planejamento_id = Column(Integer, ForeignKey("planejamentos.id"), nullable=False)
    card_from_id = Column(String(100), nullable=False)
    card_to_id = Column(String(100), nullable=False)
    
    # Relacionamentos
    planejamento = relationship("Planejamento", back_populates="conexoes")
