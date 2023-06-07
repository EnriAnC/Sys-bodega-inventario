from pydantic import BaseModel


class Stock(BaseModel):
    id_usuario: int
    id_bodega: int
    id_libro: int
    id_stock: int
