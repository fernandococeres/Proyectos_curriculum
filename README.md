# Sistema de Gestión Escolar

Sistema integral de gestión de estudiantes y docentes para instituciones educativas. Aplicación de escritorio desarrollada en Python con interfaz gráfica Tkinter y base de datos SQLite.

---

## 📋 Tabla de Contenidos

1. [Características](#características)
2. [Requisitos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Uso](#uso)
5. [Arquitectura](#arquitectura)
6. [Documentación para Desarrolladores](#documentación-para-desarrolladores)
7. [Estructura de Carpetas](#estructura-de-carpetas)
8. [Base de Datos](#base-de-datos)

---

## ✨ Características

### Gestión de Alumnos
- ✅ **CRUD Completo**: Crear, leer, actualizar, eliminar estudiantes
- ✅ **Búsqueda por DNI**: Búsqueda rápida y única de estudiantes
- ✅ **Campos Validados**: 
  - Nombre, Apellido (letras solo)
  - Email (formato válido)
  - Teléfono (10+ dígitos)
  - DNI (único, números)
  - Grado: 1ro, 2do, 3ro, 4to, 5to, 6to
  - Asignatura: Matemáticas, Lengua, Ciencias, Historia, Educación Física, Inglés
  - Fecha Nacimiento (YYYY-MM-DD)

### Gestión de Profesores
- ✅ **CRUD Completo**: Crear, leer, actualizar, eliminar docentes
- ✅ **Campos Validados**: Nombre, Apellido, Email, Teléfono, Especialidad, Documento
- ✅ **Búsqueda**: Por documento/especialidad

### Panel Administrativo
- 📊 **Estadísticas**: Totales, distribuciones por grado/asignatura/especialidad
- 📈 **Reportes**: Análisis detallado de datos
- 📥 **Exportación**: CSV y Excel (.xlsx)

### Seguridad y Validación
- ✅ Validación en tiempo real
- ✅ Prevención de duplicados (DNI/Documento únicos)
- ✅ Mensajes de error claros en español
- ✅ Confirmación antes de eliminar

---

## 📦 Requisitos Previos

- Python 3.7 o superior
- tkinter (incluido con Python)
- tkcalendar (opcional para funcionalidades futuras)

## Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone <repositorio>
   cd coceres_fernando_ie4c
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

2. **Desde el menú principal**
   - Clic en "Tablas" → "Alumnos" para gestionar alumnos
   - Clic en "Tablas" → "Profesores" para gestionar profesores
   - Clic en "Administración" → "Administración de Alumnos" para ver panel admin de alumnos
   - Clic en "Administración" → "Administración de Profesores" para ver panel admin de profesores

3. **Operaciones de Gestión disponibles**
   - **Nuevo**: Crear un nuevo registro
   - **Editar**: Modificar un registro seleccionado
   - **Eliminar**: Borrar un registro (requiere confirmación)
   - **Actualizar**: Recargar la tabla
   - **Buscar**: Filtrar por nombre

4. **Panel de Administración - Pestaña Estadísticas**
   - Ver total de registros
   - Desglose por grado (alumnos) o especialidad (profesores)
   - Análisis detallado de distribución

5. **Panel de Administración - Pestaña Reportes**
   - Generar reportes especiales
   - Buscar registros sin email/documento
   - Ver registros recientes
   - Filtrar por criterios específicos

6. **Panel de Administración - Pestaña Exportación**
   - Descargar datos en Excel (con estilos y estadísticas)
   - Descargar datos en CSV (para importar a otras aplicaciones)

## Estructura del Proyecto

```
coceres_fernando_ie4c/
├── main.py                    # Punto de entrada de la aplicación
├── centrar_ventana.py         # Función auxiliar para centrar ventanas
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
├── models/
│   └── models.py             # Clases de datos (Alumno, Profesor)
├── database/
│   └── dbConn.py            # Conexión y operaciones con SQLite
├── controlers/
│   └── controlers.py         # Lógica de negocio (CRUD)
└── views/
    └── views.py             # Interfaces gráficas Tkinter
```

## Módulos Principales

### `models.py`
Define las clases de datos:
- `Alumno`: Representa a un estudiante
- `Profesor`: Representa a un docente

### `dbConn.py`
Maneja la conexión con SQLite:
- Crear tablas
- Ejecutar consultas
- Métodos CRUD genéricos

### `controlers.py`
Contiene la lógica de negocio:
- `ControladorAlumnos`: Operaciones CRUD para alumnos
- `ControladorProfesores`: Operaciones CRUD para profesores

### `views.py`
Interfaces gráficas Tkinter:
- `VentanaAlumnos`: Ventana de gestión de alumnos
- `VentanaProfesores`: Ventana de gestión de profesores

### `admin.py`
Sistema administrativo avanzado:
- `AdminAlumnos`: Estadísticas, reportes y exportación de alumnos
- `AdminProfesores`: Estadísticas, reportes y exportación de profesores

### `admin_views.py`
Interfaces administrativas:
- `AdminAlumnosView`: Panel de administración de alumnos con 3 pestañas
- `AdminProfesoresView`: Panel de administración de profesores con 3 pestañas
- Pestañas: Estadísticas, Reportes, Exportación

## Base de Datos

La base de datos se crea automáticamente la primera vez que se ejecuta la aplicación.

### Tabla: alumnos
```sql
CREATE TABLE alumnos (
    id_alumno INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT,
    telefono TEXT,
    fecha_nacimiento TEXT,
    grado TEXT,
    seccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tabla: profesores
```sql
CREATE TABLE profesores (
    id_profesor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT,
    telefono TEXT,
    especialidad TEXT,
    documento TEXT UNIQUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Funcionalidades Futuras

- [ ] Generación de reportes (PDF, Excel)
- [ ] Sistema de calificaciones
- [ ] Horarios de clases
- [ ] Historial de asistencia
- [ ] Exportación/Importación de datos
- [ ] Autenticación de usuarios
- [ ] Interfaz mejorada

## Notas de Desarrollo

- La base de datos se almacena en `escuela.db`
- Los imports asumen que se ejecuta desde el directorio raíz
- Se usa tkinter nativo sin frameworks adicionales para la UI

## Autor

Fernando Cóceres
Instituto Educativo IE4

## Licencia

Este proyecto es de uso educativo.

---

Para reportar errores o sugerencias, contáctate con el desarrollador.


## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
