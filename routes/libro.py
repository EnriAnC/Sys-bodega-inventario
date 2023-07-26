from fastapi import APIRouter, HTTPException
from models.libro import InputLibro
from repository.categoria import CategoriaRepository

from repository.libro import LibroRepository

from starlette.responses import JSONResponse

from repository.stock import StockRepository


class RouterLibro(APIRouter):
    
    def __init__(self, libroRepository: LibroRepository, 
                 categoriaRepository: CategoriaRepository,
                 stockRepository: StockRepository):
        super().__init__()
        self.libroRepository = libroRepository
        self.categoriaRepository = categoriaRepository
        self.stockRepository = stockRepository
        
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
            
        @self.get("/libros/{id_libro}/stock", tags=['Libros'])
        def get_stock_libro_by_id(id_libro: int):
            try:
                result = self.libroRepository.get_stock_by_libro_id(id_libro)
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


        @self.post("/libros/bodega", tags=['Libros'])
        def insert_libro_in_bodega( inputLibro: InputLibro ):
            id_categoria, id_editorial, id_bodega, stock, nombre_libro, autor = inputLibro.dict().values()
            try:
                print(id_categoria, id_editorial, id_bodega, nombre_libro, stock, autor)
                libro = self.libroRepository.create(id_editorial, nombre_libro, autor)
                new_id_libro = libro[0]['id_libro']
                self.categoriaRepository.insertLibroInCategory(new_id_libro, id_categoria)
                self.stockRepository.create(id_bodega, new_id_libro, stock)
                if not libro:
                    raise Exception('No es posible insertar libro')

                return JSONResponse(content={
                    'message': 'Libro registrado correctamente',
                    'data': libro
                }, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
