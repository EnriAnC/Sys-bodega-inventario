from pydantic import BaseModel
from typing import Optional

class Proveedor(BaseModel):
    id_proveedor: Optional[int]
    nombre_proveedor: str
    contacto: str
