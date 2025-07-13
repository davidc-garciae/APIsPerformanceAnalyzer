#!/usr/bin/env python3
"""
Script de ejecución para el monitor de APIs
Lanza la interfaz especializada para analizar el rendimiento de APIs REST
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analizador_rendimiento'))

try:
    from analizador_rendimiento.api_monitor_app import main
    
    if __name__ == "__main__":
        print("🌐 Iniciando Monitor de APIs...")
        print("🔍 Especializado en análisis de rendimiento de APIs REST")
        print("🐱 Incluye tests específicos para PokéAPI")
        print("💡 Usa Ctrl+C para salir en cualquier momento")
        print("-" * 60)
        main()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("📁 Verifica que estés en el directorio correcto del proyecto")
    print("📦 Instala las dependencias: pip install -r requirements.txt")
    print("💡 Nueva dependencia requerida: aiohttp")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n👋 ¡Hasta luego! Monitor de APIs cerrado por el usuario.")
    sys.exit(0)
except Exception as e:
    print(f"💥 Error inesperado: {e}")
    sys.exit(1) 