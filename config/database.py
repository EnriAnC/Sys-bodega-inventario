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

POSTGRE_DATABASE_CONFIG_DEV = {
    'host': os.getenv("DATABASE_HOST_DEV"),
    'port': os.getenv("DATABASE_PORT_DEV"),
    'database': os.getenv("DATABASE_NAME_DEV"),
    'user': os.getenv("DATABASE_USER_DEV"),
    'password': os.getenv("DATABASE_PASSWORD_DEV")
}