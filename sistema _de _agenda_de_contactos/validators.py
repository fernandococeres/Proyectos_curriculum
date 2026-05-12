"""
Módulo de validadores para la agenda de contactos.
Contiene funciones para validar datos de entrada.
"""

from typing import Tuple


def es_nombre_valido(nombre: str) -> Tuple[bool, str]:
    """
    Valida que el nombre contenga solo letras y espacios.
    
    Args:
        nombre: Cadena a validar
        
    Returns:
        Tupla (válido, mensaje_error)
    """
    if not nombre or len(nombre.strip()) == 0:
        return False, "El nombre no puede estar vacío."
    
    if not all(c.isalpha() or c.isspace() for c in nombre):
        return False, "El nombre solo puede contener letras y espacios."
    
    return True, ""


def es_apellido_valido(apellido: str) -> Tuple[bool, str]:
    """
    Valida que el apellido contenga solo letras y espacios.
    
    Args:
        apellido: Cadena a validar
        
    Returns:
        Tupla (válido, mensaje_error)
    """
    if not apellido or len(apellido.strip()) == 0:
        return False, "El apellido no puede estar vacío."
    
    if not all(c.isalpha() or c.isspace() for c in apellido):
        return False, "El apellido solo puede contener letras y espacios."
    
    return True, ""


def es_telefono_valido(telefono: str) -> Tuple[bool, str]:
    """
    Valida que el teléfono contenga solo números.
    
    Args:
        telefono: Cadena a validar
        
    Returns:
        Tupla (válido, mensaje_error)
    """
    if not telefono or len(telefono.strip()) == 0:
        return False, "El teléfono no puede estar vacío."
    
    telefono = telefono.strip()
    
    if not telefono.isdigit():
        return False, "El teléfono solo puede contener números."
    
    return True, ""


def es_email_valido(email: str) -> Tuple[bool, str]:
    """
    Valida que el email tenga un formato válido (opcional).
    
    Args:
        email: Cadena a validar
        
    Returns:
        Tupla (válido, mensaje_error)
    """
    if not email or len(email.strip()) == 0:
        # El email es opcional
        return True, ""
    
    email = email.strip()
    
    if '@' not in email or '.' not in email.split('@')[-1]:
        return False, "El formato del email no es válido."
    
    return True, ""


def es_direccion_valida(direccion: str) -> Tuple[bool, str]:
    """
    Valida que la dirección sea válida (opcional).
    
    Args:
        direccion: Cadena a validar
        
    Returns:
        Tupla (válido, mensaje_error)
    """
    if not direccion or len(direccion.strip()) == 0:
        # La dirección es opcional
        return True, ""
    
    # Solo validar que no esté vacía si se proporciona
    return True, ""
