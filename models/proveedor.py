from pydantic import BaseModel
from typing import Optional

class Proveedor(BaseModel):
    id_proveedor: Optional[int] = None
    nombre_proveedor: str
    contacto: str
