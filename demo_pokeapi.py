#!/usr/bin/env python3
"""
Demostración específica para el análisis de rendimiento de PokéAPI
Ejecuta automáticamente varios tests para mostrar las capacidades del monitor
"""

import sys
import os
import asyncio

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analizador_rendimiento'))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

async def demo_pokeapi():
    """Ejecutar demostración completa de PokéAPI"""
    console = Console()
    
    # Pantalla de bienvenida
    welcome_text = """
[bold cyan]🐱 DEMOSTRACIÓN POKÉAPI[/bold cyan]
[bold cyan]Analizador de Rendimiento de APIs[/bold cyan]

[green]Esta demo mostrará:[/green]

🔍 [yellow]Test de endpoints comunes[/yellow]
🔥 [red]Test de carga con concurrencia[/red]
📊 [blue]Análisis de rendimiento[/blue]
📈 [magenta]Estadísticas y métricas[/magenta]
🎯 [green]Evaluación de disponibilidad[/green]

[dim]PokéAPI: https://pokeapi.co/api/v2[/dim]
[dim]Una API REST pública perfecta para testing[/dim]
    """
    
    panel = Panel(
        welcome_text,
        title="[bold red]🚀 DEMO POKEAPI MONITOR",
        border_style="bright_red",
        box=box.DOUBLE
    )
    
    console.print(panel)
    console.print("\n[yellow]Presiona Enter para continuar...[/yellow]")
    input()
    
    try:
        from analizador_rendimiento.core.api_monitor import PokemonAPIMonitor
        from analizador_rendimiento.core.api_visualizer import PokemonAPIVisualizer
        
        # Inicializar monitor y visualizador
        pokemon_monitor = PokemonAPIMonitor()
        pokemon_visualizer = PokemonAPIVisualizer()
        
        console.print("[bold green]🎮 Fase 1: Test de Endpoints Comunes[/bold green]")
        console.print("[yellow]Probando endpoints populares de PokéAPI...[/yellow]\n")
        
        # Test de endpoints comunes
        results = await pokemon_monitor.test_pokemon_endpoints()
        pokemon_visualizer.show_pokemon_endpoints_test(results)
        
        console.print("\n[yellow]Presiona Enter para continuar con el test de carga...[/yellow]")
        input()
        
        console.print("\n[bold red]🔥 Fase 2: Test de Carga[/bold red]")
        console.print("[yellow]Simulando 50 peticiones con 10 usuarios concurrentes...[/yellow]\n")
        
        # Test de carga
        stress_results = await pokemon_monitor.stress_test_pokemon_api(
            concurrent_users=10,
            requests_per_user=5
        )
        
        console.print("\n[bold blue]📊 Fase 3: Análisis de Resultados[/bold blue]")
        pokemon_visualizer.show_stress_test_results(stress_results)
        
        console.print("\n[yellow]Presiona Enter para ver el reporte final...[/yellow]")
        input()
        
        console.print("\n[bold magenta]📈 Fase 4: Reporte Completo[/bold magenta]")
        from analizador_rendimiento.core.api_visualizer import APIVisualizer
        api_visualizer = APIVisualizer()
        api_visualizer.show_api_report(pokemon_monitor, "PokéAPI - Demo Completa")
        
        # Resumen final
        stats = pokemon_monitor.get_stats()
        final_summary = f"""
[bold cyan]🎉 DEMO COMPLETADA - RESUMEN FINAL[/bold cyan]

[green]✅ Total de peticiones realizadas: {stats.total_requests:,}[/green]
[blue]⚡ Tiempo promedio de respuesta: {stats.avg_response_time:.3f}s[/blue]
[yellow]📊 Disponibilidad de PokéAPI: {stats.availability_percentage:.2f}%[/yellow]
[magenta]🚀 Throughput: {stats.throughput_per_second:.2f} peticiones/segundo[/magenta]

[bold]💡 Conclusiones de la demostración:[/bold]
• PokéAPI es {"🟢 muy confiable" if stats.availability_percentage >= 95 else "🟡 moderadamente confiable"}
• El tiempo de respuesta es {"🟢 excelente" if stats.avg_response_time < 1.0 else "🟡 aceptable"}
• Puede manejar {"🟢 bien" if stats.throughput_per_second >= 5 else "🟡 moderadamente"} la carga concurrente

[dim]¡Perfecto para aprender sobre monitoreo de APIs![/dim]
        """
        
        console.print(Panel(final_summary, title="[bold]🏆 RESULTADOS", border_style="green"))
        
        # Cleanup
        await pokemon_monitor.close()
        
        console.print("\n[green]✨ Demo completada exitosamente[/green]")
        console.print("[yellow]💡 Ejecuta 'python ejecutar_api_monitor.py' para usar la aplicación completa[/yellow]")
        
    except ImportError as e:
        console.print(f"[red]❌ Error de importación: {e}[/red]")
        console.print("[yellow]📦 Ejecuta: pip install aiohttp[/yellow]")
    except Exception as e:
        console.print(f"[red]💥 Error durante la demo: {e}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(demo_pokeapi())
    except KeyboardInterrupt:
        print("\n[yellow]👋 Demo interrumpida por el usuario[/yellow]")
    except Exception as e:
        print(f"Error ejecutando demo: {e}") 