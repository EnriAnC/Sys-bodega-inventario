from typing import Union

from fastapi import APIRouter, HTTPException, Response

from starlette.responses import JSONResponse

from models.usuario import LoginUsuario

from repository.bodeguero import BodegueroRepository
from repository.jefebodega import JefeBodegaRepository
from repository.perfil_usuario import PerfilUsuarioRepository
from repository.usuario import UsuarioRepository

from uuid import uuid4


class RouterUsuario(APIRouter):
    def __init__(self, usuarioRepository: UsuarioRepository,
                    perfilUsuarioRepository: PerfilUsuarioRepository,
                    bodegueroRepository: BodegueroRepository,
                    jefeBodegaRepository: JefeBodegaRepository,
                ):
        super().__init__()
        self.usuarioRepository = usuarioRepository
        self.perfilUsuarioRepository = perfilUsuarioRepository
        self.bodegueroRepository = bodegueroRepository
        self.jefeBodegaRepository = jefeBodegaRepository

        @self.get("/usuarios", tags=['Usuarios'])
        def obtener_usuario_por_id(id_usuario: int, ):
            result = self.usuarioRepository.read(id_usuario)

            if not result or len(result) == 0:
                return HTTPException(status_code=404, detail='no existe')

            return JSONResponse(content={
                'message': 'Se ha obtenido el usuario correctamente',
                'data': result
            }, status_code=200)

        @self.post("/login", tags=['Usuarios'])
        async def iniciar_sesion(usuario: LoginUsuario, response: Response):
            email, password = usuario.dict().values()
            key = str(uuid4())
            conn_transaction = self.usuarioRepository.cursorPG.open_transaction(key=key)
            
            try:
                user = self.usuarioRepository.readByEmail(email, conn=conn_transaction)
                if not user and user[0].pop('password') != password:
                    raise HTTPException(status_code=404, detail='El usuario o la contraseña no son válidas')

                perfil = self.perfilUsuarioRepository.read(user[0]['id_usuario'], conn=conn_transaction)
                if not perfil or len(perfil) == 0:
                    raise HTTPException(status_code=404, detail='El perfil de usuario no existe')

                response.set_cookie(key='rol', value=perfil[0]['rol'], max_age=86400, secure=False, httponly=False)
                return JSONResponse(content={
                    'message': 'Verificación de usuario y contraseña correcta',
                    'data': perfil
                }, status_code=200, headers= response.headers)
                
            except Exception as e:
                self.usuarioRepository.cursorPG.rollback(conn_transaction)
                return HTTPException(status_code=500, detail=str(e))
            finally:
                self.usuarioRepository.cursorPG.release(key=key)

        @self.post("/register", tags=['Usuarios'])
        async def registrar_usuario(nombre_usuario: str,
                                    email: str,
                                    password: str,
                                    nombre: str,
                                    rol: str,
                                    apellido_p: str,
                                    apellido_m: Union[str, None] = None,):
            key = str(uuid4())
            conn_transaction = self.usuarioRepository.cursorPG.open_transaction(key=key)
            try:
                newUsuario = self.usuarioRepository.create(nombre_usuario, email, password, conn=conn_transaction)
                id_usuario = newUsuario[0]['id_usuario']
                newPerfilUsuario = self.perfilUsuarioRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol, conn=conn_transaction)
                if rol == 'bodeguero':
                    self.bodegueroRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol, conn=conn_transaction)
                elif rol == 'jefebodega':
                    self.jefeBodegaRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol, conn=conn_transaction)
                elif rol == 'lector':
                    pass
                else:
                    raise Exception('rol no existente')

                self.usuarioRepository.commit(conn_transaction)

                return JSONResponse(content={
                    'message': 'Usuario creado correctamente',
                    'data': newPerfilUsuario
                }, status_code=200)
            except Exception as e:
                self.usuarioRepository.cursorPG.rollback(conn_transaction)
                return HTTPException(status_code=500, detail=str(e))
            finally:
                self.usuarioRepository.cursorPG.release(key=key)
                
                
