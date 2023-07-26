from typing import Optional

from pydantic import BaseModel


class Libro(BaseModel):
    id_libro: Optional[int] = None
    id_editorial: int
    nombre_libro: str
    autor: str

class InputLibro(BaseModel):
    id_categoria: int
    id_editorial: int
    id_bodega: int
    stock: int
    nombre_libro: str
    autor: str