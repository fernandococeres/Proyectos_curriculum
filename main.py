"""
SISTEMA DE GESTIÓN ESCOLAR
=========================

Aplicación desktop para la gestión integral de estudiantes y docentes en 
instituciones educativas.

ARQUITECTURA: Patrón MVC (Model-View-Controller)
- Models: Definen estructura de datos y operaciones con la base de datos (models/)
- Views: Interfaces gráficas de usuario con Tkinter (views/)
- Controllers: Lógica de negocio y control de flujo de datos (controllers/)

ESTRUCTURA DEL PROYECTO:
- main.py: Punto de entrada de la aplicación
- config.py: Configuración centralizada (BD, ventanas, estilos)
- views/: Interfaces gráficas (main_view.py, views.py, admin_views.py)
- controllers/: Lógica de negocio (controlers.py, admin.py)
- models/: Definiciones de datos (models.py, dbConn.py, validaciones.py)

FLUJO PRINCIPAL:
1. main.py inicializa la ventana Tkinter
2. VentanaPrincipal carga la interfaz principal y menú
3. Usuarios interactúan con vistas (views)
4. Vistas llaman a controladores (controllers)
5. Controladores acceden a base de datos a través de models
6. Validaciones se ejecutan en cada operación (models/validaciones.py)

BASE DE DATOS:
- SQLite (escuela.db)
- Gestión a través de models/dbConn.py
- Tablas: alumnos, profesores

FUNCIONALIDADES:
✓ CRUD Alumnos y Profesores
✓ Búsqueda por DNI
✓ Reportes y estadísticas
✓ Exportación a CSV/Excel
✓ Validación de datos en tiempo real


"""

import tkinter as tk
from views.main_view import VentanaPrincipal

if __name__ == "__main__":
    # Crear ventana raíz de Tkinter
    root = tk.Tk()
    
    # Inicializar la aplicación principal
    app = VentanaPrincipal(root)
    
    # Ejecutar el loop principal de eventos
    root.mainloop()