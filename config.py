"""
Configuración del Sistema de Gestión Escolar

DESCRIPCIÓN:
Archivo centralizado con todas las constantes y configuraciones
del sistema. Cambiar valores aquí afecta toda la aplicación.

SECCIONES:

1. BASE DE DATOS
   - DB_NAME: Nombre del archivo SQLite
   - Ubicación: raíz del proyecto

2. INTERFAZ GRÁFICA
   - WINDOW_WIDTH/HEIGHT: Tamaño ventana principal
   - TABLE_WINDOW_*: Tamaño ventanas de CRUD
   - FORM_WINDOW_*: Tamaño formularios por tipo

3. ESTILOS
   - APP_TITLE: Título de la aplicación
   - FONT_*: Fuentes para diferentes elementos
   - Temas soportados: 'clam' (usado actualmente)

4. DATOS VÁLIDOS
   - GRADOS: Años escolares disponibles
   - ASIGNATURAS: Asignaturas de alumnos
   - ESPECIALIDADES: Áreas de especialización de profesores

CAMBIOS IMPORTANTES:
✓ Grados: Cambió de "1°,2°,3°..." a "1ro,2do,3ro,..."
✓ Secciones: Cambiaron a Asignaturas
✓ Nombre: Cambió de IE4 a Sistema de Gestión Escolar

COMO MODIFICAR:
1. Cambiar valor en este archivo
2. Reiniciar la aplicación
3. El cambio se aplica globalmente

ADVERTENCIA:
- No renombres constantes sin actualizar imports
- GRADOS y ASIGNATURAS deben coincidir con validaciones
- Los cambios a DB_NAME requieren migración de datos
"""

# Configuración de Base de Datos
DB_NAME = "escuela.db"

# Configuración de Interfaz
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

TABLE_WINDOW_WIDTH = 900
TABLE_WINDOW_HEIGHT = 600

FORM_WINDOW_WIDTH = 500
FORM_WINDOW_HEIGHT_ALUMNO = 450
FORM_WINDOW_HEIGHT_PROFESOR = 350

# Estilos
APP_TITLE = "Sistema de Gestión Escolar"
FONT_TITLE = ("Arial", 20, "bold")
FONT_SUBTITLE = ("Arial", 12)
FONT_LABEL = ("Arial", 10)

# Grados disponibles (años escolares)
GRADOS = ["1ro", "2do", "3ro", "4to", "5to", "6to"]

# Asignaturas disponibles (antes llamadas secciones)
ASIGNATURAS = ["Matemáticas", "Lengua", "Ciencias", "Historia", "Educación Física", "Inglés"]

# Especialidades de profesores
ESPECIALIDADES = [
    "Matemáticas",
    "Lengua y Literatura",
    "Ciencias Naturales",
    "Ciencias Sociales",
    "Educación Física",
    "Artes Plásticas",
    "Música",
    "Inglés",
    "Informática"
]

# Mensajes
MSG_SUCCESS = "Operación realizada exitosamente"
MSG_ERROR = "Error en la operación"
MSG_CONFIRM_DELETE = "¿Deseas eliminar este registro?"
MSG_SELECT_RECORD = "Selecciona un registro para continuar"
MSG_NO_RESULTS = "No se encontraron resultados"
