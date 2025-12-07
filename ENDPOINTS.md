# 📡 Referencia Completa de Endpoints API

## Base URL
```
http://localhost:8000
```

---

## 🏥 Sistema

### Health Check
Verifica que la API está funcionando correctamente.

```http
GET /api/health
```

**Respuesta (200 OK)**:
```json
{
  "status": "ok",
  "mensaje": "API de Gestión de Casos funcionando"
}
```

**cURL**:
```bash
curl http://localhost:8000/api/health
```

**JavaScript**:
```javascript
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(data => console.log(data));
```

---

### Información de Bienvenida
```http
GET /
```

**Respuesta (200 OK)**:
```json
{
  "mensaje": "Bienvenido al Sistema de Gestión de Casos y Expedientes",
  "documentación": "http://localhost:8000/docs"
}
```

---

## 👤 Cliente

### Buscar Cliente por Nombre y Apellido
Busca clientes por nombre y/o apellido (búsqueda parcial).

```http
GET /api/cliente/buscar/{nombre}/{apellido}
```

**Parámetros**:
- `nombre` (string): Nombre del cliente (búsqueda LIKE)
- `apellido` (string): Apellido del cliente (búsqueda LIKE)

**Respuesta (200 OK)**:
```json
[
  {
    "codCliente": "5",
    "nomCliente": "Juan",
    "apellCliente": "Pérez",
    "nDocumento": "1234567890"
  },
  {
    "codCliente": "6",
    "nomCliente": "Juan",
    "apellCliente": "González",
    "nDocumento": "0987654321"
  }
]
```

**cURL**:
```bash
curl "http://localhost:8000/api/cliente/buscar/Juan/Perez"
```

**JavaScript**:
```javascript
const nombre = "Juan";
const apellido = "Perez";

fetch(`http://localhost:8000/api/cliente/buscar/${nombre}/${apellido}`)
  .then(r => r.json())
  .then(clientes => {
    console.log("Clientes encontrados:", clientes);
    // Mostrar en UI
  });
```

**Casos de Uso**:
- ✓ Usuario escribe nombre en formulario
- ✓ Usuario toca botón "Buscar"
- ✓ Sistema muestra lista de coincidencias
- ✓ Usuario selecciona cliente

---

### Obtener Cliente por Número de Documento
Obtiene los datos completos de un cliente usando su documento.

```http
GET /api/cliente/{documento}
```

**Parámetros**:
- `documento` (string): Número de documento del cliente

**Respuesta (200 OK)**:
```json
{
  "codCliente": "5",
  "nomCliente": "Juan",
  "apellCliente": "Pérez",
  "nDocumento": "1234567890"
}
```

**Respuesta (404 Not Found)**:
```json
{
  "detail": "Cliente no encontrado"
}
```

**cURL**:
```bash
curl http://localhost:8000/api/cliente/1234567890
```

**JavaScript**:
```javascript
const documento = "1234567890";

fetch(`http://localhost:8000/api/cliente/${documento}`)
  .then(r => r.json())
  .then(cliente => {
    if (cliente.nDocumento) {
      console.log("Cliente encontrado:", cliente);
      // Llenar formulario
    } else {
      console.log("Cliente no existe");
    }
  });
