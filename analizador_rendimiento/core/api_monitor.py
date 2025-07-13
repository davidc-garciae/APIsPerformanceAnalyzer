#!/usr/bin/env python3
"""
Módulo de monitoreo de rendimiento de APIs externas
Analiza latencia, tiempo de respuesta, throughput y disponibilidad
"""

import time
import asyncio
import aiohttp
import statistics
import socket
import subprocess
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import json
import psutil
import threading


@dataclass
class APIMetric:
    """Métrica individual de una petición a la API"""
    timestamp: datetime
    endpoint: str
    response_time: float  # segundos
    status_code: int
    response_size: int  # bytes
    success: bool
    error_message: Optional[str] = None
    # Nuevas métricas de sistema
    dns_resolution_time: float = 0.0
    tcp_connection_time: float = 0.0
    ssl_handshake_time: float = 0.0
    cpu_usage_during_request: float = 0.0
    memory_usage_mb: float = 0.0
    active_connections: int = 0


@dataclass
class SystemResourceMetric:
    """Métricas de recursos del sistema durante el monitoreo"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    network_bytes_sent: int
    network_bytes_recv: int
    active_tcp_connections: int
    open_file_descriptors: int


@dataclass
class NetworkLatencyMetric:
    """Métricas específicas de latencia de red"""
    timestamp: datetime
    host: str
    ping_time: float  # ms
    dns_resolution_time: float  # ms
    traceroute_hops: int
    packet_loss_percent: float


@dataclass
class APIStats:
    """Estadísticas agregadas de una API"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    percentile_95: float = 0.0
    throughput_per_second: float = 0.0
    availability_percentage: float = 100.0
    total_data_transferred: int = 0  # bytes
    # Nuevas estadísticas de sistema
    avg_dns_time: float = 0.0
    avg_tcp_time: float = 0.0
    avg_cpu_usage: float = 0.0
    avg_memory_usage: float = 0.0
    max_concurrent_connections: int = 0
    
    def update_from_metrics(self, metrics: List[APIMetric]):
        """Actualizar estadísticas basándose en las métricas"""
        if not metrics:
            return
            
        self.total_requests = len(metrics)
        self.successful_requests = sum(1 for m in metrics if m.success)
        self.failed_requests = self.total_requests - self.successful_requests
        
        response_times = [m.response_time for m in metrics if m.success]
        if response_times:
            self.avg_response_time = statistics.mean(response_times)
            self.min_response_time = min(response_times)
            self.max_response_time = max(response_times)
            if len(response_times) >= 2:
                self.percentile_95 = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        
        self.availability_percentage = (self.successful_requests / self.total_requests) * 100
        self.total_data_transferred = sum(m.response_size for m in metrics if m.success)
        
        # Calcular throughput (peticiones por segundo)
        if metrics:
            time_span = (metrics[-1].timestamp - metrics[0].timestamp).total_seconds()
            if time_span > 0:
                self.throughput_per_second = self.total_requests / time_span
        
        # Nuevas estadísticas de sistema
        dns_times = [m.dns_resolution_time for m in metrics if m.dns_resolution_time > 0]
        if dns_times:
            self.avg_dns_time = statistics.mean(dns_times)
            
        tcp_times = [m.tcp_connection_time for m in metrics if m.tcp_connection_time > 0]
        if tcp_times:
            self.avg_tcp_time = statistics.mean(tcp_times)
            
        cpu_usages = [m.cpu_usage_during_request for m in metrics if m.cpu_usage_during_request > 0]
        if cpu_usages:
            self.avg_cpu_usage = statistics.mean(cpu_usages)
            
        memory_usages = [m.memory_usage_mb for m in metrics if m.memory_usage_mb > 0]
        if memory_usages:
            self.avg_memory_usage = statistics.mean(memory_usages)
            
        connections = [m.active_connections for m in metrics if m.active_connections > 0]
        if connections:
            self.max_concurrent_connections = max(connections)


