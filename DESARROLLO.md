# 🎓 Guía de Desarrollo - Cómo Modificar el Código

## 📂 Archivos Principales

### 1. Backend: `src/backend/main.py`
Archivo principal con toda la lógica del servidor.

```python
# Estructura del archivo:

1. IMPORTACIONES (líneas 1-20)
   ├─ FastAPI, oracledb, Pydantic

2. CONFIGURACIÓN (líneas 22-40)
   ├─ DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SERVICE
   ├─ Inicialización de FastAPI
   ├─ Configuración CORS

3. MODELOS PYDANTIC (líneas 42-80)
   ├─ Cliente, Caso, Expediente, etc.

4. FUNCIÓN DE CONEXIÓN (líneas 82-95)
   ├─ get_db_connection()

5. ENDPOINTS (líneas 97 en adelante)
   ├─ Cliente (GET)
   ├─ Caso (GET, POST, PUT)
   ├─ Expediente (GET, POST, PUT)
   ├─ Especialización (GET)
   ├─ Abogado (GET)
   └─ Sistema (GET)

6. MAIN (final del archivo)
   └─ uvicorn.run(app, ...)
```

#### Modificar Conexión Oracle
```python
# Línea ~22-27
DB_USER = "nuevo_usuario"
DB_PASSWORD = "nueva_contraseña"
DB_HOST = "nuevo_host"
DB_PORT = 1521
DB_SERVICE = "nuevo_servicio"
```

#### Agregar Nuevo Endpoint
```python
# Copiar al final de main.py (antes de if __name__)

@app.get("/api/nueva-ruta/{parametro}")
def nueva_funcion(parametro: str, connection = Depends(get_db_connection)):
    """
    Descripción del endpoint
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM MiTabla
            WHERE columna = :parametro
        """
        cursor.execute(query, {"parametro": parametro})
        result = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "campo1": row[0],
                "campo2": row[1]
            }
            for row in result
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
```

#### Modificar Consulta SQL
```python
# Buscar en main.py la función que deseas modificar
# Ejemplo: obtener_cliente

@app.get("/api/cliente/{documento}")
def obtener_cliente_por_documento(documento: str, connection = Depends(get_db_connection)):
    try:
        cursor = connection.cursor()
        
        # MODIFICAR ESTA CONSULTA:
        query = """
            SELECT codCliente, nomCliente, apellCliente, nDocumento
            FROM Cliente
            WHERE nDocumento = :documento
            AND activo = 1  # ← Agregar condiciones aquí
        """
        
        cursor.execute(query, {"documento": documento})
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                "codCliente": result[0],
                "nomCliente": result[1],
                "apellCliente": result[2],
                "nDocumento": result[3]
            }
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
```

---

### 2. Frontend: `src/frontend/index.html`
Estructura de la interfaz web.

```html
<!-- Estructura básica: -->

1. HEAD (líneas 1-10)
   ├─ Meta tags
   ├─ Links a CSS
   
2. BODY (línea 11+)
   ├─ Header (línea 13-16)
   ├─ Tab Selector (línea 19-21)
   ├─ Tab Content (línea 24+)
   │   ├─ Pestaña "Caso" (línea 24-100)
   │   └─ Pestaña "Expediente" (línea 103+)
   ├─ Modal Editor (línea 200+)
   └─ Script (línea 215)
```

#### Agregar Nuevo Campo en Formulario
```html
<!-- En la sección correspondiente, copiar este bloque: -->

<div class="form-group">
    <label for="nuevoId">Etiqueta del Campo:</label>
    <input type="text" id="nuevoId" placeholder="Placeholder">
</div>

<!-- Luego en script.js, agregar en la función correspondiente: -->
const valor = document.getElementById("nuevoId").value;
```

#### Cambiar Estilos del Formulario
```html
<!-- Los estilos están en styles.css -->
<!-- Las clases usadas en HTML son: -->

.form-group        /* Grupo de formulario */
.input-group       /* Grupo de inputs con botones */
.btn-primary       /* Botón principal (morado) */
.btn-secondary     /* Botón secundario (gris) */
.tab-content       /* Contenedor de pestaña */
```

---

