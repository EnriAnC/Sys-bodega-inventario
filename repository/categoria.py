from database.cursor_pg import CursorPG

class CategoriaRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, nombre_categoria: str, conn=None):
        query = """
            INSERT INTO categoria (id_categoria, nombre_categoria)
            VALUES (default, %s)
            RETURNING id_categoria, nombre_categoria;
        """
        return self.cursorPG.query(query, (nombre_categoria, ), conn=conn)
    
    def insertLibroInCategory(self, id_libro: int, id_categoria: int, conn=None):
        query = """
            INSERT INTO libro_categoria (id_libro, id_categoria)
            VALUES (%s, %s)
            RETURNING id_libro, id_categoria ;
        """
        return self.cursorPG.query(query, (id_libro, id_categoria, ), conn=conn)
    
    
    def getAll(self, conn=None):
        query = """
            SELECT * FROM categoria 
        """
        return self.cursorPG.query(query, conn=conn)
    
    def getByNombre(self, nombre_categoria: str, conn=None):
        query = """
            SELECT * FROM categoria 
            where nombre_categoria = %s
        """
        return self.cursorPG.query(query, (nombre_categoria, ), conn=conn)

    def read(self, id_categoria: int, conn=None):
        query = """
            SELECT * FROM categoria 
            WHERE id_categoria = %s
        """
        return self.cursorPG.query(query, (id_categoria, ), conn=conn)

    def readNRows(self, n = 10, conn=None):
        query = """
            SELECT * FROM categoria
            FETCH FIRST %s ROWS ONLY
        """
        return self.cursorPG.query(query, (n,), conn=conn)

    def delete(self, id_categoria: int, conn=None):
        query = """
            DELETE FROM categoria 
            WHERE id_categoria = %s
            RETURNING id_categoria, nombre_categoria;
        """
        return self.cursorPG.query(query, (id_categoria,), conn=conn)
