#!/usr/bin/env python3
"""
Script de ejecución para la Aplicación de Ejemplo
Punto de entrada unificado para la aplicación de monitoreo de rendimiento
"""

import sys
import os

# Agregar el directorio de la aplicación al path
sys.path.append(os.path.join(os.path.dirname(__file__), "app_ejemplo"))

from app_ejemplo.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1) 