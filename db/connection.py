import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# Chemin absolu vers le fichier .env
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="lol_data_analytics",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5433
    )
