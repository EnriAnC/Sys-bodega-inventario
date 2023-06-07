# config.py
from dotenv import load_dotenv
import os
load_dotenv()

POSTGRE_DATABASE_CONFIG = {
    'host': os.getenv("DATABASE_HOST"),
    'port': os.getenv("DATABASE_PORT"),
    'database': os.getenv("DATABASE_NAME"),
    'user': os.getenv("DATABASE_USER"),
    'password': os.getenv("DATABASE_PASSWORD")
}