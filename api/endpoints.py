"""
Endpoints de la API para el analizador de rendimiento
Define todas las rutas REST para acceder a las métricas del sistema
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import time

from core.monitoring import system_monitor
from core.profiling import code_profiler
from api.schemas import (
    CPUMetrics, MemoryMetrics, DiskIOMetrics, NetworkIOMetrics,
    ProcessMetrics, SystemSummary, APIResponse, HealthCheck,
    ProfilingRequest, ProfilingResult
)

# Router principal
router = APIRouter()

# Variable para tracking del tiempo de inicio de la API
start_time = time.time()


@router.get("/", response_model=HealthCheck)
async def health_check():
    """
    Health check de la API
    """
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=time.time() - start_time
    )


@router.get("/metrics/cpu", response_model=APIResponse)
async def get_cpu_metrics():
    """
    Obtiene métricas de CPU del sistema
    
    Returns:
        APIResponse con métricas de CPU
    """
    try:
        data = system_monitor.get_cpu_metrics()
        
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas de CPU: {str(e)}")


@router.get("/metrics/memory", response_model=APIResponse)
async def get_memory_metrics():
    """
    Obtiene métricas de memoria del sistema
    
    Returns:
        APIResponse con métricas de memoria
    """
    try:
        data = system_monitor.get_memory_metrics()
        
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas de memoria: {str(e)}")


@router.get("/metrics/disk-io", response_model=APIResponse)
async def get_disk_io_metrics():
    """
    Obtiene métricas de E/S de disco
    
    Returns:
        APIResponse con métricas de E/S de disco
    """
    try:
        data = system_monitor.get_disk_io_metrics()
        
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas de E/S de disco: {str(e)}")


@router.get("/metrics/network-io", response_model=APIResponse)
async def get_network_io_metrics():
    """
    Obtiene métricas de E/S de red
    
    Returns:
        APIResponse con métricas de E/S de red
    """
    try:
        data = system_monitor.get_network_io_metrics()
        
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas de E/S de red: {str(e)}")


@router.get("/metrics/process", response_model=APIResponse)
async def get_process_metrics(pid: Optional[int] = Query(None, description="Process ID. Si no se especifica, usa el proceso actual")):
    """
    Obtiene métricas de un proceso específico
    
    Args:
        pid: Process ID. Si es None, usa el proceso actual
    
    Returns:
        APIResponse con métricas del proceso
    """
    try:
        data = system_monitor.get_process_metrics(pid)
        
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas del proceso: {str(e)}")


@router.get("/metrics/system-summary", response_model=APIResponse)
async def get_system_summary():
    """
    Obtiene un resumen completo de todas las métricas del sistema
    
    Returns:
        APIResponse con resumen completo del sistema
    """
    try:
        data = system_monitor.get_system_summary()
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo resumen del sistema: {str(e)}")


@router.get("/metrics/live-cpu", response_model=APIResponse)
async def get_live_cpu_metrics(samples: int = Query(5, ge=1, le=60, description="Número de muestras a tomar")):
    """
    Obtiene métricas de CPU en tiempo real con múltiples muestras
    
    Args:
        samples: Número de muestras a tomar (1-60)
    
    Returns:
        APIResponse con lista de métricas de CPU
    """
    try:
        metrics_list = []
        
        for i in range(samples):
            data = system_monitor.get_cpu_metrics()
            if "error" not in data:
                metrics_list.append(data)
            
            # Pequeña pausa entre muestras (excepto en la última)
            if i < samples - 1:
                time.sleep(1)
        
        return APIResponse(
            success=True,
            data={
                "samples": metrics_list,
                "sample_count": len(metrics_list),
                "duration_seconds": samples
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas de CPU en vivo: {str(e)}")


@router.get("/metrics/comparison", response_model=APIResponse)
async def get_metrics_comparison():
    """
    Obtiene una comparación de métricas antes y después de un intervalo
    Útil para ver cambios en el sistema
    
    Returns:
        APIResponse con comparación de métricas
    """
    try:
        # Tomar primera muestra
        before_cpu = system_monitor.get_cpu_metrics()
        before_memory = system_monitor.get_memory_metrics()
        before_disk = system_monitor.get_disk_io_metrics()
        before_network = system_monitor.get_network_io_metrics()
        
        # Esperar 5 segundos
        time.sleep(5)
        
        # Tomar segunda muestra
        after_cpu = system_monitor.get_cpu_metrics()
        after_memory = system_monitor.get_memory_metrics()
        after_disk = system_monitor.get_disk_io_metrics()
        after_network = system_monitor.get_network_io_metrics()
        
        comparison_data = {
            "interval_seconds": 5,
            "before": {
                "cpu": before_cpu,
                "memory": before_memory,
                "disk_io": before_disk,
                "network_io": before_network
            },
            "after": {
                "cpu": after_cpu,
                "memory": after_memory,
                "disk_io": after_disk,
                "network_io": after_network
            }
        }
        
        return APIResponse(
            success=True,
            data=comparison_data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo comparación de métricas: {str(e)}")


@router.get("/info/system", response_model=APIResponse)
async def get_system_info():
    """
    Obtiene información general del sistema
    
    Returns:
        APIResponse con información del sistema
    """
    try:
        import platform
        import psutil
        
        system_info = {
            "platform": {
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            },
            "hardware": {
                "cpu_count_logical": psutil.cpu_count(logical=True),
                "cpu_count_physical": psutil.cpu_count(logical=False),
                "memory_total": psutil.virtual_memory().total,
                "disk_partitions": len(psutil.disk_partitions()),
                "network_interfaces": len(psutil.net_if_addrs())
            },
            "uptime": {
                "boot_time": psutil.boot_time(),
                "uptime_seconds": time.time() - psutil.boot_time()
            }
        }
        
        return APIResponse(
            success=True,
            data=system_info,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo información del sistema: {str(e)}")


# =================== ENDPOINTS DE PERFILADO ===================

@router.get("/profile/process-snapshot", response_model=APIResponse)
async def get_process_profile_snapshot(pid: Optional[int] = Query(None, description="Process ID. Si no se especifica, usa el proceso actual")):
    """
    Obtiene un snapshot del perfil de un proceso
    
    Args:
        pid: Process ID. Si es None, usa el proceso actual
    
    Returns:
        APIResponse con snapshot del proceso
    """
    try:
        data = code_profiler.get_process_profile_snapshot(pid)
        
        if not data.get("success", False):
            raise HTTPException(status_code=404, detail=data.get("error", "Error desconocido"))
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo snapshot del proceso: {str(e)}")


@router.post("/profile/pyspy", response_model=APIResponse)
async def profile_with_pyspy(
    pid: int = Query(description="Process ID del proceso a perfilar"),
    duration: int = Query(10, ge=1, le=300, description="Duración del perfilado en segundos"),
    rate: int = Query(100, ge=10, le=1000, description="Frecuencia de muestreo por segundo")
):
    """
    Perfila un proceso usando py-spy
    
    Args:
        pid: Process ID del proceso a perfilar
        duration: Duración del perfilado en segundos (1-300)
        rate: Frecuencia de muestreo por segundo (10-1000)
    
    Returns:
        APIResponse con resultados del perfilado py-spy
    """
    try:
        data = code_profiler.profile_with_pyspy(pid, duration, rate)
        
        if not data.get("success", False):
            raise HTTPException(status_code=400, detail=data.get("error", "Error en py-spy"))
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ejecutando py-spy: {str(e)}")


@router.post("/profile/continuous/start", response_model=APIResponse)
async def start_continuous_profiling(
    pid: int = Query(description="Process ID del proceso a perfilar"),
    duration: int = Query(60, ge=10, le=3600, description="Duración total del perfilado en segundos"),
    interval: int = Query(5, ge=1, le=60, description="Intervalo entre muestras en segundos")
):
    """
    Inicia perfilado continuo de un proceso
    
    Args:
        pid: Process ID del proceso
        duration: Duración total del perfilado (10-3600 segundos)
        interval: Intervalo entre muestras (1-60 segundos)
    
    Returns:
        APIResponse con ID del perfil para poder detenerlo después
    """
    try:
        profile_id = code_profiler.start_continuous_profiling(pid, duration, interval)
        
        return APIResponse(
            success=True,
            data={
                "profile_id": profile_id,
                "pid": pid,
                "duration": duration,
                "interval": interval,
                "message": "Perfilado continuo iniciado",
                "note": "Usa el profile_id para detener el perfilado o obtener resultados"
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error iniciando perfilado continuo: {str(e)}")


@router.post("/profile/continuous/stop", response_model=APIResponse)
async def stop_continuous_profiling(
    profile_id: str = Query(description="ID del perfil a detener")
):
    """
    Detiene un perfilado continuo y retorna los resultados
    
    Args:
        profile_id: ID del perfil a detener
    
    Returns:
        APIResponse con resultados del perfilado continuo
    """
    try:
        data = code_profiler.stop_continuous_profiling(profile_id)
        
        if not data.get("success", True):
            raise HTTPException(status_code=404, detail=data.get("error", "Perfil no encontrado"))
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deteniendo perfilado continuo: {str(e)}")


@router.get("/profile/active", response_model=APIResponse)
async def get_active_profiles():
    """
    Obtiene información sobre los perfiles activos
    
    Returns:
        APIResponse con información de perfiles activos
    """
    try:
        data = code_profiler.get_active_profiles()
        
        return APIResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo perfiles activos: {str(e)}")


@router.get("/profile/demo/cpu-intensive", response_model=APIResponse)
async def demo_cpu_intensive_profile():
    """
    Endpoint de demostración: perfila una función intensiva de CPU
    """
    try:
        def cpu_intensive_function():
            """Función de demostración que consume CPU"""
            import math
            result = 0
            for i in range(1000000):
                result += math.sqrt(i) * math.sin(i)
            return result
        
        # Perfilar la función con cProfile
        profile_result = code_profiler.profile_with_cprofile(cpu_intensive_function)
        
        return APIResponse(
            success=True,
            data={
                "demo_type": "cpu_intensive",
                "description": "Perfil de una función que consume mucha CPU",
                "profile_result": profile_result
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en demo de perfilado CPU: {str(e)}")


@router.get("/profile/demo/memory-intensive", response_model=APIResponse)
async def demo_memory_intensive_profile():
    """
    Endpoint de demostración: perfila una función intensiva de memoria
    """
    try:
        def memory_intensive_function():
            """Función de demostración que consume memoria"""
            import random
            data = []
            for _ in range(100):
                chunk = [random.random() for _ in range(10000)]
                data.append(chunk)
            return sum(sum(chunk) for chunk in data)
        
        # Perfilar la función con memory_profiler
        profile_result = code_profiler.profile_memory_usage(memory_intensive_function)
        
        return APIResponse(
            success=True,
            data={
                "demo_type": "memory_intensive",
                "description": "Perfil de una función que consume mucha memoria",
                "profile_result": profile_result
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en demo de perfilado memoria: {str(e)}")


@router.get("/profile/demo/comprehensive", response_model=APIResponse)
async def demo_comprehensive_profile():
    """
    Endpoint de demostración: perfil comprehensivo de una función
    """
    try:
        def mixed_function():
            """Función que combina uso de CPU y memoria"""
            import math
            import random
            
            # Parte intensiva de CPU
            cpu_result = 0
            for i in range(100000):
                cpu_result += math.sqrt(i)
            
            # Parte intensiva de memoria
            data = [random.random() for _ in range(50000)]
            memory_result = sum(data)
            
            return cpu_result + memory_result
        
        # Perfilado comprehensivo
        profile_result = code_profiler.profile_function_comprehensive(mixed_function)
        
        return APIResponse(
            success=True,
            data={
                "demo_type": "comprehensive",
                "description": "Perfil comprehensivo de una función mixta (CPU + memoria)",
                "profile_result": profile_result
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en demo de perfilado comprehensivo: {str(e)}") 