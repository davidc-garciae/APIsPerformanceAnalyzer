"""
Script de prueba rápida para verificar que el analizador funciona
"""

import asyncio
import httpx
import time
import os
import subprocess
import sys


async def test_api_connectivity():
    """Prueba básica de conectividad de la API"""
    print("🧪 Probando conectividad básica de módulos...")
    
    try:
        # Probar importaciones
        from core.monitoring import system_monitor
        from core.profiling import code_profiler
        print("✅ Importaciones exitosas")
        
        # Probar funciones básicas de monitoreo
        cpu_data = system_monitor.get_cpu_metrics()
        memory_data = system_monitor.get_memory_metrics()
        
        if "error" not in cpu_data and "error" not in memory_data:
            print("✅ Módulo de monitoreo funcional")
            print(f"   💻 CPU: {cpu_data.get('cpu_percent_total', 'N/A')}%")
            print(f"   🧠 Memoria: {memory_data.get('ram', {}).get('percentage', 'N/A')}%")
        else:
            print("❌ Error en módulo de monitoreo")
            return False
        
        # Probar perfilador básico
        snapshot = code_profiler.get_process_profile_snapshot()
        if snapshot.get("success"):
            print("✅ Módulo de perfilado funcional")
            process_info = snapshot.get("process", {})
            print(f"   🔍 Proceso actual: PID {process_info.get('pid', 'N/A')}")
        else:
            print("❌ Error en módulo de perfilado")
            return False
        
        print("\n🎉 ¡Todos los módulos principales funcionan correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        return False


async def test_api_endpoints():
    """Prueba los endpoints de la API si está ejecutándose"""
    print("\n🌐 Probando endpoints de la API...")
    
    base_url = "http://localhost:8000"
    
    endpoints_to_test = [
        "/",
        "/api/v1/",
        "/api/v1/metrics/cpu",
        "/api/v1/metrics/memory",
        "/api/v1/info/system"
    ]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for endpoint in endpoints_to_test:
                try:
                    response = await client.get(f"{base_url}{endpoint}")
                    if response.status_code == 200:
                        print(f"✅ {endpoint}: OK")
                    else:
                        print(f"⚠️ {endpoint}: Status {response.status_code}")
                except httpx.ConnectError:
                    print(f"❌ {endpoint}: No se pudo conectar (¿API no ejecutándose?)")
                except Exception as e:
                    print(f"❌ {endpoint}: Error - {e}")
    
    except Exception as e:
        print(f"❌ Error general probando API: {e}")


def print_banner():
    """Imprime banner del test"""
    print("=" * 60)
    print("🚀 ANALIZADOR DE RENDIMIENTO - SCRIPT DE PRUEBA")
    print("=" * 60)


def print_instructions():
    """Imprime instrucciones para ejecutar el sistema completo"""
    print("\n" + "="*60)
    print("📋 INSTRUCCIONES PARA EJECUTAR EL SISTEMA COMPLETO")
    print("="*60)
    print("\n1️⃣ Ejecutar la API Principal:")
    print("   python main.py")
    print("   📊 URL: http://localhost:8000")
    print("   📖 Docs: http://localhost:8000/docs")
    
    print("\n2️⃣ Ejecutar la App de Ejemplo (en otra terminal):")
    print("   python app_a_monitorear/main.py")
    print("   🎯 URL: http://localhost:8001")
    print("   📖 Docs: http://localhost:8001/docs")
    
    print("\n3️⃣ Probar el sistema:")
    print("   • Visita http://localhost:8001/cpu-intensivo para generar carga")
    print("   • Luego visita http://localhost:8000/api/v1/metrics/cpu para ver métricas")
    print("   • Prueba http://localhost:8000/api/v1/profile/demo/cpu-intensive")
    
    print("\n4️⃣ Endpoints importantes de la API:")
    print("   • Métricas CPU: /api/v1/metrics/cpu")
    print("   • Métricas Memoria: /api/v1/metrics/memory")
    print("   • Resumen Sistema: /api/v1/metrics/system-summary")
    print("   • Demo Perfilado: /api/v1/profile/demo/comprehensive")
    
    print("\n🎯 ¡El proyecto está listo para usar!")


async def main():
    """Función principal"""
    print_banner()
    
    # Probar módulos básicos
    modules_ok = await test_api_connectivity()
    
    if modules_ok:
        # Probar API si está disponible
        await test_api_endpoints()
    
    # Mostrar instrucciones
    print_instructions()


if __name__ == "__main__":
    asyncio.run(main()) 