class APIMonitor:
    """Monitor de rendimiento para APIs externas"""
    
    def __init__(self):
        self.metrics: List[APIMetric] = []
        self.system_metrics: List[SystemResourceMetric] = []
        self.network_metrics: List[NetworkLatencyMetric] = []
        self.running = False
        self.session: Optional[aiohttp.ClientSession] = None
        self.system_monitor_thread = None
        self.initial_network_stats = None
    
    async def __aenter__(self):
        """Context manager entry"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()
        # Inicializar estadísticas de red
        self.initial_network_stats = psutil.net_io_counters()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()
    
    def _start_system_monitoring(self):
        """Iniciar monitoreo de recursos del sistema en hilo separado"""
        def monitor_system():
            while self.running:
                try:
                    # Recopilar métricas del sistema
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    memory = psutil.virtual_memory()
                    net_io = psutil.net_io_counters()
                    
                    # Contar conexiones TCP activas
                    tcp_connections = len([conn for conn in psutil.net_connections() 
                                         if conn.status == 'ESTABLISHED'])
                    
                    # Contar file descriptors abiertos (solo en Unix)
                    try:
                        if platform.system() != 'Windows':
                            open_fds = len(psutil.Process().open_files())
                        else:
                            open_fds = psutil.Process().num_handles()
                    except:
                        open_fds = 0
                    
                    metric = SystemResourceMetric(
                        timestamp=datetime.now(),
                        cpu_percent=cpu_percent,
                        memory_percent=memory.percent,
                        network_bytes_sent=net_io.bytes_sent - (self.initial_network_stats.bytes_sent if self.initial_network_stats else 0),
                        network_bytes_recv=net_io.bytes_recv - (self.initial_network_stats.bytes_recv if self.initial_network_stats else 0),
                        active_tcp_connections=tcp_connections,
                        open_file_descriptors=open_fds
                    )
                    
                    self.system_metrics.append(metric)
                    
                    # Mantener solo los últimos 100 registros
                    if len(self.system_metrics) > 100:
                        self.system_metrics.pop(0)
                        
                    time.sleep(1)  # Muestrear cada segundo
                except Exception:
                    pass  # Ignorar errores en el monitoreo del sistema
        
        self.system_monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        self.system_monitor_thread.start()
    
    def _stop_system_monitoring(self):
        """Detener monitoreo del sistema"""
        self.running = False
        if self.system_monitor_thread:
            self.system_monitor_thread.join(timeout=2)
    
    async def _measure_network_latency(self, host: str) -> NetworkLatencyMetric:
        """Medir latencia de red específica (ping, DNS, traceroute)"""
        timestamp = datetime.now()
        
        # Extraer hostname de URL si es necesario
        if host.startswith('http'):
            from urllib.parse import urlparse
            parsed = urlparse(host)
            host = parsed.hostname
        
        ping_time = 0.0
        dns_time = 0.0
        traceroute_hops = 0
        packet_loss = 0.0
        
        try:
            # Medir tiempo de resolución DNS
            dns_start = time.time()
            socket.gethostbyname(host)
            dns_time = (time.time() - dns_start) * 1000  # ms
            
            # Ping (usando comando del sistema)
            if platform.system() == 'Windows':
                ping_cmd = ['ping', '-n', '1', host]
            else:
                ping_cmd = ['ping', '-c', '1', host]
            
            ping_start = time.time()
            result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                # Extraer tiempo de ping del output
                output = result.stdout
                if 'time=' in output:
                    time_part = output.split('time=')[1].split('ms')[0].split(' ')[-1]
                    ping_time = float(time_part)
                elif 'tiempo=' in output:  # Windows en español
                    time_part = output.split('tiempo=')[1].split('ms')[0]
                    ping_time = float(time_part)
            
            # Traceroute simplificado (contar saltos hasta el destino)
            if platform.system() == 'Windows':
                tracert_cmd = ['tracert', '-h', '10', host]
            else:
                tracert_cmd = ['traceroute', '-m', '10', host]
            
            try:
                tracert_result = subprocess.run(tracert_cmd, capture_output=True, text=True, timeout=10)
                if tracert_result.returncode == 0:
                    lines = tracert_result.stdout.split('\n')
                    traceroute_hops = len([line for line in lines if '*' not in line and host in line])
            except:
                traceroute_hops = 0
                
        except Exception:
            pass  # En caso de error, mantener valores por defecto
        
        return NetworkLatencyMetric(
            timestamp=timestamp,
            host=host,
            ping_time=ping_time,
            dns_resolution_time=dns_time,
            traceroute_hops=traceroute_hops,
            packet_loss_percent=packet_loss
        )
        
    async def _make_request(self, url: str, method: str = 'GET', **kwargs) -> APIMetric:
        """Realizar una petición HTTP y medir métricas"""
        start_time = time.time()
        timestamp = datetime.now()
        
        # Métricas de sistema antes de la petición
        process = psutil.Process()
        cpu_before = process.cpu_percent()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        try:
            # Crear sesión temporal si no existe
            session_created = False
            if not self.session or self.session.closed:
                self.session = aiohttp.ClientSession()
                session_created = True
                
            # Medir tiempos específicos de conexión
            dns_start = time.time()
            tcp_start = 0.0
            ssl_start = 0.0
            
            async with self.session.request(method, url, **kwargs) as response:
                content = await response.read()
                end_time = time.time()
                
                response_time = end_time - start_time
                response_size = len(content)
                success = 200 <= response.status < 400
                
                # Métricas de sistema después de la petición
                cpu_after = process.cpu_percent()
                memory_after = process.memory_info().rss / 1024 / 1024  # MB
                
                # Contar conexiones activas
                try:
                    active_connections = len([conn for conn in psutil.net_connections() 
                                           if conn.status == 'ESTABLISHED'])
                except:
                    active_connections = 0
                
                return APIMetric(
                    timestamp=timestamp,
                    endpoint=url,
                    response_time=response_time,
                    status_code=response.status,
                    response_size=response_size,
                    success=success,
                    error_message=None if success else f"HTTP {response.status}",
                    dns_resolution_time=0.0,  # aiohttp maneja esto internamente
                    tcp_connection_time=0.0,   # aiohttp maneja esto internamente
                    ssl_handshake_time=0.0,    # aiohttp maneja esto internamente
                    cpu_usage_during_request=max(cpu_after - cpu_before, 0),
                    memory_usage_mb=memory_after,
                    active_connections=active_connections
                )
                
        except Exception as e:
            end_time = time.time()
            return APIMetric(
                timestamp=timestamp,
                endpoint=url,
                response_time=end_time - start_time,
                status_code=0,
                response_size=0,
                success=False,
                error_message=str(e),
                dns_resolution_time=0.0,
                tcp_connection_time=0.0,
                ssl_handshake_time=0.0,
                cpu_usage_during_request=0.0,
                memory_usage_mb=0.0,
                active_connections=0
            )
    
    async def test_single_endpoint(self, url: str, method: str = 'GET') -> APIMetric:
        """Probar un endpoint individual"""
        metric = await self._make_request(url, method)
        self.metrics.append(metric)
        return metric
    
    async def test_network_connectivity(self, url: str) -> Dict[str, Any]:
        """Test completo de conectividad de red"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        host = parsed.hostname
        
        print(f"🌐 Analizando conectividad de red para {host}...")
        
        # Medir latencia de red
        network_metric = await self._measure_network_latency(host)
        self.network_metrics.append(network_metric)
        
        # Test básico de endpoint
        api_metric = await self.test_single_endpoint(url)
        
        return {
            'host': host,
            'ping_time_ms': network_metric.ping_time,
            'dns_resolution_ms': network_metric.dns_resolution_time,
            'traceroute_hops': network_metric.traceroute_hops,
            'api_response_time_ms': api_metric.response_time * 1000,
            'api_success': api_metric.success,
            'network_overhead_percent': ((api_metric.response_time * 1000 - network_metric.ping_time) / (api_metric.response_time * 1000)) * 100 if api_metric.response_time > 0 else 0
        }
    
    async def stress_test_with_system_monitoring(self, url: str, concurrent_requests: int = 20, 
                                               total_requests: int = 100, duration_seconds: int = 30) -> Dict[str, Any]:
        """Test de estrés con monitoreo completo del sistema"""
        print(f"🔥 Test de estrés con monitoreo del sistema: {total_requests} peticiones, {concurrent_requests} concurrentes")
        
        # Iniciar monitoreo del sistema
        self.running = True
        self._start_system_monitoring()
        
        try:
            # Métricas iniciales del sistema
            initial_cpu = psutil.cpu_percent(interval=1)
            initial_memory = psutil.virtual_memory().percent
            initial_connections = len(psutil.net_connections())
            
            # Ejecutar test de carga
            start_time = time.time()
            metrics = await self.load_test(url, concurrent_requests, total_requests, 0.05)
            end_time = time.time()
            
            # Métricas finales del sistema
            final_cpu = psutil.cpu_percent(interval=1)
            final_memory = psutil.virtual_memory().percent
            final_connections = len(psutil.net_connections())
            
            # Analizar métricas del sistema durante el test
            if self.system_metrics:
                max_cpu = max(m.cpu_percent for m in self.system_metrics)
                max_memory = max(m.memory_percent for m in self.system_metrics)
                max_connections = max(m.active_tcp_connections for m in self.system_metrics)
                avg_cpu = statistics.mean(m.cpu_percent for m in self.system_metrics)
                avg_memory = statistics.mean(m.memory_percent for m in self.system_metrics)
                
                # Calcular uso de red durante el test
                total_sent = sum(m.network_bytes_sent for m in self.system_metrics)
                total_recv = sum(m.network_bytes_recv for m in self.system_metrics)
            else:
                max_cpu = final_cpu
                max_memory = final_memory
                max_connections = final_connections
                avg_cpu = (initial_cpu + final_cpu) / 2
                avg_memory = (initial_memory + final_memory) / 2
                total_sent = 0
                total_recv = 0
            
            # Calcular estadísticas de la API
            successful_requests = sum(1 for m in metrics if m.success)
            success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
            avg_response_time = statistics.mean(m.response_time for m in metrics) if metrics else 0
            
            return {
                'test_summary': {
                    'total_requests': total_requests,
                    'concurrent_users': concurrent_requests,
                    'duration_seconds': end_time - start_time,
                    'success_rate': success_rate,
                    'avg_response_time': avg_response_time,
                    'requests_per_second': total_requests / (end_time - start_time)
                },
                'system_impact': {
                    'cpu_usage': {
                        'initial': initial_cpu,
                        'final': final_cpu,
                        'max_during_test': max_cpu,
                        'avg_during_test': avg_cpu,
                        'increase_percent': max_cpu - initial_cpu
                    },
                    'memory_usage': {
                        'initial': initial_memory,
                        'final': final_memory,
                        'max_during_test': max_memory,
                        'avg_during_test': avg_memory,
                        'increase_percent': max_memory - initial_memory
                    },
                    'network_usage': {
                        'total_bytes_sent': total_sent,
                        'total_bytes_received': total_recv,
                        'total_data_mb': (total_sent + total_recv) / 1024 / 1024
                    },
                    'connections': {
                        'initial': initial_connections,
                        'final': final_connections,
                        'max_concurrent': max_connections,
                        'connection_overhead': max_connections - initial_connections
                    }
                },
                'metrics': metrics
            }
            
        finally:
            # Detener monitoreo del sistema
            self._stop_system_monitoring()
    
    async def test_api_resilience(self, url: str, test_scenarios: List[str] = None) -> Dict[str, Any]:
        """Test de resiliencia de la API bajo diferentes condiciones"""
        if test_scenarios is None:
            test_scenarios = ['normal', 'high_load', 'timeout_test', 'connection_limit']
        
        results = {}
        
        for scenario in test_scenarios:
            print(f"🧪 Ejecutando escenario: {scenario}")
            
            try:
                # Timeout general por escenario para evitar cuelgues
                scenario_result = await asyncio.wait_for(
                    self._execute_resilience_scenario(scenario, url), 
                    timeout=30.0
                )
                results[scenario] = scenario_result
            except asyncio.TimeoutError:
                print(f"⚠️ Timeout en escenario {scenario}")
                results[scenario] = {
                    'error': f'Timeout en escenario {scenario}',
                    'timeout_occurred': True
                }
            except Exception as e:
                print(f"❌ Error en escenario {scenario}: {e}")
                results[scenario] = {
                    'error': str(e),
                    'scenario_failed': True
                }
        
        return results
    
    async def _execute_resilience_scenario(self, scenario: str, url: str) -> Dict[str, Any]:
        """Ejecutar un escenario específico de resiliencia"""
        if scenario == 'normal':
            # Test normal de baseline
            metric = await self.test_single_endpoint(url)
            return {
                'response_time': metric.response_time,
                'success': metric.success,
                'status_code': metric.status_code
            }
            
        elif scenario == 'high_load':
            # Test de alta carga
            metrics = await self.load_test(url, concurrent_requests=50, total_requests=100)
            successful = sum(1 for m in metrics if m.success)
            response_times = [m.response_time for m in metrics] if metrics else []
            return {
                'success_rate': (successful / len(metrics)) * 100 if metrics else 0,
                'avg_response_time': statistics.mean(response_times) if response_times else 0,
                'max_response_time': max(response_times) if response_times else 0
            }
            
        elif scenario == 'timeout_test':
            # Test con timeout corto
            try:
                timeout = aiohttp.ClientTimeout(total=1.0)  # 1 segundo
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    start_time = time.time()
                    async with session.get(url) as response:
                        await response.read()
                        response_time = time.time() - start_time
                        return {
                            'success': True,
                            'response_time': response_time,
                            'handled_timeout': response_time < 1.0
                        }
            except asyncio.TimeoutError:
                return {
                    'success': False,
                    'timeout_occurred': True,
                    'handled_gracefully': True
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'handled_gracefully': False
                }
                
        elif scenario == 'connection_limit':
            # Test con muchas conexiones simultáneas (reducido para evitar cuelgues)
            try:
                connector = aiohttp.TCPConnector(limit=3)  # Limitar a 3 conexiones
                timeout = aiohttp.ClientTimeout(total=5)  # Timeout más corto
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    
                    async def make_limited_request():
                        try:
                            async with session.get(url) as response:
                                await response.read()  # Leer la respuesta completamente
                                return response.status
                        except Exception as e:
                            return e
                    
                    # Crear solo 10 tareas para evitar sobrecarga
                    tasks = [make_limited_request() for _ in range(10)]
                    
                    # Ejecutar con timeout más corto
                    responses = await asyncio.wait_for(
                        asyncio.gather(*tasks, return_exceptions=True), 
                        timeout=10.0
                    )
                    
                    successful = sum(1 for r in responses if isinstance(r, int) and 200 <= r < 400)
                    return {
                        'total_requests': 10,
                        'successful_requests': successful,
                        'success_rate': (successful / 10) * 100,
                        'handled_connection_limit': True
                    }
                    
            except asyncio.TimeoutError:
                return {
                    'error': 'Timeout en test de límite de conexiones',
                    'handled_connection_limit': False,
                    'timeout_occurred': True
                }
            except Exception as e:
                return {
                    'error': str(e),
                    'handled_connection_limit': False
                }
        
        # Escenario no reconocido
        return {'error': f'Escenario {scenario} no reconocido'}

    async def load_test(self, url: str, concurrent_requests: int = 10, 
                       total_requests: int = 100, delay_between_requests: float = 0.1) -> List[APIMetric]:
        """Realizar test de carga en un endpoint"""
        print(f"🚀 Iniciando test de carga: {total_requests} peticiones con {concurrent_requests} concurrentes")
        
        semaphore = asyncio.Semaphore(concurrent_requests)
        
        async def limited_request():
            async with semaphore:
                metric = await self._make_request(url)
                await asyncio.sleep(delay_between_requests)
                return metric
        
        # Crear todas las tareas
        tasks = [limited_request() for _ in range(total_requests)]
        
        # Ejecutar todas las peticiones
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar resultados válidos
        valid_metrics = []
        for result in results:
            if isinstance(result, APIMetric):
                self.metrics.append(result)
                valid_metrics.append(result)
        
        print(f"✅ Test de carga completado: {len(valid_metrics)} peticiones exitosas")
        return valid_metrics
    
    async def monitor_continuously(self, urls: List[str], interval: float = 5.0, duration: int = 60):
        """Monitorear múltiples endpoints continuamente"""
        print(f"📊 Monitoreando {len(urls)} endpoints cada {interval}s por {duration}s")
        
        self.running = True
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            tasks = [self._make_request(url) for url in urls]
            metrics = await asyncio.gather(*tasks, return_exceptions=True)
            
            for metric in metrics:
                if isinstance(metric, APIMetric):
                    self.metrics.append(metric)
            
            await asyncio.sleep(interval)
        
        self.running = False
        print(f"🔄 Monitoreo continuo completado")
    
    def get_stats(self, endpoint: Optional[str] = None, 
                  time_window: Optional[timedelta] = None) -> APIStats:
        """Obtener estadísticas de las métricas recolectadas"""
        
        # Filtrar métricas por endpoint si se especifica
        filtered_metrics = self.metrics
        if endpoint:
            filtered_metrics = [m for m in filtered_metrics if endpoint in m.endpoint]
        
        # Filtrar por ventana de tiempo si se especifica
        if time_window:
            cutoff_time = datetime.now() - time_window
            filtered_metrics = [m for m in filtered_metrics if m.timestamp >= cutoff_time]
        
        stats = APIStats()
        stats.update_from_metrics(filtered_metrics)
        return stats
    
    def get_system_impact_report(self) -> Dict[str, Any]:
        """Generar reporte del impacto en el sistema durante las pruebas"""
        if not self.system_metrics:
            return {"error": "No hay métricas del sistema disponibles"}
        
        cpu_usage = [m.cpu_percent for m in self.system_metrics]
        memory_usage = [m.memory_percent for m in self.system_metrics]
        network_sent = [m.network_bytes_sent for m in self.system_metrics]
        network_recv = [m.network_bytes_recv for m in self.system_metrics]
        tcp_connections = [m.active_tcp_connections for m in self.system_metrics]
        
        return {
            'monitoring_duration_seconds': len(self.system_metrics),
            'cpu_usage': {
                'min': min(cpu_usage),
                'max': max(cpu_usage),
                'avg': statistics.mean(cpu_usage),
                'peak_usage_percent': max(cpu_usage)
            },
            'memory_usage': {
                'min': min(memory_usage),
                'max': max(memory_usage),
                'avg': statistics.mean(memory_usage),
                'peak_usage_percent': max(memory_usage)
            },
            'network_activity': {
                'total_bytes_sent': max(network_sent) if network_sent else 0,
                'total_bytes_received': max(network_recv) if network_recv else 0,
                'peak_bytes_per_second': max(max(network_sent) if network_sent else [0], max(network_recv) if network_recv else [0])
            },
            'tcp_connections': {
                'min_connections': min(tcp_connections),
                'max_connections': max(tcp_connections),
                'avg_connections': statistics.mean(tcp_connections)
            }
        }
    
    def get_detailed_report(self) -> Dict[str, Any]:
        """Generar reporte detallado del monitoreo"""
        stats = self.get_stats()
        
        # Agrupar por endpoint
        endpoints_stats = {}
        unique_endpoints = set(m.endpoint for m in self.metrics)
        
        for endpoint in unique_endpoints:
            endpoint_stats = self.get_stats(endpoint=endpoint)
            endpoints_stats[endpoint] = {
                'total_requests': endpoint_stats.total_requests,
                'avg_response_time': endpoint_stats.avg_response_time,
                'availability': endpoint_stats.availability_percentage,
                'throughput': endpoint_stats.throughput_per_second,
                'avg_dns_time': endpoint_stats.avg_dns_time,
                'avg_tcp_time': endpoint_stats.avg_tcp_time,
                'avg_cpu_usage': endpoint_stats.avg_cpu_usage,
                'max_concurrent_connections': endpoint_stats.max_concurrent_connections
            }
        
        # Errores más comunes
        error_counts = {}
        for metric in self.metrics:
            if not metric.success and metric.error_message:
                error_counts[metric.error_message] = error_counts.get(metric.error_message, 0) + 1
        
        report = {
            'summary': {
                'total_requests': stats.total_requests,
                'successful_requests': stats.successful_requests,
                'failed_requests': stats.failed_requests,
                'avg_response_time': stats.avg_response_time,
                'availability_percentage': stats.availability_percentage,
                'total_data_transferred_mb': stats.total_data_transferred / (1024 * 1024)
            },
            'performance': {
                'min_response_time': stats.min_response_time,
                'max_response_time': stats.max_response_time,
                'percentile_95': stats.percentile_95,
                'throughput_per_second': stats.throughput_per_second
            },
            'system_metrics': {
                'avg_dns_resolution_time': stats.avg_dns_time,
                'avg_tcp_connection_time': stats.avg_tcp_time,
                'avg_cpu_usage_during_requests': stats.avg_cpu_usage,
                'avg_memory_usage_mb': stats.avg_memory_usage,
                'max_concurrent_connections': stats.max_concurrent_connections
            },
            'endpoints': endpoints_stats,
            'errors': dict(sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }
        
        # Agregar reporte del sistema si está disponible
        system_report = self.get_system_impact_report()
        if 'error' not in system_report:
            report['system_impact'] = system_report
        
        # Agregar métricas de red si están disponibles
        if self.network_metrics:
            # Filtrar datos válidos para evitar listas vacías
            ping_times = [m.ping_time for m in self.network_metrics if m.ping_time > 0]
            dns_times = [m.dns_resolution_time for m in self.network_metrics if m.dns_resolution_time > 0]
            traceroute_hops = [m.traceroute_hops for m in self.network_metrics if m.traceroute_hops > 0]
            
            network_report = {
                'total_network_tests': len(self.network_metrics),
                'avg_ping_time_ms': statistics.mean(ping_times) if ping_times else 0.0,
                'avg_dns_resolution_ms': statistics.mean(dns_times) if dns_times else 0.0,
                'avg_traceroute_hops': statistics.mean(traceroute_hops) if traceroute_hops else 0.0
            }
            report['network_analysis'] = network_report
        
        return report
    
    def clear_metrics(self):
        """Limpiar todas las métricas recolectadas"""
        self.metrics.clear()
        self.system_metrics.clear()
        self.network_metrics.clear()
    
    async def close(self):
        """Cerrar la sesión HTTP"""
        self._stop_system_monitoring()
        if self.session:
            await self.session.close()
            self.session = None


class PokemonAPIMonitor(APIMonitor):
    """Monitor específico para PokéAPI con endpoints predefinidos"""
    
    BASE_URL = "https://pokeapi.co/api/v2"
    
    def __init__(self):
        super().__init__()
        self.common_endpoints = [
            f"{self.BASE_URL}/pokemon/1",  # Bulbasaur
            f"{self.BASE_URL}/pokemon/25", # Pikachu
            f"{self.BASE_URL}/pokemon/150", # Mewtwo
            f"{self.BASE_URL}/type/electric",
            f"{self.BASE_URL}/ability/1",
            f"{self.BASE_URL}/generation/1"
        ]
    
    async def test_pokemon_endpoints(self) -> Dict[str, APIMetric]:
        """Probar endpoints comunes de Pokémon"""
        print("🔍 Probando endpoints de PokéAPI...")
        
        results = {}
        for url in self.common_endpoints:
            endpoint_name = url.split('/')[-2] + '/' + url.split('/')[-1]
            metric = await self.test_single_endpoint(url)
            results[endpoint_name] = metric
            print(f"  ✅ {endpoint_name}: {metric.response_time:.3f}s")
        
        return results
    
    async def comprehensive_pokemon_analysis(self) -> Dict[str, Any]:
        """Análisis completo de PokéAPI incluyendo métricas de sistema"""
        print("🐱 Iniciando análisis completo de PokéAPI...")
        
        # 1. Test de conectividad de red
        connectivity = await self.test_network_connectivity(f"{self.BASE_URL}/pokemon/1")
        
        # 2. Test de endpoints individuales
        endpoints_results = await self.test_pokemon_endpoints()
        
        # 3. Test de estrés con monitoreo del sistema
        stress_results = await self.stress_test_with_system_monitoring(
            f"{self.BASE_URL}/pokemon/25",  # Pikachu endpoint
            concurrent_requests=15,
            total_requests=75
        )
        
        # 4. Test de resiliencia
        resilience_results = await self.test_api_resilience(f"{self.BASE_URL}/pokemon/1")
        
        return {
            'connectivity_analysis': connectivity,
            'endpoints_performance': endpoints_results,
            'stress_test_results': stress_results,
            'resilience_test_results': resilience_results,
            'overall_stats': self.get_stats(),
            'detailed_report': self.get_detailed_report()
        }
    
    async def stress_test_pokemon_api(self, concurrent_users: int = 20, 
                                    requests_per_user: int = 10) -> Dict[str, Any]:
        """Realizar test de estrés específico para PokéAPI"""
        import time
        
        total_requests = concurrent_users * requests_per_user
        
        # Test de carga en endpoint popular
        popular_endpoint = f"{self.BASE_URL}/pokemon/25"  # Pikachu
        
        print(f"🔥 Test de estrés - {concurrent_users} usuarios, {requests_per_user} peticiones c/u")
        
        # Medir tiempo total del test
        start_time = time.time()
        
        metrics = await self.load_test(
            url=popular_endpoint,
            concurrent_requests=concurrent_users,
            total_requests=total_requests,
            delay_between_requests=0.05
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calcular tasa de éxito
        successful_requests = sum(1 for m in metrics if m.success)
        success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        
        return {
            'endpoint_tested': popular_endpoint,
            'total_requests': total_requests,
            'concurrent_users': concurrent_users,
            'total_time': total_time,
            'success_rate': success_rate,
            'metrics': metrics,
            'stats': self.get_stats(endpoint=popular_endpoint)
        }


# Instancia global del monitor de APIs
api_monitor = APIMonitor()
pokemon_monitor = PokemonAPIMonitor() 