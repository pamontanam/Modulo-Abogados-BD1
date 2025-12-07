"""
Sistema de Gestión de Casos y Expedientes
Backend con FastAPI y Oracle

NOTA: Este backend usa las tablas exactas del schema SQL en src/db/initDB.sql
Relaciones complejas manejadas mediante JOIN y subconsultas.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import oracledb
import os
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel

# ============================================================================
# CONFIGURACIÓN DE CONEXIÓN ORACLE
# ============================================================================
# Ruta al cliente instantáneo de Oracle
INSTANT_CLIENT_DIR = r"C:\oracle\instantclient_23_9"

# Inicializar cliente Oracle si existe
if os.path.isdir(INSTANT_CLIENT_DIR):
    oracledb.init_oracle_client(lib_dir=INSTANT_CLIENT_DIR)

# Credenciales de conexión (CAMBIAR CON TUS DATOS)
DB_USER = "tu_usuario"
DB_PASSWORD = "tu_contraseña"
DB_HOST = "localhost"
DB_PORT = 1521
DB_SERVICE = "XE"  # Cambia según tu servicio Oracle

# ============================================================================
# INICIALIZAR APLICACIÓN FASTAPI
# ============================================================================
app = FastAPI(title="Gestión de Casos y Expedientes", version="1.0.0")

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELOS PYDANTIC PARA VALIDACIÓN
# ============================================================================

# Modelo para Cliente - Tabla: CLIENTE
class Cliente(BaseModel):
    codCliente: Optional[str] = None
    idTipoDoc: str
    nomCliente: str
    apellCliente: str
    nDocumento: str

# Modelo para Caso - Tabla: CASO
class Caso(BaseModel):
    noCaso: Optional[int] = None
    codCliente: str
    codEspecializacion: str
    fechaInicio: date
    fechaFin: Optional[date] = None
    valor: str

# Modelo para Expediente - Tabla: EXPEDIENTE (clave compuesta)
class Expediente(BaseModel):
    codEspecializacion: str
    pasoEtapa: int
    noCaso: int
    consecExpe: Optional[int] = None
    codLugar: str
    cedula: Optional[str] = None
    fechaEtapa: date

# Modelo para Suceso - Tabla: SUCESO
class Suceso(BaseModel):
    codEspecializacion: str
    pasoEtapa: int
    noCaso: int
    consecExpe: int
    conSuceso: Optional[int] = None  # Consecutivo del suceso
    descSuceso: str

# Modelo para Resultado - Tabla: RESULTADO
class Resultado(BaseModel):
    codEspecializacion: str
    pasoEtapa: int
    noCaso: int
    consecExpe: int
    conResul: Optional[int] = None  # Consecutivo del resultado
    descResul: str

# Modelo para Documento - Tabla: DOCUMENTO
class Documento(BaseModel):
    codEspecializacion: str
    pasoEtapa: int
    noCaso: int
    consecExpe: int
    conDoc: Optional[int] = None  # Consecutivo del documento
    ubicaDoc: str

# Modelo para Especialización - Tabla: ESPECIALIZACION
class Especializacion(BaseModel):
    codEspecializacion: str
    nomEspecializacion: str

# Modelo para Abogado - Tabla: ABOGADO
class Abogado(BaseModel):
    cedula: str
    nombre: str
    apellido: str
    nTarjetaProfesional: str

# Modelo para Contacto - Tabla: CONTACTO
class Contacto(BaseModel):
    codCliente: str
    conseContacto: int
    idTipoConta: str
    valorContacto: str
    notificacion: int

# Modelo para Lugar - Tabla: LUGAR
class Lugar(BaseModel):
    codLugar: str
    lugCodLugar: Optional[str] = None
    idTipoLugar: str
    nomLugar: str
    direLugar: str
    telLugar: str
    emailLugar: Optional[str] = None

# Modelo para EtapaProcessal - Tabla: ETAPAPROCESAL
class EtapaProcessal(BaseModel):
    codEtapa: str
    nomEtapa: str

# Modelo para Especia_Etapa - Tabla: ESPECIA_ETAPA (flujo de etapas)
class EspeciaEtapa(BaseModel):
    codEspecializacion: str
    pasoEtapa: int
    idImpugna: Optional[str] = None
    codEtapa: str
    nInstancia: Optional[int] = None
    codEspecializacion: str

# ============================================================================
# FUNCIÓN PARA OBTENER CONEXIÓN A ORACLE
# ============================================================================
def get_db_connection():
    """
    Obtiene una conexión a la base de datos Oracle.
    Se usa como dependencia en los endpoints.
    """
    try:
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
        )
        return connection
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar a Oracle: {str(e)}")

# ============================================================================
# ENDPOINTS - CLIENTE
# ============================================================================

@app.get("/api/cliente/buscar/{nombre}/{apellido}")
def buscar_cliente(nombre: str, apellido: str, connection = Depends(get_db_connection)):
    """
    Busca un cliente por nombre y apellido.
    Retorna la información del cliente si existe.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT codCliente, nomCliente, apellCliente, nDocumento
            FROM Cliente
            WHERE UPPER(nomCliente) LIKE UPPER(:nombre || '%')
            AND UPPER(apellCliente) LIKE UPPER(:apellido || '%')
        """
        cursor.execute(query, {"nombre": nombre, "apellido": apellido})
        result = cursor.fetchall()
        cursor.close()
        
        if result:
            return [
                {
                    "codCliente": row[0],
                    "nomCliente": row[1],
                    "apellCliente": row[2],
                    "nDocumento": row[3]
                }
                for row in result
            ]
        else:
            return []
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda: {str(e)}")

@app.get("/api/cliente/{documento}")
def obtener_cliente_por_documento(documento: str, connection = Depends(get_db_connection)):
    """
    Obtiene información de un cliente por número de documento.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT codCliente, nomCliente, apellCliente, nDocumento
            FROM Cliente
            WHERE nDocumento = :documento
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

