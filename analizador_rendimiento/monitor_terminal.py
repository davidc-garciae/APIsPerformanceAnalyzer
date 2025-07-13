#!/usr/bin/env python3
"""
Script principal para ejecutar el monitor de terminal con visualizaciones coloridas.
"""

import sys
import time
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich import box

from core.visualizacion import SystemVisualizer
from core.monitoring import SystemMonitor
from core.profiling import CodeProfiler


def mostrar_menu_principal():
    """Mostrar menú principal del sistema"""
    console = Console()
    
    menu_text = """
[bold cyan]🖥️  ANALIZADOR DE RENDIMIENTO DEL SISTEMA[/bold cyan]

[green]✅ Sistema de monitoreo iniciado correctamente[/green]

[yellow]Opciones disponibles:[/yellow]

[bold white]1.[/bold white] 📊 [cyan]Resumen del sistema[/cyan]
[bold white]2.[/bold white] ⚡ [green]Monitoreo en tiempo real[/green]
[bold white]3.[/bold white] 🔍 [blue]Demo de profiling[/blue]
[bold white]4.[/bold white] 📈 [magenta]Comparación de métricas[/magenta]
[bold white]5.[/bold white] 🚪 [red]Salir[/red]

[dim]Desarrollado para el curso de Sistemas Operativos[/dim]
    """
    
    panel = Panel(
        menu_text,
        title="[bold]MENÚ PRINCIPAL",
        border_style="bright_blue",
        box=box.DOUBLE
    )
    
    console.print(panel)


def ejecutar_resumen_sistema():
    """Ejecutar resumen del sistema"""
    console = Console()
    visualizer = SystemVisualizer()
    
    console.clear()
    console.print("[bold green]📊 Generando resumen del sistema...[/bold green]\n")
    
    try:
        visualizer.show_system_summary()
        console.print("\n")
        Prompt.ask("[dim]Presiona Enter para continuar", default="", show_default=False)
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")


def ejecutar_monitoreo_tiempo_real():
    """Ejecutar monitoreo en tiempo real"""
    console = Console()
    visualizer = SystemVisualizer()
    
    console.clear()
    console.print("[bold green]⚡ Configuración de monitoreo en tiempo real[/bold green]\n")
    
    # Opciones de frecuencia
    opciones = {
        1: ("0.5 segundos", 0.5),
        2: ("1 segundo", 1.0),
        3: ("2 segundos", 2.0),
        4: ("5 segundos", 5.0)
    }
    
    for key, (desc, _) in opciones.items():
        console.print(f"[bold]{key}.[/bold] {desc}")
    
    choice = IntPrompt.ask(
        "\nSelecciona la frecuencia de actualización",
        choices=["1", "2", "3", "4"],
        default=3
    )
    
    _, refresh_rate = opciones[choice]
    
    console.clear()
    console.print(f"[bold green]🚀 Iniciando monitoreo (actualización cada {refresh_rate}s)[/bold green]")
    console.print("[dim]Presiona Ctrl+C para regresar al menú principal[/dim]\n")
    
    try:
        visualizer.start_live_monitoring(refresh_rate)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]🔙 Regresando al menú principal...[/bold yellow]")
        time.sleep(1)


def ejecutar_demo_profiling():
    """Ejecutar demo de profiling"""
    console = Console()
    visualizer = SystemVisualizer()
    profiler = CodeProfiler()
    
    console.clear()
    console.print("[bold blue]🔍 Demo de Profiling[/bold blue]\n")
    
    try:
        # Función de ejemplo
        def funcion_demo():
            """Función de ejemplo para hacer profiling"""
            import math
            import random
            
            resultado = 0
            for i in range(100000):
                resultado += math.sqrt(i) * math.sin(i) * random.random()
            
            # Fibonacci pequeño
            def fib(n):
                if n <= 1:
                    return n
                return fib(n-1) + fib(n-2)
            
            fib_result = [fib(i) for i in range(20)]
            return resultado, fib_result
        
        console.print("[cyan]Ejecutando función de demo para profiling...[/cyan]")
        results = profiler.profile_function(funcion_demo)
        
        # Mostrar resultados
        visualizer.show_profiling_results(results)
        
    except Exception as e:
        console.print(f"[bold red]❌ Error en profiling: {e}[/bold red]")
    
    console.print("\n")
    Prompt.ask("[dim]Presiona Enter para continuar", default="", show_default=False)


