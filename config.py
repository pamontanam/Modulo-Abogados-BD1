"""
Script de Configuración Inicial
Sistema de Gestión de Casos y Expedientes

Este script verifica todos los requisitos previos y ayuda
a configurar el entorno para ejecutar el sistema.
"""

import os
import sys
import subprocess
import platform

# Colores para terminal
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
RESET = "\033[0m"


def verificar_sistema():
    """Verifica que el sistema operativo es Windows"""
    print(f"\n{AMARILLO}[*] Verificando sistema operativo...{RESET}")
    
    if platform.system() != "Windows":
        print(f"{ROJO}[✗] Este script está diseñado para Windows{RESET}")
        return False
    
    print(f"{VERDE}[✓] Sistema operativo: Windows{RESET}")
    return True


def verificar_python():
    """Verifica que Python 3.9+ está instalado"""
    print(f"\n{AMARILLO}[*] Verificando Python...{RESET}")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"{ROJO}[✗] Python 3.9+ requerido (tienes {version.major}.{version.minor}){RESET}")
        return False
    
    print(f"{VERDE}[✓] Python {version.major}.{version.minor}.{version.micro} detectado{RESET}")
    return True


def verificar_oracle_client():
    """Verifica que Oracle Instant Client está instalado"""
    print(f"\n{AMARILLO}[*] Verificando Oracle Instant Client...{RESET}")
    
    paths = [
        r"C:\oracle\instantclient_23_9",
        r"C:\oracle\instantclient_21_13",
    ]
    
    for path in paths:
        if os.path.isdir(path):
            print(f"{VERDE}[✓] Oracle Instant Client encontrado en: {path}{RESET}")
            return True
    
    print(f"{ROJO}[✗] Oracle Instant Client NO encontrado{RESET}")
    print(f"    Descargar de: https://www.oracle.com/database/technologies/instant-client/")
    print(f"    Instalar en: C:\\oracle\\instantclient_23_9")
    return False


def crear_venv():
    """Crea un entorno virtual Python"""
    print(f"\n{AMARILLO}[*] Creando entorno virtual...{RESET}")
    
    venv_path = os.path.join("src", "backend", "venv")
    
    if os.path.exists(venv_path):
        print(f"{VERDE}[✓] Entorno virtual ya existe{RESET}")
        return True
    
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print(f"{VERDE}[✓] Entorno virtual creado en: {venv_path}{RESET}")
        return True
    except Exception as e:
        print(f"{ROJO}[✗] Error al crear entorno virtual: {e}{RESET}")
        return False


def instalar_dependencias():
    """Instala las dependencias Python"""
    print(f"\n{AMARILLO}[*] Instalando dependencias...{RESET}")
    
    venv_python = os.path.join("src", "backend", "venv", "Scripts", "python.exe")
    requirements = os.path.join("src", "backend", "requirements.txt")
    
    if not os.path.exists(venv_python):
        print(f"{ROJO}[✗] Python del entorno virtual no encontrado{RESET}")
        return False
    
    if not os.path.exists(requirements):
        print(f"{ROJO}[✗] archivo requirements.txt no encontrado{RESET}")
        return False
    
    try:
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", requirements])
        print(f"{VERDE}[✓] Dependencias instaladas correctamente{RESET}")
        return True
    except Exception as e:
        print(f"{ROJO}[✗] Error al instalar dependencias: {e}{RESET}")
        return False


def verificar_archivos():
    """Verifica que todos los archivos necesarios existen"""
    print(f"\n{AMARILLO}[*] Verificando archivos del proyecto...{RESET}")
    
    archivos_necesarios = [
        "src/backend/main.py",
        "src/backend/requirements.txt",
        "src/frontend/index.html",
        "src/frontend/styles.css",
        "src/frontend/script.js",
        "src/db/initDB.sql",
        "src/db/inserts.sql",
    ]
    
    todos_existen = True
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"{VERDE}[✓] {archivo}{RESET}")
        else:
            print(f"{ROJO}[✗] {archivo} NO ENCONTRADO{RESET}")
            todos_existen = False
    
    return todos_existen


def main():
    """Función principal"""
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║   Sistema de Gestión de Casos y Expedientes - Configuración   ║
║                      Gabinete de Abogados                     ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Lista de verificaciones
    verificaciones = [
        ("Sistema Operativo", verificar_sistema),
        ("Python", verificar_python),
        ("Oracle Instant Client", verificar_oracle_client),
        ("Archivos del Proyecto", verificar_archivos),
    ]
    
    resultados = {}
    for nombre, verificacion in verificaciones:
        resultados[nombre] = verificacion()
    
    # Resumen
    print(f"\n{AMARILLO}{'='*60}{RESET}")
    print(f"{AMARILLO}RESUMEN DE VERIFICACIONES:{RESET}")
    print(f"{AMARILLO}{'='*60}{RESET}")
    
    todas_ok = True
    for nombre, resultado in resultados.items():
        estado = f"{VERDE}✓ OK{RESET}" if resultado else f"{ROJO}✗ ERROR{RESET}"
        print(f"{nombre:.<40} {estado}")
        if not resultado:
            todas_ok = False
    
    print(f"{AMARILLO}{'='*60}{RESET}\n")
    
    if not todas_ok:
        print(f"{ROJO}[!] Algunas verificaciones fallaron. Por favor revisar arriba.{RESET}")
        sys.exit(1)
    
    # Instalar dependencias
    print(f"\n{AMARILLO}[*] Procediendoo con la instalación...{RESET}")
    crear_venv()
    instalar_dependencias()
    
    # Instrucciones finales
    print(f"\n{VERDE}{'='*60}{RESET}")
    print(f"{VERDE}¡INSTALACIÓN COMPLETADA!{RESET}")
    print(f"{VERDE}{'='*60}{RESET}\n")
    
    print(f"""
{VERDE}Próximos pasos:{RESET}

1. Configurar credenciales de Oracle:
   → Abrir: src\\backend\\main.py
   → Buscar: "CONFIGURACIÓN DE CONEXIÓN ORACLE"
   → Cambiar DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SERVICE

2. Ejecutar scripts de BD en Oracle:
   SQL> @src/db/initDB.sql
   SQL> @src/db/inserts.sql

3. Iniciar el sistema:
   → Ejecutar: iniciar.bat (o ver README.md para instrucciones detalladas)
   → Abrir navegador en: http://localhost:8001

{AMARILLO}Documentación completa en: README.md{RESET}
{AMARILLO}Contacto: equipo.desarrollo@universidad.edu{RESET}
    """)


if __name__ == "__main__":
    main()
