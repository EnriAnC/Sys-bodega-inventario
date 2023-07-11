from fastapi import APIRouter, HTTPException

from repository.libro import LibroRepository

from starlette.responses import JSONResponse


class RouterLibro(APIRouter):
    
    def __init__(self, libroRepository: LibroRepository):
        super().__init__()
        self.libroRepository = libroRepository
        
        @self.get("/libros", tags=['Libros'])
        def get_all_libros():
            try:
                result = self.libroRepository.readNRows(20)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.get("/libros/{id_libro}", tags=['Libros'])
        def get_libro_by_id(id_libro: int):
            try:
                result = self.libroRepository.read(id_libro)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.get("/libros/bodega/{id_bodega}", tags=['Libros'])
        def get_libro_by_bodega(id_bodega: int):
            try:
                result = self.libroRepository.getByBodegaId(id_bodega)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


        @self.post("/libros", tags=['Libros'])
        def insert_libro(
                id_editorial: int,
                nombre_libro: str,
                autor: str,
        ):
            try:
                libro = self.libroRepository.create(id_editorial, nombre_libro, autor)
                if not libro:
                    raise Exception('No es posible insertar libro')

                return JSONResponse(content={
                    'message': 'Bodega creada correctamente',
                    'data': libro
                }, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
