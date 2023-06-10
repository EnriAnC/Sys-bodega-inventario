from datetime import timedelta, datetime
from typing import Union
from typing_extensions import Annotated

from fastapi import APIRouter, HTTPException, Response, Form
from starlette.responses import JSONResponse

from repository.bodeguero import BodegueroRepository
from repository.jefebodega import JefeBodegaRepository
from repository.perfil_usuario import PerfilUsuarioRepository
from repository.usuario import UsuarioRepository

from uuid import uuid4


class RouterUsuario(APIRouter):
    def __init__(self):
        super().__init__()

        @self.get("/usuarios", tags=['Usuarios'])
        def obtener_usuario_por_id(id_usuario: int, ):
            result = UsuarioRepository.read(id_usuario)

            if not result or len(result) == 0:
                return HTTPException(status_code=404, detail='no existe')

            return JSONResponse(content={
                'message': 'Se ha obtenido el usuario correctamente',
                'data': result
            }, status_code=200)

        @self.post("/login", tags=['Usuarios'])
        async def iniciar_sesion(email: Annotated[str, Form()], password: Annotated[str, Form()], response: Response):
            key = str(uuid4())
            conn_transaction = UsuarioRepository.open_transaction(key=key)
            try:
                user = UsuarioRepository.readByEmail(email, conn=conn_transaction)
                if not user and user[0].pop('password') != password:
                    raise HTTPException(status_code=404, detail='El usuario o la contraseña no son válidas')

                perfil = PerfilUsuarioRepository.read(user[0]['id_usuario'], conn=conn_transaction)
                if not perfil or len(perfil) == 0:
                    raise HTTPException(status_code=404, detail='El perfil de usuario no existe')

                response.set_cookie(key='rol', value=perfil[0]['rol'], max_age=86400, secure=True, httponly=True)
                return JSONResponse(content={
                    'message': 'Verificación de usuario y contraseña correcta',
                    'data': perfil
                }, status_code=200, headers= response.headers)
            except Exception as e:
                UsuarioRepository.rollback(conn_transaction)
                return HTTPException(status_code=500, detail=str(e))
            finally:
                UsuarioRepository.release(key=key)

        @self.post("/register", tags=['Usuarios'])
        async def registrar_usuario(nombre_usuario: str,
                                    email: str,
                                    password: str,
                                    nombre: str,
                                    rol: str,
                                    apellido_p: str,
                                    apellido_m: Union[str, None] = None,):
            key = str(uuid4())
            conn_transaction = UsuarioRepository.open_transaction(key=key)
            try:
                result1 = UsuarioRepository.create(nombre_usuario, email, password, conn=conn_transaction)
                id_usuario = result1[0]['id_usuario']
                result2 = PerfilUsuarioRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol, conn=conn_transaction)
                if rol == 'bodeguero':
                    BodegueroRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol, conn=conn_transaction)
                elif rol == 'jefebodega':
                    JefeBodegaRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol, conn=conn_transaction)
                elif rol == 'lector':
                    pass
                else:
                    raise Exception('rol no existente')

                UsuarioRepository.commit(conn_transaction)

                return JSONResponse(content={
                    'message': 'Usuario creado correctamente',
                    'data': result2
                }, status_code=200)
            except Exception as e:
                UsuarioRepository.rollback(conn_transaction)
                return HTTPException(status_code=500, detail=str(e))
            finally:
                UsuarioRepository.release(key=key)
