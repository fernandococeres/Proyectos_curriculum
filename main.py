import tkinter as tk
from datetime import datetime

from centrar_ventana import centrar
from controlers.carreras_controler import carreras_controler
from controlers.cursos_controler import cursos_controler
from controlers.alumnos_controler import alumnos_controler

class mainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Administración Instituto")

        self.menubar = tk.Menu(master=root)
        # Asigna menubar a root.
        self.root.config(menu=self.menubar)
        # Establece el tamaño de la ventana
        self.root.geometry(centrar(ancho=1080, alto=600, app=self.root))
        # Fija el redimensionamiento de la ventana
        self.root.resizable(False, False)

        # Crea systemmenu.
        self.systemmenu =  tk.Menu(master=self.menubar, tearoff=False)
        # Añade las opciones a systemmenu.
        self.systemmenu.add_command(label='Editar Perfil')
        self.systemmenu.add_command(label='Preferencias')
        self.systemmenu.add_command(label='Configuración')
        # Pone una línea separadora horizontal.
        self.systemmenu.add_separator()
        self.systemmenu.add_cascade(label='Salir', command=self.root.quit)
        self.systemmenu.configure(bg="light Blue", fg="blue")
        self.menubar.add_cascade(label="Sistema", menu=self.systemmenu)

        # Crea filemenu.
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        # Añade las etiquetas de los ítems.
        self.filemenu.add_command(label="Carreras", command=lambda: self.toggle_menu('Carreras'))
        self.filemenu.add_command(label="Cursos", command=lambda: self.toggle_menu('Cursos'))
        self.filemenu.add_command(label="Alumnos", command=lambda: self.toggle_menu('Alumnos'))
        self.filemenu.configure(bg="orange", fg="green")
        self.menubar.add_cascade(label="Archivos", menu=self.filemenu)

        # Crea reportmenu.
        self.reportmenu = tk.Menu(master=self.menubar, tearoff=False)
        # Añade los ítems reportmenu.
        self.reportmenu.add_command(label="Carreras")
        self.reportmenu.add_command(label="Cursos")
        self.reportmenu.add_command(label="Alumnos")
        self.reportmenu.configure(bg="purple", fg="turquoise")
        self.menubar.add_cascade(label="Informes", menu=self.reportmenu)

        # Crea helpmenu.
        self.helpmenu = tk.Menu(master=self.menubar, tearoff=False)
        # Añade los ítems a helpmenu.
        self.helpmenu.add_command(label="Ayuda")
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Acerca de...")
        self.helpmenu.configure(bg="violet", fg="blue")
        self.menubar.add_cascade(label="Ayuda", menu=self.helpmenu)

        # Crear marco para la interfaz del usuario.
        self.containerframe = tk.Frame(root, bd=1, relief=tk.SUNKEN)
        self.containerframe.pack()

        # Crear un marco para la barra de estado
        self.statusframe = tk.Frame(root, bd=1, relief=tk.SUNKEN)
        self.statusframe.pack(side=tk.BOTTOM, fill=tk.X)

        self.statuslabel = tk.Label(self.statusframe, text='Seleccione una opción', anchor=tk.W)
        self.statuslabel.pack(side=tk.LEFT)

        # Crear la etiqueta para el estado en el lado izquierdo
        self.statusclock = tk.Label(self.statusframe, anchor=tk.E)
        self.statusclock.pack(side=tk.RIGHT)

        # Iniciar el reloj
        self.update_clock()

    # Función para actualizar el reloj
    def update_clock(self):
        current_time = datetime.now().strftime('Fecha: %d-%m-%Y Hora: %H:%M:%S')
        self.statusclock.config(text=current_time)

        # Actualizar cada 1000 ms (1 segundo)
        self.statusclock.after(1000, self.update_clock)

    def toggle_menu(self, opcion: str) -> None:
        # Alternar menú
        # Deshabilita las opciones del menú para obligar a cerrar la tabla abierta.
        # self.toggle_menu_bar_state(self.menubar)

        if opcion == 'Carreras':
            self.statuslabel.config(text='Gestión de Carreras')
            carreras_controler(self.containerframe)

        elif opcion == 'Cursos':
            self.statuslabel.config(text='Gestión de Cursos')
            cursos_controler(self.containerframe)

        elif opcion == 'Alumnos':
            self.statuslabel.config(text='Gestión de Alumnos')
            alumnos_controler(self.containerframe)

        # Habilita las opciones del menú para obligar a cerrar la tabla abierta.
        # self.toggle_menu_bar_state(self.menubar)

    def toggle_menu_bar_state(self, menubar):
        """Función para habilitar o deshabilitar los menús de la barra de menús (sin afectar submenús)."""
        # Obtener el número de menús en la barra de menú
        menu_items_count = menubar.index("end")
        # Recorrer cada menú principal en la barra
        for i in range(menu_items_count + 1):
            try:
                # Obtener el estado actual del menú
                current_state = menubar.entrycget(i, "state")
                # Alternar el estado entre "normal" (habilitado) y "disabled" (deshabilitado)
                new_state = "disabled" if current_state == "normal" else "normal"
                # Cambiar el estado del menú principal
                menubar.entryconfig(i, state=new_state)
            except tk.TclError:
                # Ignorar si no se puede obtener el estado de un menú
                pass

def main() -> None:
    '''main Función principal.
    '''
    # Crea un un objeto ventana principal con nombre root.
    root = tk.Tk()
    # Crea la instancia de la clase mainView pero no se asigna a una
    # variable por lo que no se podrá hacer referencia más adelante.
    mainView(root)
    #Cambiar el color de la ventana a rosa.
    root.config(bg="pink")

    root.mainloop()

if __name__ == "__main__":
    # Llamada a la función main.
    main()