```

---

## 📝 Caso

### Obtener Último Caso Activo de Cliente
Retorna el caso más reciente sin fecha fin.

```http
GET /api/caso/ultimo/{codCliente}
```

**Parámetros**:
- `codCliente` (string): Código del cliente

**Respuesta (200 OK)**:
```json
{
  "noCaso": 5,
  "fechaInicio": "2024-12-01",
  "fechaFin": null,
  "valor": "1000000",
  "codEspecializacion": "1"
}
```

**Respuesta si no hay casos activos**:
```json
null
```

**cURL**:
```bash
curl http://localhost:8000/api/caso/ultimo/5
```

**JavaScript**:
```javascript
async function cargarUltimoCaso(codCliente) {
  const response = await fetch(`/api/caso/ultimo/${codCliente}`);
  const caso = await response.json();
  
  if (caso) {
    document.getElementById('noCaso').value = caso.noCaso;
    document.getElementById('valor').value = caso.valor;
  }
}
```

---

### Obtener Todos los Casos Activos de Cliente
Retorna lista de todos los casos sin fecha fin (para dropdown).

```http
GET /api/caso/activos/{codCliente}
```

**Parámetros**:
- `codCliente` (string): Código del cliente

**Respuesta (200 OK)**:
```json
[
  {
    "noCaso": 5,
    "fechaInicio": "2024-12-01",
    "valor": "1000000",
    "codEspecializacion": "1"
  },
  {
    "noCaso": 4,
    "fechaInicio": "2024-11-15",
    "valor": "500000",
    "codEspecializacion": "2"
  }
]
```

**cURL**:
```bash
curl http://localhost:8000/api/caso/activos/5
```

**JavaScript**:
```javascript
async function cargarCasosEnDropdown(codCliente) {
  const response = await fetch(`/api/caso/activos/${codCliente}`);
  const casos = await response.json();
  
  const select = document.getElementById('casosActivos');
  select.innerHTML = '<option>-- Seleccionar --</option>';
  
  casos.forEach(caso => {
    const option = document.createElement('option');
    option.value = caso.noCaso;
    option.textContent = `Caso ${caso.noCaso} - $${caso.valor}`;
    select.appendChild(option);
  });
}
```

---

### Obtener Caso Específico
Obtiene los detalles completos de un caso.

```http
GET /api/caso/{noCaso}
```

**Parámetros**:
- `noCaso` (integer): Número del caso

**Respuesta (200 OK)**:
```json
{
  "noCaso": 5,
  "fechaInicio": "2024-12-01",
  "fechaFin": null,
  "valor": "1000000",
  "codEspecializacion": "1",
  "codCliente": "5"
}
```

**cURL**:
```bash
curl http://localhost:8000/api/caso/5
```

---

### Crear Nuevo Caso
Crea un nuevo caso y genera automáticamente el número consecutivo.

```http
POST /api/caso/crear
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "fechaInicio": "2024-12-05",
  "fechaFin": null,
  "valor": "2500000",
  "codEspecializacion": "1",
  "codCliente": "5"
}
```

**Respuesta (200 OK)**:
```json
{
  "success": true,
  "noCaso": 6,
  "mensaje": "Caso 6 creado exitosamente"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/caso/crear \
  -H "Content-Type: application/json" \
  -d '{
    "fechaInicio": "2024-12-05",
    "fechaFin": null,
    "valor": "2500000",
    "codEspecializacion": "1",
    "codCliente": "5"
  }'
```

**JavaScript**:
```javascript
async function crearCaso(datos) {
  const response = await fetch('http://localhost:8000/api/caso/crear', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      fechaInicio: datos.fechaInicio,
      fechaFin: null,
      valor: datos.valor,
      codEspecializacion: datos.especializacion,
      codCliente: datos.cliente.codCliente
    })
  });
  
  const result = await response.json();
  if (result.success) {
    alert(`Caso ${result.noCaso} creado`);
    document.getElementById('noCaso').value = result.noCaso;
  }
}
```

---

### Actualizar Caso
Actualiza un caso existente (solo si está activo/sin fecha fin).

```http
PUT /api/caso/{noCaso}
Content-Type: application/json
```

**Parámetros**:
- `noCaso` (integer): Número del caso a actualizar

**Body (JSON)**:
```json
{
  "fechaInicio": "2024-12-05",
  "valor": "3000000",
  "codEspecializacion": "2"
}
```

**Respuesta (200 OK)**:
```json
{
  "success": true,
  "mensaje": "Caso 5 actualizado"
}
```

**cURL**:
```bash
curl -X PUT http://localhost:8000/api/caso/5 \
  -H "Content-Type: application/json" \
  -d '{
    "fechaInicio": "2024-12-05",
    "valor": "3000000",
    "codEspecializacion": "2"
  }'
```

---

## 📂 Expediente

### Obtener Expedientes de un Caso
Lista todos los expedientes asociados a un caso.

```http
GET /api/expediente/caso/{noCaso}
```

**Parámetros**:
- `noCaso` (integer): Número del caso

**Respuesta (200 OK)**:
```json
[
  {
    "consecExpe": 1,
    "noCaso": 5,
    "fechaEtapa": "2024-12-01"
  },
  {
    "consecExpe": 2,
    "noCaso": 5,
    "fechaEtapa": "2024-12-10"
  }
]
```

**cURL**:
```bash
curl http://localhost:8000/api/expediente/caso/5
```

---

### Obtener Detalle de Expediente
Obtiene todos los detalles de un expediente específico.

```http
GET /api/expediente/{consecExpe}
```

**Parámetros**:
- `consecExpe` (integer): Número consecutivo del expediente

**Respuesta (200 OK)**:
```json
{
  "consecExpe": 1,
  "noCaso": 5,
  "codEtapa": "1",
  "fechaEtapa": "2024-12-01",
  "nomEtapa": "Demanda",
  "cedAbogado": "1234567",
  "nomLugar": "Juzgado Civil",
  "codLugar_Entidad": "001",
  "nInstancia": null,
  "idImpugna": null,
  "conSuceso": "Se presentó demanda contra el demandado",
  "conResul": "Demanda admitida"
}
```

**cURL**:
```bash
curl http://localhost:8000/api/expediente/1
```

---

### Crear Nuevo Expediente
Crea un nuevo expediente para un caso.

```http
POST /api/expediente/crear
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "noCaso": 5,
  "codEtapa": "1",
  "fechaEtapa": "2024-12-05",
  "cedAbogado": "1234567",
  "codLugar": "001",
  "codLugar_Entidad": "JUZG001"
}
```

**Respuesta (200 OK)**:
```json
{
  "success": true,
  "consecExpe": 3,
  "mensaje": "Expediente 3 creado exitosamente"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8000/api/expediente/crear \
  -H "Content-Type: application/json" \
  -d '{
    "noCaso": 5,
    "codEtapa": "1",
    "fechaEtapa": "2024-12-05",
    "cedAbogado": "1234567",
    "codLugar": "001"
  }'
