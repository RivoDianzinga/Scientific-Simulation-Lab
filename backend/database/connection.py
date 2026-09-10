"""
Ce fichier ne fait aucun calcul Lennard-Jones. Il ne connaît pas FastAPI.
Il ne connaît pas le frontend.Son unique responsabilité est :
ouvrir une connexion avec PostgreSQL.
C'est directement une notion d'architecture logicielle / séparation des responsabilités.
"""
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()
# On fait évoluer la connexion locale vers un serveur par 
# database_url
# Sur ce pc, database_url absente ---> postgresql local
# database_url présente ---> postgresql sur connexion Neon
def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg.connect(database_url)
    return psycopg.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
    )