from typing import Optional

from pydantic import BaseModel


class Editorial(BaseModel):
    id_editorial: Optional[int] = None
    nombre_editorial: str