```

---

### Actualizar Etapa de Expediente
Actualiza los datos de suceso y resultado de una etapa.

```http
PUT /api/expediente/{consecExpe}
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "consecExpe": 1,
  "conSuceso": "Se presentó demanda contenciosa",
  "conResul": "La demanda fue admitida por el juzgado"
}
```

**Respuesta (200 OK)**:
```json
{
  "success": true,
  "mensaje": "Etapa 1 actualizada"
}
```

**cURL**:
```bash
curl -X PUT http://localhost:8000/api/expediente/1 \
  -H "Content-Type: application/json" \
  -d '{
    "consecExpe": 1,
    "conSuceso": "Se presentó demanda",
    "conResul": "Demanda admitida"
  }'
```

---

## 🎓 Especialización

### Obtener Todas las Especializaciones
Lista todas las especializaciones disponibles en el sistema.

```http
GET /api/especializacion/
```

**Respuesta (200 OK)**:
```json
[
  {
    "codEspecializacion": "1",
    "nomEspecializacion": "Derecho Civil"
  },
  {
    "codEspecializacion": "2",
    "nomEspecializacion": "Derecho Penal"
  },
  {
    "codEspecializacion": "3",
    "nomEspecializacion": "Derecho Laboral"
  },
  {
    "codEspecializacion": "4",
    "nomEspecializacion": "Derecho Administrativo"
  }
]
```

**cURL**:
```bash
curl http://localhost:8000/api/especializacion/
```

**JavaScript**:
```javascript
async function cargarEspecializaciones() {
  const response = await fetch('/api/especializacion/');
  const especializaciones = await response.json();
  
  const select = document.getElementById('especializacion');
  
  especializaciones.forEach(esp => {
    const option = document.createElement('option');
    option.value = esp.codEspecializacion;
    option.textContent = esp.nomEspecializacion;
    select.appendChild(option);
  });
}
```

---

## ⚖️ Abogado

### Obtener Abogados por Especialización
Lista todos los abogados que tienen una especialización específica.

```http
GET /api/abogado/especializacion/{codEspecializacion}
```

**Parámetros**:
- `codEspecializacion` (string): Código de la especialización

**Respuesta (200 OK)**:
```json
[
  {
    "cedula": "1234567",
    "nombre": "Carlos",
    "apellido": "García",
    "nTarjetaProfesional": "12345"
  },
  {
    "cedula": "7654321",
    "nombre": "María",
    "apellido": "López",
    "nTarjetaProfesional": "54321"
  }
]
```

**cURL**:
```bash
curl http://localhost:8000/api/abogado/especializacion/1
```

**JavaScript**:
```javascript
async function cargarAbogadosPorEspecializacion(codEsp) {
  const response = await fetch(`/api/abogado/especializacion/${codEsp}`);
  const abogados = await response.json();
  
  const select = document.getElementById('abogado');
  select.innerHTML = '<option>-- Seleccionar --</option>';
  
  abogados.forEach(abogado => {
    const option = document.createElement('option');
    option.value = abogado.cedula;
    option.textContent = `${abogado.nombre} ${abogado.apellido}`;
    select.appendChild(option);
  });
}
```

---

## ⚠️ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 400 | Bad Request - Datos inválidos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error en servidor |

---

## 📊 Ejemplos de Flujos Completos

### Flujo: Crear Caso Completo

```javascript
// 1. Buscar cliente
const clienteResponse = await fetch('/api/cliente/buscar/Juan/Perez');
const clientes = await clienteResponse.json();
const cliente = clientes[0]; // Seleccionar primer resultado

// 2. Crear caso
const casoResponse = await fetch('/api/caso/crear', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fechaInicio: '2024-12-05',
    fechaFin: null,
    valor: '1000000',
    codEspecializacion: '1',
    codCliente: cliente.codCliente
  })
});
const caso = await casoResponse.json();

// 3. Crear expediente
const expedienteResponse = await fetch('/api/expediente/crear', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    noCaso: caso.noCaso,
    codEtapa: '1',
    fechaEtapa: '2024-12-05',
    cedAbogado: '1234567',
    codLugar: '001'
  })
});
const expediente = await expedienteResponse.json();

console.log('Caso creado:', caso.noCaso);
console.log('Expediente creado:', expediente.consecExpe);
```

---

**Versión**: 1.0.0  
**Última actualización**: Diciembre 2024  

[⬅️ Volver al README.md](README.md)
