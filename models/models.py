"""
Modelos de datos para el Sistema de Gestión Escolar

DESCRIPCIÓN:
Define las clases que representan las entidades principales del sistema:
Alumno y Profesor. Estas clases actúan como contenedores de datos con métodos
para conversión y representación.

RELACIÓN CON BASE DE DATOS:
- Alumno → tabla 'alumnos'
- Profesor → tabla 'profesores'

VALIDACIÓN:
Los datos en estas clases NO se validan aquí. La validación ocurre en:
- models/validaciones.py: Validadores específicos
- controllers/controlers.py: Antes de guardar en BD

USO TÍPICO:
1. View recolecta datos del usuario
2. View crea objeto Alumno/Profesor con esos datos
3. View valida usando models.validaciones
4. View pasa objeto a controlador
5. Controlador convierte a tupla y guarda en BD

CAMPOS ALUMNOS:
- id_alumno: ID único (autonumérico)
- nombre: Primer nombre
- apellido: Apellido(s)
- email: Correo electrónico
- telefono: Número de teléfono
- fecha_nacimiento: Fecha en formato YYYY-MM-DD
    
    Atributos:
        id_profesor (int): ID único en la base de datos
        nombre (str): Nombre del profesor
        apellido (str): Apellido del profesor
        email (str): Correo electrónico
        telefono (str): Número de contacto
        especialidad (str): Área de especialización o asignatura
        documento (str): Documento de identidad (único)
    
- grado: Año escolar (1ro, 2do, 3ro, 4to, 5to, 6to)
- seccion: Asignatura (Matemáticas, Lengua, Ciencias, Historia, Educación Física, Inglés)
- dni: Documento único de identidad

CAMPOS PROFESORES:
- id_profesor: ID único (autonumérico)
- nombre: Primer nombre
- apellido: Apellido(s)
- email: Correo electrónico
- telefono: Número de teléfono
- especialidad: Área de especialización
- documento: Documento único de identidad
"""
from datetime import datetime

class Alumno:
    """Clase que representa a un alumno del sistema.
    
    Atributos:
        id_alumno (int): ID único en la base de datos
        nombre (str): Nombre del alumno
        apellido (str): Apellido del alumno
        email (str): Correo electrónico
        telefono (str): Número de contacto
        fecha_nacimiento (str): Fecha en formato YYYY-MM-DD
        grado (str): Año escolar (1ro-6to)
        seccion (str): Asignatura asignada
        dni (str): Documento de identidad (único)
    """
    
    def __init__(self, id_alumno=None, nombre="", apellido="", email="", 
                 telefono="", fecha_nacimiento="", grado="", seccion="", dni=""):
        self.id_alumno = id_alumno
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.grado = grado
        self.seccion = seccion
        self.dni = dni
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.grado}° {self.seccion}"
    
    def to_tuple(self):
        """Convierte el objeto a tupla para insertar en BD."""
        return (self.nombre, self.apellido, self.email, self.telefono, 
                self.fecha_nacimiento, self.grado, self.seccion, self.dni)


class Profesor:
    """Clase que representa a un profesor del sistema."""
    
    def __init__(self, id_profesor=None, nombre="", apellido="", email="", 
                 telefono="", especialidad="", documento=""):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.especialidad = especialidad
        self.documento = documento
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad}"
    
    def to_tuple(self):
        """Convierte el objeto a tupla para insertar en BD."""
        return (self.nombre, self.apellido, self.email, self.telefono, 
                self.especialidad, self.documento)
