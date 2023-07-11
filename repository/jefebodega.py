from database.cursor_pg import CursorPG
        
class JefeBodegaRepository():

    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, id_usuario: int, nombre: str, apellido_p: str, apellido_m: str, rol: str, conn=None):
        query = """
            INSERT INTO jefebodega (id_usuario, nombre, apellido_p, apellido_m, rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario, nombre, apellido_m, rol;
        """
        return self.cursorPG.query(query, (id_usuario, nombre, apellido_p, apellido_m, rol), conn=conn)

    def read(self, id_usuario: int, conn=None):
        query = """
            SELECT * FROM jefebodega 
            WHERE id_usuario = %s
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)

    def update_fecha_contrato(self, id_usuario: int, fecha_contrato: str, conn=None):
        query = """
            UPDATE jefebodega 
            SET fecha_contrato = %s
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email, fecha_contrato;
        """
        return self.cursorPG.query(query, (fecha_contrato, id_usuario), conn=conn)

    def delete(self, id_usuario: int, conn=None):
        query = """
            DELETE FROM jefebodega 
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)