from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# Schemas para Planejamento
class PlanejamentoBase(BaseModel):
    paciente_id: str
    paciente_nome: str
    observacoes: Optional[str] = None
    status: str = "ativo"

class PlanejamentoCreate(PlanejamentoBase):
    pass

class PlanejamentoUpdate(BaseModel):
    paciente_nome: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None

class PlanejamentoResponse(PlanejamentoBase):
    id: int
    data_criacao: datetime
    data_modificacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schemas para Cards
class AgendamentoData(BaseModel):
    status: str
    data: str
    horario: str
    dataAgendamento: str

class CardData(BaseModel):
    paciente: str
    procedimento: str
    agendamento: AgendamentoData
    pacienteId: Optional[str] = None
    categoria: Optional[str] = None
    duracao: Optional[int] = None
    notas: Optional[str] = None

class PlanejamentoCardBase(BaseModel):
    card_id: str
    coluna_id: str
    dados_card: CardData

class PlanejamentoCardCreate(PlanejamentoCardBase):
    pass

class PlanejamentoCardResponse(PlanejamentoCardBase):
    id: int
    planejamento_id: int
    
    class Config:
        from_attributes = True

# Schemas para Conexões
class PlanejamentoConexaoBase(BaseModel):
    card_from_id: str
    card_to_id: str

class PlanejamentoConexaoCreate(PlanejamentoConexaoBase):
    pass

class PlanejamentoConexaoResponse(PlanejamentoConexaoBase):
    id: int
    planejamento_id: int
    
    class Config:
        from_attributes = True

# Schema completo do planejamento
class PlanejamentoCompleto(BaseModel):
    id: int
    paciente_id: str
    paciente_nome: str
    data_criacao: datetime
    data_modificacao: Optional[datetime] = None
    status: str
    observacoes: Optional[str] = None
    cards: List[PlanejamentoCardResponse] = []
    conexoes: List[PlanejamentoConexaoResponse] = []
    
    class Config:
        from_attributes = True

# Schema para salvar planejamento completo
class PlanejamentoCompletoCreate(BaseModel):
    paciente_id: str
    paciente_nome: str
    observacoes: Optional[str] = None
    cards: List[PlanejamentoCardCreate]
    conexoes: List[PlanejamentoConexaoCreate]
