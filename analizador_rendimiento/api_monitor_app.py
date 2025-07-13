#!/usr/bin/env python3
"""
Aplicación de terminal para monitorear el rendimiento de APIs externas
Interfaz específica para testing de APIs con Rich
"""

import sys
import asyncio
import time
import click
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich import box

from core.api_monitor import APIMonitor, PokemonAPIMonitor
from core.api_visualizer import APIVisualizer, PokemonAPIVisualizer


class APIMonitorApp:
    """Aplicación principal para monitoreo de APIs"""
    
    def __init__(self):
        self.console = Console()
        self.api_monitor = APIMonitor()
        self.pokemon_monitor = PokemonAPIMonitor()
        self.api_visualizer = APIVisualizer()
        self.pokemon_visualizer = PokemonAPIVisualizer()
        self.running = True
    
    def show_main_menu(self):
        """Mostrar menú principal"""
        menu_text = """
[bold cyan]🌐 ANALIZADOR DE RENDIMIENTO DE APIs[/bold cyan]

[green]✅ Sistema de monitoreo de APIs iniciado correctamente[/green]

[yellow]Opciones disponibles:[/yellow]

[bold white]1.[/bold white] 🔍 [cyan]Probar endpoint individual[/cyan]
[bold white]2.[/bold white] 🔥 [red]Test de carga personalizado[/red]
[bold white]3.[/bold white] 📊 [blue]Monitoreo continuo[/blue]
[bold white]4.[/bold white] 🐱 [yellow]Tests específicos de PokéAPI[/yellow]
[bold white]5.[/bold white] 📈 [magenta]Ver reportes y estadísticas[/magenta]
[bold white]6.[/bold white] 🔄 [green]Comparar tests[/green]
[bold white]7.[/bold white] 🧹 [dim]Limpiar métricas[/dim]
[bold white]8.[/bold white] 🚪 [red]Salir[/red]

[dim]Especializado en análisis de rendimiento de APIs REST[/dim]
"""
        
        panel = Panel(
            menu_text,
            title="[bold]MENÚ PRINCIPAL - API MONITOR",
            border_style="bright_blue",
            box=box.DOUBLE
        )
        
        self.console.clear()
        self.console.print(panel)
    
    def handle_single_endpoint_test(self):
        """Manejar prueba de endpoint individual"""
        self.console.print(Panel(
            "[bold cyan]🔍 PRUEBA DE ENDPOINT INDIVIDUAL[/bold cyan]",
            box=box.DOUBLE
        ))
        
        # Obtener URL del usuario
        url = Prompt.ask("🌐 Ingresa la URL del endpoint")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        method = Prompt.ask("📝 Método HTTP", choices=['GET', 'POST', 'PUT', 'DELETE'], default='GET')
        
        async def run_test():
            self.console.print(f"🚀 Probando: [blue]{url}[/blue]")
            
            with self.console.status("[yellow]Ejecutando petición...[/yellow]"):
                metric = await self.api_monitor.test_single_endpoint(url, method)
            
            # Mostrar resultado
            if metric.success:
                result_text = f"""
[green]✅ Petición exitosa[/green]

[cyan]📊 Métricas:[/cyan]
• Tiempo de respuesta: [yellow]{metric.response_time:.3f}s[/yellow]
• Código de estado: [green]{metric.status_code}[/green]
• Tamaño de respuesta: [blue]{metric.response_size:,} bytes[/blue]
• Timestamp: [dim]{metric.timestamp.strftime('%Y-%m-%d %H:%M:%S')}[/dim]
                """
            else:
                result_text = f"""
[red]❌ Petición fallida[/red]

[cyan]📊 Detalles del error:[/cyan]
• Tiempo transcurrido: [yellow]{metric.response_time:.3f}s[/yellow]
• Error: [red]{metric.error_message}[/red]
• Timestamp: [dim]{metric.timestamp.strftime('%Y-%m-%d %H:%M:%S')}[/dim]
                """
            
            self.console.print(Panel(result_text, border_style="green" if metric.success else "red"))
        
        asyncio.run(run_test())
        self.wait_for_continue()
    
    def handle_load_test(self):
        """Manejar test de carga personalizado"""
        self.console.print(Panel(
            "[bold red]🔥 TEST DE CARGA PERSONALIZADO[/bold red]",
            box=box.DOUBLE
        ))
        
        # Configuración del test
        url = Prompt.ask("🌐 URL del endpoint")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        total_requests = IntPrompt.ask("📊 Total de peticiones", default=100)
        concurrent_requests = IntPrompt.ask("⚡ Peticiones concurrentes", default=10)
        delay = float(Prompt.ask("⏱️ Delay entre peticiones (segundos)", default="0.1"))
        
        async def run_load_test():
            self.console.print(f"""
[cyan]🎯 Configuración del test:[/cyan]
• URL: [blue]{url}[/blue]
• Total de peticiones: [yellow]{total_requests:,}[/yellow]
• Concurrencia: [green]{concurrent_requests}[/green]
• Delay: [magenta]{delay}s[/magenta]
            """)
            
            if not Confirm.ask("¿Continuar con el test?"):
                return
            
            # Ejecutar test de carga
            start_time = time.time()
            metrics = await self.api_monitor.load_test(
                url=url,
                concurrent_requests=concurrent_requests,
                total_requests=total_requests,
                delay_between_requests=delay
            )
            end_time = time.time()
            
            # Mostrar resultados
            stats = self.api_monitor.get_stats(endpoint=url)
            
            self.console.print(f"\n[green]✅ Test completado en {end_time - start_time:.2f} segundos[/green]")
            self.api_visualizer.show_api_report(self.api_monitor, f"Test de Carga")
        
        asyncio.run(run_load_test())
        self.wait_for_continue()
    
    def handle_continuous_monitoring(self):
        """Manejar monitoreo continuo"""
        self.console.print(Panel(
            "[bold blue]📊 MONITOREO CONTINUO[/bold blue]",
            box=box.DOUBLE
        ))
        
        # Configurar endpoints
        endpoints = []
        self.console.print("[yellow]Ingresa los endpoints a monitorear (Enter vacío para terminar):[/yellow]")
        
        while True:
            url = Prompt.ask(f"Endpoint #{len(endpoints) + 1}", default="")
            if not url:
                break
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            endpoints.append(url)
        
        if not endpoints:
            self.console.print("[red]No se ingresaron endpoints[/red]")
            self.wait_for_continue()
            return
        
        interval = float(Prompt.ask("⏱️ Intervalo entre checks (segundos)", default="5.0"))
        duration = IntPrompt.ask("🕐 Duración total (segundos)", default=60)
        
        async def run_monitoring():
            self.console.print(f"""
[cyan]🎯 Configuración del monitoreo:[/cyan]
• Endpoints: [yellow]{len(endpoints)}[/yellow]
• Intervalo: [green]{interval}s[/green]
• Duración: [blue]{duration}s[/blue]
            """)
            
            if not Confirm.ask("¿Iniciar monitoreo?"):
                return
            
            # Iniciar monitoreo continuo
            await self.api_monitor.monitor_continuously(
                urls=endpoints,
                interval=interval,
                duration=duration
            )
            
            # Mostrar resultados
            self.api_visualizer.show_api_report(self.api_monitor, "Monitoreo Continuo")
        
        asyncio.run(run_monitoring())
        self.wait_for_continue()
    
    def handle_pokemon_api_tests(self):
        """Manejar tests específicos de PokéAPI"""
        pokemon_menu = """
[bold yellow]🐱 TESTS ESPECÍFICOS DE POKÉAPI[/bold yellow]

[cyan]Opciones disponibles:[/cyan]

[bold white]1.[/bold white] 🔍 [green]Probar endpoints comunes[/green]
[bold white]2.[/bold white] 🔥 [red]Test de estrés[/red]
[bold white]3.[/bold white] 📊 [blue]Monitoreo continuo de PokéAPI[/blue]
[bold white]4.[/bold white] 🔙 [dim]Volver al menú principal[/dim]
        """
        
        while True:
            self.console.print(Panel(pokemon_menu, border_style="yellow"))
            option = Prompt.ask("Selecciona una opción", choices=['1', '2', '3', '4'])
            
            if option == '1':
                self.test_pokemon_endpoints()
            elif option == '2':
                self.pokemon_stress_test()
            elif option == '3':
                self.pokemon_continuous_monitoring()
            elif option == '4':
                break
    
    def test_pokemon_endpoints(self):
        """Probar endpoints comunes de PokéAPI"""
        async def run_test():
            self.console.print("[yellow]🔍 Probando endpoints comunes de PokéAPI...[/yellow]")
            
            results = await self.pokemon_monitor.test_pokemon_endpoints()
            self.pokemon_visualizer.show_pokemon_endpoints_test(results)
        
        asyncio.run(run_test())
        self.wait_for_continue()
    
    def pokemon_stress_test(self):
        """Test de estrés específico para PokéAPI"""
        self.console.print(Panel(
            "[bold red]🔥 TEST DE ESTRÉS - POKÉAPI[/bold red]",
            box=box.DOUBLE
        ))
        
        concurrent_users = IntPrompt.ask("👥 Usuarios concurrentes", default=20)
        requests_per_user = IntPrompt.ask("📊 Peticiones por usuario", default=10)
        
        async def run_stress_test():
            self.console.print(f"""
[cyan]🎯 Configuración del test de estrés:[/cyan]
• Usuarios concurrentes: [yellow]{concurrent_users}[/yellow]
• Peticiones por usuario: [green]{requests_per_user}[/green]
• Total de peticiones: [red]{concurrent_users * requests_per_user}[/red]
• Endpoint objetivo: [blue]Pikachu (pokemon/25)[/blue]
            """)
            
            if not Confirm.ask("¿Continuar con el test de estrés?"):
                return
            
            results = await self.pokemon_monitor.stress_test_pokemon_api(
                concurrent_users=concurrent_users,
                requests_per_user=requests_per_user
            )
            
            self.pokemon_visualizer.show_stress_test_results(results)
        
        asyncio.run(run_stress_test())
        self.wait_for_continue()
    
    def pokemon_continuous_monitoring(self):
        """Monitoreo continuo específico de PokéAPI"""
        duration = IntPrompt.ask("🕐 Duración del monitoreo (segundos)", default=60)
        interval = float(Prompt.ask("⏱️ Intervalo entre checks (segundos)", default="3.0"))
        
        async def run_monitoring():
            await self.pokemon_monitor.monitor_continuously(
                urls=self.pokemon_monitor.common_endpoints,
                interval=interval,
                duration=duration
            )
            
            self.pokemon_visualizer.show_api_report(self.pokemon_monitor, "PokéAPI")
        
        asyncio.run(run_monitoring())
        self.wait_for_continue()
    
    def handle_reports_and_stats(self):
        """Mostrar reportes y estadísticas"""
        if not self.api_monitor.metrics and not self.pokemon_monitor.metrics:
            self.console.print(Panel(
                "[yellow]📊 No hay métricas disponibles[/yellow]\n"
                "[dim]Ejecuta algunos tests primero para ver estadísticas[/dim]",
                title="Sin datos",
                border_style="yellow"
            ))
            self.wait_for_continue()
            return
        
        reports_menu = """
[bold magenta]📈 REPORTES Y ESTADÍSTICAS[/bold magenta]

[cyan]Opciones disponibles:[/cyan]

[bold white]1.[/bold white] 📊 [green]Reporte general de APIs[/green]
[bold white]2.[/bold white] 🐱 [yellow]Reporte específico de PokéAPI[/yellow]
[bold white]3.[/bold white] 📈 [blue]Estadísticas detalladas[/blue]
[bold white]4.[/bold white] 🔙 [dim]Volver al menú principal[/dim]
        """
        
        while True:
            self.console.print(Panel(reports_menu, border_style="magenta"))
            option = Prompt.ask("Selecciona una opción", choices=['1', '2', '3', '4'])
            
            if option == '1':
                if self.api_monitor.metrics:
                    self.api_visualizer.show_api_report(self.api_monitor, "APIs Generales")
                else:
                    self.console.print("[yellow]No hay métricas de APIs generales[/yellow]")
                self.wait_for_continue()
            elif option == '2':
                if self.pokemon_monitor.metrics:
                    self.api_visualizer.show_api_report(self.pokemon_monitor, "PokéAPI")
                else:
                    self.console.print("[yellow]No hay métricas de PokéAPI[/yellow]")
                self.wait_for_continue()
            elif option == '3':
                self.show_detailed_stats()
            elif option == '4':
                break
    
    def show_detailed_stats(self):
        """Mostrar estadísticas detalladas"""
        # Combinar métricas de ambos monitores
        all_metrics = self.api_monitor.metrics + self.pokemon_monitor.metrics
        
        if not all_metrics:
            self.console.print("[yellow]No hay métricas disponibles[/yellow]")
            return
        
        # Crear estadísticas combinadas
        total_requests = len(all_metrics)
        successful = sum(1 for m in all_metrics if m.success)
        failed = total_requests - successful
        
        if successful > 0:
            avg_response_time = sum(m.response_time for m in all_metrics if m.success) / successful
            total_data = sum(m.response_size for m in all_metrics if m.success)
        else:
            avg_response_time = 0
            total_data = 0
        
        stats_text = f"""
[bold cyan]📊 ESTADÍSTICAS GLOBALES[/bold cyan]

[green]Total de peticiones realizadas: {total_requests:,}[/green]
[blue]✅ Exitosas: {successful:,} ({(successful/total_requests)*100:.1f}%)[/blue]
[red]❌ Fallidas: {failed:,} ({(failed/total_requests)*100:.1f}%)[/red]

[yellow]⚡ Tiempo promedio de respuesta: {avg_response_time:.3f}s[/yellow]
[magenta]📦 Datos transferidos: {total_data / (1024*1024):.2f} MB[/magenta]

[dim]APIs monitoreadas:[/dim]
• Monitor general: {len(self.api_monitor.metrics):,} métricas
• PokéAPI: {len(self.pokemon_monitor.metrics):,} métricas
        """
        
        self.console.print(Panel(stats_text, border_style="cyan"))
        self.wait_for_continue()
    
    def handle_compare_tests(self):
        """Comparar diferentes tests"""
        self.console.print(Panel(
            "[yellow]🔄 Esta funcionalidad estará disponible en próximas versiones[/yellow]",
            title="Comparación de Tests",
            border_style="yellow"
        ))
        self.wait_for_continue()
    
    def handle_clear_metrics(self):
        """Limpiar todas las métricas"""
        if Confirm.ask("¿Estás seguro de que quieres limpiar todas las métricas?"):
            self.api_monitor.clear_metrics()
            self.pokemon_monitor.clear_metrics()
            self.console.print("[green]✅ Métricas limpiadas[/green]")
        self.wait_for_continue()
    
    def wait_for_continue(self):
        """Esperar confirmación del usuario"""
        self.console.print("\n[dim]Presiona Enter para continuar...[/dim]")
        input()
    
    async def cleanup(self):
        """Limpiar recursos"""
        await self.api_monitor.close()
        await self.pokemon_monitor.close()
    
    def run(self):
        """Ejecutar la aplicación"""
        try:
            while self.running:
                self.show_main_menu()
                option = Prompt.ask("Selecciona una opción", choices=['1', '2', '3', '4', '5', '6', '7', '8'])
                
                if option == '1':
                    self.handle_single_endpoint_test()
                elif option == '2':
                    self.handle_load_test()
                elif option == '3':
                    self.handle_continuous_monitoring()
                elif option == '4':
                    self.handle_pokemon_api_tests()
                elif option == '5':
                    self.handle_reports_and_stats()
                elif option == '6':
                    self.handle_compare_tests()
                elif option == '7':
                    self.handle_clear_metrics()
                elif option == '8':
                    self.running = False
            
            # Mostrar despedida
            farewell_text = """
[bold cyan]👋 ¡Gracias por usar el Analizador de APIs![/bold cyan]

[green]Las métricas recolectadas han sido útiles para:[/green]
• Analizar la latencia de APIs
• Medir el throughput bajo carga
• Identificar problemas de disponibilidad
• Optimizar el rendimiento de aplicaciones

[yellow]💡 Consejos para el futuro:[/yellow]
• Monitorea regularmente las APIs críticas
• Establece umbrales de alerta
• Documenta los patrones de rendimiento
• Compara métricas históricas

[dim]Desarrollado para el curso de Sistemas Operativos[/dim]
            """
            
            self.console.print(Panel(farewell_text, title="¡Hasta pronto!", border_style="green"))
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]👋 Aplicación cerrada por el usuario[/yellow]")
        finally:
            # Cleanup asyncio resources
            asyncio.run(self.cleanup())


@click.command()
@click.option('--auto-pokemon', '-p', is_flag=True, help='Ejecutar automáticamente test de PokéAPI')
def main(auto_pokemon: bool):
    """
    🌐 Analizador de Rendimiento de APIs
    
    Herramienta especializada para medir y analizar el rendimiento
    de APIs REST externas con visualizaciones en tiempo real.
    """
    app = APIMonitorApp()
    
    if auto_pokemon:
        # Ejecutar test automático de PokéAPI
        async def auto_test():
            app.console.print("[yellow]🚀 Ejecutando test automático de PokéAPI...[/yellow]")
            results = await app.pokemon_monitor.test_pokemon_endpoints()
            app.pokemon_visualizer.show_pokemon_endpoints_test(results)
            await app.cleanup()
        
        asyncio.run(auto_test())
    else:
        app.run()


if __name__ == "__main__":
    main() 