# ============================================================================
# ENDPOINTS - CASO
# ============================================================================

@app.get("/api/caso/ultimo/{codCliente}")
def obtener_ultimo_caso_activo(codCliente: str, connection = Depends(get_db_connection)):
    """
    Obtiene el último caso activo (sin fecha fin) del cliente.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT noCaso, fechaInicio, fechaFin, valor, codEspecializacion
            FROM Caso
            WHERE codCliente = :codCliente
            AND fechaFin IS NULL
            ORDER BY noCaso DESC
        """
        cursor.execute(query, {"codCliente": codCliente})
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                "noCaso": result[0],
                "fechaInicio": str(result[1]),
                "fechaFin": str(result[2]) if result[2] else None,
                "valor": result[3],
                "codEspecializacion": result[4]
            }
        else:
            return None
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/caso/activos/{codCliente}")
def obtener_casos_activos(codCliente: str, connection = Depends(get_db_connection)):
    """
    Obtiene todos los casos activos (sin fecha fin) del cliente.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT noCaso, fechaInicio, valor, codEspecializacion
            FROM Caso
            WHERE codCliente = :codCliente
            AND fechaFin IS NULL
            ORDER BY noCaso DESC
        """
        cursor.execute(query, {"codCliente": codCliente})
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "noCaso": row[0],
                "fechaInicio": str(row[1]),
                "valor": row[2],
                "codEspecializacion": row[3]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/caso/crear")
