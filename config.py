import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente de .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'troque_por_uma_senha_forte')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Ex: postgres://user:pass@host:port/dbname
    SQLALCHEMY_TRACK_MODIFICATIONS = False
