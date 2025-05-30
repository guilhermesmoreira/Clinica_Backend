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