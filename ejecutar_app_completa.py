#!/usr/bin/env python3
"""
Script de ejecución para la aplicación completa del analizador de rendimiento.
Incluye todas las funcionalidades avanzadas con interfaz Rich.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analizador_rendimiento'))

try:
    from analizador_rendimiento.terminal_app import main
    
    if __name__ == "__main__":
        print("🚀 Iniciando Analizador de Rendimiento COMPLETO...")
        print("✨ Interfaz avanzada con Rich - Todas las funcionalidades")
        print("💡 Usa Ctrl+C para salir en cualquier momento")
        print("-" * 60)
        main()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("📁 Verifica que estés en el directorio correcto del proyecto")
    print("📦 Asegúrate de tener instaladas las dependencias: pip install -r requirements.txt")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n👋 ¡Hasta luego! Aplicación cerrada por el usuario.")
    sys.exit(0)
except Exception as e:
    print(f"💥 Error inesperado: {e}")
    sys.exit(1) 