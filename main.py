import mysql.connector

class ORM:
    def __init__(self, host, user, password, database, port):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a la base de datos MySQL")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS usuario (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        email VARCHAR(100) NOT NULL UNIQUE
                    )'''
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Tabla creada o ya existe.")
        except mysql.connector.Error as err:
            print(f"Error al crear la tabla: {err}")

    def insert(self, nombre, email):
        query = 'INSERT INTO usuario (nombre, email) VALUES (%s, %s)'
        try:
            self.cursor.execute(query, (nombre, email))
            self.connection.commit()
            print("Usuario insertado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al insertar datos: {err}")

    def get_all(self):
        query = 'SELECT * FROM usuario'
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener datos: {err}")
            return []

    def update(self, user_id, nombre, email):
        query = 'UPDATE usuario SET nombre = %s, email = %s WHERE id = %s'
        try:
            self.cursor.execute(query, (nombre, email, user_id))
            self.connection.commit()
            print("Usuario actualizado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al actualizar usuario: {err}")

    def delete(self, user_id):
        query = 'DELETE FROM usuario WHERE id = %s'
        try:
            self.cursor.execute(query, (user_id,))
            self.connection.commit()
            print("Usuario eliminado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar usuario: {err}")

    def close(self):
        self.connection.close()
        print("Conexión cerrada.")


if __name__ == "__main__":
    # Conectar a la base de datos MySQL en el puerto 3307
    orm = ORM(host="localhost", user="root", password="1234", database="test_db", port=3307)
    
    # Crear la tabla si no existe
    orm.create_table()
    
    # Insertar un nuevo usuario
    orm.insert("Juan David", "juan@email.com")
    
    # Obtener todos los usuarios
    usuarios = orm.get_all()
    print("Usuarios en la base de datos:", usuarios)
    
    # Cerrar la conexión
    orm.close()
