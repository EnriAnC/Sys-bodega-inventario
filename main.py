from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.bodega import router as bodega_router
# from routes.proveedor import router as proveedor_router
from routes.usuario import RouterUsuario


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(bodega_router)
# app.include_router(proveedor_router)
app.include_router(RouterUsuario())


@app.get("/")
async def root():
    return {"message": "Hello World"}
