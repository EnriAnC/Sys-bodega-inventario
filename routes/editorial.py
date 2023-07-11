from fastapi import APIRouter, HTTPException

from repository.editorial import EditorialRepository

from starlette.responses import JSONResponse


class RouterEditorial(APIRouter):
    
    def __init__(self, editorialRepository: EditorialRepository):
        super().__init__()
        self.editorialRepository = editorialRepository
        
        @self.get("/editoriales", tags=['Editoriales'])
        def get_all_editoriales():
            try:
                result = self.editorialRepository.readNRows()
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            
        @self.get("/editoriales/{id_editorial}", tags=['Editoriales'])
        def get_editorial_by_id(id_editorial: int):
            try:
                result = self.editorialRepository.read(id_editorial)
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


        @self.post("/editoriales", tags=['Editoriales'])
        def insert_editorial(
                nombre_editorial: str,
        ):
            try:
                editorial = self.editorialRepository.create(nombre_editorial)
                if not editorial:
                    raise Exception('No es posible insertar editorial')

                return JSONResponse(content={
                    'message': 'Editorial creada correctamente',
                    'data': editorial
                }, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
