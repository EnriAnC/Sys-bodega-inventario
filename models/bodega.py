from typing import Optional

from pydantic import BaseModel


class Bodega(BaseModel):
    id_usuario: Optional[int] = None
    nombre_bodega: str
    direccion_bodega: str
    