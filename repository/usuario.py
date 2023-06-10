from database.cursor_pg import CursorPG


class UsuarioRepository(CursorPG):

    @classmethod
    def create(cls, nombre_usuario, email, password, conn=None):
        query = """
            INSERT INTO usuario (id_usuario, nombre_usuario, email, password)
            VALUES (default, %s, %s, %s)
            RETURNING id_usuario, email;
        """
        return cls._query(query, (nombre_usuario, email, password,), conn=conn)

    @classmethod
    def read(cls, id_usuario: int, conn=None):
        query = """
            SELECT * FROM usuario 
            WHERE id_usuario = %s
        """
        return cls._query(query, (id_usuario,), conn=conn)

    @classmethod
    def readByEmail(cls, email: str, conn=None):
        query = """
            SELECT * FROM usuario 
            WHERE email = %s
        """
        return cls._query(query, (email, ), conn=conn)

    @classmethod
    def updateEmail(cls, id_usuario: int, oldpassword: str, newpassword: str, conn=None):
        query = """
            UPDATE usuario 
            SET password = %s
            WHERE id_usuario = %s and oldpassword = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return cls._query(query, (newpassword, id_usuario, oldpassword, ), conn=conn)

    @classmethod
    def delete(cls, id_usuario: int, conn=None):
        query = """
            DELETE FROM usuario 
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return cls._query(query, (id_usuario,), conn=conn)
