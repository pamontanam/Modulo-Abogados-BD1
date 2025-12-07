# 🏗️ Arquitectura del Sistema - Documentación Técnica

## Descripción General

```
┌─────────────────────────────────────────────────────────────────┐
│                     NAVEGADOR WEB (Cliente)                      │
│                  http://localhost:8001/index.html                │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Servidor)                     │
│                    http://localhost:8000                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   API REST Endpoints                      │  │
│  │  (/api/cliente/, /api/caso/, /api/expediente/, etc.)   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │
│                             ▼
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Conexión Directa a Oracle (oracledb)            │  │
│  │         Conexiones por solicitud HTTP                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ TCP/IP Puerto 1521
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Oracle Database 12c+                         │
│                                                                 │
│  TABLAS: CLIENTE, CASO, EXPEDIENTE, ABOGADO, LUGAR,            │
│          ESPECIALIZACION, ETAPAPROCESAL, RESULTADO, SUCESO,     │
│          DOCUMENTO, PAGO, FORMAPAGO, etc.                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos

### Crear Caso (Ejemplo)

```
┌─────────────┐
│   Usuario   │ Ingresa datos en formulario
└──────┬──────┘
       │
       ▼
┌──────────────────────────────┐
│  Frontend (JavaScript)       │ Valida datos
│  script.js → btnCrearCaso()  │
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Envía HTTP POST             │
│  POST /api/caso/crear        │
│  {"fechaInicio": "2024-12-01"} JSON
└──────┬──────────────────────┘
       │ HTTP
       ▼
┌──────────────────────────────┐
│  Backend (FastAPI)           │ Recibe y procesa
│  main.py → crear_caso()      │
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Obtiene número consecutivo  │
│  SELECT MAX(noCaso)          │
│  FROM Caso                   │
└──────┬──────────────────────┘
       │ SQL
       ▼
┌──────────────────────────────┐
│  Oracle Database             │ Retorna max
│  (Conexión directa)          │
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Inserta nuevo caso          │
│  INSERT INTO Caso (...)      │
│  VALUES (...)                │
└──────┬──────────────────────┘
       │ SQL
       ▼
┌──────────────────────────────┐
│  Oracle Database             │ Inserta y commits
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Backend retorna respuesta   │
│  JSON: {success: true,       │
│         noCaso: 5}           │
└──────┬──────────────────────┘
       │ HTTP 200 OK
       ▼
