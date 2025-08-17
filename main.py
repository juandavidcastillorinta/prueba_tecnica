import sqlite3
import requests
import time
from typing import Dict, List

class BaseDatos:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexion = sqlite3.connect(nombre)
        self.crear_tabla()

    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, valor INTEGER, categoria TEXT)''')
        self.conexion.commit()

    def guardar(self, valor, categoria):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO registros (valor, categoria) VALUES (?, ?)", (valor, categoria))
        self.conexion.commit()

    def obtener_todos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM registros")
        return cursor.fetchall()

    def actualizar(self, id, valor, categoria):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE registros SET valor = ?, categoria = ? WHERE id = ?", (valor, categoria, id))
        self.conexion.commit()

    def eliminar(self, id):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM registros WHERE id = ?", (id,))
        self.conexion.commit()

class ClienteAPI:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.url = f"https://4advance.co/testapi/get.php?user_id={id_usuario}"

    def obtener_datos(self):
        try:
            respuesta = requests.get(self.url, timeout=10)
            respuesta.raise_for_status()
            datos = respuesta.json()
            return datos
        except requests.RequestException:
            time.sleep(1)
            return self.obtener_datos()

class ServicioDominio:
    def __init__(self, cliente_api, base_datos):
        self.cliente_api = cliente_api
        self.base_datos = base_datos

    def cargar_inicial(self, cantidad):
        for _ in range(cantidad):
            datos = self.cliente_api.obtener_datos()
            self.base_datos.guardar(datos['value'], datos['category'])

    def mejorar_registros(self):
        registros = self.base_datos.obtener_todos()
        barridos = 0
        total_intentos = 0

        while any(reg[2] == 'bad' for reg in registros):
            barridos += 1
            for reg in registros:
                if reg[2] == 'bad':
                    total_intentos += 1
                    nuevos_datos = self.cliente_api.obtener_datos()
                    if nuevos_datos['category'] in ['medium', 'good']:
                        self.base_datos.actualizar(reg[0], nuevos_datos['value'], nuevos_datos['category'])
            registros = self.base_datos.obtener_todos()
            time.sleep(1)  # Evitar ráfagas

        return barridos, total_intentos

    def crear_registro(self, valor, categoria):
        self.base_datos.guardar(valor, categoria)

    def editar_registro(self, id, valor, categoria):
        self.base_datos.actualizar(id, valor, categoria)

    def eliminar_registro(self, id):
        self.base_datos.eliminar(id)

def main():
    base = BaseDatos("registros.db")
    api = ClienteAPI("J54GF1")
    servicio = ServicioDominio(api, base)
    servicio.cargar_inicial(100)
    barridos, intentos = servicio.mejorar_registros()
    registros = base.obtener_todos()
    categorias = {'bad': 0, 'medium': 0, 'good': 0}
    for reg in registros:
        categorias[reg[2]] += 1

    print(f"Barridos: {barridos}, Intentos totales: {intentos + 100}, Distribución: {categorias}")

if __name__ == "__main__":
    main()