from database.cursor_pg import CursorPG


class EditorialRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, nombre_editorial: str, conn=None):
        query = """
            INSERT INTO editorial (id_editorial, nombre_editorial)
            VALUES (default, %s)
            RETURNING id_editorial, nombre_editorial;
        """
        return self.cursorPG.query(query, (nombre_editorial), conn=conn)
    
    def read(self, id_editorial: int, conn=None):
        query = """
            SELECT * FROM editorial 
            WHERE id_editorial = %s
        """
        return self.cursorPG.query(query, (id_editorial, ), conn=conn)

    def readNRows(self, n = 10, conn=None):
        query = """
            SELECT * FROM editorial
            FETCH FIRST %s ROWS ONLY
        """
        return self.cursorPG.query(query, (n,), conn=conn)

    def delete(self, id_editorial: int, conn=None):
        query = """
            DELETE FROM editorial 
            WHERE id_editorial = %s
            RETURNING id_editorial, nombre_editorial;
        """
        return self.cursorPG.query(query, (id_editorial,), conn=conn)