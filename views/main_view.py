"""
Ventana principal del Sistema de Gestión Escolar

DESCRIPCIÓN:
Define la interfaz principal de la aplicación. Es el primer punto de contacto
del usuario con el sistema. Proporciona acceso a todos los módulos principales
a través de un menú y botones.

FLUJO:
1. Se instancia en main.py
2. Crea la ventana raíz y menú de navegación
3. Usuario elige entre Gestión (CRUD) o Administración (reportes)
4. Cada opción abre una nueva ventana específica

MÓDULOS ACCESIBLES:
- Gestión de Alumnos: CRUD de estudiantes, búsqueda por DNI
- Gestión de Profesores: CRUD de docentes
- Administración de Alumnos: Estadísticas, reportes, exportación
- Administración de Profesores: Estadísticas, reportes, exportación

MENÚ:
- Tablas: Acceso rápido a Alumnos, Profesores, Salir
- Administración: Panel administrativo
- Ayuda: Información del sistema

ESTILOS:
Usa ttk (Themed Tkinter) para interfaz moderna y consistente.
Tema utilizado: 'clam'
"""
import tkinter as tk
from tkinter import Menu, messagebox, ttk
from views.centrar_ventana import centrar_ventana
from views.views import VentanaAlumnos, VentanaProfesores
from views.admin_views import AdminAlumnosView, AdminProfesoresView
from views.tema import aplicar_tema_oscuro
from config import WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE

class VentanaPrincipal:
    """Ventana principal del sistema con menú de navegación.
    
    Responsabilidades:
    - Crear la interfaz principal
    - Gestionar el menú de navegación
    - Abrir ventanas secundarias
    - Cerrar la aplicación
    
    Atributos:
        root (tk.Tk): Ventana raíz de Tkinter
        style (ttk.Style): Gestor de estilos
    """
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        centrar_ventana(self.root, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Aplicar tema oscuro (centralizado)
        self.colores, self.style = aplicar_tema_oscuro(self.root, self.style)
        
        self.crear_menu()
        self.crear_interfaz()
        
    def abrir_alumnos(self):
        VentanaAlumnos(self.root)
        
    def abrir_profesores(self):
        VentanaProfesores(self.root)
        
    def abrir_admin_alumnos(self):
        AdminAlumnosView(self.root)
        
    def abrir_admin_profesores(self):
        AdminProfesoresView(self.root)
        
    def salir(self):
        if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
            self.root.destroy()
            
    def about(self):
        messagebox.showinfo("Acerca de", 
            "Sistema de Gestión Escolar\nv1.0\n\n"
            "Sistema de gestión de alumnos y profesores\n"
            "para instituciones educativas\n\n"
            "Autor: Fernando Cóceres")
            
    def crear_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
        menu_tablas = Menu(menu_bar, tearoff=0)
        menu_tablas.add_command(label="Alumnos", command=self.abrir_alumnos)
        menu_tablas.add_command(label="Profesores", command=self.abrir_profesores)
        menu_tablas.add_separator()
        menu_tablas.add_command(label="Salir", command=self.salir)
        menu_bar.add_cascade(label="Tablas", menu=menu_tablas)
        
        menu_admin = Menu(menu_bar, tearoff=0)
        menu_admin.add_command(label="Administración de Alumnos", command=self.abrir_admin_alumnos)
        menu_admin.add_command(label="Administración de Profesores", command=self.abrir_admin_profesores)
        menu_bar.add_cascade(label="Administración", menu=menu_admin)
        
        menu_ayuda = Menu(menu_bar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.about)
        menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
        
    def crear_interfaz(self):
        marco_principal = ttk.Frame(self.root, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(marco_principal, text="Sistema de Gestión Escolar", font=("Arial", 20, "bold")).pack(pady=20)
        ttk.Label(marco_principal, text="Bienvenido al sistema de gestión de estudiantes y profesores", font=("Arial", 12)).pack(pady=10)
        
        frame_gestion = ttk.LabelFrame(marco_principal, text="GESTIÓN", padding="15")
        frame_gestion.pack(pady=10, fill=tk.X, padx=10)
        
        ttk.Button(frame_gestion, text="Gestionar Alumnos", command=self.abrir_alumnos, width=25).pack(pady=8, side=tk.LEFT, padx=10)
        ttk.Button(frame_gestion, text="Gestionar Profesores", command=self.abrir_profesores, width=25).pack(pady=8, side=tk.LEFT, padx=10)
        
        frame_admin = ttk.LabelFrame(marco_principal, text="ADMINISTRACIÓN", padding="15")
        frame_admin.pack(pady=10, fill=tk.X, padx=10)
        
        ttk.Button(frame_admin, text="📊 Admin Alumnos", command=self.abrir_admin_alumnos, width=25).pack(pady=8, side=tk.LEFT, padx=10)
        ttk.Button(frame_admin, text="📊 Admin Profesores", command=self.abrir_admin_profesores, width=25).pack(pady=8, side=tk.LEFT, padx=10)