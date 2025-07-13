#!/usr/bin/env python3
"""
Demostración completa del Analizador de Rendimiento del Sistema
Muestra todas las funcionalidades de forma automática para presentaciones
"""

import sys
import os
import time

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analizador_rendimiento'))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

def demo_bienvenida():
    """Mostrar pantalla de bienvenida"""
    console = Console()
    
    welcome_text = """
[bold cyan]🚀 DEMOSTRACIÓN COMPLETA[/bold cyan]
[bold cyan]Analizador de Rendimiento del Sistema[/bold cyan]

[green]Esta demostración mostrará:[/green]

✨ [yellow]Interfaz Terminal Colorida[/yellow] con Rich
📊 [blue]Monitoreo en Tiempo Real[/blue] del sistema  
🔍 [magenta]Profiling de Código[/magenta] avanzado
📈 [cyan]Visualizaciones Dinámicas[/cyan] de métricas
🎯 [green]Análisis de Rendimiento[/green] detallado

[dim]Desarrollado para el curso de Sistemas Operativos[/dim]
[dim]Universidad - Ingeniería en Sistemas[/dim]
    """
    
    panel = Panel(
        welcome_text,
        title="[bold red]🎪 DEMO ANALIZADOR DE RENDIMIENTO",
        border_style="bright_red",
        box=box.DOUBLE
    )
    
    console.print(panel)
    console.print("\n[yellow]Presiona Enter para continuar...[/yellow]")
    input()

def ejecutar_demo():
    """Ejecutar demostración completa"""
    console = Console()
    
    try:
        # Pantalla de bienvenida
        demo_bienvenida()
        
        # Importar y ejecutar la aplicación
        from analizador_rendimiento.terminal_app import TerminalApp
        
        console.print("[green]🚀 Iniciando aplicación principal...[/green]\n")
        time.sleep(2)
        
        app = TerminalApp()
        app.run()
        
    except ImportError as e:
        console.print(f"[red]❌ Error de importación: {e}[/red]")
        console.print("[yellow]📁 Verifica la estructura del proyecto[/yellow]")
        console.print("[blue]📦 Ejecuta: pip install -r requirements.txt[/blue]")
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Demo interrumpida por el usuario[/yellow]")
    except Exception as e:
        console.print(f"[red]💥 Error inesperado: {e}[/red]")

if __name__ == "__main__":
    ejecutar_demo() 