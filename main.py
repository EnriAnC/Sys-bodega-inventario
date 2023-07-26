from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.cursor_pg import CursorPG
from database.pg_database import PGDatabase

from config.database import POSTGRE_DATABASE_CONFIG, POSTGRE_DATABASE_CONFIG_DEV

from repository.bodega import BodegaRepository
from repository.bodeguero import BodegueroRepository
from repository.editorial import EditorialRepository
from repository.jefebodega import JefeBodegaRepository
from repository.libro import LibroRepository
from repository.movimiento import MovimientoRepository
from repository.perfil_usuario import PerfilUsuarioRepository
from repository.stock import StockRepository
from repository.usuario import UsuarioRepository
from repository.categoria import CategoriaRepository


from routes.bodega import RouterBodega
from routes.editorial import RouterEditorial
from routes.libro import RouterLibro
from routes.movimiento import RouterMovimiento
from routes.usuario import RouterUsuario
from routes.categoria import RouterCategoria


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

postgreDatabase = PGDatabase(POSTGRE_DATABASE_CONFIG)
postgreDatabase.connect()

cursorPG = CursorPG(postgreDatabase)

bodegaRepository = BodegaRepository(cursorPG)
perfilUsuarioRepository = PerfilUsuarioRepository(cursorPG)
usuarioRepository = UsuarioRepository(cursorPG)
bodegueroRepository = BodegueroRepository(cursorPG)
jefeBodegaRepository = JefeBodegaRepository(cursorPG)
libroRepository = LibroRepository(cursorPG)
editorialRepository = EditorialRepository(cursorPG)
movimientoRepository = MovimientoRepository(cursorPG)
stockRepository = StockRepository(cursorPG)

categoriaRepository = CategoriaRepository(cursorPG)

routerBodega = RouterBodega(bodegaRepository, perfilUsuarioRepository)
routerUsuario = RouterUsuario(usuarioRepository, 
                               perfilUsuarioRepository, 
                               bodegueroRepository,
                               jefeBodegaRepository)
routerLibro = RouterLibro(libroRepository, categoriaRepository, stockRepository)
routerEditorial = RouterEditorial(editorialRepository)
routerMovimiento = RouterMovimiento(movimientoRepository, stockRepository)
routerCategoria = RouterCategoria(categoriaRepository)



app.include_router(routerBodega)
app.include_router(routerUsuario)
app.include_router(routerLibro)
app.include_router(routerEditorial)

app.include_router(routerMovimiento)

app.include_router(routerCategoria)

