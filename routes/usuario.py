from typing import Union

from fastapi import APIRouter, HTTPException, Response
from starlette.responses import JSONResponse

from repository.bodeguero import BodegueroRepository
from repository.jefebodega import JefeBodegaRepository
from repository.perfil_usuario import PerfilUsuarioRepository
from repository.usuario import UsuarioRepository


class RouterUsuario(APIRouter):
    def __init__(self):
        super().__init__()

        @self.get("/usuarios", tags=['Usuarios'])
        def get_usuarios_by_id(id_usuario: int, ):
            result = UsuarioRepository.read(id_usuario)

            if result.__len__() < 1:
                return HTTPException(status_code=404, detail='no existe')

            return JSONResponse(content={
                'message': 'Se ha obtenido el usuario correctamente',
                'data': result
            }, status_code=200)

        @self.post("/login", tags=['Usuarios'])
        def iniciar_sesion(email: str, password: str, response: Response):
            try:
                UsuarioRepository.open_transaction()
                user = UsuarioRepository.readByEmail(email)
                if user.__len__() < 1:
                    raise Exception('No se ha encontrado el usuario')
                if user[0].pop('password') == password:
                    perfil = PerfilUsuarioRepository.read(user[0]['id_usuario'])
                    if perfil:
                        UsuarioRepository.commit()
                        response.set_cookie(key='rol', value=perfil[0]['rol'], max_age=86400)
                        return JSONResponse(content={
                            'message': 'Verificación de usuario y contraseña correcta',
                            'data': perfil
                        }, status_code=200, headers= response.headers)
                    else:
                        raise Exception('El perfil de usuario no existe')
                else:
                    raise Exception('La contraseña no es valida')
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))

        @self.post("/register", tags=['Usuarios'])
        async def registrar_usuario(nombre_usuario: str,
                                    email: str,
                                    password: str,
                                    nombre: str,
                                    apellido_m: str,
                                    rol: str,
                                    apellido_p: Union[str, None] = None, ):
            try:
                UsuarioRepository.open_transaction()

                result1 = UsuarioRepository.create(nombre_usuario, email, password,)
                id_usuario = result1[0]['id_usuario']
                result2 = PerfilUsuarioRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol)
                if rol == 'bodeguero':
                    BodegueroRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol)
                elif rol == 'jefebodega':
                    JefeBodegaRepository.create(id_usuario, nombre, apellido_p, apellido_m, rol)
                else:
                    raise Exception('rol no existente')

                UsuarioRepository.commit()

                return JSONResponse(content={
                    'message': 'Usuario creado correctamente',
                    'data': result2
                }, status_code=200)
            except Exception as e:
                UsuarioRepository.rollback()
                return HTTPException(status_code=500, detail=str(e))
