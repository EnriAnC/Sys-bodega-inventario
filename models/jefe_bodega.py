from typing import Optional

from pydantic import BaseModel


class JefeBodega(BaseModel):
    id_usuario: Optional[int]
    nombre: str
    apellido_m: str
    apellido_p: str
    rol: str
    fecha_contrato: Optional[str]
