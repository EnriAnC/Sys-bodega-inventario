from typing import Optional

from pydantic import BaseModel


class Categoria(BaseModel):
    id_categoria: Optional[int]
    nombre_categoria: str