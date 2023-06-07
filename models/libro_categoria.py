from pydantic import BaseModel


class LibroCategoria(BaseModel):
    id_libro: int
    id_categoria: int
