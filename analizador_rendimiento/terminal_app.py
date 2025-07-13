#!/usr/bin/env python3
"""
Aplicación de terminal interactiva para el analizador de rendimiento del sistema.
Utiliza rich para crear una interfaz colorida y atractiva.
"""

import sys
import time
import click
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich import box

from core.visualizacion import SystemVisualizer
from core.monitoring import SystemMonitor
from core.profiling import CodeProfiler


class TerminalApp:
    """Aplicación principal de terminal"""
    
    def __init__(self):
        self.console = Console()
        self.visualizer = SystemVisualizer()
        self.monitor = SystemMonitor()
        self.profiler = CodeProfiler()
        self.running = True
    
    def show_main_menu(self):
        """Mostrar menú principal"""
        menu_text = """
[bold cyan]🖥️  ANALIZADOR DE RENDIMIENTO DEL SISTEMA[/bold cyan]

[green]✅ Sistema de monitoreo iniciado correctamente[/green]

[yellow]Opciones disponibles:[/yellow]

[bold white]1.[/bold white] 📊 [cyan]Resumen del sistema[/cyan]
[bold white]2.[/bold white] ⚡ [green]Monitoreo en tiempo real[/green]
[bold white]3.[/bold white] 🔍 [blue]Profiling de código[/blue]
[bold white]4.[/bold white] 📈 [magenta]Comparación de métricas[/magenta]
[bold white]5.[/bold white] 🔧 [yellow]Herramientas avanzadas[/yellow]
[bold white]6.[/bold white] ℹ️  [dim]Información del sistema[/dim]
[bold white]7.[/bold white] 🚪 [red]Salir[/red]

[dim]Desarrollado para el curso de Sistemas Operativos[/dim]
        """
        
        panel = Panel(
            menu_text,
            title="[bold]MENÚ PRINCIPAL",
            border_style="bright_blue",
            box=box.DOUBLE
        )
        
        self.console.print(panel)
    
    def handle_system_summary(self):
        """Manejar opción de resumen del sistema"""
        self.console.clear()
        self.console.print("[bold green]📊 Generando resumen del sistema...[/bold green]\n")
        
        try:
            self.visualizer.show_system_summary()
            
            self.console.print("\n")
            if Confirm.ask("¿Deseas actualizar el resumen?", default=False):
                self.handle_system_summary()
                
        except Exception as e:
            self.console.print(f"[bold red]❌ Error al generar resumen: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def handle_live_monitoring(self):
        """Manejar opción de monitoreo en tiempo real"""
        self.console.clear()
        
        # Opciones de refresh rate
        refresh_options = {
            1: ("0.5 segundos", 0.5),
            2: ("1 segundo", 1.0),
            3: ("2 segundos", 2.0),
            4: ("5 segundos", 5.0)
        }
        
        self.console.print("[bold green]⚡ Configuración de monitoreo en tiempo real[/bold green]\n")
        
        for key, (desc, _) in refresh_options.items():
            self.console.print(f"[bold]{key}.[/bold] {desc}")
        
        choice = IntPrompt.ask(
            "\nSelecciona la frecuencia de actualización",
            choices=["1", "2", "3", "4"],
            default=3
        )
        
        _, refresh_rate = refresh_options[choice]
        
        self.console.clear()
        self.console.print(f"[bold green]🚀 Iniciando monitoreo (actualización cada {refresh_rate}s)[/bold green]")
        self.console.print("[dim]Presiona Ctrl+C para regresar al menú principal[/dim]\n")
        
        try:
            self.visualizer.start_live_monitoring(refresh_rate)
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]🔙 Regresando al menú principal...[/bold yellow]")
            time.sleep(1)
    
    def handle_profiling(self):
        """Manejar opción de profiling"""
        self.console.clear()
        
        # Menú de profiling
        profiling_menu = """
[bold blue]🔍 HERRAMIENTAS DE PROFILING[/bold blue]

[yellow]Opciones disponibles:[/yellow]

[bold white]1.[/bold white] 🐍 [cyan]Profiling con cProfile[/cyan]
[bold white]2.[/bold white] 💾 [green]Profiling de memoria[/green]
[bold white]3.[/bold white] ⚡ [blue]Profiling de función personalizada[/blue]
[bold white]4.[/bold white] 🔄 [magenta]Profiling continuo[/magenta]
[bold white]5.[/bold white] 🔙 [dim]Volver al menú principal[/dim]
        """
        
        panel = Panel(profiling_menu, title="[bold]PROFILING", border_style="blue")
        self.console.print(panel)
        
        choice = IntPrompt.ask(
            "Selecciona una opción",
            choices=["1", "2", "3", "4", "5"],
            default=5
        )
        
        if choice == 1:
            self.handle_cprofile()
        elif choice == 2:
            self.handle_memory_profiling()
        elif choice == 3:
            self.handle_custom_profiling()
        elif choice == 4:
            self.handle_continuous_profiling()
        elif choice == 5:
            return
    
    def handle_cprofile(self):
        """Manejar profiling con cProfile"""
        self.console.print("[bold cyan]🐍 Ejecutando profiling con cProfile...[/bold cyan]\n")
        
        try:
            # Función de ejemplo para hacer profiling
            def ejemplo_fibonacci(n):
                if n <= 1:
                    return n
                return ejemplo_fibonacci(n-1) + ejemplo_fibonacci(n-2)
            
            def funcion_intensiva():
                """Función de ejemplo que consume CPU"""
                resultado = 0
                for i in range(1000000):
                    resultado += i ** 0.5
                
                # Calcular algunos fibonacci
                fib_results = [ejemplo_fibonacci(i) for i in range(25)]
                return resultado, fib_results
            
            # Ejecutar profiling
            results = self.profiler.profile_function(funcion_intensiva)
            
            # Mostrar resultados
            self.visualizer.show_profiling_results(results)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error en profiling: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def handle_memory_profiling(self):
        """Manejar profiling de memoria"""
        self.console.print("[bold green]💾 Ejecutando profiling de memoria...[/bold green]\n")
        
        try:
            def funcion_memoria():
                """Función que consume memoria"""
                # Crear listas grandes
                datos = []
                for i in range(100000):
                    datos.append([j for j in range(100)])
                
                # Crear diccionarios
                dict_grande = {i: f"valor_{i}" for i in range(50000)}
                
                return len(datos), len(dict_grande)
            
            # Ejecutar profiling de memoria
            results = self.profiler.memory_profile_function(funcion_memoria)
            
            # Mostrar resultados
            self.visualizer.show_profiling_results(results)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error en profiling de memoria: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def handle_custom_profiling(self):
        """Manejar profiling de función personalizada"""
        self.console.print("[bold blue]⚡ Profiling de función personalizada[/bold blue]\n")
        
        # Mostrar código de ejemplo
        code_example = '''
def mi_funcion_personalizada():
    """Función de ejemplo para hacer profiling"""
    import time
    import random
    
    # Simular trabajo CPU-intensivo
    resultado = 0
    for i in range(500000):
        resultado += i * random.random()
    
    # Simular I/O
    time.sleep(0.1)
    
    return resultado
'''
        
        self.console.print("[dim]Código de ejemplo:[/dim]")
        self.console.print(Panel(code_example, title="Función de ejemplo", border_style="dim"))
        
        # Ejecutar ejemplo
        try:
            def mi_funcion_personalizada():
                """Función de ejemplo para hacer profiling"""
                import time
                import random
                
                # Simular trabajo CPU-intensivo
                resultado = 0
                for i in range(500000):
                    resultado += i * random.random()
                
                # Simular I/O
                time.sleep(0.1)
                
                return resultado
            
            self.console.print("\n[cyan]Ejecutando función personalizada...[/cyan]")
            results = self.profiler.profile_function(mi_funcion_personalizada)
            
            # Mostrar resultados
            self.visualizer.show_profiling_results(results)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def handle_continuous_profiling(self):
        """Manejar profiling continuo"""
        self.console.print("[bold magenta]🔄 Profiling continuo[/bold magenta]\n")
        self.console.print("[yellow]Esta función requiere py-spy y permisos administrativos[/yellow]")
        self.console.print("[dim]En desarrollo... Regresando al menú[/dim]")
        time.sleep(2)
    
    def handle_metrics_comparison(self):
        """Manejar comparación de métricas"""
        self.console.clear()
        self.console.print("[bold magenta]📈 Comparación de métricas del sistema[/bold magenta]\n")
        
        measurements = []
        
        try:
            # Tomar primera medición
            self.console.print("[cyan]Tomando primera medición...[/cyan]")
            first_measurement = self.take_measurement("Inicial")
            measurements.append(first_measurement)
            
            self.console.print("[green]✅ Primera medición completada[/green]\n")
            
            # Esperar y tomar segunda medición
            if Confirm.ask("¿Deseas tomar una segunda medición?", default=True):
                wait_time = IntPrompt.ask("¿Cuántos segundos esperar?", default=5)
                
                self.console.print(f"[yellow]Esperando {wait_time} segundos...[/yellow]")
                time.sleep(wait_time)
                
                self.console.print("[cyan]Tomando segunda medición...[/cyan]")
                second_measurement = self.take_measurement("Después de espera")
                measurements.append(second_measurement)
                
                self.console.print("[green]✅ Segunda medición completada[/green]\n")
            
            # Mostrar comparación
            if len(measurements) > 1:
                self.visualizer.show_comparison_table(measurements)
            else:
                self.console.print("[yellow]Se necesitan al menos 2 mediciones para comparar[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bold red]❌ Error en comparación: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def take_measurement(self, label: str) -> dict:
        """Tomar una medición del sistema"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Obtener métricas
        cpu_metrics = self.monitor.get_cpu_metrics()
        memory_metrics = self.monitor.get_memory_metrics()
        disk_metrics = self.monitor.get_disk_io_metrics()
        network_metrics = self.monitor.get_network_io_metrics()
        
        return {
            'timestamp': timestamp,
            'label': label,
            'cpu_percent': cpu_metrics['cpu_percent'],
            'memory_percent': memory_metrics['virtual_memory']['percent'],
            'disk_read_rate': disk_metrics.get('read_rate', 0),
            'disk_write_rate': disk_metrics.get('write_rate', 0),
            'network_sent_rate': network_metrics.get('sent_rate', 0),
            'network_recv_rate': network_metrics.get('recv_rate', 0)
        }
    
    def handle_advanced_tools(self):
        """Manejar herramientas avanzadas"""
        self.console.clear()
        
        tools_menu = """
[bold yellow]🔧 HERRAMIENTAS AVANZADAS[/bold yellow]

[yellow]Opciones disponibles:[/yellow]

[bold white]1.[/bold white] 📋 [cyan]Lista de procesos completa[/cyan]
[bold white]2.[/bold white] 🔍 [green]Buscar proceso por nombre[/green]
[bold white]3.[/bold white] 💽 [blue]Información de discos[/blue]
[bold white]4.[/bold white] 🌐 [magenta]Información de red[/magenta]
[bold white]5.[/bold white] 🧠 [yellow]Detalles de CPU[/yellow]
[bold white]6.[/bold white] 🔙 [dim]Volver al menú principal[/dim]
        """
        
        panel = Panel(tools_menu, title="[bold]HERRAMIENTAS AVANZADAS", border_style="yellow")
        self.console.print(panel)
        
        choice = IntPrompt.ask(
            "Selecciona una opción",
            choices=["1", "2", "3", "4", "5", "6"],
            default=6
        )
        
        if choice == 1:
            self.show_all_processes()
        elif choice == 2:
            self.search_process()
        elif choice == 3:
            self.show_disk_info()
        elif choice == 4:
            self.show_network_info()
        elif choice == 5:
            self.show_cpu_details()
        elif choice == 6:
            return
    
    def show_all_processes(self):
        """Mostrar lista completa de procesos"""
        self.console.print("[bold cyan]📋 Lista completa de procesos[/bold cyan]\n")
        
        try:
            processes = self.monitor.get_top_processes_by_cpu(limit=20)
            
            from rich.table import Table
            table = Table(title="Procesos del Sistema", box=box.ROUNDED)
            table.add_column("PID", style="cyan")
            table.add_column("Nombre", style="green")
            table.add_column("CPU %", style="red")
            table.add_column("Memoria %", style="blue")
            table.add_column("Estado", style="yellow")
            
            for proc in processes:
                table.add_row(
                    str(proc['pid']),
                    proc['name'][:30],
                    f"{proc['cpu_percent']:.1f}%",
                    f"{proc['memory_percent']:.1f}%",
                    proc.get('status', 'unknown')
                )
            
            self.console.print(table)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def search_process(self):
        """Buscar proceso por nombre"""
        process_name = Prompt.ask("[cyan]Introduce el nombre del proceso a buscar")
        
        if not process_name:
            return
        
        self.console.print(f"[yellow]Buscando procesos que contengan '{process_name}'...[/yellow]\n")
        
        try:
            all_processes = self.monitor.get_top_processes_by_cpu(limit=100)
            matching = [p for p in all_processes if process_name.lower() in p['name'].lower()]
            
            if matching:
                from rich.table import Table
                table = Table(title=f"Procesos encontrados: {process_name}", box=box.ROUNDED)
                table.add_column("PID", style="cyan")
                table.add_column("Nombre", style="green")
                table.add_column("CPU %", style="red")
                table.add_column("Memoria %", style="blue")
                
                for proc in matching:
                    table.add_row(
                        str(proc['pid']),
                        proc['name'],
                        f"{proc['cpu_percent']:.1f}%",
                        f"{proc['memory_percent']:.1f}%"
                    )
                
                self.console.print(table)
            else:
                self.console.print(f"[yellow]No se encontraron procesos con '{process_name}'[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def show_disk_info(self):
        """Mostrar información detallada de discos"""
        self.console.print("[bold blue]💽 Información detallada de discos[/bold blue]\n")
        
        try:
            import psutil
            
            from rich.table import Table
            table = Table(title="Uso de Discos", box=box.ROUNDED)
            table.add_column("Dispositivo", style="cyan")
            table.add_column("Punto de Montaje", style="green")
            table.add_column("Sistema de Archivos", style="blue")
            table.add_column("Total", style="yellow")
            table.add_column("Usado", style="red")
            table.add_column("Libre", style="green")
            table.add_column("Porcentaje", style="magenta")
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    table.add_row(
                        partition.device,
                        partition.mountpoint,
                        partition.fstype,
                        f"{usage.total / (1024**3):.1f} GB",
                        f"{usage.used / (1024**3):.1f} GB",
                        f"{usage.free / (1024**3):.1f} GB",
                        f"{(usage.used / usage.total) * 100:.1f}%"
                    )
                except PermissionError:
                    continue
            
            self.console.print(table)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def show_network_info(self):
        """Mostrar información de red"""
        self.console.print("[bold magenta]🌐 Información de red[/bold magenta]\n")
        
        try:
            import psutil
            
            # Interfaces de red
            from rich.table import Table
            table = Table(title="Interfaces de Red", box=box.ROUNDED)
            table.add_column("Interfaz", style="cyan")
            table.add_column("IP", style="green")
            table.add_column("Enviado", style="red")
            table.add_column("Recibido", style="blue")
            
            net_io = psutil.net_io_counters(pernic=True)
            net_if_addrs = psutil.net_if_addrs()
            
            for interface, stats in net_io.items():
                ip_addresses = []
                if interface in net_if_addrs:
                    for addr in net_if_addrs[interface]:
                        if addr.family == 2:  # IPv4
                            ip_addresses.append(addr.address)
                
                table.add_row(
                    interface,
                    ", ".join(ip_addresses) if ip_addresses else "N/A",
                    f"{stats.bytes_sent / (1024**2):.1f} MB",
                    f"{stats.bytes_recv / (1024**2):.1f} MB"
                )
            
            self.console.print(table)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def show_cpu_details(self):
        """Mostrar detalles de CPU"""
        self.console.print("[bold yellow]🧠 Detalles de CPU[/bold yellow]\n")
        
        try:
            import psutil
            
            # Información de CPU
            from rich.table import Table
            
            # Tabla general
            general_table = Table(title="Información General de CPU", box=box.ROUNDED)
            general_table.add_column("Métrica", style="cyan")
            general_table.add_column("Valor", style="green")
            
            general_table.add_row("Núcleos Físicos", str(psutil.cpu_count(logical=False)))
            general_table.add_row("Núcleos Lógicos", str(psutil.cpu_count(logical=True)))
            
            freq = psutil.cpu_freq()
            if freq:
                general_table.add_row("Frecuencia Actual", f"{freq.current:.0f} MHz")
                general_table.add_row("Frecuencia Máxima", f"{freq.max:.0f} MHz")
                general_table.add_row("Frecuencia Mínima", f"{freq.min:.0f} MHz")
            
            self.console.print(general_table)
            
            # Tabla por núcleo
            self.console.print("\n")
            core_table = Table(title="Uso por Núcleo", box=box.ROUNDED)
            core_table.add_column("Núcleo", style="cyan")
            core_table.add_column("Uso %", style="red")
            core_table.add_column("Estado", style="yellow")
            
            cpu_per_core = psutil.cpu_percent(percpu=True, interval=1)
            for i, usage in enumerate(cpu_per_core):
                status = "🟢 Normal" if usage < 70 else "🟡 Alto" if usage < 90 else "🔴 Crítico"
                core_table.add_row(f"Núcleo {i}", f"{usage:.1f}%", status)
            
            self.console.print(core_table)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def handle_system_info(self):
        """Mostrar información general del sistema"""
        self.console.clear()
        self.console.print("[bold dim]ℹ️  Información del sistema[/bold dim]\n")
        
        try:
            import psutil
            import platform
            
            from rich.table import Table
            table = Table(title="Información del Sistema", box=box.ROUNDED)
            table.add_column("Atributo", style="cyan")
            table.add_column("Valor", style="green")
            
            # Información del sistema
            table.add_row("Sistema Operativo", platform.system())
            table.add_row("Versión del SO", platform.release())
            table.add_row("Arquitectura", platform.machine())
            table.add_row("Procesador", platform.processor())
            table.add_row("Nombre del equipo", platform.node())
            
            # Tiempo de arranque
            boot_time = psutil.boot_time()
            boot_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(boot_time))
            table.add_row("Último arranque", boot_time_str)
            
            # Usuarios conectados
            users = psutil.users()
            user_names = [user.name for user in users]
            table.add_row("Usuarios conectados", ", ".join(set(user_names)) if user_names else "Ninguno")
            
            self.console.print(table)
            
        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        self.wait_for_continue()
    
    def wait_for_continue(self):
        """Esperar a que el usuario presione Enter para continuar"""
        self.console.print("\n")
        Prompt.ask("[dim]Presiona Enter para continuar", default="", show_default=False)
    
    def run(self):
        """Ejecutar aplicación principal"""
        try:
            # Pantalla de bienvenida
            self.console.clear()
            self.visualizer.show_welcome_screen()
            time.sleep(2)
            
            while self.running:
                self.console.clear()
                self.show_main_menu()
                
                try:
                    choice = IntPrompt.ask(
                        "Selecciona una opción",
                        choices=["1", "2", "3", "4", "5", "6", "7"],
                        default=7
                    )
                    
                    if choice == 1:
                        self.handle_system_summary()
                    elif choice == 2:
                        self.handle_live_monitoring()
                    elif choice == 3:
                        self.handle_profiling()
                    elif choice == 4:
                        self.handle_metrics_comparison()
                    elif choice == 5:
                        self.handle_advanced_tools()
                    elif choice == 6:
                        self.handle_system_info()
                    elif choice == 7:
                        self.running = False
                        
                except KeyboardInterrupt:
                    self.console.print("\n[bold yellow]🔙 Regresando al menú principal...[/bold yellow]")
                    time.sleep(1)
            
            # Mensaje de despedida
            self.console.print("\n[bold green]¡Gracias por usar el Analizador de Rendimiento![/bold green]")
            self.console.print("[dim]Hasta luego! 👋[/dim]\n")
            
        except KeyboardInterrupt:
            self.console.print("\n\n[bold red]🛑 Aplicación terminada por el usuario[/bold red]")
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n[bold red]❌ Error fatal: {e}[/bold red]")
            sys.exit(1)


@click.command()
@click.option('--refresh-rate', '-r', default=2.0, help='Frecuencia de actualización en segundos')
@click.option('--live', '-l', is_flag=True, help='Iniciar directamente en modo monitoreo en tiempo real')
def main(refresh_rate: float, live: bool):
    """
    🖥️ Analizador de Rendimiento del Sistema
    
    Aplicación de terminal para monitorear el rendimiento del sistema
    con interfaces coloridas y atractivas.
    """
    app = TerminalApp()
    
    if live:
        # Modo directo de monitoreo
        console = Console()
        console.clear()
        console.print("[bold green]🚀 Modo monitoreo directo[/bold green]")
        console.print("[dim]Presiona Ctrl+C para salir[/dim]\n")
        
        try:
            app.visualizer.start_live_monitoring(refresh_rate)
        except KeyboardInterrupt:
            console.print("\n[bold red]🛑 Monitoreo terminado[/bold red]")
    else:
        # Modo interactivo normal
        app.run()


if __name__ == "__main__":
    main() 