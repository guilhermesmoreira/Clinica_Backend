from fastapi import FastAPI, Query
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI()

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
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")  # <- aqui

    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": "Erro ao buscar dados da Clinicorp", "detalhes": str(e)}

@app.get("/pacientes")
def buscar_paciente_por_nome(nome: str):
    url = "https://api.clinicorp.com/rest/v1/patient/get"
    auth = HTTPBasicAuth("teharicr", "6866dbfa-bf85-425a-8b60-2b1665fb944d")
    params = {
        "subscriber_id": "teharicr",
        "Name": nome
    }

    try:
        response = requests.get(url, auth=auth, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "erro": "Erro ao buscar paciente na Clinicorp",
            "detalhes": str(e)
        }

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
        response = requests.get(url, auth=auth, params=params)
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
        response = requests.get(url, auth=auth, params=params)
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
        response = requests.get(url, auth=auth, params=params)
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
        response = requests.get(url, auth=auth, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": "Erro ao buscar detalhes do orçamento", "detalhes": str(e)}
