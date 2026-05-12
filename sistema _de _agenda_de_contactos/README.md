# Agenda de Contactos

Sistema completo y profesional para gestionar una agenda personal de contactos en Python.

## Características

✨ **Funcionalidades principales:**
- ✅ Añadir nuevos contactos
- ✅ Eliminar contactos existentes
- ✅ Modificar información de contactos
- ✅ Buscar contactos por nombre
- ✅ Listar todos los contactos
- ✅ Almacenamiento persistente en JSON
- ✅ Validación de datos de entrada
- ✅ Interfaz de usuario amigable

## Estructura del Proyecto

```
agenda_contactos/
├── __init__.py           # Inicializador del paquete
├── controller.py         # Controlador - Lógica de negocio
├── view.py               # Vista - Interfaz gráfica (Tkinter)
├── view_model.py         # Modelo de vista - Clase Contacto
├── validators.py         # Validadores de entrada
├── storage.py            # Manejo de almacenamiento JSON
└── (obsoleto)ui.py       # Antigua interfaz (eliminada)

main.py                    # Punto de entrada de la aplicación
requirements.txt           # Dependencias (ninguna requerida)
README.md                  # Este archivo
contactos.json             # Archivo de datos (se genera automáticamente)
```

## Requisitos

- Python 3.7 o superior
- No requiere dependencias externas

## Instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   cd ruta/al/proyecto
   ```

2. **Verificar que Python esté instalado:**
   ```bash
   python --version
   ```

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Opción 1: Añadir Contacto
- Ingrese un ID único para el contacto
- Nombre (solo letras y espacios)
- Teléfono (solo números)
- Email (opcional, debe ser válido)
- Dirección (opcional)

### Opción 2: Eliminar Contacto
- Ingrese el ID del contacto a eliminar
- Confirme la eliminación

### Opción 3: Modificar Contacto
- Ingrese el ID del contacto a modificar
- Actualice los campos que desee (Enter para mantener)

### Opción 4: Buscar Contacto
- Ingrese el nombre (o parte del nombre) a buscar
- Se mostrarán todos los contactos que coincidan

### Opción 5: Listar Contactos
- Muestra todos los contactos registrados con su información completa

### Opción 6: Salir
- Sale de la aplicación (los cambios se guardan automáticamente)

## Formato de Almacenamiento

Los contactos se guardan en formato JSON en el archivo `contactos.json`:

```json
{
    "1": {
        "nombre": "Juan Pérez",
        "telefono": "1234567890",
        "email": "juan@example.com",
        "direccion": "Calle Principal 123",
        "fecha_creacion": "11/05/2026 14:30:45"
    }
}
```

## Validación de Datos

- **Nombre:** Solo acepta letras (A-Z, a-z) y espacios
- **Teléfono:** Solo acepta números (0-9)
- **Email:** Debe contener @ y un dominio válido
- **ID:** Debe ser único y no puede estar vacío

## Ejemplos de Uso

### Añadir un contacto
```
ID del contacto: 1
Nombre: Juan García
Teléfono: 555123456
Email: juan@gmail.com
Dirección: Calle 5 No. 123
```

### Buscar contactos
```
Buscar por nombre: Juan
Resultados encontrados (2):
ID: 1
  Nombre: Juan García
  Teléfono: 555123456
  Email: juan@gmail.com
  Dirección: Calle 5 No. 123
```

## Mejoras Implementadas Respecto al Original

1. **Estructura modular:** Código dividido en módulos reutilizables
2. **Documentación:** Docstrings en todas las funciones y clases
3. **Type hints:** Anotaciones de tipos para mejor claridad
4. **Manejo de errores:** Mejor captura y manejo de excepciones
5. **Validación mejorada:** Incluyendo validación de emails
6. **Interfaz mejorada:** Menús más claros y visualización mejor
7. **Búsqueda:** Funcionalidad de búsqueda por nombre
8. **Campos adicionales:** Email y dirección como campos opcionales
9. **Timestamp:** Registro de fecha y hora de creación
10. **Confirmación:** Confirmación antes de eliminar contactos

## Desarrollo Futuro

Posibles mejoras para versiones futuras:
- [ ] Base de datos SQLite o PostgreSQL
- [ ] API REST con Flask/FastAPI
- [ ] Interfaz gráfica con Tkinter o PyQt
- [ ] Exportar a CSV o Excel
- [ ] Sincronización en la nube
- [ ] Búsqueda avanzada con filtros
- [ ] Importación de contactos desde otras fuentes

## Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## Autor

Creado como una mejora del proyecto original de agenda de contactos.

## Soporte

Para reportar problemas o sugerencias, por favor crear un issue en el proyecto.
