#!/usr/bin/env python3
"""
Visualizador de métricas de APIs usando Rich
Crea tablas, gráficos y paneles específicos para el rendimiento de APIs
"""

import time
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.columns import Columns
from rich import box
from rich.align import Align

from .api_monitor import APIMonitor, APIStats, APIMetric, PokemonAPIMonitor


class APIVisualizer:
    """Visualizador de métricas de APIs"""
    
    def __init__(self):
        self.console = Console()
    
    def create_api_summary_panel(self, stats: APIStats, api_name: str = "API") -> Panel:
        """Crear panel resumen de estadísticas de API"""
        
        # Tabla principal de estadísticas
        stats_table = Table(title=f"Resumen de {api_name}", box=box.ROUNDED)
        stats_table.add_column("Métrica", style="cyan")
        stats_table.add_column("Valor", style="green")
        stats_table.add_column("Estado", style="yellow")
        
        # Determinar estado de disponibilidad
        availability_status = "🟢 Excelente" if stats.availability_percentage >= 99 else \
                            "🟡 Bueno" if stats.availability_percentage >= 95 else \
                            "🔴 Problemático"
        
        # Determinar estado de tiempo de respuesta
        response_status = "🟢 Rápido" if stats.avg_response_time < 0.5 else \
                         "🟡 Aceptable" if stats.avg_response_time < 2.0 else \
                         "🔴 Lento"
        
        stats_table.add_row("Total Peticiones", f"{stats.total_requests:,}", "📊")
        stats_table.add_row("Peticiones Exitosas", f"{stats.successful_requests:,}", "✅")
        stats_table.add_row("Peticiones Fallidas", f"{stats.failed_requests:,}", "❌")
        stats_table.add_row("Disponibilidad", f"{stats.availability_percentage:.2f}%", availability_status)
        stats_table.add_row("Tiempo Resp. Promedio", f"{stats.avg_response_time:.3f}s", response_status)
        stats_table.add_row("Throughput", f"{stats.throughput_per_second:.2f} req/s", "⚡")
        
        if stats.total_data_transferred > 0:
            data_mb = stats.total_data_transferred / (1024 * 1024)
            stats_table.add_row("Datos Transferidos", f"{data_mb:.2f} MB", "📦")
        
        return Panel(stats_table, title=f"[bold]🌐 {api_name.upper()}", border_style="blue")
    
    def create_performance_panel(self, stats: APIStats) -> Panel:
        """Crear panel de métricas de rendimiento detalladas"""
        
        perf_table = Table(title="Rendimiento Detallado", box=box.ROUNDED)
        perf_table.add_column("Métrica", style="cyan")
        perf_table.add_column("Valor", style="green")
        perf_table.add_column("Descripción", style="dim")
        
        if stats.min_response_time != float('inf'):
            perf_table.add_row("Tiempo Mínimo", f"{stats.min_response_time:.3f}s", "Mejor caso")
            perf_table.add_row("Tiempo Máximo", f"{stats.max_response_time:.3f}s", "Peor caso")
            
            if stats.percentile_95 > 0:
                perf_table.add_row("Percentil 95", f"{stats.percentile_95:.3f}s", "95% de peticiones")
        
        return Panel(perf_table, title="[bold]⚡ RENDIMIENTO", border_style="yellow")
    
    def create_endpoints_table(self, endpoints_data: Dict[str, Dict]) -> Table:
        """Crear tabla de estadísticas por endpoint"""
        
        table = Table(title="Estadísticas por Endpoint", box=box.ROUNDED)
        table.add_column("Endpoint", style="cyan")
        table.add_column("Peticiones", style="green", justify="right")
        table.add_column("Tiempo Promedio", style="yellow", justify="right")
        table.add_column("Disponibilidad", style="blue", justify="right")
        table.add_column("Throughput", style="magenta", justify="right")
        
        for endpoint, data in endpoints_data.items():
            # Acortar el endpoint para mejor visualización
            short_endpoint = endpoint.split('/')[-2:] if '/' in endpoint else [endpoint]
            display_endpoint = '/'.join(short_endpoint)
            
            table.add_row(
                display_endpoint,
                f"{data['total_requests']:,}",
                f"{data['avg_response_time']:.3f}s",
                f"{data['availability']:.1f}%",
                f"{data['throughput']:.2f} req/s"
            )
        
        return table
    
    def create_errors_panel(self, errors_data: Dict[str, int]) -> Panel:
        """Crear panel de errores comunes"""
        
        if not errors_data:
            return Panel(
                "[green]🎉 No se encontraron errores![/green]", 
                title="[bold]❌ ERRORES", 
                border_style="green"
            )
        
        errors_table = Table(title="Errores Más Comunes", box=box.ROUNDED)
        errors_table.add_column("Error", style="red")
        errors_table.add_column("Ocurrencias", style="yellow", justify="right")
        errors_table.add_column("Porcentaje", style="blue", justify="right")
        
        total_errors = sum(errors_data.values())
        
        for error, count in errors_data.items():
            percentage = (count / total_errors) * 100
            errors_table.add_row(
                error,
                f"{count:,}",
                f"{percentage:.1f}%"
            )
        
        return Panel(errors_table, title="[bold]❌ ERRORES", border_style="red")
    
    def show_api_report(self, monitor: APIMonitor, api_name: str = "API"):
        """Mostrar reporte completo de una API"""
        
        report = monitor.get_detailed_report()
        stats = monitor.get_stats()
        
        # Panel principal de resumen
        summary_panel = self.create_api_summary_panel(stats, api_name)
        
        # Panel de rendimiento
        performance_panel = self.create_performance_panel(stats)
        
        # Tabla de endpoints
        if report['endpoints']:
            endpoints_table = self.create_endpoints_table(report['endpoints'])
        else:
            endpoints_table = Table(title="No hay datos de endpoints")
        
        # Panel de errores
        errors_panel = self.create_errors_panel(report['errors'])
        
        # Layout
        self.console.print(summary_panel)
        self.console.print()
        
        # Mostrar rendimiento y errores lado a lado si hay espacio
        columns = Columns([performance_panel, errors_panel], equal=True)
        self.console.print(columns)
        self.console.print()
        
        # Tabla de endpoints
        self.console.print(endpoints_table)
    
    def show_live_monitoring(self, monitor: APIMonitor, api_name: str = "API", 
                           refresh_rate: float = 2.0):
        """Mostrar monitoreo en vivo de la API"""
        
        def generate_layout():
            stats = monitor.get_stats()
            report = monitor.get_detailed_report()
            
            # Crear layout
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main", ratio=1),
                Layout(name="footer", size=3)
            )
            
            # Header
            header_text = Text(f"🌐 MONITOREO EN VIVO - {api_name.upper()}", style="bold cyan")
            layout["header"].update(Panel(Align.center(header_text), box=box.DOUBLE))
            
            # Main content
            layout["main"].split_row(
                Layout(name="left"),
                Layout(name="right")
            )
            
            layout["left"].split_column(
                Layout(self.create_api_summary_panel(stats, api_name)),
                Layout(self.create_performance_panel(stats))
            )
            
            layout["right"].split_column(
                Layout(self.create_errors_panel(report['errors'])),
                Layout(Panel(
                    f"[green]Última actualización: {time.strftime('%H:%M:%S')}[/green]\n"
                    f"[blue]Métricas recolectadas: {len(monitor.metrics):,}[/blue]",
                    title="[bold]📊 ESTADO",
                    border_style="green"
                ))
            )
            
            # Footer
            footer_text = Text("Presiona Ctrl+C para detener el monitoreo", style="dim")
            layout["footer"].update(Panel(Align.center(footer_text)))
            
            return layout
        
        try:
            with Live(generate_layout(), refresh_per_second=1/refresh_rate, screen=True):
                while True:
                    time.sleep(refresh_rate)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Monitoreo detenido por el usuario[/yellow]")
    
    def show_load_test_progress(self, total_requests: int, concurrent_requests: int):
        """Mostrar progreso de test de carga"""
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeRemainingColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task(
                f"🔥 Test de carga ({concurrent_requests} concurrentes)", 
                total=total_requests
            )
            
            # Esta función debería ser llamada desde el monitor
            # por ahora solo mostramos la barra
            for i in range(total_requests):
                progress.update(task, advance=1)
                time.sleep(0.01)  # Simular progreso
    
    def create_comparison_table(self, comparisons: List[Dict[str, Any]]) -> Table:
        """Crear tabla de comparación entre diferentes tests"""
        
        table = Table(title="Comparación de Tests", box=box.ROUNDED)
        table.add_column("Test", style="cyan")
        table.add_column("Fecha/Hora", style="dim")
        table.add_column("Peticiones", style="green", justify="right")
        table.add_column("Tiempo Promedio", style="yellow", justify="right")
        table.add_column("Disponibilidad", style="blue", justify="right")
        table.add_column("Throughput", style="magenta", justify="right")
        
        for i, comparison in enumerate(comparisons, 1):
            stats = comparison.get('stats', {})
            table.add_row(
                f"Test #{i}",
                comparison.get('timestamp', 'N/A'),
                f"{stats.get('total_requests', 0):,}",
                f"{stats.get('avg_response_time', 0):.3f}s",
                f"{stats.get('availability_percentage', 0):.1f}%",
                f"{stats.get('throughput_per_second', 0):.2f} req/s"
            )
        
        return table