### 3. Estilos: `src/frontend/styles.css`
Todos los estilos CSS del frontend.

```css
/* Estructura del archivo: */

1. Estilos generales (línea 1-30)
2. Header (línea 31-45)
3. Selector de pestaña (línea 47-65)
4. Contenido de pestaña (línea 67-85)
5. Contenedores Caso/Expediente (línea 87-110)
6. Grupos de formulario (línea 112-160)
7. Botones (línea 162-210)
8. Resultados de búsqueda (línea 212-235)
9. Área de detalles (línea 237-300)
10. Modal (línea 302-350)
11. Responsive (línea 352+)
```

#### Cambiar Color Principal
```css
/* Buscar: #667eea (morado principal) */
/* Reemplazar por: #tu_color */

Líneas donde aparece:
- 11: body background
- 50: .header background
- 56: .tab-btn.active
- 152: .btn-primary background
- 310: .modal-content
- etc.
```

#### Cambiar Tamaño de Fuente
```css
/* Búscar en .form-group input */
font-size: 13px;  /* ← Cambiar este valor */

/* O en h1 */
font-size: 28px;  /* ← Cambiar por tu tamaño */
```

---

### 4. Lógica JavaScript: `src/frontend/script.js`
Toda la lógica del frontend.

```javascript
/* Estructura del archivo: */

1. Configuración API (línea 1-5)
   └─ API_BASE_URL

2. Variables Globales (línea 7-15)
   ├─ clienteSeleccionado
   ├─ casoSeleccionado
   └─ expedienteSeleccionado

3. Inicialización (línea 17-23)
   └─ document.addEventListener("DOMContentLoaded", ...)

4. Eventos de Pestañas (línea 25-50)
   └─ inicializarEventosPestañas()

5. Eventos de Caso (línea 52-130)
   └─ inicializarEventosCaso()

6. Eventos de Expediente (línea 132-170)
   └─ inicializarEventosExpediente()

7. Eventos de Modal (línea 172-210)
   └─ inicializarEventosModal()

8. Funciones Auxiliares (línea 212+)
   ├─ mostrarResultadosBusqueda()
   ├─ seleccionarCliente()
   ├─ cargarCaso()
   ├─ cargarEspecializaciones()
   └─ etc.
```

#### Agregar Nuevo Evento
```javascript
// En la función inicializarEventosCaso():

// Nuevo botón
const btnNuevo = document.getElementById("btnNuevo");

// Event listener
btnNuevo.addEventListener("click", async () => {
    // Tu lógica aquí
    console.log("Botón clickeado");
});
```

#### Agregar Nueva Función Fetch
```javascript
// Copiar estructura existente:

async function nuevaFuncion(parametro) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/nueva-ruta/${parametro}`
        );
        const datos = await response.json();
        
        if (response.ok) {
            console.log("Éxito:", datos);
            // Procesar datos
        } else {
            console.error("Error:", datos);
            alert("Error en la operación");
        }
    } catch (error) {
        console.error("Error de conexión:", error);
        alert("Error al conectar con el servidor");
    }
}
```

---

## 🔄 Flujos de Modificación Comunes

### Modificar Búsqueda de Cliente
```
1. Backend (main.py):
   └─ Función: buscar_cliente (línea ~130)
   └─ Modificar: query SQL (línea ~135)

2. Frontend (script.js):
   └─ Función: mostrarResultadosBusqueda (línea ~350)
   └─ Modificar: mostrado en resultados (línea ~355)

3. Frontend (index.html):
   └─ ID: resultadosBusquedaCliente (línea ~100)
   └─ Clase: resultado-item (agregar si es necesario)

4. Frontend (styles.css):
   └─ Clase: .resultados-busqueda (línea ~215)
   └─ Clase: .resultado-item (línea ~220)
```

### Agregar Nueva Tabla en BD
```
1. Script SQL (src/db/initDB.sql):
   └─ CREATE TABLE miTabla (...)
   └─ CREATE INDEX idx_miTabla (...)

2. Backend (main.py):
   └─ Agregar modelo Pydantic
   └─ Agregar endpoints (GET, POST, PUT)

3. Frontend (index.html):
   └─ Agregar campos en formulario

