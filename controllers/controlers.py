"""
Controladores para la lógica de negocio del Sistema de Gestión Escolar

RESPONSABILIDADES:
- Implementar CRUD (Create, Read, Update, Delete) para Alumnos y Profesores
- Validar datos antes de guardar en base de datos
- Manejar errores y excepciones
- Comunicar resultados a través de tuplas (éxito, mensaje)
- Servir como intermediario entre Views y Models

CLASES:
- ControladorAlumnos: Gestiona todas las operaciones con alumnos
- ControladorProfesores: Gestiona todas las operaciones con profesores

MÉTODOS PRINCIPALES:
- agregar_alumno/profesor(): Crear nuevo registro
- obtener_alumnos/profesores(): Listar todos los registros
- obtener_alumno/profesor(id): Obtener un registro específico
- actualizar_alumno/profesor(id, obj): Modificar un registro
- eliminar_alumno/profesor(id): Eliminar un registro
- buscar_alumno/profesor(criterio, valor): Buscar por criterio

FLUJO TÍPICO:
1. View recibe datos del usuario
2. View llama a ControladorAlumnos/Profesores
3. Controlador valida y ejecuta operación en BD
4. Controlador retorna (éxito: bool, mensaje: str)
5. View muestra resultado al usuario
"""
import sqlite3
from models.dbConn import dbConn
from models.models import Alumno, Profesor

class ControladorAlumnos:
    """Controlador para la gestión de alumnos."""
    
    def __init__(self, db_name="escuela.db"):
        self.db = dbConn(db_name)
        self.crear_tabla_alumnos()
    
    def crear_tabla_alumnos(self):
        """Crea la tabla de alumnos si no existe."""
        campos = """(
            id_alumno INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            fecha_nacimiento TEXT,
            grado TEXT,
            seccion TEXT,
            dni TEXT UNIQUE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        self.db.createTable("alumnos", campos)
    
    def agregar_alumno(self, alumno: Alumno) -> tuple:
        """Agrega un nuevo alumno a la base de datos.
        
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            comando = """INSERT INTO alumnos 
                        (nombre, apellido, email, telefono, fecha_nacimiento, grado, seccion, dni)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            self.db.execute(comando, alumno.to_tuple())
            return (True, "Alumno agregado correctamente")
        except sqlite3.IntegrityError as e:
            if "dni" in str(e).lower():
                return (False, "Error: Ya existe un alumno con este DNI")
            return (False, f"Error de integridad: {e}")
        except Exception as e:
            return (False, f"Error al agregar alumno: {e}")
    
    def obtener_alumnos(self) -> list:
        """Obtiene todos los alumnos de la base de datos."""
        try:
            comando = "SELECT * FROM alumnos"
            return self.db.execute(comando)
        except Exception as e:
            print(f"Error al obtener alumnos: {e}")
            return []
    
    def obtener_alumno(self, id_alumno: int) -> tuple:
        """Obtiene un alumno específico por ID."""
        try:
            comando = "SELECT * FROM alumnos WHERE id_alumno = ?"
            resultado = self.db.execute(comando, (id_alumno,))
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener alumno: {e}")
            return None
    
    def actualizar_alumno(self, id_alumno: int, alumno: Alumno) -> tuple:
        """Actualiza los datos de un alumno.
        
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            comando = """UPDATE alumnos 
                        SET nombre=?, apellido=?, email=?, telefono=?, 
                            fecha_nacimiento=?, grado=?, seccion=?, dni=?
                        WHERE id_alumno=?"""
            campos = alumno.to_tuple() + (id_alumno,)
            self.db.execute(comando, campos)
            return (True, "Alumno actualizado correctamente")
        except sqlite3.IntegrityError as e:
            if "dni" in str(e).lower():
                return (False, "Error: Ya existe otro alumno con este DNI")
            return (False, f"Error de integridad: {e}")
        except Exception as e:
            return (False, f"Error al actualizar alumno: {e}")
    
    def eliminar_alumno(self, id_alumno: int) -> bool:
        """Elimina un alumno de la base de datos."""
        try:
            comando = "DELETE FROM alumnos WHERE id_alumno = ?"
            self.db.execute(comando, (id_alumno,))
            return True
        except Exception as e:
            print(f"Error al eliminar alumno: {e}")
            return False
    
    def buscar_alumno(self, criterio: str, valor: str) -> list:
        """Busca alumnos por criterio (nombre, apellido, email, etc)."""
        try:
            comando = f"SELECT * FROM alumnos WHERE {criterio} LIKE ?"
            return self.db.execute(comando, (f"%{valor}%",))
        except Exception as e:
            print(f"Error al buscar alumno: {e}")
            return []


