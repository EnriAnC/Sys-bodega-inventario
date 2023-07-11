from pydantic import BaseModel


class Bodeguero(BaseModel):
    id_usuario: int
    nombre: str
    apellido_m: str
    apellido_p: str
    rol: str
