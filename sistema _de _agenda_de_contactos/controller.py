"""
Controlador de la aplicación Agenda de Contactos.
Maneja la lógica de negocio y la comunicación entre la vista y el modelo.
"""

import uuid
from typing import Dict, Tuple, Optional
from model import Contacto, BaseDatos
import validators


class ControladorAgenda:
    """Controlador que gestiona la lógica de negocio de la agenda."""
    
    def __init__(self, base_datos: BaseDatos = None):
        """
        Inicializa el controlador.
        
        Args:
            base_datos: Instancia de BaseDatos
        """
        self.base_datos = base_datos or BaseDatos()
        self.contactos = self.base_datos.cargar()
    
    def generar_id(self) -> str:
        """
        Genera un ID único para un contacto.
        
        Returns:
            ID único de 8 caracteres
        """
        return str(uuid.uuid4())[:8].upper()
    
    def validar_nombre(self, nombre: str) -> Tuple[bool, str]:
        """
        Valida el nombre.
        
        Returns:
            Tupla (válido, mensaje_error)
        """
        return validators.es_nombre_valido(nombre)
    
    def validar_apellido(self, apellido: str) -> Tuple[bool, str]:
        """
        Valida el apellido.
        
        Returns:
            Tupla (válido, mensaje_error)
        """
        return validators.es_apellido_valido(apellido)
    
    def validar_telefono(self, telefono: str) -> Tuple[bool, str]:
        """
        Valida el teléfono.
        
        Returns:
            Tupla (válido, mensaje_error)
        """
        return validators.es_telefono_valido(telefono)
    
    def validar_email(self, email: Optional[str]) -> Tuple[bool, str]:
        """
        Valida el email (opcional).
        
        Returns:
            Tupla (válido, mensaje_error)
        """
        return validators.es_email_valido(email)
    
    def crear_contacto(self, nombre: str, apellido: str, telefono: str, 
                      email: Optional[str] = None, direccion: Optional[str] = None,
                      fecha_nacimiento: Optional[str] = None, 
                      fecha_registro: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        
        # Validaciones
        valido, msg = self.validar_nombre(nombre)
        if not valido:
            return False, msg, None
            
        valido, msg = self.validar_apellido(apellido)
        if not valido:
            return False, msg, None
            
        valido, msg = self.validar_telefono(telefono)
        if not valido:
            return False, msg, None
            
        valido, msg = self.validar_email(email)
        if not valido:
            return False, msg, None
            
        if fecha_nacimiento:
            valido, msg = self.validar_fecha_nacimiento(fecha_nacimiento)
            if not valido:
                return False, msg, None

        # 1. Generar el ID una sola vez
        id_contacto = self.generar_id()
        
        # 2. Crear el objeto contacto
        contacto = Contacto(
            id=id_contacto,
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            telefono=telefono.strip(),
            email=email.strip() if email else None,
            direccion=direccion.strip() if direccion else None,
            fecha_nacimiento=fecha_nacimiento.strip() if fecha_nacimiento else None,
            fecha_registro=fecha_registro.strip() if fecha_registro else None
        )
        
        # 3. Guardar en el diccionario y en la Base de Datos
        self.contactos[id_contacto] = contacto.to_dict()
        
        if not self.base_datos.guardar(self.contactos):
            # Si la BD falla, borramos el contacto de la memoria para ser consistentes
            del self.contactos[id_contacto]
            error_bd = getattr(self.base_datos, 'ultimo_error', 'Desconocido')
            return False, f"Error SQLite: {error_bd}\n\n💡 Sugerencia: Si cambiaste los campos de contacto hace poco, borra el archivo 'contactos.db' para que se vuelva a generar.", None
        
        # 4. CRITICAL: Recargar la memoria del controlador desde la BD 
        # para asegurar sincronización
        self.contactos = self.base_datos.cargar() 
    
        # 5. Devolver el ID REAL que se acaba de crear
        return True, f"Contacto '{nombre} {apellido}' creado exitosamente.", id_contacto    
        
    
    def actualizar_contacto(self, id_contacto: str, nombre: str, apellido: str, 
                           telefono: str, email: Optional[str] = None, 
                           direccion: Optional[str] = None,
                           fecha_nacimiento: Optional[str] = None,
                           fecha_registro: Optional[str] = None) -> Tuple[bool, str]:
        """
        Actualiza un contacto existente.
        
        Args:
            id_contacto: ID del contacto
            nombre: Nuevo nombre
            apellido: Nuevo apellido
            telefono: Nuevo teléfono
            email: Nuevo email (opcional)
            direccion: Nueva dirección (opcional)
            fecha_nacimiento: Nueva fecha de nacimiento en formato DD/MM/YYYY (opcional)
            fecha_registro: Nueva fecha de registro en formato DD/MM/YYYY (opcional)
        
        Returns:
            Tupla (éxito, mensaje)
        """
        if id_contacto not in self.contactos:
            return False, "El contacto no existe."
        
        # Validaciones
        valido, msg = self.validar_nombre(nombre)
        if not valido:
            return False, msg
        
        valido, msg = self.validar_apellido(apellido)
        if not valido:
            return False, msg
        
        valido, msg = self.validar_telefono(telefono)
        if not valido:
            return False, msg
        
        valido, msg = self.validar_email(email)
        if not valido:
            return False, msg
        
        # Validar fecha de nacimiento si se proporciona
        if fecha_nacimiento:
            valido, msg = self.validar_fecha_nacimiento(fecha_nacimiento)
            if not valido:
                return False, msg
        
        # Actualizar
        self.contactos[id_contacto]['nombre'] = nombre.strip()
        self.contactos[id_contacto]['apellido'] = apellido.strip()
        self.contactos[id_contacto]['telefono'] = telefono.strip()
        self.contactos[id_contacto]['email'] = email.strip() if email else ''
        self.contactos[id_contacto]['direccion'] = direccion.strip() if direccion else ''
        self.contactos[id_contacto]['fecha_nacimiento'] = fecha_nacimiento.strip() if fecha_nacimiento else ''
        if fecha_registro:
            self.contactos[id_contacto]['fecha_registro'] = fecha_registro.strip()
        
        if not self.base_datos.guardar(self.contactos):
            error_bd = getattr(self.base_datos, 'ultimo_error', 'Desconocido')
            return False, f"Error al guardar los cambios: {error_bd}"
        
        return True, f"Contacto actualizado exitosamente."
    
    def obtener_contacto(self, id_contacto: str) -> Optional[Dict]:
        """
        Obtiene un contacto por ID.
        
        Args:
            id_contacto: ID del contacto
        
        Returns:
            Diccionario del contacto o None
        """
        return self.contactos.get(id_contacto)
    
    def eliminar_contacto(self, id_contacto: str) -> Tuple[bool, str]:
        """
        Elimina un contacto.
        
        Args:
            id_contacto: ID del contacto a eliminar
        
        Returns:
            Tupla (éxito, mensaje)
        """
        if id_contacto not in self.contactos:
            return False, "El contacto no existe."
        
        del self.contactos[id_contacto]
        if not self.base_datos.guardar(self.contactos):
            error_bd = getattr(self.base_datos, 'ultimo_error', 'Desconocido')
            return False, f"Error en BD al eliminar: {error_bd}"
        
        return True, "Contacto eliminado exitosamente."
    
    def obtener_todos_contactos(self) -> Dict:
        """
        Obtiene todos los contactos.
        
        Returns:
            Diccionario con todos los contactos
        """
        self.contactos = self.base_datos.cargar()
        return self.contactos
    
    def buscar_contactos(self, termino: str) -> Dict:
        """
        Busca contactos por término en múltiples campos.
        
        Args:
            termino: Término de búsqueda
        
        Returns:
            Diccionario con contactos encontrados
        """
        termino_lower = termino.lower()
        resultados = {}
        
        for id_contacto, datos in self.contactos.items():
            nombre = datos.get('nombre', '').lower()
            apellido = datos.get('apellido', '').lower()
            telefono = datos.get('telefono', '').lower()
            email = datos.get('email', '').lower()
            direccion = datos.get('direccion', '').lower()
            
            if (termino_lower in nombre or 
                termino_lower in apellido or
                termino_lower in telefono or 
                termino_lower in email or 
                termino_lower in direccion or
                termino_lower in id_contacto.lower()):
                resultados[id_contacto] = datos
        
        return resultados
    
    def validar_fecha_nacimiento(self, fecha: str) -> Tuple[bool, str]:
        """
        Valida la fecha de nacimiento en formato DD/MM/YYYY.
        
        Returns:
            Tupla (válido, mensaje_error)
        """
        if not fecha or not fecha.strip():
            return True, ""  # Es opcional
        
        try:
            dia, mes, año = map(int, fecha.split('/'))
            if not (1 <= mes <= 12 and 1 <= dia <= 31 and año > 1900):
                return False, "La fecha de nacimiento debe ser en formato DD/MM/YYYY válido."
            return True, ""
        except (ValueError, AttributeError):
            return False, "La fecha de nacimiento debe ser en formato DD/MM/YYYY (ej: 15/03/1990)."
    
    def buscar_por_edad(self, edad: int) -> Dict:
        """
        Busca contactos por edad exacta.
        
        Args:
            edad: Edad a buscar
        
        Returns:
            Diccionario con contactos encontrados
        """
        resultados = {}
        for id_contacto, datos in self.contactos.items():
            fecha_nac = datos.get('fecha_nacimiento', '')
            if fecha_nac:
                try:
                    dia, mes, año = map(int, fecha_nac.split('/'))
                    from datetime import datetime
                    fecha_nac_obj = datetime(año, mes, dia)
                    hoy = datetime.now()
                    edad_contacto = hoy.year - fecha_nac_obj.year
                    if (hoy.month, hoy.day) < (fecha_nac_obj.month, fecha_nac_obj.day):
                        edad_contacto -= 1
                    
                    if edad_contacto == edad:
                        resultados[id_contacto] = datos
                except (ValueError, AttributeError):
                    pass
        
        return resultados
    
    def buscar_rango_edad(self, edad_min: int, edad_max: int) -> Dict:
        """
        Busca contactos en un rango de edad.
        
        Args:
            edad_min: Edad mínima
            edad_max: Edad máxima
        
        Returns:
            Diccionario con contactos encontrados
        """
        resultados = {}
        for id_contacto, datos in self.contactos.items():
            fecha_nac = datos.get('fecha_nacimiento', '')
            if fecha_nac:
                try:
                    dia, mes, año = map(int, fecha_nac.split('/'))
                    from datetime import datetime
                    fecha_nac_obj = datetime(año, mes, dia)
                    hoy = datetime.now()
                    edad_contacto = hoy.year - fecha_nac_obj.year
                    if (hoy.month, hoy.day) < (fecha_nac_obj.month, fecha_nac_obj.day):
                        edad_contacto -= 1
                    
                    if edad_min <= edad_contacto <= edad_max:
                        resultados[id_contacto] = datos
                except (ValueError, AttributeError):
                    pass
        
        return resultados