def crear_caso(caso: Caso, connection = Depends(get_db_connection)):
    """
    Crea un nuevo caso. Genera automáticamente el número de caso (consecutivo).
    """
    try:
        cursor = connection.cursor()
        
        # Obtener el próximo número de caso (consecutivo)
        cursor.execute("SELECT MAX(noCaso) FROM Caso")
        max_case = cursor.fetchone()[0]
        nuevo_noCaso = (max_case if max_case else 0) + 1
        
        # Insertar nuevo caso
        query = """
            INSERT INTO Caso (noCaso, fechaInicio, fechaFin, valor, codEspecializacion, codCliente)
            VALUES (:noCaso, :fechaInicio, :fechaFin, :valor, :codEspecializacion, :codCliente)
        """
        cursor.execute(query, {
            "noCaso": nuevo_noCaso,
            "fechaInicio": caso.fechaInicio,
            "fechaFin": None,  # Siempre NULL inicialmente
            "valor": caso.valor,
            "codEspecializacion": caso.codEspecializacion,
            "codCliente": caso.codCliente
        })
        connection.commit()
        cursor.close()
        
        return {
            "success": True,
            "noCaso": nuevo_noCaso,
            "mensaje": f"Caso {nuevo_noCaso} creado exitosamente"
        }
    except oracledb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear caso: {str(e)}")

@app.get("/api/caso/{noCaso}")
def obtener_caso(noCaso: int, connection = Depends(get_db_connection)):
    """
    Obtiene información de un caso específico.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT noCaso, fechaInicio, fechaFin, valor, codEspecializacion, codCliente
            FROM Caso
            WHERE noCaso = :noCaso
        """
        cursor.execute(query, {"noCaso": noCaso})
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                "noCaso": result[0],
                "fechaInicio": str(result[1]),
                "fechaFin": str(result[2]) if result[2] else None,
                "valor": result[3],
                "codEspecializacion": result[4],
                "codCliente": result[5]
            }
        else:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.put("/api/caso/{noCaso}")
def actualizar_caso(noCaso: int, caso: Caso, connection = Depends(get_db_connection)):
    """
    Actualiza un caso existente (solo si no tiene fecha fin).
    """
    try:
        cursor = connection.cursor()
        
        # Verificar si el caso existe y no tiene fecha fin
        cursor.execute(
            "SELECT fechaFin FROM Caso WHERE noCaso = :noCaso",
            {"noCaso": noCaso}
        )
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
        
        if result[0] is not None:
            raise HTTPException(status_code=400, detail="No se puede actualizar un caso cerrado (con fecha fin)")
        
        # Actualizar caso
        query = """
            UPDATE Caso
            SET fechaInicio = :fechaInicio,
                valor = :valor,
                codEspecializacion = :codEspecializacion
            WHERE noCaso = :noCaso
        """
        cursor.execute(query, {
            "noCaso": noCaso,
            "fechaInicio": caso.fechaInicio,
            "valor": caso.valor,
            "codEspecializacion": caso.codEspecializacion
        })
        connection.commit()
        cursor.close()
        
        return {"success": True, "mensaje": f"Caso {noCaso} actualizado"}
    except oracledb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - EXPEDIENTE Y ETAPA
# ============================================================================

