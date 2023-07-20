from database.cursor_pg import CursorPG


class StockRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, id_bodega: int, id_libro: str, stock: str, conn=None):
        query = """
            INSERT INTO stock (id_bodega, id_libro, stock)
            VALUES (%s, %s, %s)
            RETURNING id_bodega, id_libro, stock;
        """
        return self.cursorPG.query(query, (id_bodega, id_libro, stock), conn=conn)
    
    def read(self, id_bodega: int, conn=None):
        query = """
            SELECT * FROM stock 
            WHERE id_bodega = %s
        """
        return self.cursorPG.query(query, (id_bodega, ), conn=conn)

    def readNRows(self, n = 10, conn=None):
        query = """
            SELECT * FROM stock
            FETCH FIRST %s ROWS ONLY
        """
        return self.cursorPG.query(query, (n,), conn=conn)

    def delete(self, id_bodega: int, conn=None):
        query = """
            DELETE FROM stock 
            WHERE id_bodega = %s
            RETURNING id_bodega, id_libro, stock;
        """
        return self.cursorPG.query(query, (id_bodega,), conn=conn)
    
    def increment_stock_bodega(self, id_bodega: int, id_libro: int, cantidad_libros: int, conn=None):
        query = """
            UPDATE stock 
            SET stock = stock + %s
            WHERE id_bodega = %s
            AND id_libro = %s
            RETURNING id_bodega, id_libro, stock;
        """
        return self.cursorPG.query(query, (cantidad_libros, id_bodega, id_libro), conn=conn)
    
    def decrement_stock_bodega(self, id_bodega: int, id_libro: int, cantidad_libros: int, conn=None):
        query = """
            UPDATE stock 
            SET stock = stock - %s
            WHERE id_bodega = %s
            AND id_libro = %s
            RETURNING id_bodega, id_libro, stock;
        """
        return self.cursorPG.query(query, (cantidad_libros, id_bodega, id_libro), conn=conn)