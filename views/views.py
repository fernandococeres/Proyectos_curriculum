"""
Vistas (interfaces gráficas) para el Sistema de Gestión Escolar

DESCRIPCIÓN:
Define las interfaces gráficas para gestionar Alumnos y Profesores.
Implementa operaciones CRUD (Create, Read, Update, Delete) con tablas interactivas.

CLASES:
- VentanaAlumnos: Interfaz para gestionar estudiantes
- VentanaProfesores: Interfaz para gestionar docentes

FUNCIONALIDADES:

VentanaAlumnos:
✓ Tabla con lista de alumnos
✓ Búsqueda por DNI (campo único)
✓ Agregar nuevo alumno
✓ Editar alumno seleccionado
✓ Eliminar alumno seleccionado
✓ Formulario con validación en tiempo real
✓ Grados: 1ro, 2do, 3ro, 4to, 5to, 6to
✓ Asignaturas: Matemáticas, Lengua, Ciencias, Historia, Educación Física, Inglés

VentanaProfesores:
✓ Tabla con lista de profesores
✓ Búsqueda por documento
✓ CRUD completo de profesores
✓ Formulario con validación

FLUJO DE DATOS:
1. Vista carga datos del controlador
2. Muestra tabla con registros
3. Usuario selecciona fila y hace clic en Editar/Eliminar
4. Vista abre formulario con validadores
5. Usuario envía datos
6. Vista llama al controlador
7. Controlador valida y guarda en BD
8. Vista recarga tabla

VALIDACIÓN:
Todos los campos usan validadores de models/validaciones.py:
- Nombres: Solo letras
- Email: Formato válido
- Teléfono: Solo dígitos
- DNI: Único en la base de datos
- Grados: Lista predefinida
- Asignaturas: Lista predefinida

IMPORTANCIA:
Esta es una de las interfaces más usadas del sistema. Maneja directamente
la interacción con usuarios para el 80% de las operaciones del sistema.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from views.centrar_ventana import centrar_ventana
from views.tema import aplicar_tema_oscuro
from models.models import Alumno, Profesor
from controllers.controlers import ControladorAlumnos, ControladorProfesores
from models.validaciones import Validador
from views.widgets import EntryNumerico, EntryFecha, EntryTexto, EntryTelefono
from config import TABLE_WINDOW_WIDTH, TABLE_WINDOW_HEIGHT, FORM_WINDOW_WIDTH, FORM_WINDOW_HEIGHT_ALUMNO, FORM_WINDOW_HEIGHT_PROFESOR, GRADOS, ASIGNATURAS


class VentanaAlumnos:
    """Ventana para gestionar alumnos (CRUD).
    
    Proporciona interfaz gráfica para todas las operaciones con estudiantes:
    crear, leer, actualizar y eliminar. Incluye búsqueda por DNI y tabla
    interactiva con selección de filas.
    
    Atributos:
        ventana (tk.Toplevel): Ventana secundaria
        controlador (ControladorAlumnos): Gestor de datos
        id_seleccionado (int): ID del alumno seleccionado en la tabla
        entrada_busqueda (ttk.Entry): Campo de búsqueda
        arbol (ttk.Treeview): Tabla de alumnos
    """
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Alumnos")
        centrar_ventana(self.ventana, TABLE_WINDOW_WIDTH, TABLE_WINDOW_HEIGHT)
        
        # Aplicar tema oscuro a ventana secundaria
        self.style = ttk.Style()
        self.colores, self.style = aplicar_tema_oscuro(self.ventana, self.style)
        
        self.controlador = ControladorAlumnos()
        self.id_seleccionado = None
        
        self.crear_interfaz()
        self.cargar_alumnos()
    
    def crear_interfaz(self):
        """Crea los elementos de la interfaz."""
        # Marco superior para botones
        marco_botones = ttk.Frame(self.ventana)
        marco_botones.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Button(marco_botones, text="Nuevo Alumno", command=self.nuevo_alumno).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones, text="Editar", command=self.editar_alumno).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones, text="Eliminar", command=self.eliminar_alumno).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones, text="Actualizar", command=self.cargar_alumnos).pack(side=tk.LEFT, padx=5)
        
        # Marco de búsqueda
        marco_busqueda = ttk.Frame(self.ventana)
        marco_busqueda.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(marco_busqueda, text="Buscar por DNI:").pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda = ttk.Entry(marco_busqueda, width=30)
        self.entrada_busqueda.pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_busqueda, text="Buscar", command=self.buscar_alumno).pack(side=tk.LEFT, padx=5)
        
        # Tabla de alumnos
        marco_tabla = ttk.Frame(self.ventana)
        marco_tabla.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.arbol = ttk.Treeview(marco_tabla, columns=("ID", "Nombre", "Apellido", "Email", 
                                                         "Teléfono", "Fecha Nac.", "Grado", "Sección", "DNI"),
                                  height=20, show="headings")
        
        # Definir columnas
        for col in ("ID", "Nombre", "Apellido", "Email", "Teléfono", "Fecha Nac.", "Grado", "Sección", "DNI"):
            self.arbol.column(col, width=80)
            self.arbol.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.arbol.yview)
        self.arbol.configure(yscroll=scrollbar.set)
        
        self.arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de selección
        self.arbol.bind("<<TreeviewSelect>>", self.on_select)
    
    def cargar_alumnos(self):
        """Carga todos los alumnos en la tabla."""
        # Limpiar tabla
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        
        # Cargar alumnos
        alumnos = self.controlador.obtener_alumnos()
        for alumno in alumnos:
            self.arbol.insert("", tk.END, values=alumno)
    
    def on_select(self, event):
        """Maneja la selección de un alumno en la tabla."""
        selection = self.arbol.selection()
        if selection:
            item = selection[0]
            valores = self.arbol.item(item, "values")
            self.id_seleccionado = valores[0]
    
    def nuevo_alumno(self):
        """Abre el formulario para crear un nuevo alumno."""
        self.abrir_formulario_alumno(None)
    
    def editar_alumno(self):
        """Abre el formulario para editar el alumno seleccionado."""
        if not self.id_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un alumno para editar")
            return
        self.abrir_formulario_alumno(int(self.id_seleccionado))
    
    def eliminar_alumno(self):
        """Elimina el alumno seleccionado."""
        if not self.id_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un alumno para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este alumno?"):
            if self.controlador.eliminar_alumno(int(self.id_seleccionado)):
                messagebox.showinfo("Éxito", "Alumno eliminado correctamente")
                self.cargar_alumnos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el alumno")
    
    def buscar_alumno(self):
        """Busca alumnos por DNI."""
        valor = self.entrada_busqueda.get()
        if not valor:
            self.cargar_alumnos()
            return
        
        # Limpiar tabla
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        
        # Cargar resultados
        resultados = self.controlador.buscar_alumno("dni", valor)
        for resultado in resultados:
            self.arbol.insert("", tk.END, values=resultado)
    
    def abrir_formulario_alumno(self, id_alumno=None):
        """Abre el formulario para crear o editar un alumno."""
        ventana_form = tk.Toplevel(self.ventana)
        ventana_form.title("Formulario de Alumno")
        centrar_ventana(ventana_form, FORM_WINDOW_WIDTH, FORM_WINDOW_HEIGHT_ALUMNO)
        
        # Obtener datos si es edición
        datos = None
        if id_alumno:
            datos = self.controlador.obtener_alumno(id_alumno)
        
        # Crear campos con widgets personalizados
        campos = {}
        
        # Nombre
        ttk.Label(ventana_form, text="Nombre:").grid(row=0, column=0, sticky="W", padx=10, pady=5)
        nombre_entry = EntryTexto(ventana_form, width=30)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)
        campos["nombre"] = nombre_entry
        if datos:
            nombre_entry.insert(0, datos[1])
        
        # Apellido
        ttk.Label(ventana_form, text="Apellido:").grid(row=1, column=0, sticky="W", padx=10, pady=5)
        apellido_entry = EntryTexto(ventana_form, width=30)
        apellido_entry.grid(row=1, column=1, padx=10, pady=5)
        campos["apellido"] = apellido_entry
        if datos:
            apellido_entry.insert(0, datos[2])
        
        # Email
        ttk.Label(ventana_form, text="Email:").grid(row=2, column=0, sticky="W", padx=10, pady=5)
        email_entry = ttk.Entry(ventana_form, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=5)
        campos["email"] = email_entry
        if datos:
            email_entry.insert(0, datos[3])
        
        # Teléfono
        ttk.Label(ventana_form, text="Teléfono:").grid(row=3, column=0, sticky="W", padx=10, pady=5)
        telefono_entry = EntryTelefono(ventana_form, width=30)
        telefono_entry.grid(row=3, column=1, padx=10, pady=5)
        campos["teléfono"] = telefono_entry
        if datos:
            telefono_entry.insert(0, datos[4])
        
        # Fecha Nacimiento
        ttk.Label(ventana_form, text="Fecha Nacimiento:").grid(row=4, column=0, sticky="W", padx=10, pady=5)
        fecha_entry = EntryFecha(ventana_form)
        fecha_entry.grid(row=4, column=1, padx=10, pady=5, sticky="EW")
        campos["fecha_nacimiento"] = fecha_entry
        if datos:
            fecha_entry.insert(0, datos[5])
        
        # Grado
        ttk.Label(ventana_form, text="Grado:").grid(row=5, column=0, sticky="W", padx=10, pady=5)
        grado_entry = ttk.Combobox(ventana_form, width=27, state="readonly", values=GRADOS)
        grado_entry.grid(row=5, column=1, padx=10, pady=5)
        campos["grado"] = grado_entry
        if datos:
            grado_entry.set(datos[6])
        
        # Asignatura
        ttk.Label(ventana_form, text="Asignatura:").grid(row=6, column=0, sticky="W", padx=10, pady=5)
        asignatura_entry = ttk.Combobox(ventana_form, width=27, state="readonly", values=ASIGNATURAS)
        asignatura_entry.grid(row=6, column=1, padx=10, pady=5)
        campos["sección"] = asignatura_entry
        if datos:
            asignatura_entry.set(datos[7])
        
        # DNI
        ttk.Label(ventana_form, text="DNI:").grid(row=7, column=0, sticky="W", padx=10, pady=5)
        dni_entry = EntryNumerico(ventana_form, width=30)
        dni_entry.grid(row=7, column=1, padx=10, pady=5)
        campos["dni"] = dni_entry
        if datos:
            dni_entry.insert(0, datos[8])
        
        # Agregar información de ayuda
        frame_ayuda = ttk.LabelFrame(ventana_form, text="Formatos esperados", padding="8")
        frame_ayuda.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="EW")
        
        ayuda_text = (
            "• Nombre/Apellido: Solo letras y espacios\n"
            "• Email: usuario@dominio.com (opcional)\n"
            "• Teléfono: Solo números, 7-15 dígitos (opcional)\n"
            "• Fecha: DD/MM/YYYY (opcional)\n"
            "• Grado: 1ro, 2do, 3ro, 4to, 5to o 6to (opcional)\n"
            "• Asignatura: Matemáticas, Lengua, Ciencias, Historia, Educación Física o Inglés (opcional)\n"
            "• DNI: 8 dígitos (opcional)"
        )
        ttk.Label(frame_ayuda, text=ayuda_text, justify=tk.LEFT, font=("Arial", 8)).pack(anchor="w")
        
        def guardar():
            """Guarda el alumno con validaciones."""
            try:
                nombre = campos["nombre"].get().strip()
                apellido = campos["apellido"].get().strip()
                email = campos["email"].get().strip()
                telefono = campos["teléfono"].get().strip()
                fecha_nacimiento = campos["fecha_nacimiento"].get().strip()
                grado = campos["grado"].get().strip()
                seccion = campos["sección"].get().strip()
                dni = campos["dni"].get().strip()
                
                # Validar todos los campos
                errores = Validador.validar_alumno_completo(
                    nombre, apellido, email, telefono, fecha_nacimiento, grado, seccion, dni
                )
                
                if errores:
                    mensaje_error = "Errores encontrados:\n\n" + "\n".join(f"• {error}" for error in errores)
                    messagebox.showerror("Validación", mensaje_error)
                    return
                
                alumno = Alumno(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    telefono=telefono,
                    fecha_nacimiento=fecha_nacimiento,
                    grado=grado,
                    seccion=seccion,
                    dni=dni
                )
                
                exito = False
                if id_alumno:
                    exito, mensaje = self.controlador.actualizar_alumno(id_alumno, alumno)
                    if exito:
                        messagebox.showinfo("Éxito", mensaje)
                    else:
                        messagebox.showerror("Error", mensaje)
                        return
                else:
                    exito, mensaje = self.controlador.agregar_alumno(alumno)
                    if exito:
                        messagebox.showinfo("Éxito", mensaje)
                    else:
                        messagebox.showerror("Error", mensaje)
                        return
                
                ventana_form.destroy()
                self.cargar_alumnos()
                
            except Exception as e:
                messagebox.showerror("Error Inesperado", f"Ocurrió un error al guardar:\n\n{str(e)}\n\nPor favor, intenta de nuevo.")
                import traceback
                traceback.print_exc()
        
        ttk.Button(ventana_form, text="Guardar", command=guardar).grid(row=9, column=0, pady=20, padx=5)
        ttk.Button(ventana_form, text="Cancelar", command=ventana_form.destroy).grid(row=9, column=1, padx=5)


class VentanaProfesores:
    """Ventana para gestionar profesores."""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Profesores")
        centrar_ventana(self.ventana, TABLE_WINDOW_WIDTH, TABLE_WINDOW_HEIGHT)
        
        # Aplicar tema oscuro a ventana secundaria
        self.style = ttk.Style()
        self.colores, self.style = aplicar_tema_oscuro(self.ventana, self.style)
        
        self.controlador = ControladorProfesores()
        self.id_seleccionado = None
        
        self.crear_interfaz()
        self.cargar_profesores()
    
    def crear_interfaz(self):
        """Crea los elementos de la interfaz."""
        # Marco superior para botones
        marco_botones = ttk.Frame(self.ventana)
        marco_botones.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Button(marco_botones, text="Nuevo Profesor", command=self.nuevo_profesor).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones, text="Editar", command=self.editar_profesor).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones, text="Eliminar", command=self.eliminar_profesor).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones, text="Actualizar", command=self.cargar_profesores).pack(side=tk.LEFT, padx=5)
        
        # Marco de búsqueda
        marco_busqueda = ttk.Frame(self.ventana)
        marco_busqueda.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(marco_busqueda, text="Buscar por nombre:").pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda = ttk.Entry(marco_busqueda, width=30)
        self.entrada_busqueda.pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_busqueda, text="Buscar", command=self.buscar_profesor).pack(side=tk.LEFT, padx=5)
        
        # Tabla de profesores
        marco_tabla = ttk.Frame(self.ventana)
        marco_tabla.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.arbol = ttk.Treeview(marco_tabla, columns=("ID", "Nombre", "Apellido", "Email", 
                                                         "Teléfono", "Especialidad", "Documento"),
                                  height=20, show="headings")
        
        # Definir columnas
        for col in ("ID", "Nombre", "Apellido", "Email", "Teléfono", "Especialidad", "Documento"):
            self.arbol.column(col, width=120)
            self.arbol.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(marco_tabla, orient=tk.VERTICAL, command=self.arbol.yview)
        self.arbol.configure(yscroll=scrollbar.set)
        
        self.arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de selección
        self.arbol.bind("<<TreeviewSelect>>", self.on_select)
    
    def cargar_profesores(self):
        """Carga todos los profesores en la tabla."""
        # Limpiar tabla
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        
        # Cargar profesores
        profesores = self.controlador.obtener_profesores()
        for profesor in profesores:
            self.arbol.insert("", tk.END, values=profesor)
    
    def on_select(self, event):
        """Maneja la selección de un profesor en la tabla."""
        selection = self.arbol.selection()
        if selection:
            item = selection[0]
            valores = self.arbol.item(item, "values")
            self.id_seleccionado = valores[0]
    
    def nuevo_profesor(self):
        """Abre el formulario para crear un nuevo profesor."""
        self.abrir_formulario_profesor(None)
    
    def editar_profesor(self):
        """Abre el formulario para editar el profesor seleccionado."""
        if not self.id_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un profesor para editar")
            return
        self.abrir_formulario_profesor(int(self.id_seleccionado))
    
    def eliminar_profesor(self):
        """Elimina el profesor seleccionado."""
        if not self.id_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un profesor para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este profesor?"):
            if self.controlador.eliminar_profesor(int(self.id_seleccionado)):
                messagebox.showinfo("Éxito", "Profesor eliminado correctamente")
                self.cargar_profesores()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el profesor")
    
    def buscar_profesor(self):
        """Busca profesores por nombre."""
        valor = self.entrada_busqueda.get()
        if not valor:
            self.cargar_profesores()
            return
        
        # Limpiar tabla
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        
        # Cargar resultados
        resultados = self.controlador.buscar_profesor("nombre", valor)
        for resultado in resultados:
            self.arbol.insert("", tk.END, values=resultado)
    
    def abrir_formulario_profesor(self, id_profesor=None):
        """Abre el formulario para crear o editar un profesor."""
        ventana_form = tk.Toplevel(self.ventana)
        ventana_form.title("Formulario de Profesor")
        centrar_ventana(ventana_form, FORM_WINDOW_WIDTH, FORM_WINDOW_HEIGHT_PROFESOR)
        
        # Obtener datos si es edición
        datos = None
        if id_profesor:
            datos = self.controlador.obtener_profesor(id_profesor)
        
        # Crear campos con widgets personalizados
        campos = {}
        
        # Nombre
        ttk.Label(ventana_form, text="Nombre:").grid(row=0, column=0, sticky="W", padx=10, pady=5)
        nombre_entry = EntryTexto(ventana_form, width=30)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)
        campos["nombre"] = nombre_entry
        if datos:
            nombre_entry.insert(0, datos[1])
        
        # Apellido
        ttk.Label(ventana_form, text="Apellido:").grid(row=1, column=0, sticky="W", padx=10, pady=5)
        apellido_entry = EntryTexto(ventana_form, width=30)
        apellido_entry.grid(row=1, column=1, padx=10, pady=5)
        campos["apellido"] = apellido_entry
        if datos:
            apellido_entry.insert(0, datos[2])
        
        # Email
        ttk.Label(ventana_form, text="Email:").grid(row=2, column=0, sticky="W", padx=10, pady=5)
        email_entry = ttk.Entry(ventana_form, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=5)
        campos["email"] = email_entry
        if datos:
            email_entry.insert(0, datos[3])
        
        # Teléfono
        ttk.Label(ventana_form, text="Teléfono:").grid(row=3, column=0, sticky="W", padx=10, pady=5)
        telefono_entry = EntryTelefono(ventana_form, width=30)
        telefono_entry.grid(row=3, column=1, padx=10, pady=5)
        campos["teléfono"] = telefono_entry
        if datos:
            telefono_entry.insert(0, datos[4])
        
        # Especialidad
        ttk.Label(ventana_form, text="Especialidad:").grid(row=4, column=0, sticky="W", padx=10, pady=5)
        especialidad_entry = EntryTexto(ventana_form, width=30)
        especialidad_entry.grid(row=4, column=1, padx=10, pady=5)
        campos["especialidad"] = especialidad_entry
        if datos:
            especialidad_entry.insert(0, datos[5])
        
        # Documento
        ttk.Label(ventana_form, text="Documento:").grid(row=5, column=0, sticky="W", padx=10, pady=5)
        documento_entry = EntryNumerico(ventana_form, width=30)
        documento_entry.grid(row=5, column=1, padx=10, pady=5)
        campos["documento"] = documento_entry
        if datos:
            documento_entry.insert(0, datos[6])
        
        # Agregar información de ayuda
        frame_ayuda = ttk.LabelFrame(ventana_form, text="Formatos esperados", padding="8")
        frame_ayuda.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="EW")
        
        ayuda_text = (
            "• Nombre/Apellido: Solo letras y espacios\n"
            "• Email: usuario@dominio.com (opcional)\n"
            "• Teléfono: Solo números, 7-15 dígitos (opcional)\n"
            "• Especialidad: Texto de 3-50 caracteres (opcional)\n"
            "• Documento: 8 dígitos (opcional)"
        )
        ttk.Label(frame_ayuda, text=ayuda_text, justify=tk.LEFT, font=("Arial", 8)).pack(anchor="w")
        
        def guardar():
            """Guarda el profesor con validaciones."""
            try:
                nombre = campos["nombre"].get().strip()
                apellido = campos["apellido"].get().strip()
                email = campos["email"].get().strip()
                telefono = campos["teléfono"].get().strip()
                especialidad = campos["especialidad"].get().strip()
                documento = campos["documento"].get().strip()
                
                # Validar todos los campos
                errores = Validador.validar_profesor_completo(
                    nombre, apellido, email, telefono, especialidad, documento
                )
                
                if errores:
                    mensaje_error = "Errores encontrados:\n\n" + "\n".join(f"• {error}" for error in errores)
                    messagebox.showerror("Validación", mensaje_error)
                    return
                
                profesor = Profesor(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    telefono=telefono,
                    especialidad=especialidad,
                    documento=documento
                )
                
                exito = False
                if id_profesor:
                    exito, mensaje = self.controlador.actualizar_profesor(id_profesor, profesor)
                    if exito:
                        messagebox.showinfo("Éxito", mensaje)
                    else:
                        messagebox.showerror("Error", mensaje)
                        return
                else:
                    exito, mensaje = self.controlador.agregar_profesor(profesor)
                    if exito:
                        messagebox.showinfo("Éxito", mensaje)
                    else:
                        messagebox.showerror("Error", mensaje)
                        return
                
                ventana_form.destroy()
                self.cargar_profesores()
                
            except Exception as e:
                messagebox.showerror("Error Inesperado", f"Ocurrió un error al guardar:\n\n{str(e)}\n\nPor favor, intenta de nuevo.")
                import traceback
                traceback.print_exc()
        
        ttk.Button(ventana_form, text="Guardar", command=guardar).grid(row=7, column=0, pady=20, padx=5)
        ttk.Button(ventana_form, text="Cancelar", command=ventana_form.destroy).grid(row=7, column=1, padx=5)
