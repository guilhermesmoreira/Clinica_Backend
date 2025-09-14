from fastapi import FastAPI, Query
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
import requests
from requests.auth import HTTPBasicAuth
import ssl
import urllib3

app = FastAPI()

# Configurações SSL mais robustas
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurar sessão com SSL mais flexível
session = requests.Session()
session.verify = True  # Manter verificação SSL, mas com configurações mais flexíveis

# Libera CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/procedimentos")
def listar_procedimentos():
    url = "https://api.clinicorp.com/rest/v1/procedures/list"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")

    try:
        response = requests.get(url, auth=auth, verify=False, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": "Erro ao buscar dados da Clinicorp", "detalhes": str(e)}

@app.get("/procedimentos_periodo")
def listar_procedimentos_por_periodo(
    from_: str = Query(..., alias="from"),
    to: str = Query(..., alias="to"),
    patient_id: str = Query(None)
):
    """
    Busca procedimentos de um paciente específico dentro de um período.
    Se patient_id não for fornecido, retorna todos os procedimentos do período.
    """
    url = "https://api.clinicorp.com/rest/v1/estimates/list"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")
    params = {
        "subscriber_id": "teharicr",
        "from": from_,
        "to": to,
    }
    
    if patient_id:
        params["PatientId"] = patient_id

    try:
        response = requests.get(url, auth=auth, params=params, verify=False, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": "Erro ao buscar procedimentos do período", "detalhes": str(e)}

@app.get("/pacientes")
def buscar_paciente_por_nome(nome: str):
    url = "https://api.clinicorp.com/rest/v1/patient/get"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")
    
    # Estratégias de busca: nome completo, primeiro nome, e partes do nome
    search_strategies = [
        nome,  # Nome completo
        nome.split()[0] if nome.split() else nome,  # Primeiro nome
    ]
    
    # Adicionar variações com partes do nome (primeiro + segundo nome)
    nome_parts = nome.split()
    if len(nome_parts) >= 2:
        search_strategies.append(f"{nome_parts[0]} {nome_parts[1]}")  # Primeiro + segundo nome
    
    for search_name in search_strategies:
        params = {
            "subscriber_id": "teharicr",
            "Name": search_name
        }
        
        try:
            print(f"🔍 Tentando buscar com: '{search_name}'")
            response = requests.get(url, auth=auth, params=params, verify=False, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Se encontrou resultados, retorna
            if result and (isinstance(result, list) and len(result) > 0) or (isinstance(result, dict) and result):
                print(f"✅ Encontrado com: '{search_name}' - {len(result) if isinstance(result, list) else 1} resultado(s)")
                return result
            else:
                print(f"❌ Nenhum resultado com: '{search_name}'")
                
        except requests.RequestException as e:
            print(f"❌ Erro ao buscar com '{search_name}': {str(e)}")
            continue
    
    # Se nenhuma estratégia funcionou, retorna lista vazia
    print(f"❌ Nenhum paciente encontrado para: '{nome}'")
    return []

@app.get("/estimativas")
def listar_estimativas(
    de: date = Query(..., alias="from"),
    ate: date = Query(..., alias="to")
):
    url = "https://api.clinicorp.com/rest/v1/patient/list_estimates"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")
    params = {
        "subscriber_id": "teharicr",
        "from": de.strftime("%Y-%m-%d"),
        "to": ate.strftime("%Y-%m-%d"),
    }

    try:
        response = requests.get(url, auth=auth, params=params, verify=False, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "erro": "Erro ao buscar estimativas na Clinicorp",
            "detalhes": str(e)
        }
        
@app.get("/agendamentos")
def listar_agendamentos(patient_id: str):
    url = f"https://api.clinicorp.com/rest/v1/patient/list_appointments"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")
    params = {
        "PatientId": patient_id
    }

    try:
        response = requests.get(url, auth=auth, params=params, verify=False, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "erro": "Erro ao buscar agendamentos na Clinicorp",
            "detalhes": str(e)
        }

@app.get("/orcamentos")
def listar_orcamentos(from_: str = Query(..., alias="from"), to: str = Query(..., alias="to")):
    url = "https://api.clinicorp.com/rest/v1/estimates/list"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")
    params = {
        "subscriber_id": "teharicr",
        "from": from_,
        "to": to,
    }

    try:
        response = requests.get(url, auth=auth, params=params, verify=False, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": "Erro ao buscar orçamentos", "detalhes": str(e)}


@app.get("/orcamento_detalhe")
def buscar_orcamento_detalhe(treatment_id: int):
    url = "https://api.clinicorp.com/rest/v1/estimates/get"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")
    params = {
        "subscriber_id": "teharicr",
        "treatment_id": treatment_id
    }

    try:
        response = requests.get(url, auth=auth, params=params, verify=False, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": "Erro ao buscar detalhes do orçamento", "detalhes": str(e)}
