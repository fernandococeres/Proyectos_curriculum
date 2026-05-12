"""
Módulo de configuración de tema oscuro para el Sistema de Gestión Escolar

Proporciona funciones para aplicar un tema oscuro consistente en todas
las ventanas de la aplicación (principal, secundarias, diálogos, etc).
"""
from tkinter import ttk


def aplicar_tema_oscuro(root_window=None, style=None):
    """
    Configura y aplica el tema oscuro de la aplicación.
    
    Args:
        root_window: Ventana raíz para configurar background
        style: Objeto ttk.Style para configurar estilos
    
    Returns:
        tuple: (colores_dict, style) para referencia
    """
    
    # Paleta de colores oscuros
    colores = {
        'bg': '#1e1e1e',           # Fondo principal
        'fg': '#ffffff',           # Texto principal
        'btn_bg': '#2d2d2d',       # Fondo botones
        'btn_active': '#3d3d3d',   # Botones activos
        'entry_bg': '#2d2d2d',     # Fondo entrada
        'entry_fg': '#ffffff',     # Texto entrada
        'border': '#1a1a1a',       # Bordes principales
        'light_border': '#333333', # Bordes claros
        'tree_bg': '#252525',      # Fondo tabla
        'tree_fg': '#ffffff',      # Texto tabla
        'heading_bg': '#2d2d2d',   # Fondo encabezados
    }
    
    # Si no se proporciona style, crearlo
    if style is None:
        style = ttk.Style()
        style.theme_use('clam')
    
    # Configurar ventana raíz si se proporciona
    if root_window:
        root_window.configure(bg=colores['bg'])
    
    # Estilos generales base
    style.configure(".", 
                   background=colores['bg'], 
                   foreground=colores['fg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'])
    
    # Labels
    style.configure("TLabel", 
                   background=colores['bg'], 
                   foreground=colores['fg'])
    
    # Frames
    style.configure("TFrame", 
                   background=colores['bg'], 
                   relief="flat", 
                   borderwidth=0)
    
    # LabelFrames
    style.configure("TLabelframe", 
                   background=colores['bg'], 
                   foreground=colores['fg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'])
    style.configure("TLabelframe.Label", 
                   background=colores['bg'], 
                   foreground=colores['fg'])
    
    # Botones
    style.configure("TButton", 
                   background=colores['btn_bg'], 
                   foreground=colores['fg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'],
                   focuscolor=colores['btn_bg'], 
                   padding=5)
    style.map("TButton", 
             background=[("active", colores['btn_active']), 
                        ("pressed", colores['border'])])
    
    # Entry
    style.configure("TEntry", 
                   fieldbackground=colores['entry_bg'], 
                   foreground=colores['entry_fg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'])
    style.map("TEntry",
             fieldbackground=[("focus", colores['entry_bg'])])
    
    # Combobox
    style.configure("TCombobox", 
                   fieldbackground=colores['entry_bg'], 
                   foreground=colores['entry_fg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'])
    style.map("TCombobox", 
             fieldbackground=[("readonly", colores['entry_bg']),
                            ("focus", colores['entry_bg'])])
    
    # Spinbox
    style.configure("TSpinbox",
                   fieldbackground=colores['entry_bg'],
                   foreground=colores['entry_fg'],
                   bordercolor=colores['border'],
                   lightcolor=colores['light_border'],
                   darkcolor=colores['border'])
    
    # Separator (líneas divisoras)
    style.configure("TSeparator", background=colores['border'])
    
    # Treeview (Tablas)
    style.configure("Treeview", 
                   background=colores['tree_bg'], 
                   foreground=colores['tree_fg'],
                   fieldbackground=colores['tree_bg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'])
    style.map("Treeview", 
             background=[("selected", "#0078d7")], 
             foreground=[("selected", "#ffffff")])
    
    # Treeview Headings
    style.configure("Treeview.Heading", 
                   background=colores['heading_bg'], 
                   foreground=colores['fg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'])
    style.map("Treeview.Heading", 
             background=[("active", colores['btn_active'])])
    
    # Notebook (Pestañas)
    style.configure("TNotebook", 
                   background=colores['bg'], 
                   bordercolor=colores['border'],
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'])
    style.configure("TNotebook.Tab", 
                   background=colores['btn_bg'], 
                   foreground=colores['fg'],
                   bordercolor=colores['border'], 
                   lightcolor=colores['light_border'], 
                   darkcolor=colores['border'],
                   padding=[10, 5])
    style.map("TNotebook.Tab", 
             background=[("selected", colores['bg']), 
                        ("active", colores['btn_active'])])
    
    # Scrollbar
    style.configure("TScrollbar",
                   background=colores['btn_bg'],
                   troughcolor=colores['tree_bg'],
                   bordercolor=colores['border'],
                   lightcolor=colores['light_border'],
                   darkcolor=colores['border'])
    
    return colores, style
