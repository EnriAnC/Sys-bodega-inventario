from fastapi import APIRouter, HTTPException

from repository.movimiento import MovimientoRepository

from starlette.responses import JSONResponse


class RouterMovimiento(APIRouter):
    
    def __init__(self, movimientoRepository: MovimientoRepository):
        super().__init__()
        self.movimientoRepository = movimientoRepository
        
        @self.get("/movimientos", tags=['movimientos'])
        def get_all_movimientos():
            try:
                result = self.movimientoRepository.readNRows()
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.get("/movimientos/{id_movimiento}", tags=['movimientos'])
        def get_movimiento_by_id(id_movimiento: int):
            try:
                result = self.movimientoRepository.read(id_movimiento)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


        @self.post("/movimientos", tags=['movimientos'])
        def insert_movimiento(
                id_bodega, 
                id_libro, 
                id_usuario, 
                fecha_despacho, 
                cantidad_libro
        ):
            try:
                movimiento = self.movimientoRepository.create(id_bodega, id_libro, id_usuario, fecha_despacho, cantidad_libro)
                if not movimiento:
                    raise Exception('No es posible insertar movimiento')

                return JSONResponse(content={
                    'message': 'Bodega creada correctamente',
                    'data': movimiento
                }, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