class PokemonAPIVisualizer(APIVisualizer):
    """Visualizador específico para PokéAPI"""
    
    def show_pokemon_endpoints_test(self, results: Dict[str, APIMetric]):
        """Mostrar resultados de test de endpoints de Pokémon"""
        
        self.console.print(Panel(
            "[bold cyan]🔍 PRUEBA DE ENDPOINTS POKÉAPI[/bold cyan]",
            box=box.DOUBLE
        ))
        
        # Tabla de resultados
        table = Table(title="Resultados por Endpoint", box=box.ROUNDED)
        table.add_column("Endpoint", style="cyan")
        table.add_column("Tiempo de Respuesta", style="green", justify="right")
        table.add_column("Código de Estado", style="yellow", justify="center")
        table.add_column("Tamaño Respuesta", style="blue", justify="right")
        table.add_column("Estado", style="bold")
        
        for endpoint_name, metric in results.items():
            status_icon = "✅" if metric.success else "❌"
            status_color = "green" if metric.success else "red"
            
            table.add_row(
                endpoint_name,
                f"{metric.response_time:.3f}s",
                str(metric.status_code),
                f"{metric.response_size:,} bytes",
                f"[{status_color}]{status_icon}[/{status_color}]"
            )
        
        self.console.print(table)
        
        # Estadísticas resumidas
        successful = sum(1 for m in results.values() if m.success)
        total = len(results)
        avg_time = sum(m.response_time for m in results.values()) / total if total > 0 else 0
        
        summary = f"""
[green]✅ Endpoints exitosos: {successful}/{total}[/green]
[blue]📊 Tiempo promedio: {avg_time:.3f}s[/blue]
[yellow]📦 PokéAPI está {'🟢 operacional' if successful == total else '🟡 con problemas'}[/yellow]
        """
        
        self.console.print(Panel(summary, title="[bold]📈 RESUMEN", border_style="green"))
    
    def show_stress_test_results(self, results: Dict[str, Any]):
        """Mostrar resultados del test de estrés de PokéAPI"""
        
        self.console.print(Panel(
            "[bold red]🔥 RESULTADOS DEL TEST DE ESTRÉS - POKÉAPI[/bold red]",
            box=box.DOUBLE
        ))
        
        stats = results['stats']
        
        # Crear resumen del test
        summary_table = Table(title="Configuración del Test", box=box.ROUNDED)
        summary_table.add_column("Parámetro", style="cyan")
        summary_table.add_column("Valor", style="green")
        
        summary_table.add_row("Endpoint Probado", results['endpoint_tested'])
        summary_table.add_row("Total de Peticiones", f"{results['total_requests']:,}")
        summary_table.add_row("Usuarios Concurrentes", f"{results['concurrent_users']:,}")
        summary_table.add_row("Peticiones por Usuario", f"{results['total_requests'] // results['concurrent_users']:,}")
        
        self.console.print(summary_table)
        self.console.print()
        
        # Mostrar estadísticas detalladas de forma simplificada
        total_time = results.get('total_time', 0)
        success_rate = results.get('success_rate', 0)
        
        summary_text = (
            "[bold green]✅ Test de estrés completado exitosamente[/bold green]\n"
            f"[yellow]• Total peticiones:[/yellow] {results.get('total_requests', 'N/A')}\n"
            f"[yellow]• Usuarios concurrentes:[/yellow] {results.get('concurrent_users', 'N/A')}\n"
            f"[yellow]• Tiempo total:[/yellow] {total_time:.2f}s\n"
            f"[yellow]• Tasa de éxito:[/yellow] {success_rate:.1f}%"
        )
        
        self.console.print(Panel.fit(
            summary_text,
            title="📊 [bold]Resumen Final[/bold]",
            border_style="green"
        ))
        
        # Análisis de rendimiento bajo carga
        analysis = f"""
[bold]🎯 ANÁLISIS DEL TEST DE ESTRÉS:[/bold]

[green]✅ Disponibilidad: {stats.availability_percentage:.2f}%[/green]
[blue]⚡ Throughput: {stats.throughput_per_second:.2f} peticiones/segundo[/blue]
[yellow]📊 Tiempo promedio: {stats.avg_response_time:.3f}s[/yellow]

[bold]💡 Conclusiones:[/bold]
- {"🟢 PokéAPI maneja bien la carga" if stats.availability_percentage >= 95 else "🔴 PokéAPI tiene problemas bajo carga"}
- {"🟢 Tiempo de respuesta aceptable" if stats.avg_response_time < 2.0 else "🔴 Tiempo de respuesta alto"}
- {"🟢 Throughput satisfactorio" if stats.throughput_per_second >= 10 else "🟡 Throughput limitado"}
        """
        
        self.console.print(Panel(analysis, title="[bold]📈 ANÁLISIS", border_style="blue"))


# Instancia global del visualizador
api_visualizer = APIVisualizer()
pokemon_visualizer = PokemonAPIVisualizer() 