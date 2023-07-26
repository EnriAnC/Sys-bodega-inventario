from typing import Optional

from pydantic import BaseModel


class Usuario(BaseModel):
    id: Optional[int] = None
    nombre_usuario: str
    email: str
    password: str
    
class LoginUsuario(BaseModel):
    email: str
    password: str
    
class RegistrarUsuario(BaseModel):
    nombre_usuario: str
    email: str
    password: str
    nombre: str
    rol: str
    apellido_p: str
    apellido_m: Optional[str] = None,