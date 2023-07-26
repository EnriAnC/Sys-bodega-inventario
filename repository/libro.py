from database.cursor_pg import CursorPG


class LibroRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, id_editorial: int, nombre_libro: str, autor: str, conn=None):
        query = """
            INSERT INTO libro (id_libro, id_editorial, nombre_libro, autor)
            VALUES (default, %s, %s, %s)
            RETURNING id_libro, id_editorial, nombre_libro, autor;
        """
        return self.cursorPG.query(query, (id_editorial, nombre_libro, autor), conn=conn)
    
    def read(self, id_libro: int, conn=None):
        query = """
            SELECT * FROM libro 
            WHERE id_libro = %s
        """
        return self.cursorPG.query(query, (id_libro, ), conn=conn)
    
    def getByBodegaId(self, id_bodega: int, conn=None):
        query = """
            SELECT * FROM libro
            natural join stock 
            WHERE id_bodega = %s
        """
        return self.cursorPG.query(query, (id_bodega, ), conn=conn)
    
    def get_stock_by_libro_id(self, id_libro: int, conn=None):
        query = """
            SELECT * FROM stock 
            WHERE id_libro = %s
        """
        return self.cursorPG.query(query, (id_libro, ), conn=conn)

    def readNRows(self, n = 10, conn=None):
        query = """
            SELECT * FROM libro
            FETCH FIRST %s ROWS ONLY
        """
        return self.cursorPG.query(query, (n,), conn=conn)

    def delete(self, id_usuario: int, conn=None):
        query = """
            DELETE FROM libro 
            WHERE id_libro = %s
            RETURNING id_bodega, id_usuario, nombre_bodega, direccion_bodega;
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)