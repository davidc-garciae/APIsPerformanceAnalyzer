"""
Aplicación de ejemplo para monitorear
Contiene funciones ineficientes a propósito para demostrar el analizador de rendimiento
"""

from fastapi import FastAPI, BackgroundTasks
import uvicorn
import time
import threading
import random
import math
import asyncio
from typing import List

app = FastAPI(
    title="Aplicación de Ejemplo para Monitorear",
    description="Aplicación web con funciones ineficientes para probar el analizador de rendimiento",
    version="1.0.0"
)

# Variables globales para simular problemas
memoria_global = []
contador_operaciones = 0


@app.get("/")
async def root():
    """Endpoint principal de la aplicación de ejemplo"""
    return {
        "message": "Aplicación de Ejemplo para Monitorear",
        "version": "1.0.0",
        "endpoints": {
            "cpu_intensivo": "/cpu-intensivo",
            "memoria_intensivo": "/memoria-intensivo",
            "io_intensivo": "/io-intensivo",
            "operacion_lenta": "/operacion-lenta",
            "fuga_memoria": "/fuga-memoria",
            "operacion_recursiva": "/operacion-recursiva",
            "stress_test": "/stress-test"
        },
        "nota": "Esta app está diseñada para generar carga de trabajo y probar el analizador"
    }


@app.get("/cpu-intensivo")
async def operacion_cpu_intensiva(iteraciones: int = 1000000):
    """
    Función que realiza cálculos intensivos de CPU
    Args:
        iteraciones: Número de iteraciones a realizar
    """
    inicio = time.time()
    
    # Cálculos matemáticos intensivos
    resultado = 0
    for i in range(iteraciones):
        resultado += math.sqrt(i) * math.sin(i) * math.cos(i)
        if i % 100000 == 0:
            # Pequeñas pausas para no bloquear completamente
            await asyncio.sleep(0.001)
    
    fin = time.time()
    
    global contador_operaciones
    contador_operaciones += 1
    
    return {
        "mensaje": "Operación CPU intensiva completada",
        "iteraciones": iteraciones,
        "resultado": resultado,
        "tiempo_segundos": fin - inicio,
        "operaciones_totales": contador_operaciones
    }


