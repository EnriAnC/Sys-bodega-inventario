from pydantic import BaseModel


class Usuario(BaseModel):
    nombre_usuario: str
    email: str
    password: str