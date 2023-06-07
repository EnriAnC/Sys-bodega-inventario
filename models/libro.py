from typing import Optional

from pydantic import BaseModel


class Libro(BaseModel):
    id_libro: Optional[int]
    id_editorial: int
    nombre_libro: str
    autor: str
