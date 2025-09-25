from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from database.base import Base

class Planejamento(Base):
    __tablename__ = "planejamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(String(100), nullable=False, index=True)
    paciente_nome = Column(String(255), nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_modificacao = Column(DateTime, nullable=True)
    status = Column(String(50), default="ativo")  # ativo, inativo, arquivado
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    cards = relationship("PlanejamentoCard", back_populates="planejamento", cascade="all, delete-orphan")
    conexoes = relationship("PlanejamentoConexao", back_populates="planejamento", cascade="all, delete-orphan")
