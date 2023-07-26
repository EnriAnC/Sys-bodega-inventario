from database.cursor_pg import CursorPG
        
class BodegueroRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, id_usuario: int, nombre: str, apellido_p: str, apellido_m: str, rol: str, conn=None):
        query = """
            INSERT INTO bodeguero (id_usuario, nombre, apellido_p, apellido_m, rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario, nombre, apellido_m, rol;
        """
        return self.cursorPG.query(query, (id_usuario, nombre, apellido_p, apellido_m, rol), conn=conn)

    def getAll(self, conn=None):
        query = """
            SELECT * FROM bodeguero
        """
        return self.cursorPG.query(query, conn=conn)
    
    def read(self, id_usuario: int, conn=None):
        query = """
            SELECT * FROM bodeguero 
            WHERE id_usuario = %s
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)

    def delete(self, id_usuario: int, conn=None):
        query = """
            DELETE FROM bodeguero 
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)