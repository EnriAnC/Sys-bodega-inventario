from pydantic import BaseModel


class Stock(BaseModel):
    id_bodega: int
    id_libro: int
    stock: int