@app.get("/memoria-intensivo")
async def operacion_memoria_intensiva(tamaño_mb: int = 100):
    """
    Función que consume mucha memoria
    Args:
        tamaño_mb: Tamaño en MB de datos a crear en memoria
    """
    inicio = time.time()
    
    # Crear listas grandes en memoria
    datos_grandes = []
    bytes_por_mb = 1024 * 1024
    
    for _ in range(tamaño_mb):
        # Crear arrays de 1MB cada uno
        chunk = [random.random() for _ in range(bytes_por_mb // 8)]  # 8 bytes por float
        datos_grandes.append(chunk)
    
    # Realizar operaciones sobre los datos
    suma_total = sum(sum(chunk) for chunk in datos_grandes)
    
    fin = time.time()
    
    return {
        "mensaje": "Operación memoria intensiva completada",
        "tamaño_mb": tamaño_mb,
        "elementos_totales": len(datos_grandes) * len(datos_grandes[0]) if datos_grandes else 0,
        "suma_total": suma_total,
        "tiempo_segundos": fin - inicio
    }


@app.get("/io-intensivo")
async def operacion_io_intensiva(archivos: int = 10, tamaño_kb: int = 1024):
    """
    Función que realiza muchas operaciones de E/S
    Args:
        archivos: Número de archivos temporales a crear
        tamaño_kb: Tamaño de cada archivo en KB
    """
    import os
    import tempfile
    
    inicio = time.time()
    archivos_creados = []
    
    try:
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            
            # Crear múltiples archivos
            for i in range(archivos):
                archivo_path = os.path.join(temp_dir, f"test_file_{i}.txt")
                
                # Escribir datos al archivo
                with open(archivo_path, 'w') as f:
                    for j in range(tamaño_kb):
                        f.write(f"Línea {j} del archivo {i} - " + "x" * 50 + "\n")
                
                archivos_creados.append(archivo_path)
            
            # Leer todos los archivos
            contenido_total = 0
            for archivo in archivos_creados:
                with open(archivo, 'r') as f:
                    contenido = f.read()
                    contenido_total += len(contenido)
            
            fin = time.time()
            
            return {
                "mensaje": "Operación E/S intensiva completada",
                "archivos_procesados": len(archivos_creados),
                "tamaño_total_bytes": contenido_total,
                "tiempo_segundos": fin - inicio
            }
    
    except Exception as e:
        return {
            "error": f"Error en operación E/S: {str(e)}",
            "tiempo_segundos": time.time() - inicio
        }


@app.get("/operacion-lenta")
async def operacion_deliberadamente_lenta(segundos: int = 5):
    """
    Función que simula una operación lenta (ej: consulta a base de datos lenta)
    Args:
        segundos: Número de segundos a esperar
    """
    inicio = time.time()
    
    # Simular trabajo con sleep
    time.sleep(segundos)
    
    # Agregar algo de trabajo CPU después del sleep
    resultado = sum(i * i for i in range(10000))
    
    fin = time.time()
    
    return {
        "mensaje": "Operación lenta completada",
        "segundos_esperados": segundos,
        "tiempo_real_segundos": fin - inicio,
        "resultado_calculo": resultado
    }


@app.get("/fuga-memoria")
async def simular_fuga_memoria(elementos: int = 10000):
    """
    Función que simula una fuga de memoria agregando datos a una variable global
    Args:
        elementos: Número de elementos a agregar a la "fuga"
    """
    global memoria_global
    
    inicio = time.time()
    
    # Agregar datos a la variable global (simulando fuga)
    nuevos_datos = [
        {
            "id": len(memoria_global) + i,
            "timestamp": time.time(),
            "datos": [random.random() for _ in range(100)],
            "texto": f"Elemento {i} " * 20
        }
        for i in range(elementos)
    ]
    
    memoria_global.extend(nuevos_datos)
    
    fin = time.time()
    
    return {
        "mensaje": "Fuga de memoria simulada",
        "elementos_agregados": elementos,
        "total_elementos_en_memoria": len(memoria_global),
        "memoria_estimada_mb": len(memoria_global) * 0.01,  # Estimación aproximada
        "tiempo_segundos": fin - inicio
    }


@app.get("/limpiar-memoria")
async def limpiar_memoria():
    """Limpia la memoria global para resetear la 'fuga'"""
    global memoria_global
    elementos_liberados = len(memoria_global)
    memoria_global.clear()
    
    return {
        "mensaje": "Memoria limpiada",
        "elementos_liberados": elementos_liberados
    }


@app.get("/operacion-recursiva")
async def operacion_recursiva_ineficiente(n: int = 35):
    """
    Función recursiva ineficiente (Fibonacci sin memoización)
    Args:
        n: Número para calcular Fibonacci
    """
    def fibonacci_ineficiente(num):
        if num <= 1:
            return num
        return fibonacci_ineficiente(num - 1) + fibonacci_ineficiente(num - 2)
    
    inicio = time.time()
    
    # Limitar el número para evitar que tome demasiado tiempo
    n = min(n, 40)
    resultado = fibonacci_ineficiente(n)
    
    fin = time.time()
    
    return {
        "mensaje": "Fibonacci recursivo ineficiente completado",
        "n": n,
        "resultado": resultado,
        "tiempo_segundos": fin - inicio,
        "advertencia": "Esta implementación es deliberadamente ineficiente para testing"
    }


@app.get("/stress-test")
async def stress_test(background_tasks: BackgroundTasks, duración: int = 30):
    """
    Ejecuta múltiples operaciones en paralelo para estresar el sistema
    Args:
        duración: Duración del stress test en segundos
    """
    
    def tarea_cpu():
        fin_tiempo = time.time() + duración
        while time.time() < fin_tiempo:
            sum(i * i for i in range(1000))
    
    def tarea_memoria():
        datos_temp = []
        fin_tiempo = time.time() + duración
        while time.time() < fin_tiempo:
            datos_temp.append([random.random() for _ in range(1000)])
            if len(datos_temp) > 100:
                datos_temp.clear()
    
    # Iniciar tareas en background
    for _ in range(3):  # 3 tareas CPU
        background_tasks.add_task(tarea_cpu)
    
    for _ in range(2):  # 2 tareas memoria
        background_tasks.add_task(tarea_memoria)
    
    return {
        "mensaje": "Stress test iniciado",
        "duración_segundos": duración,
        "tareas_cpu": 3,
        "tareas_memoria": 2,
        "nota": "Las tareas se ejecutan en background. Monitorea el sistema durante los próximos segundos."
    }


@app.get("/stats")
async def obtener_estadisticas():
    """Obtiene estadísticas de la aplicación"""
    global memoria_global, contador_operaciones
    
    return {
        "estadisticas": {
            "operaciones_cpu_realizadas": contador_operaciones,
            "elementos_en_memoria_global": len(memoria_global),
            "memoria_estimada_mb": len(memoria_global) * 0.01,
            "uptime_segundos": time.time() - inicio_app
        }
    }


# Variable para tracking del tiempo de inicio
inicio_app = time.time()


if __name__ == "__main__":
    print("🎯 Iniciando Aplicación de Ejemplo para Monitorear...")
    print("📊 Disponible en: http://localhost:8001")
    print("📖 Documentación en: http://localhost:8001/docs")
    print("\n🔥 Endpoints para generar carga:")
    print("   • CPU intensivo: http://localhost:8001/cpu-intensivo")
    print("   • Memoria intensiva: http://localhost:8001/memoria-intensivo")
    print("   • E/S intensiva: http://localhost:8001/io-intensivo")
    print("   • Operación lenta: http://localhost:8001/operacion-lenta")
    print("   • Fuga memoria: http://localhost:8001/fuga-memoria")
    print("   • Recursión ineficiente: http://localhost:8001/operacion-recursiva")
    print("   • Stress test: http://localhost:8001/stress-test")
    print("\n💡 Usa estos endpoints para generar carga y probar el analizador!")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    ) 