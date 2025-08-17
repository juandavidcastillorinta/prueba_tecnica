# Prueba Técnica - Desarrollador/a de Software Jr

## Requisitos y ejecución
- **Tecnologías**: Python 3.x, SQLite.
- **Dependencias**: `requests` (instalar con `pip install requests`).
- **Variables de entorno**: No se requieren.

### Pasos para ejecutar
1. Clonar el repositorio o descomprimir el .zip.
2. Instalar las dependencias con `pip install -r requirements.txt` (crear archivo si es necesario).
3. Ejecutar `python main.py` para realizar la carga inicial y los barridos.

### Proceso de carga y barridos
- La carga inicial realiza 100 llamadas a la API y guarda los resultados en la base de datos.
- Los barridos mejoran los registros 'bad' hasta convertirlos en 'medium' o 'good'.

### Endpoints CRUD
- No se implementa interfaz web, pero las operaciones CRUD están disponibles en el servicio:
  - Crear: `servicio.crear_registro(valor, categoria)`
  - Editar: `servicio.editar_registro(id, valor, categoria)`
  - Eliminar: `servicio.eliminar_registro(id)`
- Probar con scripts personalizados o modificar `main.py`.