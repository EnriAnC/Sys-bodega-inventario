from typing import Optional

from pydantic import BaseModel


class Movimiento(BaseModel):
    id_movimiento: Optional[int] = None
    id_bodega: int
    id_libro: int
    id_usuario: int
    fecha_despacho: str
    fecha_ingreso: str
    cantidad_libro: int
    url_informe: str
