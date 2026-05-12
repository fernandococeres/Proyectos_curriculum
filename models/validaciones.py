"""
Módulo de validaciones para el Sistema de Gestión Escolar

DESCRIPCIÓN:
Centraliza todos los validadores de datos del sistema.
Cada validador retorna una tupla (bool, str) donde:
- bool: True si es válido, False si no
- str: Mensaje de error si no es válido, vacío si es válido

RESPONSABILIDADES:
- Validar datos antes de guardar en BD
- Proporcionar mensajes de error claros
- Garantizar integridad de datos
- Aceptar caracteres acentuados y especiales (español)

VALIDADORES DISPONIBLES:
- validar_nombre(): Nombres de personas (letras, espacios, acentos)
- validar_apellido(): Apellidos (mismo criterio que nombres)
- validar_email(): Correos electrónicos (formato RFC5322 simplificado)
- validar_telefono(): Números telefónicos (10+ dígitos)
- validar_dni(): Documento de identidad (números)
- validar_fecha(): Fechas en formato YYYY-MM-DD
- validar_grado(): Grado escolar (1ro-6to)
- validar_seccion(): Asignatura (lista predefinida)
- validar_especialidad(): Especialidad de profesor

FORMATO DE RETORNO:
Todos los validadores retornan: (bool_valido, str_mensaje_error)

Ejemplo:
    valido, msg = Validador.validar_email("test@example.com")
    if not valido:
        messagebox.showerror("Error", msg)

LISTA BLANCA (Enumeraciones):
- GRADOS = ["1ro", "2do", "3ro", "4to", "5to", "6to"]
- ASIGNATURAS = ["Matemáticas", "Lengua", "Ciencias", "Historia", 
                 "Educación Física", "Inglés"]

USO EN EL SISTEMA:
1. Views reciben entrada del usuario
2. Views llaman a Validador antes de crear objeto Model
3. Si validación falla, Views muestra error
4. Si validación pasa, Views crea objeto y lo pasa al Controlador
5. Controlador valida nuevamente (defensa en profundidad)
6. Si todo es OK, se guarda en BD
"""
import re
from config import GRADOS, ASIGNATURAS


