import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# Chemin absolu vers le fichier .env (dev local)
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

def get_connection():
    """
    Retourne une connexion PostgreSQL.
    En production (Render), utilise DATABASE_URL.
    En local, utilise les parametres locaux.
    """
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Production (Render/Supabase)
        return psycopg2.connect(database_url)
    else:
        # Developpement local
        return psycopg2.connect(
            host="localhost",
            database="lol_data_analytics",
            user="postgres",
            password=os.getenv("POSTGRES_PASSWORD"),
            port=5433
        )
