from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from database.cursor_pg import CursorPG
from models.proveedor import Proveedor

router = APIRouter()


@router.get("/proveedores", tags=['Proveedores'])
def get_all_proveedores():
    try:
        query = 'SELECT * FROM proveedor'
        results = CursorPG.execute_query(query)

        return JSONResponse(content={
            'message':'Consulta realizada correctamente',
            'data': results
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/proveedores/{id_proveedor}", tags=['Proveedores'])
async def get_proveedor_by_id(id_proveedor: int):
    try:
        query = """
            SELECT *
            FROM proveedor
            WHERE id_proveedor = %s
        """
        result = CursorPG.execute_query(query, (id_proveedor, ))
        if result:
            return JSONResponse(content={
                'message': 'Consulta realizada correctamente',
                'data': result
            }, status_code=200)
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/proveedores", tags=['Proveedores'])
async def insert_proveedor(proveedor: Proveedor):
    try:
        query = """
                INSERT INTO proveedor (id_proveedor, nombre_proveedor, contacto)
                VALUES (default, %s, %s)
                RETURNING id_proveedor, nombre_proveedor, contacto;
                """
        result = CursorPG.execute_query(query, (proveedor.nombre_proveedor, proveedor.contacto, ))
        return JSONResponse(content={
            'message': 'Se ha añadido un proveedor correctamente',
            'data': result
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


