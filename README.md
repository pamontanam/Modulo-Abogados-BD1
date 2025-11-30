# Gabinete de Abogados – Proyecto de Base de Datos

Proyecto académico para el diseño e implementación de la base de datos de un **gabinete de abogados**, incluyendo modelado conceptual, lógico y físico, así como los scripts SQL para creación e inserción de datos en Oracle 12c.

## Contenido del repositorio

- `doc/`
  - Documentación general del módulo/proyecto (apuntes, entregables, etc.).
- `gabinete_abogados_powerdesigner/`
  - `Conceptual.cdm` / `Conceptual.cdb`: modelo conceptual del dominio (gabinete de abogados).
  - `Logico.ldm`: modelo lógico de datos.
  - `Fisico.pdm`: modelo físico de la base de datos.
  - Archivos de proyecto de PowerDesigner (`*.pjb`, `*.prj`).
- `src/`
  - `db/`
    - `initDB.sql`: script de **creación y reseteo** de la base de datos en Oracle 12c. Incluye:
      - Eliminación de restricciones y tablas existentes (si las hay).
      - Creación de tablas principales: `ABOGADO`, `CLIENTE`, `CASO`, `EXPEDIENTE`, `LUGAR`, `PAGO`, `RESULTADO`, `SUCESO`, `ESPECIALIZACION`, `ETAPAPROCESAL`, `ESPECIA_ETAPA`, `TIPODOCUMENTO`, `TIPOCONTACT`, `TIPOLUGAR`, `FORMAPAGO`, `FRANQUICIA`, `IMPUGNACION`, `INSTANCIA`, entre otras.
      - Creación de índices y restricciones de integridad (claves primarias y foráneas).
    - `inserts.sql`: script de **carga de datos de ejemplo**, que inserta registros en:
      - Tablas de catálogos: `TIPOCONTACT`, `TIPODOCUMENTO`, `TIPOLUGAR`, `FORMAPAGO`, `FRANQUICIA`, `ESPECIALIZACION`, `ETAPAPROCESAL`, `IMPUGNACION`, `INSTANCIA`.
      - Tabla de relación de etapas por especialización: `ESPECIA_ETAPA` (flujos procesales por tipo de caso: civil, penal, laboral).
      - Tablas de negocio: `ABOGADO`, `CLIENTE`, `LUGAR` (ciudades, juzgados, tribunales) y otros datos base para casos/expedientes.
  - `backend/` y `frontend/`
    - Directorios reservados para futuras implementaciones de backend y frontend (actualmente sólo contienen archivos de ejemplo).

## Objetivo del modelo

La base de datos modela la operación de un gabinete de abogados, permitiendo registrar:

- **Abogados** y sus especializaciones.
- **Clientes** y sus datos de contacto.
- **Casos** asociados a clientes y especialidades del derecho.
- **Expedientes** vinculados a casos, abogados, lugares (juzgados/tribunales) y resultados.
- **Pagos** y formas de pago (incluyendo franquicias de tarjetas).
- **Etapas procesales** e **instancias** del proceso judicial, con posibles recursos de impugnación.
- **Lugares** jerárquicos (ciudad → juzgado/tribunal).

## Requisitos

- **DBMS**: Oracle Database 12c (o compatible).
- Usuario con permisos para crear y eliminar tablas, índices y restricciones en el esquema de trabajo.
- Cliente SQL (SQL*Plus, SQL Developer, DBeaver, etc.).

## Instrucciones de uso

1. Conectarse a la base de datos Oracle 12c con el usuario/esquema deseado.
2. Ejecutar el script de inicialización de esquema:

   ```sql
   @src/db/initDB.sql
   ```

3. Ejecutar el script de inserción de datos de ejemplo:

   ```sql
   @src/db/inserts.sql
   ```

4. Verificar las tablas y datos, por ejemplo:

   ```sql
   SELECT * FROM ABOGADO;
   SELECT * FROM CLIENTE;
   SELECT * FROM CASO;
   ```

## Estructura lógica principal

A alto nivel, el modelo incluye:

- `ABOGADO` ↔ `ESPECIALIZACION` (por `ESPECIALIZACION_ABOGADO`).
- `CLIENTE` ↔ `CASO` ↔ `EXPEDIENTE`.
- `EXPEDIENTE` ↔ `LUGAR` (juzgado/tribunal) y `RESULTADO`.
- `PAGO` asociado a `FORMAPAGO` y `FRANQUICIA`.
- Flujos procesales por especialidad en `ESPECIA_ETAPA`, vinculando `ESPECIALIZACION`, `ETAPAPROCESAL`, `IMPUGNACION` e `INSTANCIA`.

## Trabajo futuro

- Implementar capa de **backend** (APIs) para gestionar casos, clientes y expedientes.
- Implementar interfaz **frontend** para consulta y administración de la información.
- Añadir scripts adicionales de **consultas, vistas, procedimientos almacenados** y casos de prueba.

## Autores

- Proyecto desarrollado como parte del módulo de **Bases de Datos I** (Gabinete de Abogados).