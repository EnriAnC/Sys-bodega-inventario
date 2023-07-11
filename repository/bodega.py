from database.cursor_pg import CursorPG

class BodegaRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, id_usuario: int, nombre_bodega: str, direccion_bodega: str, conn=None):
        query = """
            INSERT INTO bodega (id_bodega, id_usuario, nombre_bodega, direccion_bodega)
            VALUES (default, %s, %s, %s)
            RETURNING id_bodega, id_usuario, nombre_bodega, direccion_bodega;
        """
        return self.cursorPG.query(query, (id_usuario, nombre_bodega, direccion_bodega), conn=conn)

    def read(self, id_bodega: int, conn=None):
        query = """
            SELECT * FROM bodega 
            WHERE id_bodega = %s
        """
        return self.cursorPG.query(query, (id_bodega, ), conn=conn)

    def readNRows(self, n = 10, conn=None):
        query = """
            SELECT * FROM bodega
            FETCH FIRST %s ROWS ONLY
        """
        return self.cursorPG.query(query, (n,), conn=conn)

    def getBodegaByUsuario(self, id_usuario, conn=None):
        query = """
            SELECT * FROM bodega 
            WHERE id_usuario = %s
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)

    def delete(self, id_usuario: int, conn=None):
        query = """
            DELETE FROM bodega 
            WHERE id_bodega = %s
            RETURNING id_bodega, id_usuario, nombre_bodega, direccion_bodega;
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)
