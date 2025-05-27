from fastapi import FastAPI
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
