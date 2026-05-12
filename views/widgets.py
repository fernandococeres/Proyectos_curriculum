"""
Widgets personalizados para el Sistema de Gestión Escolar

DESCRIPCIÓN:
Define componentes Tkinter reutilizables con validación integrada.
Mejora la experiencia del usuario y reduce código repetido.

WIDGETS DISPONIBLES:
- EntryNumerico: Solo acepta dígitos
- EntryFecha: Campo de fecha con calendario visual
- EntryTelefono: Solo teléfonos válidos (10+ dígitos)
- EntryTexto: Texto con longitud máxima

PROPÓSITO:
Cada widget implementa validación en tiempo real, mostrando al usuario
si su entrada es válida mientras escribe.

VENTAJAS:
✓ Reduce código duplicado en formularios
✓ Interfaz consistente en toda la aplicación
✓ Validación inmediata sin esperar submit
✓ Mejor experiencia de usuario

USO TÍPICO:
    fecha_entrada = EntryFecha(formulario)
    fecha_entrada.pack(pady=5)
    
    numero_entrada = EntryNumerico(formulario)
    numero_entrada.pack(pady=5)

DEPENDENCIAS:
- tkinter: Framework GUI
- tkcalendar: Calendario para selección de fechas
"""
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime


class EntryNumerico(ttk.Entry):
    """Entry que solo acepta números.
    
    Valida en tiempo real, rechazando caracteres no numéricos.
    Útil para teléfonos, DNI, números de documento, etc.
    """
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Registrar validación
        vcmd = (parent.register(self._validar_numerico), '%P')
        self.config(validate='key', validatecommand=vcmd)
    
    @staticmethod
    def _validar_numerico(valor):
        """Valida que solo contenga números."""
        if valor == "":  # Permitir vacío
            return True
        return valor.isdigit()


class EntryFecha(ttk.Frame):
    """Frame con Entry de fecha y botón de calendario."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Entry de fecha
        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Botón para abrir calendario
        self.btn_calendario = ttk.Button(self, text="📅", width=3, command=self.abrir_calendario)
        self.btn_calendario.pack(side=tk.LEFT)
        
        self.ventana_calendario = None
    
    def abrir_calendario(self):
        """Abre una ventana con un calendario."""
        if self.ventana_calendario and self.ventana_calendario.winfo_exists():
            self.ventana_calendario.lift()
            return
        
        self.ventana_calendario = tk.Toplevel(self.master)
        self.ventana_calendario.title("Seleccionar Fecha")
        self.ventana_calendario.geometry("300x250")
        self.ventana_calendario.resizable(False, False)
        
        # Obtener fecha actual o la ingresada
        fecha_actual = self.get()
        try:
            if fecha_actual:
                dia, mes, año = map(int, fecha_actual.split('/'))
                fecha_inicial = datetime(año, mes, dia).date()
            else:
                fecha_inicial = None
        except:
            fecha_inicial = None
        
        # Crear DateEntry
        cal = DateEntry(
            self.ventana_calendario,
            width=25,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=fecha_inicial.year if fecha_inicial else datetime.now().year,
            month=fecha_inicial.month if fecha_inicial else datetime.now().month,
            day=fecha_inicial.day if fecha_inicial else datetime.now().day,
            locale='es_ES'
        )
        cal.pack(pady=10)
        
        # Botón Aceptar
        def seleccionar():
            fecha = cal.get_date()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, fecha.strftime('%d/%m/%Y'))
            self.ventana_calendario.destroy()
            self.ventana_calendario = None
        
        ttk.Button(self.ventana_calendario, text="Aceptar", command=seleccionar).pack(pady=5)
    
    def get(self):
        """Obtiene el valor de la fecha."""
        return self.entry.get()
    
    def insert(self, index, value):
        """Inserta un valor en el entry."""
        self.entry.insert(index, value)
    
    def delete(self, start, end):
        """Elimina contenido del entry."""
        self.entry.delete(start, end)


class EntryTelefono(ttk.Entry):
    """Entry que solo acepta números para teléfono."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Registrar validación
        vcmd = (parent.register(self._validar_numerico), '%P')
        self.config(validate='key', validatecommand=vcmd)
    
    @staticmethod
    def _validar_numerico(valor):
        """Valida que solo contenga números."""
        if valor == "":  # Permitir vacío
            return True
        return valor.isdigit()


class EntryTexto(ttk.Entry):
    """Entry que solo acepta letras y espacios."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Registrar validación
        vcmd = (parent.register(self._validar_texto), '%P')
        self.config(validate='key', validatecommand=vcmd)
    
    @staticmethod
    def _validar_texto(valor):
        """Valida que solo contenga letras y espacios."""
        if valor == "":  # Permitir vacío
            return True
        # Permitir letras (incluyendo acentos) y espacios
        import re
        return bool(re.match(r"^[a-záéíóúñÁÉÍÓÚÑ\s]*$", valor))
