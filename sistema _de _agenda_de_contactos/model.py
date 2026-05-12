"""
Módulo de modelo para la agenda de contactos.
Define las clases principales y manejo de base de datos SQLite.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
import sqlite3
from pathlib import Path


@dataclass
class Contacto:
    """Clase que representa un contacto en la agenda."""
    
    id: str
    nombre: str
    apellido: str
    telefono: str
    email: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    fecha_registro: str = None
    
    def __post_init__(self):
        """Inicializa la fecha de registro si no se proporciona."""
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def calcular_edad(self) -> Optional[int]:
        """
        Calcula la edad a partir de la fecha de nacimiento.
        
        Returns:
            Edad en años o None si no hay fecha de nacimiento
        """
        if not self.fecha_nacimiento:
            return None
        try:
            # Formato esperado: DD/MM/YYYY
            dia, mes, año = map(int, self.fecha_nacimiento.split('/'))
            fecha_nac = datetime(año, mes, dia)
            hoy = datetime.now()
            edad = hoy.year - fecha_nac.year
            if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
                edad -= 1
            return edad
        except (ValueError, AttributeError):
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el contacto a un diccionario.
        
        Returns:
            Diccionario con los datos del contacto
        """
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email or '',
            'direccion': self.direccion or '',
            'fecha_nacimiento': self.fecha_nacimiento or '',
            'fecha_registro': self.fecha_registro
        }
    
    @staticmethod
    def from_dict(id: str, data: Dict[str, Any]) -> 'Contacto':
        """
        Crea un contacto a partir de un diccionario.
        
        Args:
            id: Identificador del contacto
            data: Diccionario con los datos
            
        Returns:
            Instancia de Contacto
        """
        return Contacto(
            id=id,
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            telefono=data.get('telefono', ''),
            email=data.get('email', None),
            direccion=data.get('direccion', None),
            fecha_nacimiento=data.get('fecha_nacimiento', None),
            fecha_registro=data.get('fecha_registro')
        )
    
    def __str__(self) -> str:
        """Representación en texto del contacto."""
        edad = self.calcular_edad()
        edad_str = f" ({edad} años)" if edad else ""
        return f"{self.nombre} {self.apellido}{edad_str} ({self.telefono})"


class BaseDatos:
    """Clase para manejar el almacenamiento de contactos en SQLite."""
    
    def __init__(self, archivo: str = 'contactos.db'):
        """
        Inicializa la base de datos SQLite.
        
        Args:
            archivo: Nombre de la base de datos SQLite
        """
        self.archivo = archivo
        self.ultimo_error = ""
        self._inicializar_bd()
    
    def _inicializar_bd(self) -> None:
        """Crea la tabla de contactos si no existe."""
        try:
            with sqlite3.connect(self.archivo) as conexion:
                cursor = conexion.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contactos (
                        id TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        telefono TEXT NOT NULL,
                        email TEXT,
                        direccion TEXT,
                        fecha_nacimiento TEXT,
                        fecha_registro TEXT NOT NULL
                    )
                ''')
                conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            raise
    
    def cargar(self) -> Dict:
        """
        Carga los contactos desde la base de datos.
        
        Returns:
            Diccionario con los contactos
        """
        try:
            contactos = {}
            with sqlite3.connect(self.archivo) as conexion:
                conexion.row_factory = sqlite3.Row
                cursor = conexion.cursor()
                cursor.execute('SELECT * FROM contactos')
                
                for fila in cursor.fetchall():
                    id_contacto = fila['id']
                    contactos[id_contacto] = {
                        'nombre': fila['nombre'],
                        'apellido': fila['apellido'],
                        'telefono': fila['telefono'],
                        'email': fila['email'] or '',
                        'direccion': fila['direccion'] or '',
                        'fecha_nacimiento': fila['fecha_nacimiento'] or '',
                        'fecha_registro': fila['fecha_registro']
                    }
            return contactos
        except sqlite3.Error as e:
            print(f"Error al leer la base de datos: {e}")
            return {}
    
    def guardar(self, contactos: Dict) -> bool:
        """
        Guarda los contactos en la base de datos.
        
        Args:
            contactos: Diccionario con los contactos
            
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            with sqlite3.connect(self.archivo) as conexion:
                cursor = conexion.cursor()
                
                # Limpiar tabla existente
                cursor.execute('DELETE FROM contactos')
                
                # Insertar contactos
                for id_contacto, datos in contactos.items():
                    cursor.execute('''
                        INSERT INTO contactos 
                        (id, nombre, apellido, telefono, email, direccion, fecha_nacimiento, fecha_registro)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        id_contacto,
                        datos.get('nombre', ''),
                        datos.get('apellido', ''),
                        datos.get('telefono', ''),
                        datos.get('email', '') or None,
                        datos.get('direccion', '') or None,
                        datos.get('fecha_nacimiento', '') or None,
                        datos.get('fecha_registro', '')
                    ))
                
                conexion.commit()
            return True
        except sqlite3.Error as e:
            self.ultimo_error = str(e)
            print(f"Error al guardar en la base de datos: {e}")
            return False
    
    def existe_archivo(self) -> bool:
        """
        Verifica si la base de datos existe.
        
        Returns:
            True si existe, False en caso contrario
        """
        return Path(self.archivo).exists()
    
    def eliminar_archivo(self) -> bool:
        """
        Elimina la base de datos.
        
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            if self.existe_archivo():
                Path(self.archivo).unlink()
            return True
        except Exception as e:
            print(f"Error al eliminar la base de datos: {e}")
            return False
    
    def obtener_contacto(self, id_contacto: str) -> Optional[Dict]:
        """
        Obtiene un contacto específico.
        
        Args:
            id_contacto: ID del contacto
        
        Returns:
            Diccionario con el contacto o None
        """
        try:
            with sqlite3.connect(self.archivo) as conexion:
                conexion.row_factory = sqlite3.Row
                cursor = conexion.cursor()
                cursor.execute('SELECT * FROM contactos WHERE id = ?', (id_contacto,))
                fila = cursor.fetchone()
                
                if fila:
                    return {
                        'nombre': fila['nombre'],
                        'apellido': fila['apellido'],
                        'telefono': fila['telefono'],
                        'email': fila['email'] or '',
                        'direccion': fila['direccion'] or '',
                        'fecha_nacimiento': fila['fecha_nacimiento'] or '',
                        'fecha_registro': fila['fecha_registro']
                    }
            return None
        except sqlite3.Error as e:
            print(f"Error al obtener contacto: {e}")
            return None
    
    def contar_contactos(self) -> int:
        """
        Cuenta el número de contactos.
        
        Returns:
            Número de contactos en la base de datos
        """
        try:
            with sqlite3.connect(self.archivo) as conexion:
                cursor = conexion.cursor()
                cursor.execute('SELECT COUNT(*) FROM contactos')
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error al contar contactos: {e}")
            return 0
