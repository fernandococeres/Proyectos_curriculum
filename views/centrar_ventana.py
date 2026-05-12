"""
Utilidad para centrar ventanas en la pantalla.

DESCRIPCIÓN:
Función auxiliar que posiciona una ventana Tkinter en el centro de la pantalla.

FUNCIÓN:
centrar_ventana(ventana, ancho, alto)
    Centra una ventana en la pantalla con las dimensiones especificadas.
    
    Args:
        ventana (tk.Tk/tk.Toplevel): Ventana a centrar
        ancho (int): Ancho deseado en píxeles
        alto (int): Alto deseado en píxeles

CÁLCULO:
1. Obtiene resolución de pantalla
2. Calcula posición X como: (ancho_pantalla / 2) - (ancho_ventana / 2)
3. Calcula posición Y como: (alto_pantalla / 2) - (alto_ventana / 2)
4. Aplica geometría a la ventana

USO:
    root = tk.Tk()
    centrar_ventana(root, 800, 600)  # Centra ventana de 800x600
    root.mainloop()

NOTA:
update_idletasks() es necesario para obtener dimensiones correctas de pantalla.
"""

def centrar_ventana(ventana, ancho, alto):
    """Centra una ventana en la pantalla.
    
    Calcula la posición central basada en las dimensiones de la pantalla
    y aplica la geometría correspondiente a la ventana.
    
    Args:
        ventana (tk.Tk or tk.Toplevel): Ventana a centrar
        ancho (int): Ancho deseado en píxeles
        alto (int): Alto deseado en píxeles
    
    Returns:
        None
    """
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
