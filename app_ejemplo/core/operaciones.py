#!/usr/bin/env python3
"""
Módulo de operaciones de ejemplo para monitoreo de rendimiento
Contiene operaciones deliberadamente ineficientes para demostrar el análisis de rendimiento
"""

import time
import random
import threading
import os
import math
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ResultadoOperacion:
    """Resultado de una operación con métricas"""
    nombre: str
    tiempo_ejecucion: float
    resultado: any
    memoria_usada_mb: Optional[float] = None
    cpu_porcentaje: Optional[float] = None


class OperacionesEjemplo:
    """Clase que contiene operaciones de ejemplo para monitoreo"""
    
    def __init__(self):
        self.datos_memoria = []
        self.contador_operaciones = 0
        self.running = False
        self.threads = []
    
    def operacion_cpu_intensiva(self, iteraciones: int = 1000000) -> ResultadoOperacion:
        """
        Operación que consume mucho CPU
        Args:
            iteraciones: Número de iteraciones a realizar
        Returns:
            ResultadoOperacion con métricas de la operación
        """
        print(f"🔥 Iniciando operación CPU intensiva ({iteraciones:,} iteraciones)")
        
        start_time = time.time()
        resultado = 0.0
        
        for i in range(iteraciones):
            # Operaciones matemáticas complejas
            resultado += math.sqrt(i) * math.sin(i) * math.cos(i)
            
            # Agregar trabajo extra cada 1000 iteraciones
            if i % 1000 == 0:
                resultado += math.factorial(10) / 3628800
        
        end_time = time.time()
        tiempo_total = end_time - start_time
        
        print(f"✅ Operación CPU completada en {tiempo_total:.2f} segundos")
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="CPU Intensiva",
            tiempo_ejecucion=tiempo_total,
            resultado=resultado
        )
    
    def operacion_memoria_intensiva(self, tamaño_mb: int = 100) -> ResultadoOperacion:
        """
        Operación que consume mucha memoria
        Args:
            tamaño_mb: Cantidad de memoria a consumir en MB
        Returns:
            ResultadoOperacion con métricas de la operación
        """
        print(f"💾 Iniciando operación intensiva de memoria ({tamaño_mb} MB)")
        
        start_time = time.time()
        datos_temporales = []
        
        # Calcular número de elementos (aprox 1MB = 250,000 enteros)
        elementos_por_mb = 250000
        total_elementos = tamaño_mb * elementos_por_mb
        
        # Crear datos en memoria
        for i in range(total_elementos):
            datos_temporales.append(random.randint(1, 1000000))
            
            # Mostrar progreso cada 10%
            if i % (total_elementos // 10) == 0:
                progreso = (i / total_elementos) * 100
                print(f"  Progreso: {progreso:.1f}%")
        
        # Realizar algunas operaciones con los datos
        suma_total = sum(datos_temporales)
        promedio = suma_total / len(datos_temporales)
        
        end_time = time.time()
        tiempo_total = end_time - start_time
        
        print(f"✅ Operación memoria completada en {tiempo_total:.2f} segundos")
        print(f"  Elementos creados: {len(datos_temporales):,}")
        print(f"  Suma total: {suma_total:,}")
        print(f"  Promedio: {promedio:.2f}")
        
        # Limpiar memoria
        del datos_temporales
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="Memoria Intensiva",
            tiempo_ejecucion=tiempo_total,
            resultado={"suma": suma_total, "promedio": promedio, "elementos": total_elementos},
            memoria_usada_mb=tamaño_mb
        )
    
    def operacion_io_intensiva(self, num_archivos: int = 10, tamaño_archivo_kb: int = 1024) -> ResultadoOperacion:
        """
        Operación que realiza muchas operaciones de E/S
        Args:
            num_archivos: Número de archivos a crear
            tamaño_archivo_kb: Tamaño de cada archivo en KB
        Returns:
            ResultadoOperacion con métricas de la operación
        """
        print(f"💿 Iniciando operación intensiva de E/S ({num_archivos} archivos de {tamaño_archivo_kb} KB)")
        
        start_time = time.time()
        archivos_creados = []
        
        # Crear directorio temporal
        temp_dir = "temp_io_test"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            for i in range(num_archivos):
                nombre_archivo = f"{temp_dir}/test_file_{i}.txt"
                
                # Crear contenido del archivo
                contenido = "A" * (tamaño_archivo_kb * 1024)  # KB a bytes
                
                # Escribir archivo
                with open(nombre_archivo, 'w') as f:
                    f.write(contenido)
                
                # Leer archivo para verificar
                with open(nombre_archivo, 'r') as f:
                    datos_leidos = f.read()
                
                archivos_creados.append(nombre_archivo)
                print(f"  Archivo {i+1}/{num_archivos} procesado")
            
            # Leer todos los archivos de nuevo
            total_bytes_leidos = 0
            for archivo in archivos_creados:
                with open(archivo, 'r') as f:
                    datos = f.read()
                    total_bytes_leidos += len(datos)
            
        finally:
            # Limpiar archivos temporales
            for archivo in archivos_creados:
                try:
                    os.remove(archivo)
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass
        
        end_time = time.time()
        tiempo_total = end_time - start_time
        
        print(f"✅ Operación E/S completada en {tiempo_total:.2f} segundos")
        print(f"  Archivos procesados: {len(archivos_creados)}")
        print(f"  Total bytes leídos: {total_bytes_leidos:,}")
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="E/S Intensiva",
            tiempo_ejecucion=tiempo_total,
            resultado={
                "archivos_procesados": len(archivos_creados),
                "bytes_totales": total_bytes_leidos,
                "archivos_por_segundo": len(archivos_creados) / tiempo_total if tiempo_total > 0 else 0
            }
        )
    
    def fibonacci_recursivo(self, n: int) -> int:
        """Implementación recursiva ineficiente de Fibonacci"""
        if n <= 1:
            return n
        return self.fibonacci_recursivo(n - 1) + self.fibonacci_recursivo(n - 2)
    
    def operacion_fibonacci(self, max_n: int = 35) -> ResultadoOperacion:
        """
        Operación recursiva ineficiente usando Fibonacci
        Args:
            max_n: Número máximo de Fibonacci a calcular
        Returns:
            ResultadoOperacion con métricas de la operación
        """
        print(f"🔄 Iniciando operación recursiva Fibonacci (n={max_n})")
        
        start_time = time.time()
        resultado = self.fibonacci_recursivo(max_n)
        end_time = time.time()
        
        tiempo_total = end_time - start_time
        
        print(f"✅ Fibonacci({max_n}) = {resultado} calculado en {tiempo_total:.2f} segundos")
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="Fibonacci Recursivo",
            tiempo_ejecucion=tiempo_total,
            resultado=resultado
        )
    
    def operacion_multithreading(self, num_threads: int = 4, trabajo_por_thread: int = 100000) -> ResultadoOperacion:
        """
        Operación que usa múltiples hilos
        Args:
            num_threads: Número de hilos a crear
            trabajo_por_thread: Cantidad de trabajo por hilo
        Returns:
            ResultadoOperacion con métricas de la operación
        """
        print(f"🧵 Iniciando operación multithreading ({num_threads} hilos)")
        
        start_time = time.time()
        resultados = []
        threads = []
        
        def trabajo_thread(thread_id: int):
            """Trabajo que ejecuta cada hilo"""
            resultado_local = 0
            for i in range(trabajo_por_thread):
                resultado_local += math.sqrt(i + thread_id * trabajo_por_thread)
            resultados.append(resultado_local)
            print(f"  Hilo {thread_id} completado")
        
        # Crear y lanzar hilos
        for i in range(num_threads):
            thread = threading.Thread(target=trabajo_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Esperar que terminen todos los hilos
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        tiempo_total = end_time - start_time
        suma_resultados = sum(resultados)
        
        print(f"✅ Operación multithreading completada en {tiempo_total:.2f} segundos")
        print(f"  Suma de resultados: {suma_resultados:.2f}")
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="Multithreading",
            tiempo_ejecucion=tiempo_total,
            resultado={
                "suma_resultados": suma_resultados,
                "num_threads": num_threads,
                "trabajo_por_thread": trabajo_por_thread
            }
        )
    
    def simulacion_memory_leak(self, incremento_mb: int = 10, iteraciones: int = 5) -> ResultadoOperacion:
        """
        Simula una fuga de memoria
        Args:
            incremento_mb: MB a agregar en cada iteración
            iteraciones: Número de iteraciones
        Returns:
            ResultadoOperacion con métricas de la operación
        """
        print(f"🕳️ Simulando fuga de memoria ({incremento_mb} MB x {iteraciones} iteraciones)")
        
        start_time = time.time()
        
        for i in range(iteraciones):
            # Agregar datos a la memoria global (no se libera)
            elementos_por_mb = 250000
            nuevos_datos = [random.randint(1, 1000000) for _ in range(incremento_mb * elementos_por_mb)]
            self.datos_memoria.extend(nuevos_datos)
            
            memoria_actual_mb = len(self.datos_memoria) / elementos_por_mb
            print(f"  Iteración {i+1}: Memoria acumulada ≈ {memoria_actual_mb:.1f} MB")
            time.sleep(0.5)  # Pausa para observar el crecimiento
        
        end_time = time.time()
        tiempo_total = end_time - start_time
        memoria_total_mb = len(self.datos_memoria) / 250000
        
        print(f"⚠️ Fuga de memoria simulada. Memoria total: {memoria_total_mb:.1f} MB")
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="Memory Leak",
            tiempo_ejecucion=tiempo_total,
            resultado={
                "memoria_total_mb": memoria_total_mb,
                "elementos_totales": len(self.datos_memoria)
            },
            memoria_usada_mb=memoria_total_mb
        )
    
    def limpiar_memoria(self) -> ResultadoOperacion:
        """Limpia la memoria acumulada"""
        print("🧹 Limpiando memoria...")
        
        start_time = time.time()
        elementos_antes = len(self.datos_memoria)
        self.datos_memoria.clear()
        end_time = time.time()
        
        tiempo_total = end_time - start_time
        
        print(f"✅ Memoria limpiada. Elementos eliminados: {elementos_antes:,}")
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="Limpieza de Memoria",
            tiempo_ejecucion=tiempo_total,
            resultado={"elementos_eliminados": elementos_antes}
        )
    
    def operacion_deliberadamente_lenta(self, segundos: int = 5) -> ResultadoOperacion:
        """
        Operación que simplemente espera
        Args:
            segundos: Tiempo a esperar
        Returns:
            ResultadoOperacion con métricas de la operación
        """
        print(f"⏰ Iniciando operación lenta ({segundos} segundos)")
        
        start_time = time.time()
        time.sleep(segundos)
        end_time = time.time()
        
        tiempo_total = end_time - start_time
        
        print(f"✅ Operación lenta completada en {tiempo_total:.2f} segundos")
        
        self.contador_operaciones += 1
        
        return ResultadoOperacion(
            nombre="Operación Lenta",
            tiempo_ejecucion=tiempo_total,
            resultado={"tiempo_esperado": segundos, "tiempo_real": tiempo_total}
        )
    
    def benchmark_completo(self) -> Dict[str, ResultadoOperacion]:
        """Ejecuta un benchmark completo con todas las operaciones"""
        print("🏁 Iniciando benchmark completo...")
        
        resultados = {}
        
        # Ejecutar todas las operaciones con parámetros moderados
        operaciones = [
            ("cpu_intensiva", lambda: self.operacion_cpu_intensiva(500000)),
            ("memoria_intensiva", lambda: self.operacion_memoria_intensiva(50)),
            ("io_intensiva", lambda: self.operacion_io_intensiva(5, 512)),
            ("fibonacci", lambda: self.operacion_fibonacci(30)),
            ("multithreading", lambda: self.operacion_multithreading(2, 50000)),
            ("operacion_lenta", lambda: self.operacion_deliberadamente_lenta(2))
        ]
        
        for nombre, operacion in operaciones:
            print(f"\n--- Ejecutando: {nombre} ---")
            resultado = operacion()
            resultados[nombre] = resultado
        
        print("\n🎯 Benchmark completo finalizado")
        return resultados
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas actuales de la aplicación"""
        return {
            "contador_operaciones": self.contador_operaciones,
            "memoria_acumulada_elementos": len(self.datos_memoria),
            "memoria_acumulada_mb": len(self.datos_memoria) / 250000 if self.datos_memoria else 0,
            "threads_activos": len(self.threads),
            "running": self.running
        } 