#!/usr/bin/env python3
"""
Script de ejecución para el monitor de APIs
Lanza la interfaz especializada para analizar el rendimiento de APIs REST
"""

import sys
import os
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from analizador_rendimiento.core.api_monitor import APIMonitor, PokemonAPIMonitor
    from analizador_rendimiento.core.api_visualizer import APIVisualizer, PokemonAPIVisualizer
    
    def main():
        """Función principal del monitor de APIs"""
        console = Console()
        
        # Mostrar bienvenida
        console.print(Panel.fit(
            "🌐 [bold cyan]Monitor de APIs[/bold cyan] 🌐\n"
            "[yellow]Análisis de rendimiento de APIs REST[/yellow]\n"
            "[green]🔧 Incluye métricas de sistemas operativos[/green]\n"
            "[dim]Presiona Ctrl+C para salir[/dim]",
            title="🚀 [bold]Analizador de APIs[/bold]",
            border_style="cyan"
        ))
        
        monitor = APIMonitor()
        visualizer = APIVisualizer()
        
        while True:
            console.print("\n📋 [bold]Opciones disponibles:[/bold]")
            console.print("1. 🧪 Test de endpoint individual")
            console.print("2. 🔥 Test de carga personalizado")
            console.print("3. 🌐 Test de conectividad de red")
            console.print("4. 🔥💻 Test de estrés con monitoreo del sistema")
            console.print("5. 🛡️ Test de resiliencia de API")
            console.print("6. 🐱💎 Análisis completo de PokéAPI")
            console.print("7. 👀 Monitoreo continuo")
            console.print("8. 🚪 Salir")
            
            choice = Prompt.ask("\n¿Qué opción eliges?", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
            
            if choice == "1":
                url = Prompt.ask("🔗 Ingresa la URL del endpoint")
                asyncio.run(test_single_endpoint(monitor, visualizer, url))
            elif choice == "2":
                url = Prompt.ask("🔗 URL para test de carga")
                requests = int(Prompt.ask("📊 Número de peticiones", default="50"))
                concurrent = int(Prompt.ask("👥 Usuarios concurrentes", default="10"))
                asyncio.run(load_test(monitor, visualizer, url, requests, concurrent))
            elif choice == "3":
                url = Prompt.ask("🔗 URL para análisis de conectividad")
                asyncio.run(test_network_connectivity(monitor, visualizer, url))
            elif choice == "4":
                url = Prompt.ask("🔗 URL para test de estrés")
                requests = int(Prompt.ask("📊 Número de peticiones", default="100"))
                concurrent = int(Prompt.ask("👥 Usuarios concurrentes", default="20"))
                asyncio.run(stress_test_with_monitoring(monitor, visualizer, url, requests, concurrent))
            elif choice == "5":
                url = Prompt.ask("🔗 URL para test de resiliencia")
                asyncio.run(test_api_resilience(monitor, visualizer, url))
            elif choice == "6":
                # Análisis completo de PokéAPI con todas las métricas
                pokemon_monitor = PokemonAPIMonitor()
                pokemon_visualizer = PokemonAPIVisualizer()
                asyncio.run(comprehensive_pokemon_analysis(pokemon_monitor, pokemon_visualizer))
            elif choice == "7":
                console.print("🔄 [yellow]Función en desarrollo[/yellow]")
            elif choice == "8":
                console.print("👋 [green]¡Hasta luego![/green]")
                break
    
    async def test_single_endpoint(monitor, visualizer, url):
        """Test de endpoint individual"""
        console = Console()
        console.print(f"🧪 Probando endpoint: {url}")
        
        async with monitor:
            result = await monitor.test_single_endpoint(url)
            
            # Mostrar resultado
            if result.success:
                console.print(f"✅ [green]Éxito[/green]: {result.status_code} - {result.response_time:.3f}s")
                console.print(f"📦 Tamaño de respuesta: {result.response_size:,} bytes")
                console.print(f"💻 Uso de CPU: {result.cpu_usage_during_request:.2f}%")
                console.print(f"🧠 Memoria utilizada: {result.memory_usage_mb:.1f} MB")
                console.print(f"🔗 Conexiones activas: {result.active_connections}")
            else:
                console.print(f"❌ [red]Error[/red]: {result.error_message}")
                console.print(f"⏱️ Tiempo transcurrido: {result.response_time:.3f}s")
            
            # Mostrar estadísticas básicas
            stats = monitor.get_stats()
            console.print(f"\n📊 Estadísticas actuales:")
            console.print(f"  Total peticiones: {stats.total_requests}")
            console.print(f"  Disponibilidad: {stats.availability_percentage:.1f}%")
    
    async def load_test(monitor, visualizer, url, total_requests, concurrent_users):
        """Test de carga personalizado"""
        console = Console()
        console.print(f"🔥 Test de carga: {total_requests} peticiones, {concurrent_users} usuarios")
        
        async with monitor:
            # Ejecutar test de carga
            metrics = await monitor.load_test(url, concurrent_users, total_requests)
            
            # Calcular estadísticas
            successful = sum(1 for m in metrics if m.success)
            success_rate = (successful / total_requests) * 100 if total_requests > 0 else 0
            avg_time = sum(m.response_time for m in metrics) / len(metrics) if metrics else 0
            
            # Mostrar resultados
            console.print(f"✅ [green]Test completado[/green]")
            console.print(f"📊 Peticiones exitosas: {successful}/{total_requests}")
            console.print(f"📈 Tasa de éxito: {success_rate:.1f}%")
            console.print(f"⏱️ Tiempo promedio: {avg_time:.3f}s")
            
            # Mostrar reporte completo
            visualizer.show_api_report(monitor, f"Test de Carga - {url}")
    
    async def test_network_connectivity(monitor, visualizer, url):
        """Test de conectividad de red"""
        console = Console()
        console.print(f"🌐 Analizando conectividad de red para: {url}")
        
        async with monitor:
            result = await monitor.test_network_connectivity(url)
            
            # Mostrar resultados de conectividad
            console.print(f"\n📊 [bold]Resultados de Conectividad:[/bold]")
            console.print(f"🏠 Host: {result['host']}")
            console.print(f"🏓 Ping: {result['ping_time_ms']:.1f} ms")
            console.print(f"🔍 Resolución DNS: {result['dns_resolution_ms']:.1f} ms")
            console.print(f"🛣️ Saltos de red: {result['traceroute_hops']}")
            console.print(f"⚡ Tiempo API: {result['api_response_time_ms']:.1f} ms")
            console.print(f"🌐 Overhead de red: {result['network_overhead_percent']:.1f}%")
            console.print(f"✅ Estado API: {'🟢 Funcionando' if result['api_success'] else '🔴 Error'}")
    
    async def stress_test_with_monitoring(monitor, visualizer, url, total_requests, concurrent_users):
        """Test de estrés con monitoreo del sistema"""
        console = Console()
        console.print(f"🔥💻 Test de estrés con monitoreo del sistema")
        console.print(f"📊 {total_requests} peticiones, {concurrent_users} usuarios concurrentes")
        
        async with monitor:
            result = await monitor.stress_test_with_system_monitoring(
                url, concurrent_users, total_requests
            )
            
            # Mostrar resultados del test
            test_summary = result['test_summary']
            system_impact = result['system_impact']
            
            console.print(f"\n🎯 [bold]Resumen del Test:[/bold]")
            console.print(f"⏱️ Duración: {test_summary['duration_seconds']:.1f}s")
            console.print(f"📈 Tasa de éxito: {test_summary['success_rate']:.1f}%")
            console.print(f"⚡ Peticiones/segundo: {test_summary['requests_per_second']:.1f}")
            console.print(f"🕐 Tiempo promedio: {test_summary['avg_response_time']:.3f}s")
            
            console.print(f"\n💻 [bold]Impacto en el Sistema:[/bold]")
            cpu = system_impact['cpu_usage']
            memory = system_impact['memory_usage']
            network = system_impact['network_usage']
            connections = system_impact['connections']
            
            console.print(f"🔥 CPU - Inicial: {cpu['initial']:.1f}% | Pico: {cpu['max_during_test']:.1f}% | Incremento: +{cpu['increase_percent']:.1f}%")
            console.print(f"🧠 Memoria - Inicial: {memory['initial']:.1f}% | Pico: {memory['max_during_test']:.1f}% | Incremento: +{memory['increase_percent']:.1f}%")
            console.print(f"🌐 Red - Enviado: {network['total_data_mb']:.2f} MB")
            console.print(f"🔗 Conexiones - Inicial: {connections['initial']} | Pico: {connections['max_concurrent']} | Overhead: +{connections['connection_overhead']}")
            
            # Mostrar reporte completo
            visualizer.show_api_report(monitor, f"Test de Estrés con Monitoreo - {url}")
    
    async def test_api_resilience(monitor, visualizer, url):
        """Test de resiliencia de API"""
        console = Console()
        console.print(f"🛡️ Probando resiliencia de la API: {url}")
        
        async with monitor:
            results = await monitor.test_api_resilience(url)
            
            console.print(f"\n🧪 [bold]Resultados de Resiliencia:[/bold]")
            
            for scenario, result in results.items():
                if scenario == 'normal':
                    status = "🟢" if result['success'] else "🔴"
                    console.print(f"{status} Test Normal: {result['response_time']:.3f}s (HTTP {result['status_code']})")
                
                elif scenario == 'high_load':
                    status = "🟢" if result['success_rate'] > 90 else "🟡" if result['success_rate'] > 70 else "🔴"
                    console.print(f"{status} Alta Carga: {result['success_rate']:.1f}% éxito, {result['avg_response_time']:.3f}s promedio")
                
                elif scenario == 'timeout_test':
                    if result.get('success'):
                        status = "🟢" if result.get('handled_timeout') else "🟡"
                        console.print(f"{status} Test Timeout: {result['response_time']:.3f}s (dentro del límite)")
                    else:
                        status = "🟢" if result.get('handled_gracefully') else "🔴"
                        console.print(f"{status} Test Timeout: {'Manejado correctamente' if result.get('handled_gracefully') else 'Error no manejado'}")
                
                elif scenario == 'connection_limit':
                    status = "🟢" if result.get('handled_connection_limit') else "🔴"
                    if 'success_rate' in result:
                        console.print(f"{status} Límite Conexiones: {result['success_rate']:.1f}% éxito con pool limitado")
                    else:
                        console.print(f"{status} Límite Conexiones: Error - {result.get('error', 'Desconocido')}")
    
    async def comprehensive_pokemon_analysis(monitor, visualizer):
        """Análisis completo de PokéAPI con todas las métricas"""
        console = Console()
        console.print("🐱💎 Iniciando análisis completo de PokéAPI...")
        console.print("🔧 Incluye: conectividad, rendimiento, estrés y resiliencia")
        
        async with monitor:
            results = await monitor.comprehensive_pokemon_analysis()
            
            # Mostrar conectividad
            connectivity = results['connectivity_analysis']
            console.print(f"\n🌐 [bold]Análisis de Conectividad:[/bold]")
            console.print(f"🏠 Host: {connectivity['host']}")
            console.print(f"🏓 Ping: {connectivity['ping_time_ms']:.1f} ms")
            console.print(f"🔍 DNS: {connectivity['dns_resolution_ms']:.1f} ms")
            console.print(f"🛣️ Saltos: {connectivity['traceroute_hops']}")
            
            # Mostrar rendimiento de endpoints
            console.print(f"\n⚡ [bold]Rendimiento de Endpoints:[/bold]")
            endpoints = results['endpoints_performance']
            for endpoint, metric in endpoints.items():
                status = "🟢" if metric.success else "🔴"
                console.print(f"{status} {endpoint}: {metric.response_time:.3f}s")
            
            # Mostrar resultados de estrés
            stress = results['stress_test_results']
            test_summary = stress['test_summary']
            system_impact = stress['system_impact']
            
            console.print(f"\n🔥 [bold]Test de Estrés:[/bold]")
            console.print(f"📈 Tasa de éxito: {test_summary['success_rate']:.1f}%")
            console.print(f"⚡ Req/seg: {test_summary['requests_per_second']:.1f}")
            console.print(f"🔥 CPU pico: {system_impact['cpu_usage']['max_during_test']:.1f}%")
            console.print(f"🧠 Memoria pico: {system_impact['memory_usage']['max_during_test']:.1f}%")
            
            # Mostrar resiliencia
            resilience = results['resilience_test_results']
            console.print(f"\n🛡️ [bold]Test de Resiliencia:[/bold]")
            for scenario, result in resilience.items():
                if scenario == 'normal':
                    status = "🟢" if result['success'] else "🔴"
                    console.print(f"{status} Normal: {result['response_time']:.3f}s")
                elif scenario == 'high_load':
                    status = "🟢" if result['success_rate'] > 90 else "🟡" if result['success_rate'] > 70 else "🔴"
                    console.print(f"{status} Alta carga: {result['success_rate']:.1f}%")
            
            # Mostrar reporte completo
            console.print(f"\n📊 [bold]Generando reporte detallado...[/bold]")
            visualizer.show_api_report(monitor, "PokéAPI - Análisis Completo")
    
    if __name__ == "__main__":
        print("🌐 Iniciando Monitor de APIs...")
        print("🔍 Especializado en análisis de rendimiento de APIs REST")
        print("🔧 Incluye métricas de sistemas operativos")
        print("🐱 Incluye tests específicos para PokéAPI")
        print("💡 Usa Ctrl+C para salir en cualquier momento")
        print("-" * 60)
        main()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("📁 Verifica que estés en el directorio correcto del proyecto")
    print("📦 Instala las dependencias: pip install -r requirements.txt")
    print("💡 Nueva dependencia requerida: aiohttp")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n👋 ¡Hasta luego! Monitor de APIs cerrado por el usuario.")
    sys.exit(0)
except Exception as e:
    print(f"💥 Error inesperado: {e}")
    sys.exit(1) 