@app.get("/api/expediente/caso/{noCaso}")
def obtener_expedientes_caso(noCaso: int, connection = Depends(get_db_connection)):
    """
    Obtiene todos los expedientes de un caso específico.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT consecExpe, noCaso, fechaEtapa
            FROM Expediente
            WHERE noCaso = :noCaso
            ORDER BY consecExpe
        """
        cursor.execute(query, {"noCaso": noCaso})
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "consecExpe": row[0],
                "noCaso": row[1],
                "fechaEtapa": str(row[2])
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/expediente/{codEsp}/{pasoEtapa}/{noCaso}/{consecExpe}")
def obtener_expediente_detalle(codEsp: str, pasoEtapa: int, noCaso: int, consecExpe: int, connection = Depends(get_db_connection)):
    """
    Obtiene los detalles completos de un expediente usando su clave compuesta.
    Clave: (codEspecializacion, pasoEtapa, noCaso, consecExpe)
    """
    try:
        cursor = connection.cursor()
        
        # Obtener datos del expediente con clave compuesta
        query = """
            SELECT e.codEspecializacion, e.pasoEtapa, e.noCaso, e.consecExpe,
                   e.codLugar, e.cedula, e.fechaEtapa,
                   et.nomEtapa, l.nomLugar, ee.idImpugna, ee.nInstancia
            FROM Expediente e
            LEFT JOIN EtapaProcesal et ON e.codEtapa = et.codEtapa
            LEFT JOIN Lugar l ON e.codLugar = l.codLugar
            LEFT JOIN Especia_Etapa ee ON e.codEspecializacion = ee.codEspecializacion 
                                       AND e.pasoEtapa = ee.pasoEtapa
            WHERE e.codEspecializacion = :codEsp
            AND e.pasoEtapa = :pasoEtapa
            AND e.noCaso = :noCaso
            AND e.consecExpe = :consecExpe
        """
        cursor.execute(query, {
            "codEsp": codEsp,
            "pasoEtapa": pasoEtapa,
            "noCaso": noCaso,
            "consecExpe": consecExpe
        })
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            # Obtener sucesos, resultados y documentos del expediente
            cursor = connection.cursor()
            
            # Obtener sucesos
            cursor.execute("""
                SELECT conSuceso, descSuceso FROM Suceso
                WHERE codEspecializacion = :codEsp
                AND pasoEtapa = :pasoEtapa
                AND noCaso = :noCaso
                AND consecExpe = :consecExpe
            """, {"codEsp": codEsp, "pasoEtapa": pasoEtapa, "noCaso": noCaso, "consecExpe": consecExpe})
            sucesos = [{"conSuceso": row[0], "descSuceso": row[1]} for row in cursor.fetchall()]
            
            # Obtener resultados
            cursor.execute("""
                SELECT conResul, descResul FROM Resultado
                WHERE codEspecializacion = :codEsp
                AND pasoEtapa = :pasoEtapa
                AND noCaso = :noCaso
                AND consecExpe = :consecExpe
            """, {"codEsp": codEsp, "pasoEtapa": pasoEtapa, "noCaso": noCaso, "consecExpe": consecExpe})
            resultados = [{"conResul": row[0], "descResul": row[1]} for row in cursor.fetchall()]
            
            # Obtener documentos
            cursor.execute("""
                SELECT conDoc, ubicaDoc FROM Documento
                WHERE codEspecializacion = :codEsp
                AND pasoEtapa = :pasoEtapa
                AND noCaso = :noCaso
                AND consecExpe = :consecExpe
            """, {"codEsp": codEsp, "pasoEtapa": pasoEtapa, "noCaso": noCaso, "consecExpe": consecExpe})
            documentos = [{"conDoc": row[0], "ubicaDoc": row[1]} for row in cursor.fetchall()]
            cursor.close()
            
            return {
                "codEspecializacion": result[0],
                "pasoEtapa": result[1],
                "noCaso": result[2],
                "consecExpe": result[3],
                "codLugar": result[4],
                "cedula": result[5],
                "fechaEtapa": str(result[6]),
                "nomEtapa": result[7],
                "nomLugar": result[8],
                "idImpugna": result[9],
                "nInstancia": result[10],
                "sucesos": sucesos,
                "resultados": resultados,
                "documentos": documentos
            }
        else:
            raise HTTPException(status_code=404, detail="Expediente no encontrado")
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/expediente/crear")
def crear_expediente(expediente: Expediente, connection = Depends(get_db_connection)):
    """
    Crea un nuevo expediente para un caso. Genera número de expediente (consecutivo).
    La primera etapa es determinada por la especialización del caso.
    """
    try:
        cursor = connection.cursor()
        
        # Obtener el próximo número de expediente
        cursor.execute("SELECT MAX(consecExpe) FROM Expediente")
        max_exp = cursor.fetchone()[0]
        nuevo_consecExpe = (max_exp if max_exp else 0) + 1
        
        # Obtener especialización del caso
        cursor.execute(
            "SELECT codEspecializacion FROM Caso WHERE noCaso = :noCaso",
            {"noCaso": expediente.noCaso}
        )
        esp_result = cursor.fetchone()
        
        if not esp_result:
            raise HTTPException(status_code=404, detail="Caso no encontrado")
        
        # Obtener la primera etapa para la especialización (por defecto, etapa 1)
        # Esto depende de tu estructura. Asumiendo que la etapa inicial es siempre 1
        primera_etapa = "1"  # O obtener dinámicamente según especialización
        
        # Insertar expediente
        query = """
            INSERT INTO Expediente (consecExpe, noCaso, codEtapa, fechaEtapa)
            VALUES (:consecExpe, :noCaso, :codEtapa, :fechaEtapa)
        """
        cursor.execute(query, {
            "consecExpe": nuevo_consecExpe,
            "noCaso": expediente.noCaso,
            "codEtapa": primera_etapa,
            "fechaEtapa": expediente.fechaEtapa
        })
        connection.commit()
        cursor.close()
        
        return {
            "success": True,
            "consecExpe": nuevo_consecExpe,
            "mensaje": f"Expediente {nuevo_consecExpe} creado exitosamente"
        }
    except oracledb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear expediente: {str(e)}")

