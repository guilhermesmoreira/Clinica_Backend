import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Banco de Dados
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost:3306/clinica_planejamentos"
)

# Configurações da API Clinicorp
CLINICORP_API_URL = os.getenv("CLINICORP_API_URL", "https://api.clinicorp.com")
CLINICORP_API_KEY = os.getenv("CLINICORP_API_KEY", "sua_chave_aqui")
