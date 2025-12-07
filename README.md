# Sistema de Gestión de Casos y Expedientes  Gabinete de Abogados

Sistema web completo para la gestión de casos y expedientes de un gabinete de abogados, desarrollado con **FastAPI** (Python) en el backend, **HTML5/CSS3/JavaScript** en el frontend, y **Oracle** como base de datos.

## Descripción

Este proyecto incluye:
- Backend REST API con FastAPI para gestión de clientes, casos y expedientes
- Frontend web responsivo con interfaz moderna e intuitiva
- Conexión directa a Oracle sin ORMs (para máximo control de BD)
- Documentación automática de API con Swagger
- Módulo de Gestión de Caso y Módulo de Gestión de Expediente

## Guía de Instalación Completa

 Crea un entorno virtual de Python:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si tienes problemas de ejecución de scripts, ejecuta:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

4. Instala las dependencias del backend:

```powershell
cd src/backend
pip install -r requirements.txt
```

### Paso 3: Configurar Credenciales de Oracle

Edita `src/backend/main.py` y localiza la sección de configuración de base de datos (aproximadamente líneas 10-20).

Actualiza las credenciales:

```python
DATABASE_CONFIG = {
    "user": "tu_usuario_oracle",
    "password": "tu_contraseña_oracle",
    "dsn": "tu_host:1521/tu_servicio"
}
```

Reemplaza los siguientes valores con los de tu instancia Oracle:
- `tu_usuario_oracle`: Usuario de tu base de datos Oracle
- `tu_contraseña_oracle`: Contraseña del usuario
- `tu_host`: Dirección del servidor Oracle (ej: localhost o 192.168.1.100)
- `tu_servicio`: Nombre del servicio Oracle (ej: ORCL, XE)

### Paso 4: Inicializar la Base de Datos (Opcional)

Si necesitas crear las tablas desde cero:

1. Conéctate a tu instancia Oracle usando SQL*Plus o SQL Developer
2. Ejecuta el script de creación:

```sql
@src/db/initDB.sql
```

3. Carga los datos de prueba:

```sql
@src/db/inserts.sql
```

**Nota:** Si la base de datos ya existe, omite este paso.

## Ejecución del Sistema

### Iniciar el Backend (FastAPI)

Desde la carpeta raíz del proyecto:

```powershell
cd src/backend
python main.py
```

El servidor estará disponible en: **http://localhost:8000**

Para ver la documentación interactiva de la API (Swagger UI):
- Abre en tu navegador: **http://localhost:8000/docs**

### Iniciar el Frontend

En una nueva ventana de PowerShell (desde la carpeta raíz):

```powershell
cd src/frontend
python -m http.server 8001
```

El frontend estará disponible en: **http://localhost:8001**

**Importante:** Asegúrate de que ambos servidores (backend en 8000 y frontend en 8001) estén corriendo simultáneamente.

## Estructura de Endpoints API

### Clientes
- `GET /api/clientes` - Listar todos los clientes
- `GET /api/clientes/{id}` - Obtener cliente por ID
- `POST /api/clientes` - Crear nuevo cliente
- `PUT /api/clientes/{id}` - Actualizar cliente

### Casos
- `GET /api/casos` - Listar todos los casos
- `GET /api/casos/{id}` - Obtener caso por ID
- `POST /api/casos` - Crear nuevo caso
- `PUT /api/casos/{id}` - Actualizar caso

### Expedientes
- `GET /api/expedientes` - Listar expedientes
- `GET /api/expedientes/{codEspecializacion}/{pasoEtapa}/{noCaso}/{consecExpe}` - Obtener expediente (clave compuesta)
- `POST /api/expedientes` - Crear nuevo expediente

### Sucesos
- `GET /api/sucesos` - Listar sucesos
- `POST /api/sucesos` - Crear suceso
- `PUT /api/sucesos/{id}` - Actualizar suceso

### Resultados
- `GET /api/resultados` - Listar resultados
- `POST /api/resultados` - Crear resultado
- `PUT /api/resultados/{id}` - Actualizar resultado

### Documentos
- `GET /api/documentos` - Listar documentos
- `POST /api/documentos` - Subir documento
- `DELETE /api/documentos/{id}` - Eliminar documento

**Nota:** Algunos expedientes usan claves compuestas (codEspecializacion, pasoEtapa, noCaso, consecExpe).

## Notas Técnicas Importantes

### Claves Compuestas
La tabla EXPEDIENTE usa una clave primaria compuesta de 4 campos. Cuando consultes o actualices un expediente, necesitarás proporcionar todos 4 valores:
- `codEspecializacion`
- `pasoEtapa`
- `noCaso`
- `consecExpe`

### Numeración Automática
El sistema genera automáticamente:
- Números de caso (`noCaso`)
- Consecutivos de suceso, resultado y documento dentro de cada expediente

### Conexión a Oracle
El backend usa `oracledb` (cliente nativo de Oracle) sin ORM. Esto permite:
- Mayor control sobre queries SQL
- Mejor rendimiento
- Acceso directo a stored procedures si es necesario

## Solución de Problemas

### "ModuleNotFoundError: No module named 'oracledb'"
- Asegúrate de haber activado el entorno virtual: `.\venv\Scripts\Activate.ps1`
- Reinstala dependencias: `pip install -r requirements.txt`

### "ORA-12154: TNS:could not resolve the connect identifier specified"
- Verifica que Oracle Instant Client esté en: `C:\oracle\instantclient_23_9`
- Revisa que la variable `dsn` en `main.py` sea correcta

### El frontend no se conecta al backend
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Revisa la consola del navegador (F12) para ver errores de CORS o conexión

### Puerto 8000 o 8001 ya está en uso
```powershell
# Para cambiar el puerto del backend, edita main.py:
# uvicorn.run(app, host="0.0.0.0", port=9000)

# Para cambiar el puerto del frontend:
python -m http.server 9001
```

## Recursos Adicionales

- Documentación ER: Ver archivos en `doc/` y `gabinete_abogados_powerdesigner/`
- Modelos: Archivos .cdm, .ldm, .pdm en PowerDesigner
- Scripts SQL: `src/db/initDB.sql` y `src/db/inserts.sql`

## Versión y Licencia

- Versión: 1.0
- Proyecto: Gestión de Casos Legales - Gabinete de Abogados
- Año: 2025