@app.put("/api/expediente/{consecExpe}")
def actualizar_etapa_expediente(consecExpe: int, etapa: Expediente, connection = Depends(get_db_connection)):
    """
    Actualiza los datos de una etapa del expediente.
    """
    try:
        cursor = connection.cursor()
        
        # Actualizar expediente con datos de lugar y abogado
        query = """
            UPDATE Expediente
            SET codLugar = :codLugar,
                cedula = :cedula,
                fechaEtapa = :fechaEtapa
            WHERE codEspecializacion = :codEsp
            AND pasoEtapa = :pasoEtapa
            AND noCaso = :noCaso
            AND consecExpe = :consecExpe
        """
        cursor.execute(query, {
            "codEsp": etapa.codEspecializacion,
            "pasoEtapa": etapa.pasoEtapa,
            "noCaso": etapa.noCaso,
            "consecExpe": etapa.consecExpe,
            "codLugar": etapa.codLugar,
            "cedula": etapa.cedula,
            "fechaEtapa": etapa.fechaEtapa
        })
        connection.commit()
        cursor.close()
        
        return {"success": True, "mensaje": f"Expediente {etapa.consecExpe} actualizado"}
    except oracledb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - SUCESO
# ============================================================================

@app.post("/api/suceso/crear")
def crear_suceso(suceso: Suceso, connection = Depends(get_db_connection)):
    """
    Crea un nuevo suceso en un expediente.
    Clave compuesta: (codEspecializacion, pasoEtapa, noCaso, consecExpe, conSuceso)
    """
    try:
        cursor = connection.cursor()
        
        # Obtener el próximo número de suceso para este expediente
        cursor.execute("""
            SELECT MAX(conSuceso) FROM Suceso
            WHERE codEspecializacion = :codEsp
            AND pasoEtapa = :pasoEtapa
            AND noCaso = :noCaso
            AND consecExpe = :consecExpe
        """, {
            "codEsp": suceso.codEspecializacion,
            "pasoEtapa": suceso.pasoEtapa,
            "noCaso": suceso.noCaso,
            "consecExpe": suceso.consecExpe
        })
        max_suceso = cursor.fetchone()[0]
        nuevo_conSuceso = (max_suceso if max_suceso else 0) + 1
        
        # Insertar suceso
        query = """
            INSERT INTO Suceso (codEspecializacion, pasoEtapa, noCaso, consecExpe, conSuceso, descSuceso)
            VALUES (:codEsp, :pasoEtapa, :noCaso, :consecExpe, :conSuceso, :descSuceso)
        """
        cursor.execute(query, {
            "codEsp": suceso.codEspecializacion,
            "pasoEtapa": suceso.pasoEtapa,
            "noCaso": suceso.noCaso,
            "consecExpe": suceso.consecExpe,
            "conSuceso": nuevo_conSuceso,
            "descSuceso": suceso.descSuceso
        })
        connection.commit()
        cursor.close()
        
        return {
            "success": True,
            "conSuceso": nuevo_conSuceso,
            "mensaje": "Suceso creado exitosamente"
        }
    except oracledb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear suceso: {str(e)}")

