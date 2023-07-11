from typing import Optional

from pydantic import BaseModel


class Informe(BaseModel):
    id_informe: Optional[int] = None
    id_tipoinforme: int
    id_usuario: int
    url_informe: str