┌──────────────────────────────┐
│  Frontend recibe respuesta   │
│  Actualiza UI                │
│  Muestra confirmación        │
└──────────────────────────────┘
```

---

## 📁 Estructura de Carpetas

```
Modulo-Abogados-BD1/
│
├── README.md .......................... Documentación principal (LEER PRIMERO)
├── QUICKSTART.md ...................... Guía rápida de 5 minutos
├── ARQUITECTURA.md .................... Este archivo
│
├── config.py .......................... Script de configuración inicial
├── iniciar.bat ........................ Script para iniciar todo (Windows)
│
├── .env.example ....................... Template de variables de entorno
├── .gitignore ......................... Archivos a ignorar en Git
│
├── doc/ ............................... Documentación del proyecto
│   └── (Documentos PDF, imágenes, apuntes)
│
├── gabinete_abogados_powerdesigner/
│   ├── Conceptual.cdm ................. Modelo conceptual (PowerDesigner)
│   ├── Logico.ldm ..................... Modelo lógico (PowerDesigner)
│   ├── Fisico.pdm ..................... Modelo físico (PowerDesigner)
│   └── (Otros archivos PowerDesigner)
│
├── interfaz/ .......................... Proyecto Django anterior (referencia)
│   ├── manage.py
│   ├── requirements.txt
│   ├── clientes/
│   ├── interfaz/
│   │   └── oracle_client.py ........... Referencia de conexión Oracle
│   └── ...
│
├── src/
│   │
│   ├── backend/
│   │   ├── main.py .................... ⭐ ARCHIVO PRINCIPAL (FastAPI)
│   │   ├── requirements.txt ........... Dependencias Python
│   │   ├── venv/ ...................... Entorno virtual (creado al instalar)
│   │   │   ├── Scripts/
│   │   │   │   ├── python.exe
│   │   │   │   └── activate.bat
│   │   │   └── Lib/
│   │   │       └── site-packages/
│   │   └── sample.txt
│   │
│   ├── frontend/
│   │   ├── index.html ................. ⭐ INTERFAZ WEB (HTML)
│   │   ├── styles.css ................. ⭐ ESTILOS (CSS)
│   │   ├── script.js .................. ⭐ LÓGICA (JavaScript)
│   │   └── sample.txt
│   │
│   └── db/
│       ├── initDB.sql ................. ⭐ CREAR TABLAS (Oracle SQL)
│       └── inserts.sql ................ ⭐ DATOS INICIALES (Oracle SQL)
│
└── (Otros archivos de proyecto)
```

---

## 🛠️ Stack Tecnológico

### Backend
```
FastAPI 0.104.1        → Framework web asincrónico
Uvicorn 0.24.0         → Servidor ASGI
oracledb 2.1.0         → Driver Oracle nativo Python
Pydantic 2.5.0         → Validación de datos
Python 3.9+            → Lenguaje
```

### Frontend
```
HTML5                  → Estructura
CSS3                   → Estilos (Flexbox, Grid, Gradients)
JavaScript (Vanilla)   → Lógica (Sin frameworks)
Fetch API              → Comunicación con backend
```

### Base de Datos
```
Oracle Database 12c+   → DBMS principal
SQL Puro               → Sin ORMs (control total)
```

---

## 📡 API REST - Endpoints

### Patrón de Respuesta
```json
{
  "success": true,
  "data": {...},
  "mensaje": "Operación exitosa"
}
```

### Categorías de Endpoints

#### 1. CLIENTE
```
GET  /api/cliente/buscar/{nombre}/{apellido}
GET  /api/cliente/{documento}
```

#### 2. CASO
```
GET  /api/caso/ultimo/{codCliente}
GET  /api/caso/activos/{codCliente}
GET  /api/caso/{noCaso}
POST /api/caso/crear
PUT  /api/caso/{noCaso}
```

#### 3. EXPEDIENTE
```
GET  /api/expediente/caso/{noCaso}
GET  /api/expediente/{consecExpe}
POST /api/expediente/crear
PUT  /api/expediente/{consecExpe}
```

#### 4. ESPECIALIZACION
```
GET  /api/especializacion/
```

#### 5. ABOGADO
```
GET  /api/abogado/especializacion/{codEspecializacion}
```

#### 6. SISTEMA
```
GET  /api/health
GET  /
```

---

## 🔐 Seguridad y Validaciones

### Backend (main.py)
```python
✓ Validación con Pydantic
✓ Conexión preparada (previene SQL injection)
✓ Manejo de excepciones
✓ CORS configurado
✓ HTTPException para errores
✓ Rollback en transacciones fallidas
```

### Frontend (script.js)
```python
✓ Validación de campos requeridos
✓ Verificación de cliente seleccionado
✓ Estados deshabilitados para lectura
✓ Confirmaciones antes de operaciones
✓ Manejo de errores con try-catch
```

### Base de Datos
```sql
✓ Restricciones de integridad (FK, PK)
✓ Tipos de datos validados
✓ Índices para performance
✓ Transacciones ACID
```

---

## 🔄 Ciclo de Vida de una Solicitud

### Paso 1: Solicitud HTTP
```
Client → Server
GET http://localhost:8000/api/cliente/12345678
Headers: Content-Type: application/json
```

### Paso 2: Procesamiento en FastAPI
```python
@app.get("/api/cliente/{documento}")
def obtener_cliente_por_documento(documento: str):
    # 1. Validación de parámetros (automática)
    # 2. Conexión a Oracle
    # 3. Ejecución de SQL
    # 4. Procesar resultados
    # 5. Retornar JSON
```

### Paso 3: Conexión a Oracle
```python
connection = oracledb.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    dsn=f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
)
cursor = connection.cursor()
cursor.execute(query, params)
result = cursor.fetchone()
connection.close()
```

### Paso 4: Respuesta HTTP
```
Server → Client
200 OK
Content-Type: application/json