@app.get("/api/suceso/{codEsp}/{pasoEtapa}/{noCaso}/{consecExpe}")
def obtener_sucesos_expediente(codEsp: str, pasoEtapa: int, noCaso: int, consecExpe: int, connection = Depends(get_db_connection)):
    """
    Obtiene todos los sucesos de un expediente específico.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT conSuceso, descSuceso
            FROM Suceso
            WHERE codEspecializacion = :codEsp
            AND pasoEtapa = :pasoEtapa
            AND noCaso = :noCaso
            AND consecExpe = :consecExpe
            ORDER BY conSuceso
        """
        cursor.execute(query, {
            "codEsp": codEsp,
            "pasoEtapa": pasoEtapa,
            "noCaso": noCaso,
            "consecExpe": consecExpe
        })
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "conSuceso": row[0],
                "descSuceso": row[1]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - RESULTADO
# ============================================================================

@app.post("/api/resultado/crear")
def crear_resultado(resultado: Resultado, connection = Depends(get_db_connection)):
    """
    Crea un nuevo resultado en un expediente.
    Clave compuesta: (codEspecializacion, pasoEtapa, noCaso, consecExpe, conResul)
    """
    try:
        cursor = connection.cursor()
        
        # Obtener el próximo número de resultado
        cursor.execute("""
            SELECT MAX(conResul) FROM Resultado
            WHERE codEspecializacion = :codEsp
            AND pasoEtapa = :pasoEtapa
            AND noCaso = :noCaso
            AND consecExpe = :consecExpe
        """, {
            "codEsp": resultado.codEspecializacion,
            "pasoEtapa": resultado.pasoEtapa,
            "noCaso": resultado.noCaso,
            "consecExpe": resultado.consecExpe
        })
        max_resultado = cursor.fetchone()[0]
        nuevo_conResul = (max_resultado if max_resultado else 0) + 1
        
        # Insertar resultado
        query = """
            INSERT INTO Resultado (codEspecializacion, pasoEtapa, noCaso, consecExpe, conResul, descResul)
            VALUES (:codEsp, :pasoEtapa, :noCaso, :consecExpe, :conResul, :descResul)
        """
        cursor.execute(query, {
            "codEsp": resultado.codEspecializacion,
            "pasoEtapa": resultado.pasoEtapa,
            "noCaso": resultado.noCaso,
            "consecExpe": resultado.consecExpe,
            "conResul": nuevo_conResul,
            "descResul": resultado.descResul
        })
        connection.commit()
        cursor.close()
        
        return {
            "success": True,
            "conResul": nuevo_conResul,
            "mensaje": "Resultado creado exitosamente"
        }
    except oracledb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear resultado: {str(e)}")

@app.get("/api/resultado/{codEsp}/{pasoEtapa}/{noCaso}/{consecExpe}")
def obtener_resultados_expediente(codEsp: str, pasoEtapa: int, noCaso: int, consecExpe: int, connection = Depends(get_db_connection)):
    """
    Obtiene todos los resultados de un expediente específico.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT conResul, descResul
            FROM Resultado
            WHERE codEspecializacion = :codEsp
            AND pasoEtapa = :pasoEtapa
            AND noCaso = :noCaso
            AND consecExpe = :consecExpe
            ORDER BY conResul
        """
        cursor.execute(query, {
            "codEsp": codEsp,
            "pasoEtapa": pasoEtapa,
            "noCaso": noCaso,
            "consecExpe": consecExpe
        })
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "conResul": row[0],
                "descResul": row[1]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - DOCUMENTO
# ============================================================================

