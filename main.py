import tkinter as tk
from tkinter import Menu, messagebox
from centrar_ventana import centrar_ventana

# --- funciones que abren tus módulos ---
def abrir_alumnos():
    messagebox.showinfo("Módulo Alumnos", "Abrir formulario de alumnos")

def abrir_profesores():
    messagebox.showinfo("Módulo Profesores", "Abrir formulario de profesores")

def salir():
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        root.destroy()

# --- ventana principal ---
root = tk.Tk()
root.title("Sistema de Gestión - IE4")
centrar_ventana(root, 800, 600)

# --- menú principal ---
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Menú de Tablas
menu_tablas = Menu(menu_bar, tearoff=0)
menu_tablas.add_command(label="Alumnos", command=abrir_alumnos)
menu_tablas.add_command(label="Profesores", command=abrir_profesores)
menu_tablas.add_separator()
menu_tablas.add_command(label="Salir", command=salir)
menu_bar.add_cascade(label="Tablas", menu=menu_tablas)

# --- contenido de la ventana principal ---
label_bienvenida = tk.Label(root, text="Bienvenido al Sistema de Gestión", font=("Arial", 16))
label_bienvenida.pack(pady=50)

root.mainloop()