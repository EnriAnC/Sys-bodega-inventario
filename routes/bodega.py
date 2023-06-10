from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from repository.bodega import BodegaRepository
from repository.perfil_usuario import PerfilUsuarioRepository

router = APIRouter()


@router.get("/bodegas", tags=['Bodegas'])
def get_all_bodegas():
    try:
        result = BodegaRepository.readNRows()
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
        perfil = PerfilUsuarioRepository.read(id_usuario=id_usuario)
        print(perfil)
        if not perfil:
            raise Exception('No existe usuario')

        if perfil[0]['rol'] != 'jefebodega':
            raise Exception('No eres el jefe de bodega')

        bodega = BodegaRepository.getByUsuarioId(id_usuario=id_usuario)

        if bodega is not None and len(bodega) > 0:
            raise Exception(f'El Jefe de bodega con id {id_usuario} ya pertenece a una bodega')

        result = BodegaRepository.create(id_usuario, nombre_bodegea, direccion_bodegea, )

        return JSONResponse(content={
            'message': 'Bodega creada correctamente',
            'data': result
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
