"""
Vistas administrativas para el Sistema de Gestión Escolar

DESCRIPCIÓN:
Proporciona interfaces para administradores y personal de gestión.
Permite ver estadísticas, generar reportes y exportar datos.

CLASES:
- AdminAlumnosView: Panel administrativo para alumnos
- AdminProfesoresView: Panel administrativo para profesores

FUNCIONALIDADES:

Pestaña Estadísticas:
✓ Total de alumnos/profesores
✓ Distribución por grado
✓ Distribución por asignatura
✓ Gráficos de barras

Pestaña Reportes:
✓ Alumnos por grado y asignatura
✓ Alumnos y profesores por documento
✓ Reportes filtrados

Pestaña Exportación:
✓ Exportar a CSV (compatible con Excel)
✓ Exportar a XLSX (formato Excel nativo)
✓ Seleccionar ruta de guardado

ACCESO:
Accesible desde menú principal > Administración
O desde botones en VentanaPrincipal

IMPORTANCIA:
Herramienta clave para toma de decisiones administrativas.
Permite análisis de datos y generación de reportes formales.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from views.centrar_ventana import centrar_ventana
from views.tema import aplicar_tema_oscuro
from controllers.admin import AdminAlumnos, AdminProfesores
from datetime import datetime


class AdminAlumnosView:
    """Ventana administrativa para alumnos.
    
    Proporciona:
    - Estadísticas detalladas de alumnos
    - Reportes por grado, asignatura, documento
    - Exportación a CSV y Excel
    
    Atributos:
        ventana (tk.Toplevel): Ventana secundaria
        admin (AdminAlumnos): Controlador administrativo
        notebook (ttk.Notebook): Pestañas para diferentes vistas
    """
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Administración de Alumnos")
        centrar_ventana(self.ventana, 1000, 700)
        
        # Aplicar tema oscuro a ventana secundaria
        self.style = ttk.Style()
        self.colores, self.style = aplicar_tema_oscuro(self.ventana, self.style)
        
        self.admin = AdminAlumnos()
        
        self.crear_interfaz()
        self.cargar_estadisticas()
    
    def crear_interfaz(self):
        """Crea los elementos de la interfaz."""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Estadísticas
        frame_stats = ttk.Frame(self.notebook)
        self.notebook.add(frame_stats, text="Estadísticas")
        self.crear_tab_estadisticas(frame_stats)
        
        # Pestaña 2: Reportes
        frame_reportes = ttk.Frame(self.notebook)
        self.notebook.add(frame_reportes, text="Reportes")
        self.crear_tab_reportes(frame_reportes)
        
        # Pestaña 3: Exportación
        frame_export = ttk.Frame(self.notebook)
        self.notebook.add(frame_export, text="Exportación")
        self.crear_tab_exportacion(frame_export)
    
    def crear_tab_estadisticas(self, parent):
        """Crea la pestaña de estadísticas."""
        marco_principal = ttk.Frame(parent, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(marco_principal, text="ESTADÍSTICAS GENERALES", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Grid de estadísticas
        self.labels_stats = {}
        
        # Total de alumnos
        ttk.Label(marco_principal, text="Total de Alumnos:").grid(row=1, column=0, sticky="W", padx=10, pady=10)
        self.labels_stats['total'] = ttk.Label(marco_principal, text="0", font=("Arial", 12, "bold"))
        self.labels_stats['total'].grid(row=1, column=1, sticky="W", padx=10, pady=10)
        
        # Marco para grados
        frame_grados = ttk.LabelFrame(marco_principal, text="Alumnos por Grado", padding="10")
        frame_grados.grid(row=2, column=0, columnspan=2, sticky="EW", padx=10, pady=10)
        
        self.text_grados = tk.Text(frame_grados, height=6, width=50)
        self.text_grados.pack(fill=tk.BOTH, expand=True)
        
        # Marco para secciones
        frame_secciones = ttk.LabelFrame(marco_principal, text="Alumnos por Sección", padding="10")
        frame_secciones.grid(row=3, column=0, columnspan=2, sticky="EW", padx=10, pady=10)
        
        self.text_secciones = tk.Text(frame_secciones, height=4, width=50)
        self.text_secciones.pack(fill=tk.BOTH, expand=True)
        
        # Marco para grado y sección
        frame_combo = ttk.LabelFrame(marco_principal, text="Alumnos por Grado y Sección", padding="10")
        frame_combo.grid(row=4, column=0, columnspan=2, sticky="EW", padx=10, pady=10)
        
        self.text_combo = tk.Text(frame_combo, height=8, width=50)
        self.text_combo.pack(fill=tk.BOTH, expand=True)
        
        # Botón de refrescar
        ttk.Button(marco_principal, text="Refrescar Estadísticas", 
                  command=self.cargar_estadisticas).grid(row=5, column=0, columnspan=2, pady=20)
    
    def crear_tab_reportes(self, parent):
        """Crea la pestaña de reportes."""
        marco_principal = ttk.Frame(parent, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(marco_principal, text="REPORTES ESPECIALES", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Botón: Alumnos sin email
        ttk.Button(marco_principal, text="Alumnos sin Email", 
                  command=self.reporte_sin_email).grid(row=1, column=0, padx=10, pady=10, sticky="EW")
        
        # Botón: Alumnos recientes
        ttk.Button(marco_principal, text="Alumnos Registrados (Últimos 7 días)", 
                  command=self.reporte_recientes).grid(row=1, column=1, padx=10, pady=10, sticky="EW")
        
        # Botón: Por grado
        ttk.Button(marco_principal, text="Alumnos por Grado Específico", 
                  command=self.reporte_por_grado).grid(row=2, column=0, padx=10, pady=10, sticky="EW")
        
        # Botón: Por sección
        ttk.Button(marco_principal, text="Alumnos por Sección Específica", 
                  command=self.reporte_por_seccion).grid(row=2, column=1, padx=10, pady=10, sticky="EW")
        
        # Área de resultados
        frame_resultados = ttk.LabelFrame(marco_principal, text="Resultados", padding="10")
        frame_resultados.grid(row=3, column=0, columnspan=2, sticky="EWNS", padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_reportes = tk.Text(frame_resultados, height=20, width=70, yscrollcommand=scrollbar.set)
        self.text_reportes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_reportes.yview)
    
    def crear_tab_exportacion(self, parent):
        """Crea la pestaña de exportación."""
        marco_principal = ttk.Frame(parent, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(marco_principal, text="EXPORTAR DATOS", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Botones de exportación
        ttk.Button(marco_principal, text="Exportar a Excel", 
                  command=self.exportar_excel).grid(row=1, column=0, padx=10, pady=20, sticky="EW")
        
        ttk.Button(marco_principal, text="Exportar a CSV", 
                  command=self.exportar_csv).grid(row=1, column=1, padx=10, pady=20, sticky="EW")
        
        # Info
        info_frame = ttk.LabelFrame(marco_principal, text="Información", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky="EWNS", padx=10, pady=10)
        
        info_text = (
            "Excel:\n"
            "• Formato profesional con estilos\n"
            "• Hoja de estadísticas incluida\n"
            "• Compatible con Excel, Google Sheets, LibreOffice\n\n"
            "CSV:\n"
            "• Formato separado por punto y coma\n"
            "• Abierto por cualquier editor de texto\n"
            "• Compatible con bases de datos\n\n"
            "Los archivos se guardan en la carpeta actual"
        )
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack()
        
        # Etiqueta de estado
        self.label_export_status = ttk.Label(marco_principal, text="", foreground="green")
        self.label_export_status.grid(row=3, column=0, columnspan=2, pady=10)
    
    def cargar_estadisticas(self):
        """Carga las estadísticas."""
        try:
            stats = self.admin.get_estadisticas_generales()
            
            # Actualizar total
            self.labels_stats['total'].config(text=str(stats['total_alumnos']))
            
            # Grados
            self.text_grados.delete(1.0, tk.END)
            for grado, cantidad in sorted(stats['grados'].items()):
                self.text_grados.insert(tk.END, f"Grado {grado}: {cantidad} alumno(s)\n")
            
            # Secciones
            self.text_secciones.delete(1.0, tk.END)
            for seccion, cantidad in sorted(stats['secciones'].items()):
                self.text_secciones.insert(tk.END, f"Sección {seccion}: {cantidad} alumno(s)\n")
            
            # Combinado
            self.text_combo.delete(1.0, tk.END)
            for combo, cantidad in stats['alumnos_por_grado_seccion'].items():
                self.text_combo.insert(tk.END, f"{combo}: {cantidad} alumno(s)\n")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estadísticas: {e}")
    
    def reporte_sin_email(self):
        """Muestra reporte de alumnos sin email."""
        try:
            alumnos = self.admin.get_alumnos_sin_email()
            self.mostrar_reporte(f"ALUMNOS SIN EMAIL ({len(alumnos)})", alumnos)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def reporte_recientes(self):
        """Muestra reporte de alumnos recientes."""
        try:
            alumnos = self.admin.get_alumnos_recientes(7)
            self.mostrar_reporte(f"ALUMNOS REGISTRADOS EN ÚLTIMOS 7 DÍAS ({len(alumnos)})", alumnos)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def reporte_por_grado(self):
        """Muestra reporte de alumnos por grado seleccionado."""
        try:
            stats = self.admin.get_estadisticas_generales()
            grados = list(stats['grados'].keys())
            
            if not grados:
                messagebox.showwarning("Aviso", "No hay grados registrados")
                return
            
            # Diálogo para seleccionar grado
            ventana_dialogo = tk.Toplevel(self.ventana)
            ventana_dialogo.title("Seleccionar Grado")
            centrar_ventana(ventana_dialogo, 300, 150)
            
            ttk.Label(ventana_dialogo, text="Selecciona el grado:").pack(pady=10)
            combo_grado = ttk.Combobox(ventana_dialogo, values=grados, state="readonly")
            combo_grado.pack(pady=10, padx=20, fill=tk.X)
            
            def mostrar():
                grado = combo_grado.get()
                if grado:
                    alumnos = self.admin.get_alumnos_por_grado(grado)
                    self.mostrar_reporte(f"ALUMNOS DEL GRADO {grado} ({len(alumnos)})", alumnos)
                    ventana_dialogo.destroy()
            
            ttk.Button(ventana_dialogo, text="Mostrar", command=mostrar).pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def reporte_por_seccion(self):
        """Muestra reporte de alumnos por sección seleccionada."""
        try:
            stats = self.admin.get_estadisticas_generales()
            secciones = list(stats['secciones'].keys())
            
            if not secciones:
                messagebox.showwarning("Aviso", "No hay secciones registradas")
                return
            
            # Diálogo para seleccionar sección
            ventana_dialogo = tk.Toplevel(self.ventana)
            ventana_dialogo.title("Seleccionar Sección")
            centrar_ventana(ventana_dialogo, 300, 150)
            
            ttk.Label(ventana_dialogo, text="Selecciona la sección:").pack(pady=10)
            combo_seccion = ttk.Combobox(ventana_dialogo, values=secciones, state="readonly")
            combo_seccion.pack(pady=10, padx=20, fill=tk.X)
            
            def mostrar():
                seccion = combo_seccion.get()
                if seccion:
                    alumnos = self.admin.get_alumnos_por_seccion(seccion)
                    self.mostrar_reporte(f"ALUMNOS DE LA SECCIÓN {seccion} ({len(alumnos)})", alumnos)
                    ventana_dialogo.destroy()
            
            ttk.Button(ventana_dialogo, text="Mostrar", command=mostrar).pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def mostrar_reporte(self, titulo: str, alumnos: list):
        """Muestra un reporte en el text widget."""
        self.text_reportes.delete(1.0, tk.END)
        self.text_reportes.insert(tk.END, titulo + "\n")
        self.text_reportes.insert(tk.END, "=" * 80 + "\n\n")
        
        if not alumnos:
            self.text_reportes.insert(tk.END, "No hay registros.\n")
        else:
            for alumno in alumnos:
                self.text_reportes.insert(tk.END, 
                    f"ID: {alumno[0]} | {alumno[1]} {alumno[2]} | Email: {alumno[3]} | "
                    f"Tel: {alumno[4]} | {alumno[6]}° {alumno[7]}\n")
    
    def exportar_excel(self):
        """Exporta a Excel."""
        try:
            archivo = self.admin.exportar_a_excel()
            self.label_export_status.config(text=f"✓ Exportado a: {archivo}", foreground="green")
            messagebox.showinfo("Éxito", f"Archivo creado: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def exportar_csv(self):
        """Exporta a CSV."""
        try:
            archivo = self.admin.exportar_a_csv()
            self.label_export_status.config(text=f"✓ Exportado a: {archivo}", foreground="green")
            messagebox.showinfo("Éxito", f"Archivo creado: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


class AdminProfesoresView:
    """Ventana administrativa para profesores."""
    
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Administración de Profesores")
        centrar_ventana(self.ventana, 1000, 700)
        
        # Aplicar tema oscuro a ventana secundaria
        self.style = ttk.Style()
        self.colores, self.style = aplicar_tema_oscuro(self.ventana, self.style)
        
        self.admin = AdminProfesores()
        
        self.crear_interfaz()
        self.cargar_estadisticas()
    
    def crear_interfaz(self):
        """Crea los elementos de la interfaz."""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Estadísticas
        frame_stats = ttk.Frame(self.notebook)
        self.notebook.add(frame_stats, text="Estadísticas")
        self.crear_tab_estadisticas(frame_stats)
        
        # Pestaña 2: Reportes
        frame_reportes = ttk.Frame(self.notebook)
        self.notebook.add(frame_reportes, text="Reportes")
        self.crear_tab_reportes(frame_reportes)
        
        # Pestaña 3: Exportación
        frame_export = ttk.Frame(self.notebook)
        self.notebook.add(frame_export, text="Exportación")
        self.crear_tab_exportacion(frame_export)
    
    def crear_tab_estadisticas(self, parent):
        """Crea la pestaña de estadísticas."""
        marco_principal = ttk.Frame(parent, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(marco_principal, text="ESTADÍSTICAS GENERALES", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Grid de estadísticas
        self.labels_stats = {}
        
        # Total de profesores
        ttk.Label(marco_principal, text="Total de Profesores:").grid(row=1, column=0, sticky="W", padx=10, pady=10)
        self.labels_stats['total'] = ttk.Label(marco_principal, text="0", font=("Arial", 12, "bold"))
        self.labels_stats['total'].grid(row=1, column=1, sticky="W", padx=10, pady=10)
        
        # Sin email
        ttk.Label(marco_principal, text="Profesores sin Email:").grid(row=2, column=0, sticky="W", padx=10, pady=10)
        self.labels_stats['sin_email'] = ttk.Label(marco_principal, text="0", font=("Arial", 12, "bold"))
        self.labels_stats['sin_email'].grid(row=2, column=1, sticky="W", padx=10, pady=10)
        
        # Marco para especialidades
        frame_especialidades = ttk.LabelFrame(marco_principal, text="Profesores por Especialidad", padding="10")
        frame_especialidades.grid(row=3, column=0, columnspan=2, sticky="EW", padx=10, pady=10)
        
        self.text_especialidades = tk.Text(frame_especialidades, height=10, width=50)
        self.text_especialidades.pack(fill=tk.BOTH, expand=True)
        
        # Botón de refrescar
        ttk.Button(marco_principal, text="Refrescar Estadísticas", 
                  command=self.cargar_estadisticas).grid(row=4, column=0, columnspan=2, pady=20)
    
    def crear_tab_reportes(self, parent):
        """Crea la pestaña de reportes."""
        marco_principal = ttk.Frame(parent, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(marco_principal, text="REPORTES ESPECIALES", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Botón: Profesores sin email
        ttk.Button(marco_principal, text="Profesores sin Email", 
                  command=self.reporte_sin_email).grid(row=1, column=0, padx=10, pady=10, sticky="EW")
        
        # Botón: Profesores sin documento
        ttk.Button(marco_principal, text="Profesores sin Documento", 
                  command=self.reporte_sin_documento).grid(row=1, column=1, padx=10, pady=10, sticky="EW")
        
        # Botón: Profesores recientes
        ttk.Button(marco_principal, text="Profesores Registrados (Últimos 7 días)", 
                  command=self.reporte_recientes).grid(row=2, column=0, padx=10, pady=10, sticky="EW")
        
        # Botón: Por especialidad
        ttk.Button(marco_principal, text="Profesores por Especialidad", 
                  command=self.reporte_por_especialidad).grid(row=2, column=1, padx=10, pady=10, sticky="EW")
        
        # Área de resultados
        frame_resultados = ttk.LabelFrame(marco_principal, text="Resultados", padding="10")
        frame_resultados.grid(row=3, column=0, columnspan=2, sticky="EWNS", padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_resultados)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_reportes = tk.Text(frame_resultados, height=20, width=70, yscrollcommand=scrollbar.set)
        self.text_reportes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_reportes.yview)
    
    def crear_tab_exportacion(self, parent):
        """Crea la pestaña de exportación."""
        marco_principal = ttk.Frame(parent, padding="20")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(marco_principal, text="EXPORTAR DATOS", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Botones de exportación
        ttk.Button(marco_principal, text="Exportar a Excel", 
                  command=self.exportar_excel).grid(row=1, column=0, padx=10, pady=20, sticky="EW")
        
        ttk.Button(marco_principal, text="Exportar a CSV", 
                  command=self.exportar_csv).grid(row=1, column=1, padx=10, pady=20, sticky="EW")
        
        # Info
        info_frame = ttk.LabelFrame(marco_principal, text="Información", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky="EWNS", padx=10, pady=10)
        
        info_text = (
            "Excel:\n"
            "• Formato profesional con estilos\n"
            "• Hoja de estadísticas incluida\n"
            "• Compatible con Excel, Google Sheets, LibreOffice\n\n"
            "CSV:\n"
            "• Formato separado por punto y coma\n"
            "• Abierto por cualquier editor de texto\n"
            "• Compatible con bases de datos\n\n"
            "Los archivos se guardan en la carpeta actual"
        )
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack()
        
        # Etiqueta de estado
        self.label_export_status = ttk.Label(marco_principal, text="", foreground="green")
        self.label_export_status.grid(row=3, column=0, columnspan=2, pady=10)
    
    def cargar_estadisticas(self):
        """Carga las estadísticas."""
        try:
            stats = self.admin.get_estadisticas_generales()
            
            # Actualizar total
            self.labels_stats['total'].config(text=str(stats['total_profesores']))
            self.labels_stats['sin_email'].config(text=str(stats['profesores_sin_email']))
            
            # Especialidades
            self.text_especialidades.delete(1.0, tk.END)
            for especialidad, cantidad in stats['especialidades'].items():
                self.text_especialidades.insert(tk.END, f"{especialidad}: {cantidad} profesor(es)\n")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estadísticas: {e}")
    
    def reporte_sin_email(self):
        """Muestra reporte de profesores sin email."""
        try:
            profesores = self.admin.get_profesores_sin_email()
            self.mostrar_reporte(f"PROFESORES SIN EMAIL ({len(profesores)})", profesores)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def reporte_sin_documento(self):
        """Muestra reporte de profesores sin documento."""
        try:
            profesores = self.admin.get_profesores_sin_documento()
            self.mostrar_reporte(f"PROFESORES SIN DOCUMENTO ({len(profesores)})", profesores)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def reporte_recientes(self):
        """Muestra reporte de profesores recientes."""
        try:
            profesores = self.admin.get_profesores_recientes(7)
            self.mostrar_reporte(f"PROFESORES REGISTRADOS EN ÚLTIMOS 7 DÍAS ({len(profesores)})", profesores)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def reporte_por_especialidad(self):
        """Muestra reporte de profesores por especialidad seleccionada."""
        try:
            especialidades = self.admin.get_especialidades()
            
            if not especialidades:
                messagebox.showwarning("Aviso", "No hay especialidades registradas")
                return
            
            # Diálogo para seleccionar especialidad
            ventana_dialogo = tk.Toplevel(self.ventana)
            ventana_dialogo.title("Seleccionar Especialidad")
            centrar_ventana(ventana_dialogo, 350, 150)
            
            ttk.Label(ventana_dialogo, text="Selecciona la especialidad:").pack(pady=10)
            combo_especialidad = ttk.Combobox(ventana_dialogo, values=especialidades, state="readonly", width=40)
            combo_especialidad.pack(pady=10, padx=20, fill=tk.X)
            
            def mostrar():
                especialidad = combo_especialidad.get()
                if especialidad:
                    profesores = self.admin.get_profesores_por_especialidad(especialidad)
                    self.mostrar_reporte(f"PROFESORES DE {especialidad.upper()} ({len(profesores)})", profesores)
                    ventana_dialogo.destroy()
            
            ttk.Button(ventana_dialogo, text="Mostrar", command=mostrar).pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def mostrar_reporte(self, titulo: str, profesores: list):
        """Muestra un reporte en el text widget."""
        self.text_reportes.delete(1.0, tk.END)
        self.text_reportes.insert(tk.END, titulo + "\n")
        self.text_reportes.insert(tk.END, "=" * 80 + "\n\n")
        
        if not profesores:
            self.text_reportes.insert(tk.END, "No hay registros.\n")
        else:
            for profesor in profesores:
                self.text_reportes.insert(tk.END, 
                    f"ID: {profesor[0]} | {profesor[1]} {profesor[2]} | Email: {profesor[3]} | "
                    f"Tel: {profesor[4]} | {profesor[5]} | Doc: {profesor[6]}\n")
    
    def exportar_excel(self):
        """Exporta a Excel."""
        try:
            archivo = self.admin.exportar_a_excel()
            self.label_export_status.config(text=f"✓ Exportado a: {archivo}", foreground="green")
            messagebox.showinfo("Éxito", f"Archivo creado: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def exportar_csv(self):
        """Exporta a CSV."""
        try:
            archivo = self.admin.exportar_a_csv()
            self.label_export_status.config(text=f"✓ Exportado a: {archivo}", foreground="green")
            messagebox.showinfo("Éxito", f"Archivo creado: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
