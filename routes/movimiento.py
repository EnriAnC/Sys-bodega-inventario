from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from models.movimiento import InputCreateMovimiento

from repository.movimiento import MovimientoRepository

from starlette.responses import JSONResponse

from repository.stock import StockRepository


class RouterMovimiento(APIRouter):
    
    def __init__(self, movimientoRepository: MovimientoRepository, stockRepository: StockRepository):
        super().__init__()
        self.movimientoRepository = movimientoRepository
        self.stockRepository = stockRepository
        
        @self.get("/movimientos", tags=['movimientos'])
        def get_all_movimientos():
            try:
                result = self.movimientoRepository.readNRows(20)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.post("/movimientos", tags=['movimientos'])
        def insert_movimiento( inputCreateMovimiento: InputCreateMovimiento ):
            try:
                
                id_bodega_origen, id_bodega_destino, id_libro, id_usuario, cantidad_libro, fecha_despacho = inputCreateMovimiento.dict().values()
                
                if cantidad_libro <= 0:
                    raise Exception("La cantidad de libros debe ser mayor a 0")
                
                if fecha_despacho is None:
                    fecha_despacho = datetime.now(timezone.utc)
                
                res1 = self.stockRepository.decrement_stock_bodega(id_bodega_origen, id_libro, cantidad_libro)
                if res1[0]["stock"] < 0:
                    self.stockRepository.increment_stock_bodega(id_bodega_origen, id_libro, cantidad_libro)
                    raise Exception("El stock no puede queda menor a 0")
                
                res2 = self.stockRepository.increment_stock_bodega(id_bodega_destino, id_libro, cantidad_libro)
                if res2 is None or len(res2) == 0:
                    self.stockRepository.create(id_bodega_destino, id_libro, cantidad_libro)
                
                movimiento = self.movimientoRepository.create(id_bodega_destino, id_libro, id_usuario, fecha_despacho, cantidad_libro)
                
                if movimiento is None or len(movimiento)==0:
                    raise Exception('No es posible insertar movimiento')
                
                respuesta = {
                    'message': 'Movimiento creado correctamente',
                    'data': movimiento
                }

                return respuesta
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.put("/movimientos", tags=['movimientos'])
        def update_fecha_ingreso( id_movimiento: int, fecha_ingreso: int ):
            try:
                result = self.movimientoRepository.update_fecha_ingreso(id_movimiento, fecha_ingreso)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
            
        @self.post
            
        @self.get("/movimientos/{id_movimiento}", tags=['movimientos'])
        def get_movimiento_by_id(id_movimiento: int):
            try:
                result = self.movimientoRepository.read(id_movimiento)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


        
