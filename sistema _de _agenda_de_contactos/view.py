"""
Módulo de vista para la agenda de contactos usando tkinter.
Proporciona la interfaz gráfica de usuario.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from controller import ControladorAgenda
import validators


class Vista:
    """Clase que maneja la interfaz gráfica de la agenda usando tkinter."""
    
    # Colores para tema claro
    COLORES_CLARO = {
        'bg': '#ffffff',
        'fg': '#000000',
        'bg_frame': '#f0f0f0',
        'bg_entrada': '#ffffff',
        'fg_entrada': '#000000'
    }
    
    # Colores para tema oscuro
    COLORES_OSCURO = {
        'bg': '#2b2b2b',
        'fg': '#ffffff',
        'bg_frame': '#1e1e1e',
        'bg_entrada': '#3d3d3d',
        'fg_entrada': '#ffffff'
    }
    
    def __init__(self, controlador: ControladorAgenda = None):
        """
        Inicializa la interfaz gráfica.
        
        Args:
            controlador: Instancia del ControladorAgenda
        """
        self.controlador = controlador or ControladorAgenda()
        self.tema_oscuro = True  # Tema oscuro por defecto
        
        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Agenda de Contactos")
        self.ventana.geometry("900x600")
        self.ventana.resizable(True, True)
        
        # Configurar estilo
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self._configurar_estilos()
        
        self._crear_interfaz()
        self._aplicar_tema()
        self._cargar_contactos_en_tabla()
    
    def _configurar_estilos(self) -> None:
        """Configura los estilos para tema claro y oscuro."""
        # Estilos para tema claro
        self.estilo.configure('Claro.TFrame', background=self.COLORES_CLARO['bg_frame'])
        self.estilo.configure('Claro.TLabel', background=self.COLORES_CLARO['bg_frame'], foreground=self.COLORES_CLARO['fg'])
        self.estilo.configure('Claro.TButton', background=self.COLORES_CLARO['bg_frame'], foreground=self.COLORES_CLARO['fg'])
        self.estilo.configure('Claro.Treeview', background=self.COLORES_CLARO['bg_entrada'], foreground=self.COLORES_CLARO['fg_entrada'], fieldbackground=self.COLORES_CLARO['bg_entrada'])
        self.estilo.map('Claro.Treeview', background=[('selected', '#0078d4')])
        
        # Estilos para tema oscuro
        self.estilo.configure('Oscuro.TFrame', background=self.COLORES_OSCURO['bg_frame'])
        self.estilo.configure('Oscuro.TLabel', background=self.COLORES_OSCURO['bg_frame'], foreground=self.COLORES_OSCURO['fg'])
        self.estilo.configure('Oscuro.TButton', background=self.COLORES_OSCURO['bg_frame'], foreground=self.COLORES_OSCURO['fg'])
        self.estilo.configure('Oscuro.Treeview', background=self.COLORES_OSCURO['bg_entrada'], foreground=self.COLORES_OSCURO['fg_entrada'], fieldbackground=self.COLORES_OSCURO['bg_entrada'])
        self.estilo.map('Oscuro.Treeview', background=[('selected', '#0078d4')])
        self.estilo.map('Oscuro.TButton', background=[('active', '#4d4d4d')])
    
    def _aplicar_tema(self) -> None:
        """Aplica el tema claro u oscuro a toda la interfaz."""
        colores = self.COLORES_OSCURO if self.tema_oscuro else self.COLORES_CLARO
        tema = 'Oscuro' if self.tema_oscuro else 'Claro'
        
        # Cambiar fondo de la ventana
        self.ventana.config(bg=colores['bg_frame'])
        
        # Actualizar estilos globales
        self.estilo.configure('TFrame', background=colores['bg_frame'])
        self.estilo.configure('TLabel', background=colores['bg_frame'], foreground=colores['fg'])
        self.estilo.configure('TButton', background=colores['bg_frame'], foreground=colores['fg'])
        self.estilo.configure('TEntry', fieldbackground=colores['bg_entrada'], background=colores['bg_entrada'], foreground=colores['fg_entrada'])
        self.estilo.configure('Treeview', background=colores['bg_entrada'], foreground=colores['fg_entrada'], fieldbackground=colores['bg_entrada'])
        self.estilo.configure('Treeview.Heading', background=colores['bg_frame'], foreground=colores['fg'])
        self.estilo.map('Treeview', background=[('selected', '#0078d4')])
        self.estilo.map('Treeview.Heading', background=[('active', colores['bg_entrada'])])
        
        # Aplicar a la tabla
        if hasattr(self, 'tabla'):
            self.tabla.configure(style=f'{tema}.Treeview')
    
    def _cambiar_tema(self) -> None:
        """Cambia entre tema claro y oscuro."""
        self.tema_oscuro = not self.tema_oscuro
        self._aplicar_tema()
        self._actualizar_boton_tema()
    
    def _actualizar_boton_tema(self) -> None:
        """Actualiza el texto del botón de tema."""
        texto = "☀️ Claro" if self.tema_oscuro else "🌙 Oscuro"
        self.boton_tema.config(text=texto)
    
    def _crear_interfaz(self) -> None:
        """Crea los componentes de la interfaz gráfica."""
        
        # Frame superior con botón de tema
        frame_tema = ttk.Frame(self.ventana)
        frame_tema.pack(fill=tk.X, padx=5, pady=5)
        
        # Botón de cambio de tema (alineado a la derecha)
        self.boton_tema = ttk.Button(frame_tema, text="☀️ Claro", command=self._cambiar_tema)
        self.boton_tema.pack(side=tk.RIGHT, padx=5)
        

        ttk.Button(frame_tema, text="➕ Añadir", command=self._anadir_contacto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_tema, text="✏️ Editar", command=self._editar_contacto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_tema, text="🗑️ Eliminar", command=self._eliminar_contacto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_tema, text="🔄 Actualizar", command=self._cargar_contactos_en_tabla).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_tema, text="🔍 Filtro", command=self._abrir_filtros).pack(side=tk.LEFT, padx=5)
        
        # Frame para la tabla
        frame_tabla = ttk.Frame(self.ventana)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear tabla (Treeview)
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=('ID', 'Nombre', 'Apellido', 'Teléfono', 'Edad', 'Email', 'Dirección', 'Fecha Registro'),
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tabla.yview)
        
        # Configurar encabezados
        self.tabla.column('#0', width=0, stretch=tk.NO)
        self.tabla.column('ID', anchor=tk.W, width=70)
        self.tabla.column('Nombre', anchor=tk.W, width=90)
        self.tabla.column('Apellido', anchor=tk.W, width=90)
        self.tabla.column('Teléfono', anchor=tk.W, width=90)
        self.tabla.column('Edad', anchor=tk.W, width=50)
        self.tabla.column('Email', anchor=tk.W, width=120)
        self.tabla.column('Dirección', anchor=tk.W, width=130)
        self.tabla.column('Fecha Registro', anchor=tk.W, width=120)
        
        self.tabla.heading('#0', text='', anchor=tk.W)
        self.tabla.heading('ID', text='ID', anchor=tk.W)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tabla.heading('Apellido', text='Apellido', anchor=tk.W)
        self.tabla.heading('Teléfono', text='Teléfono', anchor=tk.W)
        self.tabla.heading('Edad', text='Edad', anchor=tk.W)
        self.tabla.heading('Email', text='Email', anchor=tk.W)
        self.tabla.heading('Dirección', text='Dirección', anchor=tk.W)
        self.tabla.heading('Fecha Registro', text='Fecha Registro', anchor=tk.W)
        
        self.tabla.pack(fill=tk.BOTH, expand=True)
        
        # Bind doble clic para editar
        self.tabla.bind('<Double-1>', lambda e: self._editar_contacto())
        
        # Barra de estado
        self.estado = ttk.Label(self.ventana, text="Contactos cargados", relief=tk.SUNKEN)
        self.estado.pack(fill=tk.X, padx=10, pady=5)
    
    def _cargar_contactos_en_tabla(self) -> None:
        """Carga los contactos en la tabla."""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Cargar contactos
        contactos = self.controlador.obtener_todos_contactos()
        for id_contacto, datos in contactos.items():
            # Calcular edad
            fecha_nac = datos.get('fecha_nacimiento', '')
            edad = ''
            if fecha_nac:
                try:
                    from datetime import datetime
                    dia, mes, año = map(int, fecha_nac.split('/'))
                    fecha_nac_obj = datetime(año, mes, dia)
                    hoy = datetime.now()
                    edad_calc = hoy.year - fecha_nac_obj.year
                    if (hoy.month, hoy.day) < (fecha_nac_obj.month, fecha_nac_obj.day):
                        edad_calc -= 1
                    edad = str(edad_calc)
                except (ValueError, AttributeError):
                    edad = ''
            
            self.tabla.insert(
                '',
                'end',
                text='',
                values=(
                    id_contacto,
                    datos.get('nombre', ''),
                    datos.get('apellido', ''),
                    datos.get('telefono', ''),
                    edad,
                    datos.get('email', ''),
                    datos.get('direccion', ''),
                    datos.get('fecha_registro', '')
                )
            )
        
        self._actualizar_estado()
    
    def _obtener_contacto_seleccionado(self) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Obtiene el contacto seleccionado en la tabla.
        
        Returns:
            Tupla (id, datos) del contacto seleccionado
        """
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un contacto.")
            return None, None
        
        item = self.tabla.item(seleccion[0])
        id_contacto = item['values'][0]
        datos = self.controlador.obtener_contacto(id_contacto)
        
        return id_contacto, datos
    
    def _anadir_contacto(self) -> None:
        """Abre un diálogo para añadir un nuevo contacto."""
        ventana_dialogo = tk.Toplevel(self.ventana)
        ventana_dialogo.title("Añadir Contacto")
        ventana_dialogo.geometry("500x750")
        ventana_dialogo.resizable(False, False)
        
        # Frame principal con scrollbar
        frame = ttk.Frame(ventana_dialogo, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nombre - Validar solo letras y espacios
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entrada_nombre = ttk.Entry(frame, width=30)
        entrada_nombre.grid(row=0, column=1, pady=5, sticky=tk.EW)
        ttk.Label(frame, text="(Solo letras)", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Apellido - Validar solo letras y espacios
        ttk.Label(frame, text="Apellido:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entrada_apellido = ttk.Entry(frame, width=30)
        entrada_apellido.grid(row=1, column=1, pady=5, sticky=tk.EW)
        ttk.Label(frame, text="(Solo letras)", font=("Arial", 8)).grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # Teléfono - Validar solo números
        ttk.Label(frame, text="Teléfono:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entrada_telefono = ttk.Entry(frame, width=30)
        entrada_telefono.grid(row=2, column=1, pady=5, sticky=tk.EW)
        ttk.Label(frame, text="(Solo números)", font=("Arial", 8)).grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # Email
        ttk.Label(frame, text="Email (opcional):").grid(row=3, column=0, sticky=tk.W, pady=5)
        entrada_email = ttk.Entry(frame, width=30)
        entrada_email.grid(row=3, column=1, pady=5, sticky=tk.EW)
        
        # Dirección
        ttk.Label(frame, text="Dirección (opcional):").grid(row=4, column=0, sticky=tk.W, pady=5)
        entrada_direccion = ttk.Entry(frame, width=30)
        entrada_direccion.grid(row=4, column=1, pady=5, sticky=tk.EW)
        
        # Fecha de Registro con Calendar
        ttk.Label(frame, text="Fecha Registro:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        # Calendar para fecha de registro
        calendario_reg = Calendar(
            frame,
            selectmode='day',
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            font=("Arial", 9),
            background='#1e1e1e' if self.tema_oscuro else '#ffffff',
            foreground='#ffffff' if self.tema_oscuro else '#000000',
            headersforeground='#ffffff' if self.tema_oscuro else '#000000',
            headersbackground='#2b2b2b' if self.tema_oscuro else '#e0e0e0',
            normalbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            normalforeground='#ffffff' if self.tema_oscuro else '#000000',
            othermonthweforeground='#666666' if self.tema_oscuro else '#cccccc',
            othermonthwebackground='#1e1e1e' if self.tema_oscuro else '#f0f0f0',
            weekendforeground='#ff9999' if self.tema_oscuro else '#cc0000',
            weekendbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            selectforeground='#ffffff' if self.tema_oscuro else '#000000',
            selectbackground='#0078d4'
        )
        calendario_reg.grid(row=5, column=1, pady=5, sticky=tk.EW)
        
        # Fecha de Nacimiento con Calendar - SIEMPRE VISIBLE
        ttk.Label(frame, text="Fecha Nacimiento:").grid(row=6, column=0, sticky=tk.W, pady=5)
        
        # Calendar para seleccionar fecha de nacimiento
        calendario = Calendar(
            frame,
            selectmode='day',
            year=2000,
            month=1,
            day=1,
            font=("Arial", 9),
            background='#1e1e1e' if self.tema_oscuro else '#ffffff',
            foreground='#ffffff' if self.tema_oscuro else '#000000',
            headersforeground='#ffffff' if self.tema_oscuro else '#000000',
            headersbackground='#2b2b2b' if self.tema_oscuro else '#e0e0e0',
            normalbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            normalforeground='#ffffff' if self.tema_oscuro else '#000000',
            othermonthweforeground='#666666' if self.tema_oscuro else '#cccccc',
            othermonthwebackground='#1e1e1e' if self.tema_oscuro else '#f0f0f0',
            weekendforeground='#ff9999' if self.tema_oscuro else '#cc0000',
            weekendbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            selectforeground='#ffffff' if self.tema_oscuro else '#000000',
            selectbackground='#0078d4'
        )
        calendario.grid(row=6, column=1, pady=5, sticky=tk.EW)
        
        frame.columnconfigure(1, weight=1)
        
        def guardar():
            nombre = entrada_nombre.get().strip()
            apellido = entrada_apellido.get().strip()
            telefono = entrada_telefono.get().strip()
            email = entrada_email.get().strip() or None
            direccion = entrada_direccion.get().strip() or None
            
            # Validar nombre
            valido, error = validators.es_nombre_valido(nombre)
            if not valido:
                messagebox.showerror("Error de validación", error)
                return
            
            # Validar apellido
            valido, error = validators.es_apellido_valido(apellido)
            if not valido:
                messagebox.showerror("Error de validación", error)
                return
            
            # Validar teléfono
            valido, error = validators.es_telefono_valido(telefono)
            if not valido:
                messagebox.showerror("Error de validación", error)
                return
            
            # Validar email (si se proporciona)
            if email:
                valido, error = validators.es_email_valido(email)
                if not valido:
                    messagebox.showerror("Error de validación", error)
                    return
            
            # Validar dirección (si se proporciona)
            if direccion:
                valido, error = validators.es_direccion_valida(direccion)
                if not valido:
                    messagebox.showerror("Error de validación", error)
                    return
            
            # Obtener fechas del calendario
            try:
                fecha_reg = calendario_reg.selection_get().strftime("%d/%m/%Y")
                fecha_nac = calendario.selection_get().strftime("%d/%m/%Y")
            except AttributeError:
                fecha_reg = calendario_reg.get_date()
                fecha_nac = calendario.get_date()
            
            # Usar el controlador para guardar el contacto
            exito, mensaje, id_contacto = self.controlador.crear_contacto(
                nombre, apellido, telefono, email, direccion, fecha_nac, fecha_reg
            )
            
            if exito:
                messagebox.showinfo("Éxito", f"{mensaje}\nID: {id_contacto}")
                ventana_dialogo.destroy()
                self._cargar_contactos_en_tabla()
            else:
                messagebox.showerror("Error de validación", mensaje)
        


# Frame de botones
        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=7, column=0, columnspan=3, pady=20) # Asegúrate de que sea grid si el resto es grid
        ttk.Button(frame_botones, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana_dialogo.destroy).pack(side=tk.LEFT, padx=5)
        
    def _editar_contacto(self) -> None:
        """Abre un diálogo para editar el contacto seleccionado."""
        id_contacto, datos = self._obtener_contacto_seleccionado()
        if not id_contacto:
            return
        
        ventana_dialogo = tk.Toplevel(self.ventana)
        ventana_dialogo.title("Editar Contacto")
        ventana_dialogo.geometry("500x800")
        ventana_dialogo.resizable(False, False)
        
        # Frame principal
        frame = ttk.Frame(ventana_dialogo, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # ID (deshabilitado)
        ttk.Label(frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entrada_id = ttk.Entry(frame, width=30, state=tk.DISABLED)
        entrada_id.insert(0, id_contacto)
        entrada_id.grid(row=0, column=1, pady=5, sticky=tk.EW)
        
        # Nombre - Validar solo letras y espacios
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entrada_nombre = ttk.Entry(frame, width=30)
        entrada_nombre.insert(0, datos.get('nombre', ''))
        entrada_nombre.grid(row=1, column=1, pady=5, sticky=tk.EW)
        ttk.Label(frame, text="(Solo letras)", font=("Arial", 8)).grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # Apellido - Validar solo letras y espacios
        ttk.Label(frame, text="Apellido:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entrada_apellido = ttk.Entry(frame, width=30)
        entrada_apellido.insert(0, datos.get('apellido', ''))
        entrada_apellido.grid(row=2, column=1, pady=5, sticky=tk.EW)
        ttk.Label(frame, text="(Solo letras)", font=("Arial", 8)).grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # Teléfono - Validar solo números
        ttk.Label(frame, text="Teléfono:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entrada_telefono = ttk.Entry(frame, width=30)
        entrada_telefono.insert(0, datos.get('telefono', ''))
        entrada_telefono.grid(row=3, column=1, pady=5, sticky=tk.EW)
        ttk.Label(frame, text="(Solo números)", font=("Arial", 8)).grid(row=3, column=2, sticky=tk.W, padx=5)
        
        # Email
        ttk.Label(frame, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=5)
        entrada_email = ttk.Entry(frame, width=30)
        entrada_email.insert(0, datos.get('email', ''))
        entrada_email.grid(row=4, column=1, pady=5, sticky=tk.EW)
        
        # Dirección
        ttk.Label(frame, text="Dirección:").grid(row=5, column=0, sticky=tk.W, pady=5)
        entrada_direccion = ttk.Entry(frame, width=30)
        entrada_direccion.insert(0, datos.get('direccion', ''))
        entrada_direccion.grid(row=5, column=1, pady=5, sticky=tk.EW)
        
        # Fecha de Registro con Calendar
        ttk.Label(frame, text="Fecha Registro:").grid(row=6, column=0, sticky=tk.W, pady=5)
        
        # Inicializar fecha de registro
        fecha_reg_str = datos.get('fecha_registro', '')
        if fecha_reg_str:
            try:
                # Formato: DD/MM/YYYY o DD/MM/YYYY HH:MM:SS
                fecha_parte = fecha_reg_str.split()[0]  # Obtener solo la parte de fecha
                dia_reg, mes_reg, año_reg = map(int, fecha_parte.split('/'))
            except (ValueError, AttributeError):
                dia_reg, mes_reg, año_reg = datetime.now().day, datetime.now().month, datetime.now().year
        else:
            dia_reg, mes_reg, año_reg = datetime.now().day, datetime.now().month, datetime.now().year
        
        # Calendar para fecha de registro
        calendario_reg = Calendar(
            frame,
            selectmode='day',
            year=año_reg,
            month=mes_reg,
            day=dia_reg,
            font=("Arial", 9),
            background='#1e1e1e' if self.tema_oscuro else '#ffffff',
            foreground='#ffffff' if self.tema_oscuro else '#000000',
            headersforeground='#ffffff' if self.tema_oscuro else '#000000',
            headersbackground='#2b2b2b' if self.tema_oscuro else '#e0e0e0',
            normalbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            normalforeground='#ffffff' if self.tema_oscuro else '#000000',
            othermonthweforeground='#666666' if self.tema_oscuro else '#cccccc',
            othermonthwebackground='#1e1e1e' if self.tema_oscuro else '#f0f0f0',
            weekendforeground='#ff9999' if self.tema_oscuro else '#cc0000',
            weekendbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            selectforeground='#ffffff' if self.tema_oscuro else '#000000',
            selectbackground='#0078d4'
        )
        calendario_reg.grid(row=6, column=1, pady=5, sticky=tk.EW)
        
        # Fecha de Nacimiento con Calendar - SIEMPRE VISIBLE
        ttk.Label(frame, text="Fecha Nacimiento:").grid(row=7, column=0, sticky=tk.W, pady=5)
        
        # Inicializar fecha
        fecha_nac_str = datos.get('fecha_nacimiento', '')
        if fecha_nac_str:
            try:
                dia_ini, mes_ini, año_ini = map(int, fecha_nac_str.split('/'))
            except (ValueError, AttributeError):
                dia_ini, mes_ini, año_ini = 1, 1, 2000
        else:
            dia_ini, mes_ini, año_ini = 1, 1, 2000
        
        # Calendar para seleccionar fecha
        calendario = Calendar(
            frame,
            selectmode='day',
            year=año_ini,
            month=mes_ini,
            day=dia_ini,
            font=("Arial", 9),
            background='#1e1e1e' if self.tema_oscuro else '#ffffff',
            foreground='#ffffff' if self.tema_oscuro else '#000000',
            headersforeground='#ffffff' if self.tema_oscuro else '#000000',
            headersbackground='#2b2b2b' if self.tema_oscuro else '#e0e0e0',
            normalbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            normalforeground='#ffffff' if self.tema_oscuro else '#000000',
            othermonthweforeground='#666666' if self.tema_oscuro else '#cccccc',
            othermonthwebackground='#1e1e1e' if self.tema_oscuro else '#f0f0f0',
            weekendforeground='#ff9999' if self.tema_oscuro else '#cc0000',
            weekendbackground='#2b2b2b' if self.tema_oscuro else '#ffffff',
            selectforeground='#ffffff' if self.tema_oscuro else '#000000',
            selectbackground='#0078d4'
        )
        calendario.grid(row=7, column=1, pady=5, sticky=tk.EW)
        
        frame.columnconfigure(1, weight=1)
        
        def guardar():
            nombre = entrada_nombre.get().strip()
            apellido = entrada_apellido.get().strip()
            telefono = entrada_telefono.get().strip()
            email = entrada_email.get().strip() or None
            direccion = entrada_direccion.get().strip() or None
            
            # Validar nombre
            valido, error = validators.es_nombre_valido(nombre)
            if not valido:
                messagebox.showerror("Error de validación", error)
                return
            
            # Validar apellido
            valido, error = validators.es_apellido_valido(apellido)
            if not valido:
                messagebox.showerror("Error de validación", error)
                return
            
            # Validar teléfono
            valido, error = validators.es_telefono_valido(telefono)
            if not valido:
                messagebox.showerror("Error de validación", error)
                return
            
            # Validar email (si se proporciona)
            if email:
                valido, error = validators.es_email_valido(email)
                if not valido:
                    messagebox.showerror("Error de validación", error)
                    return
            
            # Validar dirección (si se proporciona)
            if direccion:
                valido, error = validators.es_direccion_valida(direccion)
                if not valido:
                    messagebox.showerror("Error de validación", error)
                    return
            
            # Obtener fechas de los calendarios
            fecha_reg_obj = calendario_reg.get_date()
            fecha_nac_obj = calendario.get_date()
            fecha_reg = fecha_reg_obj.strftime("%d/%m/%Y")
            fecha_nac = fecha_nac_obj.strftime("%d/%m/%Y")
            
            # Usar el controlador para actualizar el contacto
            exito, mensaje = self.controlador.actualizar_contacto(
                id_contacto, nombre, apellido, telefono, email, direccion, fecha_nac, fecha_reg
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_dialogo.destroy()
                self._cargar_contactos_en_tabla()
            else:
                messagebox.showerror("Error de validación", mensaje)
        
        # Frame de botones

        
        ttk.Button(frame, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Cancelar", command=ventana_dialogo.destroy).pack(side=tk.LEFT, padx=5)
    
    def _eliminar_contacto(self) -> None:
        """Elimina el contacto seleccionado."""
        id_contacto, datos = self._obtener_contacto_seleccionado()
        if not id_contacto:
            return
        
        nombre_completo = f"{datos.get('nombre', '')} {datos.get('apellido', '')}"
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar a '{nombre_completo}'?"
        )
        
        if confirmacion:
            exito, mensaje = self.controlador.eliminar_contacto(id_contacto)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self._cargar_contactos_en_tabla()
            else:
                messagebox.showerror("Error", mensaje)
    
    def _actualizar_estado(self) -> None:
        """Actualiza la barra de estado."""
        total = len(self.controlador.obtener_todos_contactos())
        self.estado.config(text=f"Total de contactos: {total}")
    
    def _abrir_filtros(self) -> None:
        """Abre un diálogo para filtrar contactos con múltiples opciones."""
        ventana_dialogo = tk.Toplevel(self.ventana)
        ventana_dialogo.title("Filtro")
        ventana_dialogo.geometry("400x600")
        ventana_dialogo.resizable(True, True)
        
        # Aplicar colores del tema
        colores = self.COLORES_OSCURO if self.tema_oscuro else self.COLORES_CLARO
        ventana_dialogo.config(bg=colores['bg_frame'])
        
        # Crear frame con scrollbar
        frame_contenedor = ttk.Frame(ventana_dialogo)
        frame_contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar para el scroll
        canvas = tk.Canvas(
            frame_contenedor, 
            bg=colores['bg_frame'], 
            highlightthickness=0,
            relief=tk.FLAT
        )
        scrollbar = ttk.Scrollbar(frame_contenedor, orient=tk.VERTICAL, command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=colores['bg_frame'])
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Permitir scroll con mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Empacar canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Título de filtros
        titulo = tk.Label(frame_scroll, text="Filtros de búsqueda", font=("Arial", 10, "bold"), 
                         bg=colores['bg_frame'], fg=colores['fg'])
        titulo.pack(anchor=tk.W, pady=10)
        
        # ===== FILTRO POR NOMBRE =====
        etiqueta = tk.Label(frame_scroll, text="Nombre:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W)
        entrada_nombre = ttk.Entry(frame_scroll, width=35)
        entrada_nombre.pack(pady=5, fill=tk.X)
        
        # ===== FILTRO POR APELLIDO =====
        etiqueta = tk.Label(frame_scroll, text="Apellido:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W, pady=(10, 0))
        entrada_apellido = ttk.Entry(frame_scroll, width=35)
        entrada_apellido.pack(pady=5, fill=tk.X)
        
        # ===== FILTRO POR TELÉFONO =====
        etiqueta = tk.Label(frame_scroll, text="Teléfono:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W, pady=(10, 0))
        entrada_telefono = ttk.Entry(frame_scroll, width=35)
        entrada_telefono.pack(pady=5, fill=tk.X)
        
        # ===== FILTRO POR EMAIL =====
        etiqueta = tk.Label(frame_scroll, text="Email:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W, pady=(10, 0))
        entrada_email = ttk.Entry(frame_scroll, width=35)
        entrada_email.pack(pady=5, fill=tk.X)
        
        # ===== FILTRO POR DIRECCIÓN =====
        etiqueta = tk.Label(frame_scroll, text="Dirección:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W, pady=(10, 0))
        entrada_direccion = ttk.Entry(frame_scroll, width=35)
        entrada_direccion.pack(pady=5, fill=tk.X)
        
        # ===== FILTRO POR EDAD =====
        separador = tk.Frame(frame_scroll, bg=colores['fg'], height=1)
        separador.pack(fill=tk.X, pady=15)
        
        etiqueta_edad = tk.Label(frame_scroll, text="Edad (opcional):", font=("Arial", 9, "bold"),
                                bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta_edad.pack(anchor=tk.W)
        
        # Opción 1: Edad exacta
        etiqueta = tk.Label(frame_scroll, text="Edad exacta:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W, pady=(10, 0))
        entrada_edad_exacta = ttk.Entry(frame_scroll, width=35)
        entrada_edad_exacta.pack(pady=5, fill=tk.X)
        
        # Opción 2: Rango de edad
        etiqueta = tk.Label(frame_scroll, text="Edad mínima:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W, pady=(10, 0))
        entrada_edad_min = ttk.Entry(frame_scroll, width=35)
        entrada_edad_min.pack(pady=5, fill=tk.X)
        
        etiqueta = tk.Label(frame_scroll, text="Edad máxima:", bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta.pack(anchor=tk.W, pady=(5, 0))
        entrada_edad_max = ttk.Entry(frame_scroll, width=35)
        entrada_edad_max.pack(pady=5, fill=tk.X)
        
        # Separator
        separador2 = tk.Frame(frame_scroll, bg=colores['fg'], height=1)
        separador2.pack(fill=tk.X, pady=15)
        
        # ===== FILTRO POR FECHA DE REGISTRO =====
        etiqueta_fecha = tk.Label(frame_scroll, text="Fecha de Registro:", font=("Arial", 9, "bold"),
                                 bg=colores['bg_frame'], fg=colores['fg'])
        etiqueta_fecha.pack(anchor=tk.W)
        entrada_fecha_reg = ttk.Entry(frame_scroll, width=35)
        entrada_fecha_reg.pack(pady=5, fill=tk.X)
        ttk.Label(frame_scroll, text="(Ej: 11/05/2026 o 11/05)", font=("Arial", 8)).pack(anchor=tk.W)
        
        # Separator
        separador3 = tk.Frame(frame_scroll, bg=colores['fg'], height=1)
        separador3.pack(fill=tk.X, pady=15)
        
        def aplicar_filtros():
            # Obtener valores de filtros
            filtro_nombre = entrada_nombre.get().strip().lower()
            filtro_apellido = entrada_apellido.get().strip().lower()
            filtro_telefono = entrada_telefono.get().strip().lower()
            filtro_email = entrada_email.get().strip().lower()
            filtro_direccion = entrada_direccion.get().strip().lower()
            filtro_fecha_reg = entrada_fecha_reg.get().strip().lower()
            
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            resultados = {}
            contactos = self.controlador.obtener_todos_contactos()
            
            for id_contacto, datos in contactos.items():
                nombre = datos.get('nombre', '').lower()
                apellido = datos.get('apellido', '').lower()
                telefono = datos.get('telefono', '').lower()
                email = datos.get('email', '').lower()
                direccion = datos.get('direccion', '').lower()
                fecha_registro = datos.get('fecha_registro', '').lower()
                fecha_nac = datos.get('fecha_nacimiento', '')
                
                # Verificar filtros de texto
                cumple_nombre = not filtro_nombre or filtro_nombre in nombre
                cumple_apellido = not filtro_apellido or filtro_apellido in apellido
                cumple_telefono = not filtro_telefono or filtro_telefono in telefono
                cumple_email = not filtro_email or filtro_email in email
                cumple_direccion = not filtro_direccion or filtro_direccion in direccion
                cumple_fecha_reg = not filtro_fecha_reg or filtro_fecha_reg in fecha_registro
                
                # Verificar filtros de edad
                cumple_edad = True
                edad_exacta = entrada_edad_exacta.get().strip()
                edad_min = entrada_edad_min.get().strip()
                edad_max = entrada_edad_max.get().strip()
                
                if edad_exacta or edad_min or edad_max:
                    if fecha_nac:
                        try:
                            dia, mes, año = map(int, fecha_nac.split('/'))
                            fecha_nac_obj = datetime(año, mes, dia)
                            hoy = datetime.now()
                            edad_calc = hoy.year - fecha_nac_obj.year
                            if (hoy.month, hoy.day) < (fecha_nac_obj.month, fecha_nac_obj.day):
                                edad_calc -= 1
                            
                            if edad_exacta:
                                try:
                                    cumple_edad = edad_calc == int(edad_exacta)
                                except ValueError:
                                    messagebox.showerror("Error", "La edad exacta debe ser un número.")
                                    return
                            elif edad_min or edad_max:
                                edad_min_int = int(edad_min) if edad_min else 0
                                edad_max_int = int(edad_max) if edad_max else 150
                                cumple_edad = edad_min_int <= edad_calc <= edad_max_int
                        except (ValueError, AttributeError):
                            cumple_edad = False
                    else:
                        cumple_edad = False
                
                # Si cumple todos los filtros, agregar a resultados
                if (cumple_nombre and cumple_apellido and cumple_telefono and 
                    cumple_email and cumple_direccion and cumple_edad and cumple_fecha_reg):
                    resultados[id_contacto] = datos
            
            # Mostrar resultados
            for id_contacto, datos in resultados.items():
                # Calcular edad
                fecha_nac = datos.get('fecha_nacimiento', '')
                edad = ''
                if fecha_nac:
                    try:
                        dia, mes, año = map(int, fecha_nac.split('/'))
                        fecha_nac_obj = datetime(año, mes, dia)
                        hoy = datetime.now()
                        edad_calc = hoy.year - fecha_nac_obj.year
                        if (hoy.month, hoy.day) < (fecha_nac_obj.month, fecha_nac_obj.day):
                            edad_calc -= 1
                        edad = str(edad_calc)
                    except (ValueError, AttributeError):
                        edad = ''
                
                self.tabla.insert(
                    '',
                    'end',
                    text='',
                    values=(
                        id_contacto,
                        datos.get('nombre', ''),
                        datos.get('apellido', ''),
                        datos.get('telefono', ''),
                        edad,
                        datos.get('email', ''),
                        datos.get('direccion', ''),
                        datos.get('fecha_registro', '')
                    )
                )
            
            self._actualizar_estado()
            if resultados:
                messagebox.showinfo("Búsqueda", f"Se encontraron {len(resultados)} contacto(s).")
            else:
                messagebox.showinfo("Búsqueda", "No se encontraron contactos con esos criterios.")
            ventana_dialogo.destroy()
        
        # Frame de botones en el frame scroll
        frame_botones = tk.Frame(frame_scroll, bg=colores['bg_frame'])
        frame_botones.pack(fill=tk.X, pady=10)
        
        ttk.Button(frame_botones, text="Aplicar Filtros", command=aplicar_filtros).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=lambda: [
            entrada_nombre.delete(0, tk.END),
            entrada_apellido.delete(0, tk.END),
            entrada_telefono.delete(0, tk.END),
            entrada_email.delete(0, tk.END),
            entrada_direccion.delete(0, tk.END),
            entrada_fecha_reg.delete(0, tk.END),
            entrada_edad_exacta.delete(0, tk.END),
            entrada_edad_min.delete(0, tk.END),
            entrada_edad_max.delete(0, tk.END)
        ]).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana_dialogo.destroy).pack(side=tk.LEFT, padx=5)
    
    def iniciar(self) -> None:
        """Inicia la aplicación gráfica."""
        self.ventana.mainloop()
