from sqlalchemy.orm import Session
from models.planejamento import Planejamento
from models.planejamento_card import PlanejamentoCard
from models.planejamento_conexao import PlanejamentoConexao
from schemas import (
    PlanejamentoCreate, 
    PlanejamentoUpdate, 
    PlanejamentoCompletoCreate,
    PlanejamentoCardCreate,
    PlanejamentoConexaoCreate
)
from datetime import datetime
from typing import List, Optional

class PlanejamentoService:
    def __init__(self, db: Session):
        self.db = db

    def criar_planejamento(self, planejamento_data: PlanejamentoCompletoCreate) -> Planejamento:
        """Criar um novo planejamento completo com cards e conexões"""
        # Criar o planejamento principal
        planejamento = Planejamento(
            paciente_id=planejamento_data.paciente_id,
            paciente_nome=planejamento_data.paciente_nome,
            data_criacao=datetime.now(),
            observacoes=planejamento_data.observacoes,
            status="ativo"
        )
        
        self.db.add(planejamento)
        self.db.flush()  # Para obter o ID
        
        # Criar os cards
        for card_data in planejamento_data.cards:
            card = PlanejamentoCard(
                planejamento_id=planejamento.id,
                card_id=card_data.card_id,
                coluna_id=card_data.coluna_id,
                dados_card=card_data.dados_card.dict()
            )
            self.db.add(card)
        
        # Criar as conexões
        for conexao_data in planejamento_data.conexoes:
            conexao = PlanejamentoConexao(
                planejamento_id=planejamento.id,
                card_from_id=conexao_data.card_from_id,
                card_to_id=conexao_data.card_to_id
            )
            self.db.add(conexao)
        
        self.db.commit()
        self.db.refresh(planejamento)
        return planejamento

    def buscar_planejamento_por_id(self, planejamento_id: int) -> Optional[Planejamento]:
        """Buscar planejamento por ID"""
        return self.db.query(Planejamento).filter(Planejamento.id == planejamento_id).first()

    def buscar_planejamentos_por_paciente(self, paciente_id: str) -> List[Planejamento]:
        """Buscar todos os planejamentos de um paciente"""
        return self.db.query(Planejamento).filter(Planejamento.paciente_id == paciente_id).all()

    def listar_todos_planejamentos(self) -> List[Planejamento]:
        """Listar todos os planejamentos"""
        return self.db.query(Planejamento).all()

    def atualizar_planejamento(self, planejamento_id: int, planejamento_data: PlanejamentoUpdate) -> Optional[Planejamento]:
        """Atualizar um planejamento"""
        planejamento = self.buscar_planejamento_por_id(planejamento_id)
        if not planejamento:
            return None
        
        # Atualizar campos fornecidos
        update_data = planejamento_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(planejamento, field, value)
        
        planejamento.data_modificacao = datetime.now()
        self.db.commit()
        self.db.refresh(planejamento)
        return planejamento

    def deletar_planejamento(self, planejamento_id: int) -> bool:
        """Deletar um planejamento (soft delete)"""
        planejamento = self.buscar_planejamento_por_id(planejamento_id)
        if not planejamento:
            return False
        
        planejamento.status = "inativo"
        planejamento.data_modificacao = datetime.now()
        self.db.commit()
        return True

    def buscar_planejamento_completo(self, planejamento_id: int) -> Optional[Planejamento]:
        """Buscar planejamento com todos os relacionamentos"""
        return self.db.query(Planejamento).filter(
            Planejamento.id == planejamento_id
        ).first()
