import mysql.connector
import csv
from tkinter import *
from tkinter import filedialog, messagebox

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

    def create_tables(self):
        usuario_query = '''CREATE TABLE IF NOT EXISTS usuario (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL,
                            email VARCHAR(100) NOT NULL UNIQUE,
                            ciudad_id INT,
                            FOREIGN KEY (ciudad_id) REFERENCES ciudad(id)
                        )'''
        ciudad_query = '''CREATE TABLE IF NOT EXISTS ciudad (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(100) NOT NULL
                        )'''
        try:
            self.cursor.execute(ciudad_query)
            self.cursor.execute(usuario_query)
            self.connection.commit()
            print("Tablas creadas o ya existen.")
        except mysql.connector.Error as err:
            print(f"Error al crear las tablas: {err}")

    def insert_user(self, nombre, email, ciudad_id):
        query = 'INSERT INTO usuario (nombre, email, ciudad_id) VALUES (%s, %s, %s)'
        try:
            self.cursor.execute(query, (nombre, email, ciudad_id))
            self.connection.commit()
            print("Usuario insertado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al insertar datos: {err}")

    def insert_city(self, nombre):
        query = 'INSERT INTO ciudad (nombre) VALUES (%s)'
        try:
            self.cursor.execute(query, (nombre,))
            self.connection.commit()
            print("Ciudad insertada exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al insertar ciudad: {err}")

    def get_all_users(self):
        query = '''SELECT usuario.nombre, usuario.email, ciudad.nombre 
                   FROM usuario JOIN ciudad ON usuario.ciudad_id = ciudad.id'''
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener datos: {err}")
            return []

    def get_all_cities(self):
        query = 'SELECT * FROM ciudad'
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener datos: {err}")
            return []

    def close(self):
        self.connection.close()
        print("Conexión cerrada.")

def cargar_csv(orm, tipo):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la primera línea (cabeceras)
            if tipo == "usuarios":
                for row in reader:
                    orm.insert_user(row[0], row[1], row[2])  # Asumimos que CSV tiene nombre, email, ciudad_id
                messagebox.showinfo("Éxito", "Usuarios cargados correctamente.")
            elif tipo == "ciudades":
                for row in reader:
                    orm.insert_city(row[0])  # Asumimos que CSV tiene solo nombre de la ciudad
                messagebox.showinfo("Éxito", "Ciudades cargadas correctamente.")

def mostrar_usuarios(orm):
    usuarios = orm.get_all_users()
    result = "\n".join([f"Nombre: {u[0]}, Email: {u[1]}, Ciudad: {u[2]}" for u in usuarios])
    messagebox.showinfo("Usuarios", result)

def mostrar_ciudades(orm):
    ciudades = orm.get_all_cities()
    result = "\n".join([f"ID: {c[0]}, Nombre: {c[1]}" for c in ciudades])
    messagebox.showinfo("Ciudades", result)

def iniciar_interfaz():
    # Conectar a la base de datos MySQL en el puerto 3307
    orm = ORM(host="localhost", user="root", password="1234", database="test_db", port=3307)
    
    # Crear las tablas
    orm.create_tables()

    # Crear la ventana principal
    root = Tk()
    root.title("ORM con Tkinter")
    root.geometry("400x300")

    # Botón para cargar CSV de usuarios
    btn_cargar_usuarios = Button(root, text="Cargar CSV de Usuarios", command=lambda: cargar_csv(orm, "usuarios"))
    btn_cargar_usuarios.pack(pady=10)

    # Botón para cargar CSV de ciudades
    btn_cargar_ciudades = Button(root, text="Cargar CSV de Ciudades", command=lambda: cargar_csv(orm, "ciudades"))
    btn_cargar_ciudades.pack(pady=10)

    # Botón para mostrar todos los usuarios
    btn_mostrar_usuarios = Button(root, text="Mostrar Usuarios", command=lambda: mostrar_usuarios(orm))
    btn_mostrar_usuarios.pack(pady=10)

    # Botón para mostrar todas las ciudades
    btn_mostrar_ciudades = Button(root, text="Mostrar Ciudades", command=lambda: mostrar_ciudades(orm))
    btn_mostrar_ciudades.pack(pady=10)

    # Iniciar la interfaz gráfica
    root.mainloop()

    # Cerrar la conexión al salir
    orm.close()

if __name__ == "__main__":
    iniciar_interfaz()
