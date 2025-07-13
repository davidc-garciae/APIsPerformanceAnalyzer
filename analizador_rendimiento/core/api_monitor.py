#!/usr/bin/env python3
"""
Módulo de monitoreo de rendimiento de APIs externas
Analiza latencia, tiempo de respuesta, throughput y disponibilidad
"""

import time
import asyncio
import aiohttp
import statistics
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


class APIMonitor:
    """Monitor de rendimiento para APIs externas"""
    
    def __init__(self):
        self.metrics: List[APIMetric] = []
        self.running = False
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _make_request(self, url: str, method: str = 'GET', **kwargs) -> APIMetric:
        """Realizar una petición HTTP y medir métricas"""
        start_time = time.time()
        timestamp = datetime.now()
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            async with self.session.request(method, url, **kwargs) as response:
                content = await response.read()
                end_time = time.time()
                
                response_time = end_time - start_time
                response_size = len(content)
                success = 200 <= response.status < 400
                
                return APIMetric(
                    timestamp=timestamp,
                    endpoint=url,
                    response_time=response_time,
                    status_code=response.status,
                    response_size=response_size,
                    success=success,
                    error_message=None if success else f"HTTP {response.status}"
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
                error_message=str(e)
            )
    
    async def test_single_endpoint(self, url: str, method: str = 'GET') -> APIMetric:
        """Probar un endpoint individual"""
        metric = await self._make_request(url, method)
        self.metrics.append(metric)
        return metric
    
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
                'throughput': endpoint_stats.throughput_per_second
            }
        
        # Errores más comunes
        error_counts = {}
        for metric in self.metrics:
            if not metric.success and metric.error_message:
                error_counts[metric.error_message] = error_counts.get(metric.error_message, 0) + 1
        
        return {
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
            'endpoints': endpoints_stats,
            'errors': dict(sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def clear_metrics(self):
        """Limpiar todas las métricas recolectadas"""
        self.metrics.clear()
    
    async def close(self):
        """Cerrar la sesión HTTP"""
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