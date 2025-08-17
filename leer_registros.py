import sqlite3

class BaseDatos:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexion = sqlite3.connect(nombre)

    def leer_todos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM registros")
        return cursor.fetchall()

    def cerrar(self):
        self.conexion.close()

class ServicioLectura:
    def __init__(self, base_datos):
        self.base_datos = base_datos

    def mostrar_registros(self):
        datos = self.base_datos.leer_todos()
        for fila in datos:
            print(f"ID: {fila[0]}, Valor: {fila[1]}, Categoria: {fila[2]}")

def main():
    base = BaseDatos("registros.db")
    servicio = ServicioLectura(base)
    servicio.mostrar_registros()
    base.cerrar()

if __name__ == "__main__":
    main()