class Validador:
    """Clase para validar datos del sistema.
    
    Todos los métodos son estáticos y retornan tupla (bool, str).
    Primero validaciones de tipo/formato, luego de contenido.
    Mensajes de error en español para usuarios finales.
    """
    
    @staticmethod
    def validar_nombre(nombre: str) -> tuple[bool, str]:
        """Valida un nombre (solo letras y espacios, min 2 caracteres)."""
        nombre = nombre.strip()
        
        if not nombre:
            return False, "Nombre es OBLIGATORIO"
        
        if len(nombre) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"
        
        if len(nombre) > 50:
            return False, "El nombre no puede exceder 50 caracteres"
        
        # Permitir letras, espacios y acentos
        if not re.match(r"^[a-záéíóúñÁÉÍÓÚÑ\s]+$", nombre):
            return False, "El nombre solo puede contener letras y espacios"
        
        return True, ""
    
    @staticmethod
    def validar_apellido(apellido: str) -> tuple[bool, str]:
        """Valida un apellido (solo letras y espacios, min 2 caracteres)."""
        apellido = apellido.strip()
        
        if not apellido:
            return False, "Apellido es OBLIGATORIO"
        
        if len(apellido) < 2:
            return False, "El apellido debe tener al menos 2 caracteres"
        
        if len(apellido) > 50:
            return False, "El apellido no puede exceder 50 caracteres"
        
        # Permitir letras, espacios y acentos
        if not re.match(r"^[a-záéíóúñÁÉÍÓÚÑ\s]+$", apellido):
            return False, "El apellido solo puede contener letras y espacios"
        
        return True, ""
    
    @staticmethod
    def validar_email(email: str) -> tuple[bool, str]:
        """Valida un email (formato válido o vacío)."""
        email = email.strip()
        
        # Email opcional
        if not email:
            return True, ""
        
        if len(email) > 100:
            return False, "El email no puede exceder 100 caracteres"
        
        # Patrón simple de email
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron, email):
            return False, "El email no tiene un formato válido (ejemplo: usuario@dominio.com)"
        
        return True, ""
    
    @staticmethod
    def validar_telefono(telefono: str) -> tuple[bool, str]:
        """Valida un teléfono (solo números, 7-15 dígitos o vacío)."""
        telefono = telefono.strip()
        
        # Teléfono opcional
        if not telefono:
            return True, ""
        
        # Solo números
        if not telefono.isdigit():
            return False, "El teléfono solo puede contener números"
        
        if len(telefono) < 7:
            return False, "El teléfono debe tener al menos 7 dígitos"
        
        if len(telefono) > 15:
            return False, "El teléfono no puede exceder 15 dígitos"
        
        return True, ""
    
    @staticmethod
    def validar_dni(dni: str) -> tuple[bool, str]:
        """Valida un DNI (solo números, 8 dígitos o vacío)."""
        dni = dni.strip()
        
        # DNI opcional
        if not dni:
            return True, ""
        
        # Solo números
        if not dni.isdigit():
            return False, "El DNI solo puede contener números"
        
        if len(dni) != 8:
            return False, "El DNI debe tener exactamente 8 dígitos"
        
        return True, ""
    
    @staticmethod
    def validar_fecha(fecha: str) -> tuple[bool, str]:
        """Valida una fecha (formato DD/MM/YYYY o vacío)."""
        fecha = fecha.strip()
        
        # Fecha opcional
        if not fecha:
            return True, ""
        
        try:
            # Patrón DD/MM/YYYY
            partes = fecha.split('/')
            if len(partes) != 3:
                return False, "Usa el formato DD/MM/YYYY"
            
            dia = int(partes[0])
            mes = int(partes[1])
            año = int(partes[2])
            
            if not (1 <= dia <= 31):
                return False, "El día debe estar entre 1 y 31"
            
            if not (1 <= mes <= 12):
                return False, "El mes debe estar entre 1 y 12"
            
            if año < 1900 or año > 2026:
                return False, "El año debe estar entre 1900 y 2026"
            
            return True, ""
        except ValueError:
            return False, "La fecha debe contener solo números en formato DD/MM/YYYY"
    
    @staticmethod
    def validar_grado(grado: str) -> tuple[bool, str]:
        """Valida un grado (1ro a 6to o vacío)."""
        grado = grado.strip()
        
        # Grado opcional
        if not grado:
            return True, ""
        
        grados_validos = ["1ro", "2do", "3ro", "4to", "5to", "6to"]
        if grado not in grados_validos:
            return False, f"El grado debe ser uno de: {', '.join(grados_validos)}"
        
        return True, ""
    
    @staticmethod
    def validar_seccion(seccion: str) -> tuple[bool, str]:
        """Valida una asignatura (Matemáticas, Lengua, etc o vacío)."""
        seccion = seccion.strip()
        
        # Asignatura opcional
        if not seccion:
            return True, ""
        
        asignaturas_validas = ["Matemáticas", "Lengua", "Ciencias", "Historia", "Educación Física", "Inglés"]
        if seccion not in asignaturas_validas:
            return False, f"La asignatura debe ser una de: {', '.join(asignaturas_validas)}"
        
        return True, ""
    
    @staticmethod
    def validar_especialidad(especialidad: str) -> tuple[bool, str]:
        """Valida una especialidad (texto válido o vacío)."""
        especialidad = especialidad.strip()
        
        # Especialidad opcional
        if not especialidad:
            return True, ""
        
        if len(especialidad) < 3:
            return False, "La especialidad debe tener al menos 3 caracteres"
        
        if len(especialidad) > 50:
            return False, "La especialidad no puede exceder 50 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_alumno_completo(nombre: str, apellido: str, email: str, 
                               telefono: str, fecha_nacimiento: str, 
                               grado: str, seccion: str, dni: str) -> list:
        """Valida todos los campos de un alumno. Retorna lista de errores."""
        errores = []
        
        # Validaciones obligatorias
        valido, msg = Validador.validar_nombre(nombre)
        if not valido:
            errores.append(f"Nombre: {msg}")
        
        valido, msg = Validador.validar_apellido(apellido)
        if not valido:
            errores.append(f"Apellido: {msg}")
        
        # Validaciones opcionales
        valido, msg = Validador.validar_email(email)
        if not valido:
            errores.append(f"Email: {msg}")
        
        valido, msg = Validador.validar_telefono(telefono)
        if not valido:
            errores.append(f"Teléfono: {msg}")
        
        valido, msg = Validador.validar_fecha(fecha_nacimiento)
        if not valido:
            errores.append(f"Fecha de Nacimiento: {msg}")
        
        valido, msg = Validador.validar_grado(grado)
        if not valido:
            errores.append(f"Grado: {msg}")
        
        valido, msg = Validador.validar_seccion(seccion)
        if not valido:
            errores.append(f"Sección: {msg}")
        
        valido, msg = Validador.validar_dni(dni)
        if not valido:
            errores.append(f"DNI: {msg}")
        
        return errores
    
    @staticmethod
    def validar_profesor_completo(nombre: str, apellido: str, email: str, 
                                 telefono: str, especialidad: str, 
                                 documento: str) -> list:
        """Valida todos los campos de un profesor. Retorna lista de errores."""
        errores = []
        
        # Validaciones obligatorias
        valido, msg = Validador.validar_nombre(nombre)
        if not valido:
            errores.append(f"Nombre: {msg}")
        
        valido, msg = Validador.validar_apellido(apellido)
        if not valido:
            errores.append(f"Apellido: {msg}")
        
        # Validaciones opcionales
        valido, msg = Validador.validar_email(email)
        if not valido:
            errores.append(f"Email: {msg}")
        
        valido, msg = Validador.validar_telefono(telefono)
        if not valido:
            errores.append(f"Teléfono: {msg}")
        
        valido, msg = Validador.validar_especialidad(especialidad)
        if not valido:
            errores.append(f"Especialidad: {msg}")
        
        valido, msg = Validador.validar_dni(documento)
        if not valido:
            errores.append(f"Documento: {msg}")
        
        return errores