def ejecutar_comparacion_metricas():
    """Ejecutar comparación de métricas"""
    console = Console()
    visualizer = SystemVisualizer()
    monitor = SystemMonitor()
    
    console.clear()
    console.print("[bold magenta]📈 Comparación de métricas del sistema[/bold magenta]\n")
    
    mediciones = []
    
    try:
        # Primera medición
        console.print("[cyan]Tomando primera medición...[/cyan]")
        
        cpu_metrics = monitor.get_cpu_metrics()
        memory_metrics = monitor.get_memory_metrics()
        disk_metrics = monitor.get_disk_io_metrics()
        
        primera_medicion = {
            'timestamp': time.strftime("%H:%M:%S"),
            'label': 'Inicial',
            'cpu_percent_total': cpu_metrics['cpu_percent_total'],
            'memory_percent': memory_metrics['virtual_memory']['percent'],
            'disk_read_rate': disk_metrics.get('read_rate', 0),
            'network_sent_rate': 0  # Simplificado para demo
        }
        mediciones.append(primera_medicion)
        
        console.print("[green]✅ Primera medición completada[/green]\n")
        
        # Segunda medición después de un tiempo
        if Confirm.ask("¿Deseas tomar una segunda medición?", default=True):
            tiempo_espera = IntPrompt.ask("¿Cuántos segundos esperar?", default=5)
            
            console.print(f"[yellow]Esperando {tiempo_espera} segundos...[/yellow]")
            time.sleep(tiempo_espera)
            
            console.print("[cyan]Tomando segunda medición...[/cyan]")
            
            cpu_metrics = monitor.get_cpu_metrics()
            memory_metrics = monitor.get_memory_metrics()
            disk_metrics = monitor.get_disk_io_metrics()
            
            segunda_medicion = {
                'timestamp': time.strftime("%H:%M:%S"),
                'label': 'Después de espera',
                'cpu_percent_total': cpu_metrics['cpu_percent_total'],
                'memory_percent': memory_metrics['virtual_memory']['percent'],
                'disk_read_rate': disk_metrics.get('read_rate', 0),
                'network_sent_rate': 0
            }
            mediciones.append(segunda_medicion)
            
            console.print("[green]✅ Segunda medición completada[/green]\n")
        
        # Mostrar comparación
        if len(mediciones) > 1:
            visualizer.show_comparison_table(mediciones)
        else:
            console.print("[yellow]Se necesitan al menos 2 mediciones para comparar[/yellow]")
            
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
    
    console.print("\n")
    Prompt.ask("[dim]Presiona Enter para continuar", default="", show_default=False)


def main():
    """Función principal"""
    console = Console()
    
    try:
        # Pantalla de bienvenida
        console.clear()
        
        bienvenida = """
[bold cyan]🖥️  ANALIZADOR DE RENDIMIENTO DEL SISTEMA[/bold cyan]

[green]✅ Sistema de monitoreo iniciado correctamente[/green]

[yellow]Este sistema te permite:[/yellow]
• Monitorear CPU, memoria y E/S en tiempo real
• Realizar profiling de código
• Comparar métricas del sistema
• Visualizar datos de forma colorida en la terminal

[dim]Cargando interfaz...[/dim]
        """
        
        panel = Panel(
            bienvenida,
            title="[bold]BIENVENIDO",
            border_style="bright_blue",
            box=box.DOUBLE
        )
        
        console.print(panel)
        time.sleep(2)
        
        # Loop principal
        while True:
            console.clear()
            mostrar_menu_principal()
            
            try:
                opcion = IntPrompt.ask(
                    "Selecciona una opción",
                    choices=["1", "2", "3", "4", "5"],
                    default=5
                )
                
                if opcion == 1:
                    ejecutar_resumen_sistema()
                elif opcion == 2:
                    ejecutar_monitoreo_tiempo_real()
                elif opcion == 3:
                    ejecutar_demo_profiling()
                elif opcion == 4:
                    ejecutar_comparacion_metricas()
                elif opcion == 5:
                    break
                    
            except KeyboardInterrupt:
                console.print("\n[bold yellow]🔙 Regresando al menú principal...[/bold yellow]")
                time.sleep(1)
        
        # Despedida
        console.print("\n[bold green]¡Gracias por usar el Analizador de Rendimiento![/bold green]")
        console.print("[dim]Hasta luego! 👋[/dim]\n")
        
    except KeyboardInterrupt:
        console.print("\n\n[bold red]🛑 Aplicación terminada por el usuario[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error fatal: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main() 