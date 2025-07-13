#!/usr/bin/env python3
"""
Aplicación de ejemplo para monitorear - Sistemas Operativos
Esta aplicación contiene funciones deliberadamente ineficientes para demostrar
el monitoreo de rendimiento y el profiling de código.
"""

import time
import random
import threading
import os
from typing import List, Dict
import math


class AplicacionEjemplo:
    """Aplicación de ejemplo con operaciones intensivas"""
    
    def __init__(self):
        self.datos_memoria = []
        self.running = False
        self.threads = []
    
    def operacion_cpu_intensiva(self, iteraciones: int = 1000000) -> float:
        """Operación que consume mucho CPU"""
        print(f"🔥 Iniciando operación CPU intensiva ({iteraciones:,} iteraciones)")
        
        start_time = time.time()
        resultado = 0.0
        
        for i in range(iteraciones):
            # Operaciones matemáticas complejas
            resultado += math.sqrt(i) * math.sin(i) * math.cos(i)
            
            # Agregar algo de trabajo extra cada 1000 iteraciones
            if i % 1000 == 0:
                resultado += math.factorial(10) / 3628800  # Factorial(10) = 3628800
        
        end_time = time.time()
        print(f"✅ Operación CPU completada en {end_time - start_time:.2f} segundos")
        return resultado
    
    def operacion_memoria_intensiva(self, tamaño_mb: int = 100) -> int:
        """Operación que consume mucha memoria"""
        print(f"💾 Iniciando operación intensiva de memoria ({tamaño_mb} MB)")
        
        start_time = time.time()
        datos_temporales = []
        
        # Calcular número de elementos necesarios (aprox 1MB = 250,000 enteros)
        elementos_por_mb = 250000
        total_elementos = tamaño_mb * elementos_por_mb
        
        # Crear datos en memoria
        for i in range(total_elementos):
            datos_temporales.append(random.randint(1, 1000))
        
        # Operaciones con los datos
        suma_total = sum(datos_temporales)
        promedio = suma_total / len(datos_temporales)
        
        # Guardar en memoria de la instancia (simular memory leak)
        self.datos_memoria.extend(datos_temporales[:10000])  # Solo guardar una parte
        
        end_time = time.time()
        print(f"✅ Operación memoria completada en {end_time - start_time:.2f} segundos")
        print(f"📊 Datos procesados: {len(datos_temporales):,} elementos")
        print(f"📈 Promedio calculado: {promedio:.2f}")
        
        return len(datos_temporales)
    
    def operacion_io_intensiva(self, num_archivos: int = 10, tamaño_archivo_kb: int = 1024):
        """Operación que realiza mucha E/S de disco"""
        print(f"💿 Iniciando operación I/O intensiva ({num_archivos} archivos de {tamaño_archivo_kb} KB)")
        
        start_time = time.time()
        archivos_creados = []
        
        # Crear directorio temporal si no existe
        temp_dir = "temp_io_test"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        try:
            # Crear y escribir archivos
            for i in range(num_archivos):
                filename = os.path.join(temp_dir, f"test_file_{i}.txt")
                archivos_creados.append(filename)
                
                # Generar datos para escribir
                data = "X" * (tamaño_archivo_kb * 1024)  # KB a bytes
                
                # Escribir archivo
                with open(filename, 'w') as f:
                    f.write(data)
                
                # Leer archivo inmediatamente
                with open(filename, 'r') as f:
                    contenido = f.read()
                    assert len(contenido) == len(data)
            
            # Operaciones adicionales de I/O
            for filename in archivos_creados:
                # Leer archivo múltiples veces
                for _ in range(3):
                    with open(filename, 'r') as f:
                        f.read()
            
            end_time = time.time()
            print(f"✅ Operación I/O completada en {end_time - start_time:.2f} segundos")
            print(f"📁 Archivos procesados: {len(archivos_creados)}")
            
        finally:
            # Limpiar archivos temporales
            for filename in archivos_creados:
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass
            
            try:
                os.rmdir(temp_dir)
            except OSError:
                pass
    
    def fibonacci_recursivo(self, n: int) -> int:
        """Implementación recursiva ineficiente de Fibonacci"""
        if n <= 1:
            return n
        return self.fibonacci_recursivo(n-1) + self.fibonacci_recursivo(n-2)
    
    def operacion_fibonacci(self, max_n: int = 35):
        """Calcular Fibonacci de forma recursiva (ineficiente)"""
        print(f"🔢 Calculando Fibonacci hasta {max_n} (recursivo)")
        
        start_time = time.time()
        resultados = []
        
        for i in range(max_n + 1):
            resultado = self.fibonacci_recursivo(i)
            resultados.append(resultado)
            
            if i % 5 == 0:
                print(f"   Fibonacci({i}) = {resultado}")
        
        end_time = time.time()
        print(f"✅ Fibonacci completado en {end_time - start_time:.2f} segundos")
        return resultados
    
    def operacion_multithreading(self, num_threads: int = 4, trabajo_por_thread: int = 100000):
        """Operación con múltiples hilos"""
        print(f"🧵 Iniciando operación multithreading ({num_threads} hilos)")
        
        def trabajo_thread(thread_id: int):
            """Trabajo que realizará cada hilo"""
            resultado = 0
            for i in range(trabajo_por_thread):
                resultado += math.sqrt(i + thread_id * trabajo_por_thread)
            print(f"   Hilo {thread_id} completado: {resultado:.2f}")
            return resultado
        
        start_time = time.time()
        threads = []
        
        # Crear y iniciar hilos
        for i in range(num_threads):
            thread = threading.Thread(target=trabajo_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        print(f"✅ Multithreading completado en {end_time - start_time:.2f} segundos")
    
    def simulacion_memory_leak(self, incremento_mb: int = 10, iteraciones: int = 5):
        """Simular un memory leak controlado"""
        print(f"🚰 Simulando memory leak ({incremento_mb} MB por iteración, {iteraciones} iteraciones)")
        
        for i in range(iteraciones):
            print(f"   Iteración {i+1}: Agregando {incremento_mb} MB a memoria")
            
            # Crear datos que no se liberarán
            nuevos_datos = [random.random() for _ in range(incremento_mb * 250000)]
            self.datos_memoria.extend(nuevos_datos)
            
            print(f"   Memoria acumulada: ~{len(self.datos_memoria) // 250000} MB")
            time.sleep(1)  # Pausa para ver el crecimiento gradual
        
        print(f"✅ Memory leak simulado completado")
        print(f"📊 Total en memoria: {len(self.datos_memoria):,} elementos")
    
    def limpiar_memoria(self):
        """Limpiar datos acumulados en memoria"""
        print("🧹 Limpiando memoria acumulada...")
        self.datos_memoria.clear()
        print("✅ Memoria limpiada")
    
    def benchmark_completo(self):
        """Ejecutar un benchmark completo de todas las operaciones"""
        print("🚀 Iniciando benchmark completo del sistema")
        print("=" * 60)
        
        total_start = time.time()
        
        # Test 1: CPU
        print("\n1️⃣ TEST CPU")
        self.operacion_cpu_intensiva(500000)
        
        # Test 2: Memoria
        print("\n2️⃣ TEST MEMORIA")
        self.operacion_memoria_intensiva(50)
        
        # Test 3: I/O
        print("\n3️⃣ TEST I/O")
        self.operacion_io_intensiva(5, 512)
        
        # Test 4: Fibonacci
        print("\n4️⃣ TEST FIBONACCI")
        self.operacion_fibonacci(30)
        
        # Test 5: Multithreading
        print("\n5️⃣ TEST MULTITHREADING")
        self.operacion_multithreading(3, 50000)
        
        total_end = time.time()
        print(f"\n🏁 Benchmark completo terminado en {total_end - total_start:.2f} segundos")
        print("=" * 60)
    
    def test_estres_continuo(self, duracion_segundos: int = 30):
        """Test de estrés continuo del sistema"""
        print(f"⚡ Iniciando test de estrés continuo ({duracion_segundos} segundos)")
        
        end_time = time.time() + duracion_segundos
        iteracion = 0
        
        while time.time() < end_time:
            iteracion += 1
            print(f"   Iteración de estrés {iteracion}")
            
            # Operaciones mixtas
            self.operacion_cpu_intensiva(100000)
            self.operacion_memoria_intensiva(10)
            
            # Pequeña pausa
            time.sleep(0.5)
        
        print(f"✅ Test de estrés completado ({iteracion} iteraciones)")


def mostrar_menu():
    """Mostrar menú de opciones"""
    print("\n" + "="*60)
    print("🖥️  APLICACIÓN DE EJEMPLO PARA MONITOREO")
    print("   Sistemas Operativos - Test de Rendimiento")
    print("="*60)
    print("1. 🔥 Operación CPU intensiva")
    print("2. 💾 Operación memoria intensiva")
    print("3. 💿 Operación I/O intensiva")
    print("4. 🔢 Fibonacci recursivo")
    print("5. 🧵 Operación multithreading")
    print("6. 🚰 Simular memory leak")
    print("7. 🧹 Limpiar memoria")
    print("8. 🚀 Benchmark completo")
    print("9. ⚡ Test de estrés continuo")
    print("0. 🚪 Salir")
    print("="*60)


def main():
    """Función principal"""
    app = AplicacionEjemplo()
    
    print("🖥️ Aplicación de ejemplo iniciada")
    print("Esta aplicación está diseñada para generar carga en el sistema")
    print("para demostrar las capacidades de monitoreo y profiling.\n")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSelecciona una opción (0-9): ").strip()
            
            if opcion == "1":
                iteraciones = int(input("Número de iteraciones (por defecto 1000000): ") or "1000000")
                app.operacion_cpu_intensiva(iteraciones)
                
            elif opcion == "2":
                mb = int(input("Tamaño en MB (por defecto 100): ") or "100")
                app.operacion_memoria_intensiva(mb)
                
            elif opcion == "3":
                archivos = int(input("Número de archivos (por defecto 10): ") or "10")
                tamaño = int(input("Tamaño por archivo en KB (por defecto 1024): ") or "1024")
                app.operacion_io_intensiva(archivos, tamaño)
                
            elif opcion == "4":
                n = int(input("Fibonacci hasta N (por defecto 35, ¡cuidado con números grandes!): ") or "35")
                app.operacion_fibonacci(n)
                
            elif opcion == "5":
                threads = int(input("Número de hilos (por defecto 4): ") or "4")
                trabajo = int(input("Trabajo por hilo (por defecto 100000): ") or "100000")
                app.operacion_multithreading(threads, trabajo)
                
            elif opcion == "6":
                mb = int(input("MB por iteración (por defecto 10): ") or "10")
                iters = int(input("Número de iteraciones (por defecto 5): ") or "5")
                app.simulacion_memory_leak(mb, iters)
                
            elif opcion == "7":
                app.limpiar_memoria()
                
            elif opcion == "8":
                app.benchmark_completo()
                
            elif opcion == "9":
                duracion = int(input("Duración en segundos (por defecto 30): ") or "30")
                app.test_estres_continuo(duracion)
                
            elif opcion == "0":
                print("\n👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida. Por favor selecciona 0-9.")
                
        except ValueError:
            print("❌ Por favor introduce un número válido.")
        except KeyboardInterrupt:
            print("\n\n🛑 Programa interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Limpiar memoria antes de salir
    app.limpiar_memoria()
    print("🧹 Limpieza completada. Programa terminado.")


if __name__ == "__main__":
    main() 