#!/usr/bin/env python3
"""
Script para testar os endpoints de planejamento
"""

import requests
import json
from datetime import datetime

# URL base da API
BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Testar todos os endpoints de planejamento"""
    
    print("🧪 Testando endpoints de planejamento...")
    
    # Dados de teste
    planejamento_data = {
        "paciente_id": "12345",
        "paciente_nome": "João Silva",
        "observacoes": "Planejamento de teste",
        "cards": [
            {
                "card_id": "card-1",
                "coluna_id": "agendar",
                "dados_card": {
                    "paciente": "João Silva",
                    "procedimento": "Limpeza Dental",
                    "agendamento": {
                        "status": "agendar",
                        "data": "",
                        "horario": "",
                        "dataAgendamento": ""
                    }
                }
            },
            {
                "card_id": "card-2", 
                "coluna_id": "agendado",
                "dados_card": {
                    "paciente": "João Silva",
                    "procedimento": "Consulta de Rotina",
                    "agendamento": {
                        "status": "agendado",
                        "data": "2024-01-15",
                        "horario": "08:30",
                        "dataAgendamento": "2024-01-10"
                    }
                }
            }
        ],
        "conexoes": [
            {
                "card_from_id": "card-1",
                "card_to_id": "card-2"
            }
        ]
    }
    
    try:
        # Teste 1: Criar planejamento
        print("\n1️⃣ Testando criação de planejamento...")
        response = requests.post(f"{BASE_URL}/planejamentos", json=planejamento_data)
        if response.status_code == 200:
            planejamento = response.json()
            print(f"✅ Planejamento criado com ID: {planejamento['id']}")
            planejamento_id = planejamento['id']
        else:
            print(f"❌ Erro ao criar planejamento: {response.status_code} - {response.text}")
            return
        
        # Teste 2: Listar planejamentos
        print("\n2️⃣ Testando listagem de planejamentos...")
        response = requests.get(f"{BASE_URL}/planejamentos")
        if response.status_code == 200:
            planejamentos = response.json()
            print(f"✅ Encontrados {len(planejamentos)} planejamentos")
        else:
            print(f"❌ Erro ao listar planejamentos: {response.status_code}")
        
        # Teste 3: Buscar planejamento por ID
        print("\n3️⃣ Testando busca por ID...")
        response = requests.get(f"{BASE_URL}/planejamentos/{planejamento_id}")
        if response.status_code == 200:
            planejamento = response.json()
            print(f"✅ Planejamento encontrado: {planejamento['paciente_nome']}")
            print(f"   Cards: {len(planejamento['cards'])}")
            print(f"   Conexões: {len(planejamento['conexoes'])}")
        else:
            print(f"❌ Erro ao buscar planejamento: {response.status_code}")
        
        # Teste 4: Buscar por paciente
        print("\n4️⃣ Testando busca por paciente...")
        response = requests.get(f"{BASE_URL}/planejamentos/paciente/12345")
        if response.status_code == 200:
            planejamentos = response.json()
            print(f"✅ Encontrados {len(planejamentos)} planejamentos para o paciente")
        else:
            print(f"❌ Erro ao buscar por paciente: {response.status_code}")
        
        # Teste 5: Atualizar planejamento
        print("\n5️⃣ Testando atualização...")
        update_data = {
            "observacoes": "Planejamento atualizado",
            "status": "ativo"
        }
        response = requests.put(f"{BASE_URL}/planejamentos/{planejamento_id}", json=update_data)
        if response.status_code == 200:
            print("✅ Planejamento atualizado com sucesso")
        else:
            print(f"❌ Erro ao atualizar: {response.status_code}")
        
        print("\n🎉 Todos os testes concluídos!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando. Execute 'uvicorn main:app --reload' primeiro.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_endpoints()
