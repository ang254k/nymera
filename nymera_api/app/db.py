import os
import psycopg
from dotenv import load_dotenv

#Para instalar:
# pip install python-dotenv

# Para cargar: variables del archivo .env
load_dotenv()


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )