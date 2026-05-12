"""
Punto de entrada de la aplicación Agenda de Contactos.
Ejecute este archivo para iniciar la aplicación con interfaz gráfica.
"""

from view import Vista
from controller import ControladorAgenda
from model import BaseDatos


def main():
    """Función principal de la aplicación."""
    base_datos = BaseDatos('contactos.db')
    controlador = ControladorAgenda(base_datos)
    vista = Vista(controlador)
    vista.iniciar()


if __name__ == "__main__":
    main()
