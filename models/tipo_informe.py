from typing import Optional

from pydantic import BaseModel


class TipoInforme(BaseModel):
    id_tipoinforme: Optional[int]
    nombre_tipoinformr: str
