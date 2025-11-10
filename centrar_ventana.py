# centrar_ventana.py
# función centrar.
def centrar(ancho: int, alto: int, app) -> str:
    '''centrar Centra una ventana en la pantalla.

    Args:
        ancho (int): Ancho de la ventana.
        alto (int): Alto de la ventana.
        app (_type_): Instancia de la aplicación.

    Returns:
        str: Devuelve la posición de la ventana.
    '''
    # Obtenemos el ancho y alto de la pantalla.
    x = app.winfo_screenwidth() // 2 - ancho // 2
    # El alto de la pantalla se divide entre 2 y
    # se le resta el alto de la ventana entre 2.
    y = app.winfo_screenheight() // 2 - alto // 2
    # El formato de geometry es: ancho x alto + x + y
    posi = str(ancho) + 'x' + str(alto) + '+' + str(x) + '+' + str(y)

    return posi
