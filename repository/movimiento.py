from database.cursor_pg import CursorPG


class MovimientoRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, id_bodega: int, id_libro: int, id_usuario: int, fecha_despacho: str, cantidad_libro: int, conn=None):
        query = """
            INSERT INTO movimiento 
            (id_movimiento, id_bodega, id_libro, id_usuario, fecha_despacho, cantidad_libro)
            VALUES (default, %s, %s, %s, %s, %s)
            RETURNING id_movimiento, id_bodega, id_libro, id_usuario, fecha_despacho, cantidad_libro;
        """
        return self.cursorPG.query(query, (id_bodega, id_libro, id_usuario, fecha_despacho, cantidad_libro), conn=conn)
    
    def read(self, id_bodega: int, conn=None):
        query = """
            SELECT * FROM movimiento 
            WHERE id_movimiento = %s
        """
        return self.cursorPG.query(query, (id_bodega, ), conn=conn)

    def readNRows(self, n = 10, conn=None):
        query = """
            SELECT * FROM movimiento
            FETCH FIRST %s ROWS ONLY
        """
        return self.cursorPG.query(query, (n,), conn=conn)

    def delete(self, id_usuario: int, conn=None):
        query = """
            DELETE FROM movimiento 
            WHERE id_movimiento = %s
            RETURNING id_movimiento, id_bodega, id_libro, id_usuario, cantidad_libro;
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)