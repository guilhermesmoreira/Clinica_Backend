#!/usr/bin/env python3
"""
Teste simples dos endpoints sem MySQL
"""

import requests
import json

# URL base da API
BASE_URL = "http://localhost:8000"

def test_simple_endpoints():
    """Testar endpoints básicos"""
    
    print("🧪 Testando endpoints básicos...")
    
    try:
        # Teste 1: Verificar se a API está rodando
        print("\n1️⃣ Testando se a API está rodando...")
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API está rodando! Documentação disponível em /docs")
        else:
            print(f"❌ API não está rodando: {response.status_code}")
            return
        
        # Teste 2: Testar endpoint de procedimentos (que já existia)
        print("\n2️⃣ Testando endpoint de procedimentos...")
        response = requests.get(f"{BASE_URL}/procedimentos")
        if response.status_code == 200:
            print("✅ Endpoint de procedimentos funcionando")
        else:
            print(f"❌ Erro no endpoint de procedimentos: {response.status_code}")
        
        # Teste 3: Verificar se os endpoints de planejamento estão registrados
        print("\n3️⃣ Verificando endpoints de planejamento...")
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            openapi_data = response.json()
            paths = openapi_data.get('paths', {})
            
            planejamento_endpoints = [path for path in paths.keys() if 'planejamento' in path]
            if planejamento_endpoints:
                print(f"✅ Endpoints de planejamento encontrados: {planejamento_endpoints}")
            else:
                print("❌ Nenhum endpoint de planejamento encontrado")
        else:
            print(f"❌ Erro ao obter OpenAPI: {response.status_code}")
        
        print("\n🎉 Teste básico concluído!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando. Execute o servidor primeiro.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_simple_endpoints()