4. Frontend (script.js):
   └─ Agregar lógica de carga/guardado

5. Frontend (styles.css):
   └─ Agregar estilos si es necesario
```

### Cambiar Validación de Formulario
```
Backend: Modificar modelo Pydantic (main.py, línea ~45)
├─ Agregar required=True
├─ Cambiar tipos de datos
└─ Agregar validadores custom

Frontend: Modificar validación en script.js
├─ Validar campos requeridos
├─ Validar formato
└─ Validar valores mínimos/máximos
```

---

## 🔧 Ejemplos de Modificaciones Reales

### Ejemplo 1: Agregar Campo "Teléfono" a Cliente

**Paso 1: Base de Datos**
```sql
-- En src/db/initDB.sql, tabla Cliente:
ALTER TABLE Cliente ADD (
    telCliente VARCHAR2(15)
);
```

**Paso 2: Backend**
```python
# En main.py, modelo Cliente:
class Cliente(BaseModel):
    codCliente: Optional[str] = None
    nomCliente: str
    apellCliente: str
    nDocumento: str
    telCliente: Optional[str] = None  # ← Agregar

# En endpoint buscar_cliente:
query = """
    SELECT codCliente, nomCliente, apellCliente, nDocumento, telCliente
    FROM Cliente
    WHERE ...
"""
# Y en el return:
"telCliente": row[4]  # ← Agregar
```

**Paso 3: Frontend**
```html
<!-- En index.html, dentro de la columna derecha del Caso: -->
<div class="form-group">
    <label for="telCliente">Teléfono:</label>
    <input type="tel" id="telCliente" disabled>
</div>
```

**Paso 4: JavaScript**
```javascript
// En seleccionarCliente():
document.getElementById("telCliente").value = cliente.telCliente || "";
```

---

### Ejemplo 2: Agregar Validación de Email

**Backend (main.py)**:
```python
from pydantic import EmailStr

class Cliente(BaseModel):
    # ... otros campos
    emailCliente: Optional[EmailStr] = None  # Valida automáticamente
```

**Frontend (script.js)**:
```javascript
// Antes de crear cliente:
if (!validarEmail(email)) {
    alert("Email inválido");
    return;
}

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}
```

---

## 📊 Debug y Testing

### Debug en Backend
```python
# Agregar prints en main.py:
print(f"DEBUG: Query = {query}")
print(f"DEBUG: Parámetros = {params}")
print(f"DEBUG: Resultado = {result}")

# Ver en terminal donde ejecutas python main.py
```

### Debug en Frontend
```javascript
// Abrir consola del navegador: F12 → Console

// Logs útiles:
console.log("Variable:", variable);
console.table(arrayDatos);
console.error("Error:", error);
```

### Testing Manual de Endpoints
```bash
# Terminal PowerShell:

# Probar GET
curl http://localhost:8000/api/cliente/12345678

# Probar POST
curl -X POST http://localhost:8000/api/caso/crear `
  -H "Content-Type: application/json" `
  -d '{...}'
```

---

## ⚠️ Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `500 Internal Server Error` | Error en SQL o conexión | Revisar logs del backend |
| `404 Not Found` | Endpoint no existe | Verificar URL y método HTTP |
| `CORS Error` | Cliente no autorizado | Agregar a allow_origins |
| `TypeError` en JS | Variable undefined | Usar `console.log()` para debug |
| `ORA-xxx` en DB | Error de Oracle | Verificar sintaxis SQL |

---

## 🚀 Deploy en Producción

Cuando estés listo para producción:

1. **Cambiar credenciales a variables de entorno**
   ```python
   import os
   DB_USER = os.getenv("DB_USER")
   ```

2. **Desactivar debug**
   ```python
   DEBUG = False
   ```

3. **Configurar CORS restringido**
   ```python
   allow_origins=["https://tupagina.com"]
   ```

4. **Usar HTTPS/SSL**
   ```bash
   uvicorn main.py --ssl-keyfile=key.pem --ssl-certfile=cert.pem
   ```

5. **Agregar rate limiting**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

---

**Versión**: 1.0.0  
**Última actualización**: Diciembre 2024  

[⬅️ Volver al README.md](README.md)
