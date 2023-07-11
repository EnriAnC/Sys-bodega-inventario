from typing import Optional

from pydantic import BaseModel


class TipoInforme(BaseModel):
    id_tipoinforme: Optional[int] = None
    nombre_tipoinformr: str
