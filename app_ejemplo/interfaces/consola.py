#!/usr/bin/env python3
"""
Interfaz de consola para la aplicación de ejemplo
"""

import sys
import os
from typing import Dict, Optional

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.operaciones import OperacionesEjemplo, ResultadoOperacion
from core.utils import MonitorRendimiento, mostrar_tabla_resultados, generar_reporte_html


class InterfazConsola:
    """Interfaz de consola para ejecutar operaciones de ejemplo"""
    
    def __init__(self):
        self.operaciones = OperacionesEjemplo()
        self.monitor = MonitorRendimiento()
        self.resultados_sesion: Dict[str, ResultadoOperacion] = {}
    
    def mostrar_menu_principal(self) -> None:
        """Muestra el menú principal"""
        print("\n" + "="*60)
        print("🔧 APLICACIÓN DE EJEMPLO PARA MONITOREO DE RENDIMIENTO")
        print("="*60)
        print("1. 🔥 Operación CPU Intensiva")
        print("2. 💾 Operación Memoria Intensiva") 
        print("3. 💿 Operación E/S Intensiva")
        print("4. 🔄 Operación Fibonacci Recursiva")
        print("5. 🧵 Operación Multithreading")
        print("6. 🕳️  Simulación Memory Leak")
        print("7. 🧹 Limpiar Memoria")
        print("8. ⏰ Operación Deliberadamente Lenta")
        print("9. 🏁 Benchmark Completo")
        print("10. 📊 Ver Estadísticas")
        print("11. 📈 Ver Resumen de Rendimiento")
        print("12. 📄 Generar Reporte HTML")
        print("0. ❌ Salir")
        print("="*60)
    
    def ejecutar_opcion_1(self) -> None:
        """Operación CPU Intensiva"""
        print("\n🔥 OPERACIÓN CPU INTENSIVA")
        try:
            iteraciones = int(input("Iteraciones (default 1000000): ") or "1000000")
            resultado = self.operaciones.operacion_cpu_intensiva(iteraciones)
            self.resultados_sesion["cpu_intensiva"] = resultado
            print(f"✅ Completado: {resultado.resultado:.2f}")
        except ValueError:
            print("❌ Error: Ingrese un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_2(self) -> None:
        """Operación Memoria Intensiva"""
        print("\n💾 OPERACIÓN MEMORIA INTENSIVA")
        try:
            tamaño_mb = int(input("Tamaño en MB (default 100): ") or "100")
            resultado = self.operaciones.operacion_memoria_intensiva(tamaño_mb)
            self.resultados_sesion["memoria_intensiva"] = resultado
            print(f"✅ Completado: {resultado.resultado['elementos']:,} elementos")
        except ValueError:
            print("❌ Error: Ingrese un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_3(self) -> None:
        """Operación E/S Intensiva"""
        print("\n💿 OPERACIÓN E/S INTENSIVA")
        try:
            num_archivos = int(input("Número de archivos (default 10): ") or "10")
            tamaño_kb = int(input("Tamaño por archivo en KB (default 1024): ") or "1024")
            resultado = self.operaciones.operacion_io_intensiva(num_archivos, tamaño_kb)
            self.resultados_sesion["io_intensiva"] = resultado
            print(f"✅ Completado: {resultado.resultado['archivos_procesados']} archivos")
        except ValueError:
            print("❌ Error: Ingrese números válidos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_4(self) -> None:
        """Operación Fibonacci Recursiva"""
        print("\n🔄 OPERACIÓN FIBONACCI RECURSIVA")
        try:
            max_n = int(input("Número máximo (default 35): ") or "35")
            if max_n > 40:
                print("⚠️ Advertencia: Valores > 40 pueden tomar mucho tiempo")
                confirmar = input("¿Continuar? (s/N): ").lower()
                if confirmar != 's':
                    return
            
            resultado = self.operaciones.operacion_fibonacci(max_n)
            self.resultados_sesion["fibonacci"] = resultado
            print(f"✅ Completado: Fibonacci({max_n}) = {resultado.resultado}")
        except ValueError:
            print("❌ Error: Ingrese un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_5(self) -> None:
        """Operación Multithreading"""
        print("\n🧵 OPERACIÓN MULTITHREADING")
        try:
            num_threads = int(input("Número de hilos (default 4): ") or "4")
            trabajo = int(input("Trabajo por hilo (default 100000): ") or "100000")
            resultado = self.operaciones.operacion_multithreading(num_threads, trabajo)
            self.resultados_sesion["multithreading"] = resultado
            print(f"✅ Completado: {num_threads} hilos")
        except ValueError:
            print("❌ Error: Ingrese números válidos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_6(self) -> None:
        """Simulación Memory Leak"""
        print("\n🕳️ SIMULACIÓN MEMORY LEAK")
        try:
            incremento_mb = int(input("Incremento MB por iteración (default 10): ") or "10")
            iteraciones = int(input("Número de iteraciones (default 5): ") or "5")
            resultado = self.operaciones.simulacion_memory_leak(incremento_mb, iteraciones)
            self.resultados_sesion["memory_leak"] = resultado
            print(f"✅ Completado: {resultado.resultado['memoria_total_mb']:.1f} MB acumulados")
        except ValueError:
            print("❌ Error: Ingrese números válidos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_7(self) -> None:
        """Limpiar Memoria"""
        print("\n🧹 LIMPIAR MEMORIA")
        resultado = self.operaciones.limpiar_memoria()
        self.resultados_sesion["limpiar_memoria"] = resultado
        print(f"✅ Completado: {resultado.resultado['elementos_eliminados']:,} elementos eliminados")
    
    def ejecutar_opcion_8(self) -> None:
        """Operación Deliberadamente Lenta"""
        print("\n⏰ OPERACIÓN DELIBERADAMENTE LENTA")
        try:
            segundos = int(input("Segundos a esperar (default 5): ") or "5")
            resultado = self.operaciones.operacion_deliberadamente_lenta(segundos)
            self.resultados_sesion["operacion_lenta"] = resultado
            print(f"✅ Completado: {resultado.resultado['tiempo_real']:.2f} segundos")
        except ValueError:
            print("❌ Error: Ingrese un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_9(self) -> None:
        """Benchmark Completo"""
        print("\n🏁 BENCHMARK COMPLETO")
        print("⚠️ Esta operación ejecutará todas las pruebas. Puede tomar varios minutos.")
        confirmar = input("¿Continuar? (s/N): ").lower()
        if confirmar != 's':
            return
        
        try:
            resultados = self.operaciones.benchmark_completo()
            self.resultados_sesion.update(resultados)
            mostrar_tabla_resultados(resultados)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def ejecutar_opcion_10(self) -> None:
        """Ver Estadísticas"""
        print("\n📊 ESTADÍSTICAS ACTUALES")
        stats = self.operaciones.obtener_estadisticas()
        metricas = self.monitor.obtener_metricas_actuales()
        
        print(f"Operaciones ejecutadas: {stats['contador_operaciones']}")
        print(f"Memoria acumulada: {stats['memoria_acumulada_mb']:.1f} MB")
        print(f"Threads activos: {stats['threads_activos']}")
        print(f"Sistema en ejecución: {'Sí' if stats['running'] else 'No'}")
        print("\n📈 MÉTRICAS DEL SISTEMA:")
        print(f"CPU: {metricas.cpu_porcentaje:.1f}%")
        print(f"Memoria: {metricas.memoria_porcentaje:.1f}% ({metricas.memoria_usada_mb:.1f} MB)")
        print(f"Disco lectura: {metricas.disco_lectura_mb:.1f} MB")
        print(f"Disco escritura: {metricas.disco_escritura_mb:.1f} MB")
    
    def ejecutar_opcion_11(self) -> None:
        """Ver Resumen de Rendimiento"""
        print("\n📈 RESUMEN DE RENDIMIENTO")
        resumen = self.monitor.obtener_resumen_rendimiento()
        
        if not resumen:
            print("No hay datos de rendimiento disponibles")
            return
        
        print(f"Tiempo de monitoreo: {resumen['tiempo_monitoreo_segundos']:.1f} segundos")
        print(f"Muestras tomadas: {resumen['muestras_tomadas']}")
        print(f"\nCPU:")
        print(f"  Promedio: {resumen['cpu']['promedio']:.1f}%")
        print(f"  Máximo: {resumen['cpu']['maximo']:.1f}%")
        print(f"  Actual: {resumen['cpu']['actual']:.1f}%")
        print(f"\nMemoria:")
        print(f"  Promedio: {resumen['memoria']['promedio']:.1f}%")
        print(f"  Máximo: {resumen['memoria']['maximo']:.1f}%")
        print(f"  Actual: {resumen['memoria']['actual']:.1f}%")
    
    def ejecutar_opcion_12(self) -> None:
        """Generar Reporte HTML"""
        print("\n📄 GENERAR REPORTE HTML")
        if not self.resultados_sesion:
            print("❌ No hay resultados para generar reporte")
            return
        
        try:
            archivo = input("Nombre del archivo (default: reporte_rendimiento.html): ") or "reporte_rendimiento.html"
            generar_reporte_html(self.resultados_sesion, archivo)
            print(f"✅ Reporte generado: {archivo}")
        except Exception as e:
            print(f"❌ Error generando reporte: {e}")
    
    def ejecutar(self) -> None:
        """Ejecuta la interfaz de consola"""
        print("🚀 Iniciando aplicación de ejemplo...")
        
        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("\nSeleccione una opción: ").strip()
                
                if opcion == "0":
                    print("👋 ¡Hasta luego!")
                    break
                elif opcion == "1":
                    self.ejecutar_opcion_1()
                elif opcion == "2":
                    self.ejecutar_opcion_2()
                elif opcion == "3":
                    self.ejecutar_opcion_3()
                elif opcion == "4":
                    self.ejecutar_opcion_4()
                elif opcion == "5":
                    self.ejecutar_opcion_5()
                elif opcion == "6":
                    self.ejecutar_opcion_6()
                elif opcion == "7":
                    self.ejecutar_opcion_7()
                elif opcion == "8":
                    self.ejecutar_opcion_8()
                elif opcion == "9":
                    self.ejecutar_opcion_9()
                elif opcion == "10":
                    self.ejecutar_opcion_10()
                elif opcion == "11":
                    self.ejecutar_opcion_11()
                elif opcion == "12":
                    self.ejecutar_opcion_12()
                else:
                    print("❌ Opción no válida. Intente de nuevo.")
                
                input("\nPresione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                input("Presione Enter para continuar...")


def main():
    """Función principal"""
    interfaz = InterfazConsola()
    interfaz.ejecutar()


if __name__ == "__main__":
    main() 