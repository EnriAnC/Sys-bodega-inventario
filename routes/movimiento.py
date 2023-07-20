from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

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
        def insert_movimiento(
                id_bodega_origen,
                id_bodega_destino, 
                id_libro, 
                id_usuario, 
                cantidad_libro,
                fecha_despacho = datetime.now(timezone.utc)
        ):
            try:
                
                res1 = self.stockRepository.decrement_stock_bodega(id_bodega_origen, id_libro, cantidad_libro)
                print(res1)
                if res1[0]["stock"] < 0:
                    self.stockRepository.increment_stock_bodega(id_bodega_origen, id_libro, cantidad_libro)
                    raise Exception("El stock no puede queda menor a 0")
                
                res2 = self.stockRepository.increment_stock_bodega(id_bodega_destino, id_libro, cantidad_libro)
                print(res2)
                if res2 is None or len(res2) == 0:
                    res3 = self.stockRepository.create(id_bodega_destino, id_libro, cantidad_libro)
                    print(res3)
                
                movimiento = self.movimientoRepository.create(id_bodega_destino, id_libro, id_usuario, fecha_despacho, cantidad_libro)
                print(movimiento)
                
                if movimiento is None or len(movimiento)==0:
                    raise Exception('No es posible insertar movimiento')
                
                
                respuesta = {
                    'message': 'Movimiento creada correctamente',
                    'data': movimiento
                }

                return respuesta
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.get("/movimientos/{id_movimiento}", tags=['movimientos'])
        def get_movimiento_by_id(id_movimiento: int):
            try:
                result = self.movimientoRepository.read(id_movimiento)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


        
