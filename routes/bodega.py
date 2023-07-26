from fastapi import APIRouter, HTTPException

from starlette.responses import JSONResponse
from models.bodega import Bodega

from repository.bodega import BodegaRepository
from repository.perfil_usuario import PerfilUsuarioRepository

class RouterBodega(APIRouter):
    
    def __init__(self, bodegaRepository: BodegaRepository, perfilUsuarioRepository: PerfilUsuarioRepository):
        super().__init__()
        self.bodegaRepository = bodegaRepository
        self.perfilUsuarioRepository = perfilUsuarioRepository
        
        @self.get("/bodegas", tags=['Bodegas'])
        def get_all_bodegas():
            try:
                result = self.bodegaRepository.readNRows()
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.get("/bodegas/{id_usuario}", tags=['Bodegas'])
        def get_bodega_by_id_usuario(id_usuario: int):
            try:
                result = self.bodegaRepository.getBodegaByUsuario(id_usuario)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


        @self.post("/bodegas", tags=['Bodegas'])
        def insert_bodega( inputBodega: Bodega ):
            id_usuario, nombre_bodega, direccion_bodega = inputBodega.dict().values()
            try:
                perfil = self.perfilUsuarioRepository.read(id_usuario=id_usuario)
                
                if not perfil:
                    raise Exception('No existe usuario')

                if perfil[0]['rol'] != 'jefebodega':
                    raise Exception('No eres el jefe de bodega')

                bodega = self.bodegaRepository.getBodegaByUsuario(id_usuario=id_usuario)

                if bodega is not None and len(bodega) > 0:
                    raise Exception(f'El Jefe de bodega con id {id_usuario} ya pertenece a una bodega')

                new_bodega = self.bodegaRepository.create(id_usuario, nombre_bodega, direccion_bodega, )

                return JSONResponse(content={
                    'message': 'Bodega creada correctamente',
                    'data': new_bodega
                }, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