@app.post("/api/documento/crear")
def crear_documento(documento: Documento, connection = Depends(get_db_connection)):
    """
    Crea un nuevo documento en un expediente.
    Clave compuesta: (codEspecializacion, pasoEtapa, noCaso, consecExpe, conDoc)
    """
    try:
        cursor = connection.cursor()
        
        # Obtener el próximo número de documento
        cursor.execute("""
            SELECT MAX(conDoc) FROM Documento
            WHERE codEspecializacion = :codEsp
            AND pasoEtapa = :pasoEtapa
            AND noCaso = :noCaso
            AND consecExpe = :consecExpe
        """, {
            "codEsp": documento.codEspecializacion,
            "pasoEtapa": documento.pasoEtapa,
            "noCaso": documento.noCaso,
            "consecExpe": documento.consecExpe
        })
        max_doc = cursor.fetchone()[0]
        nuevo_conDoc = (max_doc if max_doc else 0) + 1
        
        # Insertar documento
        query = """
            INSERT INTO Documento (codEspecializacion, pasoEtapa, noCaso, consecExpe, conDoc, ubicaDoc)
            VALUES (:codEsp, :pasoEtapa, :noCaso, :consecExpe, :conDoc, :ubicaDoc)
        """
        cursor.execute(query, {
            "codEsp": documento.codEspecializacion,
            "pasoEtapa": documento.pasoEtapa,
            "noCaso": documento.noCaso,
            "consecExpe": documento.consecExpe,
            "conDoc": nuevo_conDoc,
            "ubicaDoc": documento.ubicaDoc
        })
        connection.commit()
        cursor.close()
        
        return {
            "success": True,
            "conDoc": nuevo_conDoc,
            "mensaje": "Documento creado exitosamente"
        }
    except oracledb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear documento: {str(e)}")

@app.get("/api/documento/{codEsp}/{pasoEtapa}/{noCaso}/{consecExpe}")
def obtener_documentos_expediente(codEsp: str, pasoEtapa: int, noCaso: int, consecExpe: int, connection = Depends(get_db_connection)):
    """
    Obtiene todos los documentos de un expediente específico.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT conDoc, ubicaDoc
            FROM Documento
            WHERE codEspecializacion = :codEsp
            AND pasoEtapa = :pasoEtapa
            AND noCaso = :noCaso
            AND consecExpe = :consecExpe
            ORDER BY conDoc
        """
        cursor.execute(query, {
            "codEsp": codEsp,
            "pasoEtapa": pasoEtapa,
            "noCaso": noCaso,
            "consecExpe": consecExpe
        })
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "conDoc": row[0],
                "ubicaDoc": row[1]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - ESPECIALIZACIÓN
# ============================================================================

@app.get("/api/especializacion/")
def obtener_especializaciones(connection = Depends(get_db_connection)):
    """
    Obtiene todas las especializaciones disponibles.
    """
    try:
        cursor = connection.cursor()
        query = "SELECT codEspecializacion, nomEspecializacion FROM Especializacion"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "codEspecializacion": row[0],
                "nomEspecializacion": row[1]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - ABOGADO
# ============================================================================

@app.get("/api/abogado/especializacion/{codEspecializacion}")
def obtener_abogados_especializacion(codEspecializacion: str, connection = Depends(get_db_connection)):
    """
    Obtiene todos los abogados con una especialización específica.
    Usa la tabla ESPECIALIZACION_ABOGADO para la relación.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT a.cedula, a.nombre, a.apellido, a.nTarjetaProfesional
            FROM Abogado a
            INNER JOIN Especializacion_Abogado ea ON a.cedula = ea.cedula
            WHERE ea.codEspecializacion = :codEsp
            ORDER BY a.apellido, a.nombre
        """
        cursor.execute(query, {"codEsp": codEspecializacion})
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "cedula": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "nTarjetaProfesional": row[3]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - LUGAR
# ============================================================================

