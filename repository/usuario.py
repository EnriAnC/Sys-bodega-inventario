from database.cursor_pg import CursorPG

class UsuarioRepository():
    
    def __init__(self, cursorPG: CursorPG) -> None:
        self.cursorPG = cursorPG

    def create(self, nombre_usuario, email, password, conn=None):
        query = """
            INSERT INTO usuario (id_usuario, nombre_usuario, email, password)
            VALUES (default, %s, %s, %s)
            RETURNING id_usuario, email;
        """
        return self.cursorPG.query(query, (nombre_usuario, email, password,), conn=conn)

    def read(self, id_usuario: int, conn=None):
        query = """
            SELECT * FROM usuario 
            WHERE id_usuario = %s
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)

    def readByEmail(self, email: str, conn=None):
        query = """
            SELECT * FROM usuario 
            WHERE email = %s
        """
        return self.cursorPG.query(query, (email, ), conn=conn)

    def updateEmail(self, id_usuario: int, oldpassword: str, newpassword: str, conn=None):
        query = """
            UPDATE usuario 
            SET password = %s
            WHERE id_usuario = %s and oldpassword = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return self.cursorPG.query(query, (newpassword, id_usuario, oldpassword, ), conn=conn)

    def delete(self, id_usuario: int, conn=None):
        query = """
            DELETE FROM usuario 
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return self.cursorPG.query(query, (id_usuario,), conn=conn)
