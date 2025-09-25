#!/usr/bin/env python3
"""
Script para testar a conexão com o MySQL e criar as tabelas
"""

from database.connection import engine, create_tables
from sqlalchemy import text

# Importar todos os modelos para que sejam registrados
from models.planejamento import Planejamento
from models.planejamento_card import PlanejamentoCard
from models.planejamento_conexao import PlanejamentoConexao

def test_connection():
    """Testar conexão com o banco"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexão com MySQL estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar com MySQL: {e}")
        return False

def create_database_tables():
    """Criar todas as tabelas"""
    try:
        create_tables()
        print("✅ Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testando configuração do banco de dados...")
    
    # Testar conexão
    if test_connection():
        # Criar tabelas
        create_database_tables()
        print("\n🎉 Configuração concluída com sucesso!")
    else:
        print("\n❌ Falha na configuração. Verifique se o MySQL está rodando.")
