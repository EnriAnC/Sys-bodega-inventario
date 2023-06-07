from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from repository.bodega import BodegaRepository

router = APIRouter()


@router.get("/bodegas", tags=['Bodegas'])
def get_all_bodegas(id_bodega: int):
    try:
        result = BodegaRepository.read(id_bodega)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bodegas", tags=['Bodegas'])
def insert_bodega(
        id_usuario: int,
        nombre_bodegea: str,
        direccion_bodegea: str,
):
    try:
        result = BodegaRepository.create(id_usuario, nombre_bodegea, direccion_bodegea, )
        return JSONResponse(content={
            'message': 'Bodega creada correctamente',
            'data': result
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
