#!/usr/bin/env python3
"""
Aplicación de Ejemplo para Monitoreo de Rendimiento
Archivo principal que permite elegir entre interfaz de consola y web
"""

import sys
import os
from typing import Optional

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaces.consola import InterfazConsola
from interfaces.web import main as web_main


def mostrar_menu_principal():
    """Muestra el menú para elegir interfaz"""
    print("\n" + "="*70)
    print("🔧 APLICACIÓN DE EJEMPLO PARA MONITOREO DE RENDIMIENTO")
    print("="*70)
    print("Seleccione la interfaz que desea usar:")
    print()
    print("1. 💻 Interfaz de Consola (Menú interactivo)")
    print("2. 🌐 Interfaz Web (Servidor FastAPI)")
    print("3. ❓ Ayuda")
    print("0. ❌ Salir")
    print("="*70)


def mostrar_ayuda():
    """Muestra información de ayuda"""
    print("\n📖 AYUDA - APLICACIÓN DE EJEMPLO")
    print("="*50)
    print("Esta aplicación contiene operaciones deliberadamente ineficientes")
    print("para demostrar el monitoreo de rendimiento y análisis de código.")
    print()
    print("🎯 PROPÓSITO:")
    print("- Generar carga de trabajo para probar analizadores de rendimiento")
    print("- Demostrar diferentes tipos de operaciones intensivas")
    print("- Proporcionar métricas de rendimiento en tiempo real")
    print()
    print("💻 INTERFAZ DE CONSOLA:")
    print("- Menú interactivo con 12 opciones")
    print("- Ejecución paso a paso de operaciones")
    print("- Visualización de resultados en tiempo real")
    print("- Generación de reportes HTML")
    print()
    print("🌐 INTERFAZ WEB:")
    print("- Servidor FastAPI en http://localhost:8000")
    print("- Interfaz web moderna y responsiva")
    print("- API REST documentada en /docs")
    print("- Métricas del sistema en tiempo real")
    print()
    print("🔥 OPERACIONES DISPONIBLES:")
    print("- CPU Intensiva: Cálculos matemáticos complejos")
    print("- Memoria Intensiva: Creación de grandes estructuras de datos")
    print("- E/S Intensiva: Operaciones de lectura/escritura de archivos")
    print("- Fibonacci Recursivo: Algoritmo recursivo ineficiente")
    print("- Multithreading: Operaciones con múltiples hilos")
    print("- Memory Leak: Simulación de fuga de memoria")
    print("- Operación Lenta: Esperas deliberadas")
    print("- Benchmark Completo: Ejecuta todas las operaciones")
    print()
    print("📊 MONITOREO:")
    print("- CPU: Porcentaje de uso del procesador")
    print("- Memoria: Uso de RAM del sistema")
    print("- Disco: Operaciones de lectura/escritura")
    print("- Red: Tráfico de red (si aplica)")
    print()
    print("🛠️ USO RECOMENDADO:")
    print("1. Ejecute el analizador de rendimiento en otra terminal")
    print("2. Inicie esta aplicación")
    print("3. Ejecute operaciones mientras monitorea el rendimiento")
    print("4. Analice los resultados y métricas obtenidas")
    print("="*50)


def main():
    """Función principal"""
    print("🚀 Iniciando aplicación de ejemplo...")
    
    while True:
        try:
            mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "0":
                print("👋 ¡Hasta luego!")
                break
            elif opcion == "1":
                print("\n💻 Iniciando interfaz de consola...")
                interfaz_consola = InterfazConsola()
                interfaz_consola.ejecutar()
            elif opcion == "2":
                print("\n🌐 Iniciando interfaz web...")
                print("⚠️ Presione Ctrl+C para detener el servidor")
                try:
                    web_main()
                except KeyboardInterrupt:
                    print("\n🛑 Servidor web detenido")
            elif opcion == "3":
                mostrar_ayuda()
                input("\nPresione Enter para continuar...")
            else:
                print("❌ Opción no válida. Intente de nuevo.")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main() 