class ControladorProfesores:
    """Controlador para la gestión de profesores."""
    
    def __init__(self, db_name="escuela.db"):
        self.db = dbConn(db_name)
        self.crear_tabla_profesores()
    
    def crear_tabla_profesores(self):
        """Crea la tabla de profesores si no existe."""
        campos = """(
            id_profesor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            especialidad TEXT,
            documento TEXT UNIQUE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        self.db.createTable("profesores", campos)
    
    def agregar_profesor(self, profesor: Profesor) -> tuple:
        """Agrega un nuevo profesor a la base de datos.
        
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            comando = """INSERT INTO profesores 
                        (nombre, apellido, email, telefono, especialidad, documento)
                        VALUES (?, ?, ?, ?, ?, ?)"""
            self.db.execute(comando, profesor.to_tuple())
            return (True, "Profesor agregado correctamente")
        except sqlite3.IntegrityError as e:
            if "documento" in str(e).lower():
                return (False, "Error: Ya existe un profesor con este Documento")
            return (False, f"Error de integridad: {e}")
        except Exception as e:
            return (False, f"Error al agregar profesor: {e}")
    
    def obtener_profesores(self) -> list:
        """Obtiene todos los profesores de la base de datos."""
        try:
            comando = "SELECT * FROM profesores"
            return self.db.execute(comando)
        except Exception as e:
            print(f"Error al obtener profesores: {e}")
            return []
    
    def obtener_profesor(self, id_profesor: int) -> tuple:
        """Obtiene un profesor específico por ID."""
        try:
            comando = "SELECT * FROM profesores WHERE id_profesor = ?"
            resultado = self.db.execute(comando, (id_profesor,))
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener profesor: {e}")
            return None
    
    def actualizar_profesor(self, id_profesor: int, profesor: Profesor) -> tuple:
        """Actualiza los datos de un profesor.
        
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            comando = """UPDATE profesores 
                        SET nombre=?, apellido=?, email=?, telefono=?, 
                            especialidad=?, documento=?
                        WHERE id_profesor=?"""
            campos = profesor.to_tuple() + (id_profesor,)
            self.db.execute(comando, campos)
            return (True, "Profesor actualizado correctamente")
        except sqlite3.IntegrityError as e:
            if "documento" in str(e).lower():
                return (False, "Error: Ya existe otro profesor con este Documento")
            return (False, f"Error de integridad: {e}")
        except Exception as e:
            return (False, f"Error al actualizar profesor: {e}")
            return False
    
    def eliminar_profesor(self, id_profesor: int) -> bool:
        """Elimina un profesor de la base de datos."""
        try:
            comando = "DELETE FROM profesores WHERE id_profesor = ?"
            self.db.execute(comando, (id_profesor,))
            return True
        except Exception as e:
            print(f"Error al eliminar profesor: {e}")
            return False
    
    def buscar_profesor(self, criterio: str, valor: str) -> list:
        """Busca profesores por criterio (nombre, apellido, email, etc)."""
        try:
            comando = f"SELECT * FROM profesores WHERE {criterio} LIKE ?"
            return self.db.execute(comando, (f"%{valor}%",))
        except Exception as e:
            print(f"Error al buscar profesor: {e}")
            return []