{"codCliente": "5", "nomCliente": "Juan", ...}
```

### Paso 5: Procesamiento en Frontend
```javascript
// 1. Fetch recibe respuesta
// 2. JSON.parse() convierte a objeto
// 3. Validar resultado
// 4. Actualizar DOM
// 5. Mostrar UI actualizada
```

---

## 🗄️ Modelos de Datos Principales

### Cliente
```python
{
    "codCliente": "5",
    "nomCliente": "Juan",
    "apellCliente": "Pérez",
    "nDocumento": "1234567890"
}
```

### Caso
```python
{
    "noCaso": 1,
    "fechaInicio": "2024-12-01",
    "fechaFin": None,
    "valor": "1000000",
    "codEspecializacion": "1",
    "codCliente": "5"
}
```

### Expediente
```python
{
    "consecExpe": 1,
    "noCaso": 1,
    "codEtapa": "1",
    "fechaEtapa": "2024-12-01",
    "cedAbogado": "1234567",
    "conSuceso": "Texto del suceso",
    "conResul": "Resultado del caso"
}
```

---

## 🔧 Configuración y Personalización

### Cambiar Puerto Backend
```python
# main.py, línea final
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)  # Cambiar 8000 por 9000
```

### Cambiar Puerto Frontend
```powershell
# En terminal
python -m http.server 9001  # En lugar de 8001
```

### Agregar Nuevo Endpoint
```python
@app.get("/api/nueva-ruta/{parametro}")
def nueva_funcion(parametro: str):
    # Lógica aquí
    return {"resultado": "valor"}
```

---

## 📊 Performance y Optimización

### Índices en Oracle
```sql
-- Crear índices para búsquedas frecuentes
CREATE INDEX idx_cliente_nombre ON Cliente(nomCliente);
CREATE INDEX idx_caso_cliente ON Caso(codCliente);
CREATE INDEX idx_expediente_caso ON Expediente(noCaso);
```

### Caché Frontend
```javascript
// Los datos se almacenan en variables globales
let clienteSeleccionado = null;
let casoSeleccionado = null;
```

### Connection Pooling (Futuro)
```python
# Implementar para conexiones reutilizables
from oracledb import SessionPool
```

---

## 🐛 Debugging

### Backend Debugging
```python
# Agregar prints para debugging
print(f"DEBUG: Query = {query}")
print(f"DEBUG: Resultado = {result}")

# O usar logging
import logging
logging.debug(f"Información: {data}")
```

### Frontend Debugging
```javascript
// F12 en navegador → Console
console.log("Debug:", variable);
console.error("Error:", error);
console.table(datos);  // Ver arrays como tabla
```

### SQL Debugging
```sql
-- En SQL*Plus
SET ECHO ON;
@src/db/initDB.sql
SET ECHO OFF;

-- O usar SQL Developer con breakpoints
```

---

## 📈 Escalabilidad Futura

### Mejoras Planeadas
- [ ] Autenticación y autorización (JWT)
- [ ] Base de datos en caché (Redis)
- [ ] Connection pooling
- [ ] Paginación de resultados
- [ ] Búsqueda full-text
- [ ] Reportes PDF
- [ ] Upload de archivos
- [ ] Auditoría de cambios
- [ ] API versioning
- [ ] Rate limiting

### Deployments Futuros
- Docker containerization
- Azure/AWS cloud deployment
- CI/CD pipeline
- Monitoring y logging centralizado

---

## 📝 Convenciones de Código

### Python (Backend)
```python
# Nombres en inglés/español mezcla según contexto
# Funciones en snake_case
def obtener_cliente()

# Variables en español (según requiere el usuario)
cliente_seleccionado

# Comentarios en español con #
# Esto es un comentario
```

### JavaScript (Frontend)
```javascript
// camelCase para variables y funciones
let clienteSeleccionado = null;
function seleccionarCliente() {}

// Comentarios en español
// Cargar datos del cliente
```

### SQL (Oracle)
```sql
-- MAYÚSCULAS para palabras clave
-- snake_case para nombres de tablas y columnas
SELECT nomCliente, apellCliente
FROM Cliente
WHERE codCliente = '5'
```

---

## 🤝 Contribución y Mejoras

Para agregar nuevas funcionalidades:

1. **Crear endpoint en backend** (`main.py`)
2. **Agregar función en frontend** (`script.js`)
3. **Actualizar interfaz si es necesario** (`index.html`, `styles.css`)
4. **Documentar cambios** (README.md)
5. **Probar end-to-end**

---

**Versión**: 1.0.0  
**Actualizado**: Diciembre 2024  
**Autor**: Equipo de Desarrollo  

[⬅️ Volver al README.md](README.md)