@app.get("/api/lugar/ciudades")
def obtener_ciudades(connection = Depends(get_db_connection)):
    """
    Obtiene todas las ciudades (lugares raíz sin lugCodLugar).
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT codLugar, nomLugar, direLugar, telLugar
            FROM Lugar
            WHERE lugCodLugar IS NULL
            AND idTipoLugar = 'CIUDAD'
            ORDER BY nomLugar
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "codLugar": row[0],
                "nomLugar": row[1],
                "direLugar": row[2],
                "telLugar": row[3]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/lugar/entidades/{codCiudad}")
def obtener_entidades_por_ciudad(codCiudad: str, connection = Depends(get_db_connection)):
    """
    Obtiene todas las entidades (juzgados, tribunales, etc.) de una ciudad.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT codLugar, nomLugar, direLugar, telLugar, idTipoLugar
            FROM Lugar
            WHERE lugCodLugar = :codCiudad
            ORDER BY nomLugar
        """
        cursor.execute(query, {"codCiudad": codCiudad})
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "codLugar": row[0],
                "nomLugar": row[1],
                "direLugar": row[2],
                "telLugar": row[3],
                "idTipoLugar": row[4]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/lugar/{codLugar}")
def obtener_lugar(codLugar: str, connection = Depends(get_db_connection)):
    """
    Obtiene detalles de un lugar específico.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT codLugar, lugCodLugar, idTipoLugar, nomLugar, direLugar, telLugar, emailLugar
            FROM Lugar
            WHERE codLugar = :codLugar
        """
        cursor.execute(query, {"codLugar": codLugar})
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                "codLugar": result[0],
                "lugCodLugar": result[1],
                "idTipoLugar": result[2],
                "nomLugar": result[3],
                "direLugar": result[4],
                "telLugar": result[5],
                "emailLugar": result[6]
            }
        else:
            raise HTTPException(status_code=404, detail="Lugar no encontrado")
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# ENDPOINTS - ESPECIA_ETAPA (Workflow de etapas por especialización)
# ============================================================================

@app.get("/api/especia-etapa/{codEspecializacion}")
def obtener_etapas_especializacion(codEspecializacion: str, connection = Depends(get_db_connection)):
    """
    Obtiene todas las etapas del flujo de trabajo para una especialización.
    Muestra las etapas en orden secuencial.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT ee.pasoEtapa, ee.codEtapa, et.nomEtapa, 
                   ee.idImpugna, ee.nInstancia, ee.codEspecializacion
            FROM Especia_Etapa ee
            INNER JOIN EtapaProcesal et ON ee.codEtapa = et.codEtapa
            WHERE ee.codEspecializacion = :codEsp
            ORDER BY ee.pasoEtapa
        """
        cursor.execute(query, {"codEsp": codEspecializacion})
        results = cursor.fetchall()
        cursor.close()
        
        return [
            {
                "pasoEtapa": row[0],
                "codEtapa": row[1],
                "nomEtapa": row[2],
                "idImpugna": row[3],
                "nInstancia": row[4],
                "codEspecializacion": row[5]
            }
            for row in results
        ]
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/especia-etapa/{codEspecializacion}/{pasoEtapa}")
def obtener_etapa_especifica(codEspecializacion: str, pasoEtapa: int, connection = Depends(get_db_connection)):
    """
    Obtiene los detalles de una etapa específica en el flujo de una especialización.
    """
    try:
        cursor = connection.cursor()
        query = """
            SELECT ee.pasoEtapa, ee.codEtapa, et.nomEtapa, 
                   ee.idImpugna, ee.nInstancia
            FROM Especia_Etapa ee
            INNER JOIN EtapaProcesal et ON ee.codEtapa = et.codEtapa
            WHERE ee.codEspecializacion = :codEsp
            AND ee.pasoEtapa = :pasoEtapa
        """
        cursor.execute(query, {
            "codEsp": codEspecializacion,
            "pasoEtapa": pasoEtapa
        })
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {
                "pasoEtapa": result[0],
                "codEtapa": result[1],
                "nomEtapa": result[2],
                "idImpugna": result[3],
                "nInstancia": result[4]
            }
        else:
            raise HTTPException(status_code=404, detail="Etapa no encontrada")
    except oracledb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/health")
def health_check():
    """
    Verifica que la API está funcionando.
    """
    return {"status": "ok", "mensaje": "API de Gestión de Casos funcionando"}

# ============================================================================
# ENDPOINT RAÍZ
# ============================================================================

@app.get("/")
def root():
    """
    Endpoint raíz de bienvenida.
    """
    return {
        "mensaje": "Bienvenido al Sistema de Gestión de Casos y Expedientes",
        "documentación": "http://localhost:8000/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
