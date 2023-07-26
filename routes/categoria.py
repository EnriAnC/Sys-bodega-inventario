
from fastapi import APIRouter, HTTPException

from repository.categoria import CategoriaRepository


class RouterCategoria(APIRouter):
    
    def __init__(self, categoriaRepository: CategoriaRepository):
        super().__init__()
        self.categoriaRepository = categoriaRepository
        
        
        @self.get("/categorias", tags=['Categoria'])
        def get_all_categorias():
            try:
                resultado = self.categoriaRepository.getAll()
                return resultado
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.post("/categorias", tags=['Categoria'])
        def create_categoria(nombre_categoria):
            try:
                res1 = self.categoriaRepository.getByNombre(nombre_categoria)
                
                if res1[0]["nombre_categoria"] == nombre_categoria:
                    raise Exception("El nombre de la categoria ya existe")
                
                resultado = self.categoriaRepository.create(nombre_categoria)
                return resultado
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))                            
        