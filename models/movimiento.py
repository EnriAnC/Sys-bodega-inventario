from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel


class Movimiento(BaseModel):
    id_movimiento: Optional[int] = None
    id_bodega: int
    id_libro: int
    id_usuario: int
    fecha_despacho: Optional[datetime] = None
    fecha_ingreso: Optional[datetime] = None
    cantidad_libro: int
    url_informe: Optional[str] = None

class InputCreateMovimiento(BaseModel):
    id_bodega_origen: int
    id_bodega_destino: Optional[int] = None
    id_libro: int
    id_usuario: int
    cantidad_libro: int
    fecha_despacho: Optional[datetime] = None