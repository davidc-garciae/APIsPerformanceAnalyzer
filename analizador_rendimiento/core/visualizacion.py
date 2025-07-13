"""
Módulo de visualización para mostrar métricas del sistema en la terminal
usando la librería rich para interfaces coloridas y atractivas.
"""

import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.tree import Tree
from rich.text import Text
from rich.columns import Columns
from rich import box
from rich.align import Align
from rich.spinner import Spinner

from .monitoring import SystemMonitor
from .profiling import CodeProfiler


@dataclass
class MetricHistory:
    """Historial de métricas para gráficos temporales"""
    timestamps: List[datetime] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    max_size: int = 50
    
    def add_value(self, value: float):
        self.timestamps.append(datetime.now())
        self.values.append(value)
        
        # Mantener solo los últimos max_size valores
        if len(self.values) > self.max_size:
            self.timestamps.pop(0)
            self.values.pop(0)


class SystemVisualizer:
    """Visualizador del sistema con rich"""
    
    def __init__(self):
        self.console = Console()
        self.monitor = SystemMonitor()
        self.profiler = CodeProfiler()
        
        # Historial de métricas
        self.cpu_history = MetricHistory()
        self.memory_history = MetricHistory()
        self.disk_io_history = MetricHistory()
        
        # Estado de monitoreo
        self.monitoring = False
        self.monitor_thread = None
    
    def create_header(self) -> Panel:
        """Crear encabezado del dashboard"""
        title = Text("🖥️  MONITOR DE RENDIMIENTO DEL SISTEMA", style="bold magenta")
        subtitle = Text(f"Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
        
        header_content = Align.center(f"{title}\n{subtitle}")
        return Panel(header_content, box=box.DOUBLE, style="bright_blue")
    
    def create_cpu_panel(self) -> Panel:
        """Crear panel de información de CPU"""
        cpu_metrics = self.monitor.get_cpu_metrics()
        
        # Tabla de CPU
        cpu_table = Table(title="CPU", box=box.ROUNDED)
        cpu_table.add_column("Métrica", style="cyan")
        cpu_table.add_column("Valor", style="green")
        cpu_table.add_column("Estado", style="yellow")
        
        # CPU total
        cpu_percent = cpu_metrics['cpu_percent_total']
        status = self._get_status_color(cpu_percent, 70, 90)
        cpu_table.add_row("Uso Total", f"{cpu_percent:.1f}%", status)
        
        # Frecuencia
        freq = cpu_metrics['cpu_frequency']
        if freq:
            cpu_table.add_row("Frecuencia", f"{freq['current']:.0f} MHz", "🔄")
        
        # Cores
        cores = cpu_metrics['cpu_count']['logical']
        cpu_table.add_row("Núcleos", str(cores), "🧠")
        
        # Barra de progreso para CPU
        progress_bar = self._create_progress_bar(cpu_percent, 100, "CPU")
        
        content = f"{cpu_table}\n\n{progress_bar}"
        return Panel(content, title="[bold]🔥 CPU", border_style="red")
    
    def create_memory_panel(self) -> Panel:
        """Crear panel de información de memoria"""
        memory_metrics = self.monitor.get_memory_metrics()
        
        # Memoria RAM
        ram = memory_metrics['ram']
        memory_table = Table(title="Memoria", box=box.ROUNDED)
        memory_table.add_column("Tipo", style="cyan")
        memory_table.add_column("Usado", style="green")
        memory_table.add_column("Total", style="blue")
        memory_table.add_column("Porcentaje", style="yellow")
        
        # Convertir bytes a GB
        ram_used_gb = ram['used'] / (1024**3)
        ram_total_gb = ram['total'] / (1024**3)
        ram_percent = ram['percentage']
        
        memory_table.add_row(
            "RAM",
            f"{ram_used_gb:.1f} GB",
            f"{ram_total_gb:.1f} GB",
            f"{ram_percent:.1f}%"
        )
        
        # Swap si está disponible
        if 'swap' in memory_metrics:
            swap = memory_metrics['swap']
            swap_used_gb = swap['used'] / (1024**3)
            swap_total_gb = swap['total'] / (1024**3)
            swap_percent = swap['percentage']
            
            memory_table.add_row(
                "SWAP",
                f"{swap_used_gb:.1f} GB",
                f"{swap_total_gb:.1f} GB",
                f"{swap_percent:.1f}%"
            )
        
        # Barra de progreso para memoria
        progress_bar = self._create_progress_bar(ram_percent, 100, "RAM")
        
        content = f"{memory_table}\n\n{progress_bar}"
        return Panel(content, title="[bold]💾 MEMORIA", border_style="green")
    
    def create_disk_panel(self) -> Panel:
        """Crear panel de información de disco"""
        disk_metrics = self.monitor.get_disk_io_metrics()
        
        disk_table = Table(title="E/S de Disco", box=box.ROUNDED)
        disk_table.add_column("Métrica", style="cyan")
        disk_table.add_column("Valor", style="green")
        
        # Convertir bytes a MB/s
        read_rate = disk_metrics.get('disk_io_rates', {}).get('read_bytes_per_sec', 0) / (1024**2)
        write_rate = disk_metrics.get('disk_io_rates', {}).get('write_bytes_per_sec', 0) / (1024**2)
        
        disk_table.add_row("Lectura", f"{read_rate:.2f} MB/s")
        disk_table.add_row("Escritura", f"{write_rate:.2f} MB/s")
        disk_table.add_row("Total Lecturas", f"{disk_metrics['disk_io_counters']['read_bytes'] / (1024**3):.2f} GB")
        disk_table.add_row("Total Escrituras", f"{disk_metrics['disk_io_counters']['write_bytes'] / (1024**3):.2f} GB")
        
        return Panel(disk_table, title="[bold]💿 DISCO", border_style="blue")
    
    def create_network_panel(self) -> Panel:
        """Crear panel de información de red"""
        network_metrics = self.monitor.get_network_io_metrics()
        
        network_table = Table(title="E/S de Red", box=box.ROUNDED)
        network_table.add_column("Métrica", style="cyan")
        network_table.add_column("Valor", style="green")
        
        # Convertir bytes a MB/s
        sent_rate = network_metrics.get('network_io_rates', {}).get('bytes_sent_per_sec', 0) / (1024**2)
        recv_rate = network_metrics.get('network_io_rates', {}).get('bytes_recv_per_sec', 0) / (1024**2)
        
        network_table.add_row("Enviado", f"{sent_rate:.2f} MB/s")
        network_table.add_row("Recibido", f"{recv_rate:.2f} MB/s")
        network_table.add_row("Total Enviado", f"{network_metrics['network_io_counters']['bytes_sent'] / (1024**3):.2f} GB")
        network_table.add_row("Total Recibido", f"{network_metrics['network_io_counters']['bytes_recv'] / (1024**3):.2f} GB")
        
        return Panel(network_table, title="[bold]🌐 RED", border_style="yellow")
    
    def create_processes_panel(self) -> Panel:
        """Crear panel de procesos top"""
        processes = self.monitor.get_top_processes_by_cpu(limit=5)
        
        proc_table = Table(title="Top 5 Procesos (CPU)", box=box.ROUNDED)
        proc_table.add_column("PID", style="cyan")
        proc_table.add_column("Nombre", style="green")
        proc_table.add_column("CPU %", style="red")
        proc_table.add_column("Memoria %", style="blue")
        
        for proc in processes:
            proc_table.add_row(
                str(proc['pid']),
                proc['name'][:20],  # Truncar nombres largos
                f"{proc['cpu_percent']:.1f}%",
                f"{proc['memory_percent']:.1f}%"
            )
        
        return Panel(proc_table, title="[bold]⚡ PROCESOS", border_style="magenta")
    
    def _create_progress_bar(self, value: float, max_value: float, label: str) -> str:
        """Crear una barra de progreso visual"""
        percentage = (value / max_value) * 100
        bar_length = 30
        filled_length = int(bar_length * value / max_value)
        
        # Colores según el porcentaje
        if percentage < 50:
            color = "green"
        elif percentage < 80:
            color = "yellow"
        else:
            color = "red"
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"[{color}]{bar}[/{color}] {percentage:.1f}%"
    
    def _get_status_color(self, value: float, warning_threshold: float, critical_threshold: float) -> str:
        """Obtener color de estado según thresholds"""
        if value < warning_threshold:
            return "🟢 Normal"
        elif value < critical_threshold:
            return "🟡 Alerta"
        else:
            return "🔴 Crítico"
    
    def show_system_summary(self):
        """Mostrar resumen del sistema"""
        summary = self.monitor.get_system_summary()
        
        self.console.print("\n")
        self.console.print(self.create_header())
        
        # Layout en columnas
        layout = Layout()
        layout.split_column(
            Layout(name="top", size=3),
            Layout(name="middle"),
            Layout(name="bottom", size=8)
        )
        
        layout["top"].update(self.create_header())
        
        # División en 2x2 para métricas principales
        layout["middle"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["middle"]["left"].split_column(
            Layout(self.create_cpu_panel()),
            Layout(self.create_memory_panel())
        )
        
        layout["middle"]["right"].split_column(
            Layout(self.create_disk_panel()),
            Layout(self.create_network_panel())
        )
        
        layout["bottom"].update(self.create_processes_panel())
        
        self.console.print(layout)
    
    def start_live_monitoring(self, refresh_rate: float = 2.0):
        """Iniciar monitoreo en tiempo real"""
        def generate_layout():
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="footer", size=8)
            )
            
            layout["header"].update(self.create_header())
            
            layout["main"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
            
            layout["main"]["left"].split_column(
                Layout(self.create_cpu_panel()),
                Layout(self.create_memory_panel())
            )
            
            layout["main"]["right"].split_column(
                Layout(self.create_disk_panel()),
                Layout(self.create_network_panel())
            )
            
            layout["footer"].update(self.create_processes_panel())
            
            return layout
        
        try:
            with Live(generate_layout(), refresh_per_second=1/refresh_rate, screen=True) as live:
                self.console.print("\n[bold green]🚀 Monitoreo en tiempo real iniciado[/bold green]")
                self.console.print("[dim]Presiona Ctrl+C para salir[/dim]\n")
                
                while True:
                    live.update(generate_layout())
                    time.sleep(refresh_rate)
                    
        except KeyboardInterrupt:
            self.console.print("\n[bold red]🛑 Monitoreo detenido[/bold red]")
    
    def show_profiling_results(self, profile_results: Dict[str, Any]):
        """Mostrar resultados de profiling de forma visual"""
        self.console.print("\n")
        
        # Panel principal
        title = Text("📊 RESULTADOS DE PROFILING", style="bold cyan")
        self.console.print(Panel(title, box=box.DOUBLE))
        
        # Información general
        info_table = Table(title="Información General", box=box.ROUNDED)
        info_table.add_column("Métrica", style="cyan")
        info_table.add_column("Valor", style="green")
        
        if 'execution_time' in profile_results:
            info_table.add_row("Tiempo de Ejecución", f"{profile_results['execution_time']:.3f}s")
        
        if 'total_calls' in profile_results:
            info_table.add_row("Total de Llamadas", f"{profile_results['total_calls']:,}")
        
        if 'memory_usage' in profile_results:
            info_table.add_row("Uso de Memoria", f"{profile_results['memory_usage']:.2f} MB")
        
        self.console.print(info_table)
        
        # Top funciones si están disponibles
        if 'top_functions' in profile_results:
            self.console.print("\n")
            func_table = Table(title="Top Funciones (por tiempo)", box=box.ROUNDED)
            func_table.add_column("Función", style="cyan")
            func_table.add_column("Llamadas", style="yellow")
            func_table.add_column("Tiempo Total", style="red")
            func_table.add_column("Tiempo/Llamada", style="green")
            
            for func in profile_results['top_functions'][:10]:  # Top 10
                func_table.add_row(
                    func.get('name', 'Unknown')[:50],  # Truncar nombres largos
                    f"{func.get('calls', 0):,}",
                    f"{func.get('tottime', 0):.3f}s",
                    f"{func.get('tottime', 0)/max(func.get('calls', 1), 1)*1000:.2f}ms"
                )
            
            self.console.print(func_table)
    
    def show_comparison_table(self, comparisons: List[Dict[str, Any]]):
        """Mostrar tabla de comparación de métricas"""
        if not comparisons:
            self.console.print("[yellow]No hay datos de comparación disponibles[/yellow]")
            return
        
        # Crear tabla de comparación
        comp_table = Table(title="Comparación de Métricas", box=box.HEAVY)
        comp_table.add_column("Métrica", style="cyan")
        
        # Agregar columnas para cada timestamp
        for i, comp in enumerate(comparisons):
            timestamp = comp.get('timestamp', f'Medición {i+1}')
            comp_table.add_column(f"T{i+1}\n{timestamp}", style="green")
        
        # Métricas a comparar
        metrics_to_show = ['cpu_percent_total', 'memory_percent', 'disk_read_rate', 'network_sent_rate']
        
        for metric in metrics_to_show:
            row_data = [metric.replace('_', ' ').title()]
            
            for comp in comparisons:
                value = comp.get(metric, 'N/A')
                if isinstance(value, (int, float)):
                    row_data.append(f"{value:.2f}")
                else:
                    row_data.append(str(value))
            
            comp_table.add_row(*row_data)
        
        self.console.print("\n")
        self.console.print(comp_table)
    
    def show_welcome_screen(self):
        """Mostrar pantalla de bienvenida"""
        welcome_text = """
[bold cyan]🖥️  ANALIZADOR DE RENDIMIENTO DEL SISTEMA[/bold cyan]

[green]✅ Sistema de monitoreo iniciado correctamente[/green]

[yellow]Opciones disponibles:[/yellow]
1. 📊 Resumen del sistema
2. ⚡ Monitoreo en tiempo real  
3. 🔍 Profiling de código
4. 📈 Comparación de métricas
5. 🚪 Salir

[dim]Desarrollado para el curso de Sistemas Operativos[/dim]
        """
        
        panel = Panel(
            welcome_text,
            title="[bold]BIENVENIDO",
            border_style="bright_blue",
            box=box.DOUBLE
        )
        
        self.console.print(panel) 