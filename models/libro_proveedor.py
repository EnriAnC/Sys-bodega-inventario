from pydantic import BaseModel


class LibroProveedor(BaseModel):
    id_libro: int
    id_proveedor: int
