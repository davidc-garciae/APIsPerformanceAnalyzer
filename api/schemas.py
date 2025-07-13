"""
Esquemas de datos para la API usando Pydantic
Define las estructuras de respuesta y validación de datos
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime


class CPUFrequency(BaseModel):
    current: Optional[float] = Field(None, description="Frecuencia actual del CPU en MHz")
    min: Optional[float] = Field(None, description="Frecuencia mínima del CPU en MHz")
    max: Optional[float] = Field(None, description="Frecuencia máxima del CPU en MHz")


class CPUCount(BaseModel):
    logical: int = Field(description="Número de núcleos lógicos")
    physical: int = Field(description="Número de núcleos físicos")


class CPUStats(BaseModel):
    ctx_switches: int = Field(description="Número de cambios de contexto")
    interrupts: int = Field(description="Número de interrupciones")
    soft_interrupts: int = Field(description="Número de interrupciones software")
    syscalls: Optional[int] = Field(None, description="Número de llamadas al sistema")


class CPUMetrics(BaseModel):
    timestamp: str = Field(description="Timestamp de la medición")
    cpu_percent_total: float = Field(description="Porcentaje total de uso de CPU")
    cpu_percent_per_core: List[float] = Field(description="Porcentaje de uso por núcleo")
    cpu_frequency: CPUFrequency
    cpu_count: CPUCount
    cpu_stats: CPUStats


class VirtualMemory(BaseModel):
    total: int = Field(description="Memoria total en bytes")
    available: int = Field(description="Memoria disponible en bytes")
    used: int = Field(description="Memoria usada en bytes")
    free: int = Field(description="Memoria libre en bytes")
    percent: float = Field(description="Porcentaje de memoria usada")
    active: Optional[int] = Field(None, description="Memoria activa en bytes")
    inactive: Optional[int] = Field(None, description="Memoria inactiva en bytes")
    buffers: Optional[int] = Field(None, description="Buffers en bytes")
    cached: Optional[int] = Field(None, description="Memoria cacheada en bytes")


class SwapMemory(BaseModel):
    total: int = Field(description="Swap total en bytes")
    used: int = Field(description="Swap usado en bytes")
    free: int = Field(description="Swap libre en bytes")
    percent: float = Field(description="Porcentaje de swap usado")
    sin: int = Field(description="Bytes leídos del swap")
    sout: int = Field(description="Bytes escritos al swap")


class MemoryMetrics(BaseModel):
    timestamp: str = Field(description="Timestamp de la medición")
    virtual_memory: VirtualMemory
    swap_memory: SwapMemory


class DiskIOCounters(BaseModel):
    read_count: int = Field(description="Número de operaciones de lectura")
    write_count: int = Field(description="Número de operaciones de escritura")
    read_bytes: int = Field(description="Bytes leídos")
    write_bytes: int = Field(description="Bytes escritos")
    read_time: int = Field(description="Tiempo gastado leyendo (ms)")
    write_time: int = Field(description="Tiempo gastado escribiendo (ms)")


class DiskIORates(BaseModel):
    read_bytes_per_sec: Optional[float] = Field(None, description="Bytes leídos por segundo")
    write_bytes_per_sec: Optional[float] = Field(None, description="Bytes escritos por segundo")
    read_count_per_sec: Optional[float] = Field(None, description="Lecturas por segundo")
    write_count_per_sec: Optional[float] = Field(None, description="Escrituras por segundo")


class DiskPartition(BaseModel):
    device: str = Field(description="Dispositivo")
    mountpoint: str = Field(description="Punto de montaje")
    fstype: str = Field(description="Sistema de archivos")
    total: int = Field(description="Espacio total en bytes")
    used: int = Field(description="Espacio usado en bytes")
    free: int = Field(description="Espacio libre en bytes")
    percent: float = Field(description="Porcentaje de uso")


class DiskIOMetrics(BaseModel):
    timestamp: str = Field(description="Timestamp de la medición")
    disk_io_counters: DiskIOCounters
    disk_io_rates: DiskIORates
    disk_partitions: List[DiskPartition]


class NetworkIOCounters(BaseModel):
    bytes_sent: int = Field(description="Bytes enviados")
    bytes_recv: int = Field(description="Bytes recibidos")
    packets_sent: int = Field(description="Paquetes enviados")
    packets_recv: int = Field(description="Paquetes recibidos")
    errin: int = Field(description="Errores de entrada")
    errout: int = Field(description="Errores de salida")
    dropin: int = Field(description="Paquetes de entrada descartados")
    dropout: int = Field(description="Paquetes de salida descartados")


class NetworkIORates(BaseModel):
    bytes_sent_per_sec: Optional[float] = Field(None, description="Bytes enviados por segundo")
    bytes_recv_per_sec: Optional[float] = Field(None, description="Bytes recibidos por segundo")
    packets_sent_per_sec: Optional[float] = Field(None, description="Paquetes enviados por segundo")
    packets_recv_per_sec: Optional[float] = Field(None, description="Paquetes recibidos por segundo")


class NetworkInterface(BaseModel):
    bytes_sent: int = Field(description="Bytes enviados")
    bytes_recv: int = Field(description="Bytes recibidos")
    packets_sent: int = Field(description="Paquetes enviados")
    packets_recv: int = Field(description="Paquetes recibidos")
    errin: int = Field(description="Errores de entrada")
    errout: int = Field(description="Errores de salida")
    dropin: int = Field(description="Paquetes de entrada descartados")
    dropout: int = Field(description="Paquetes de salida descartados")


class NetworkIOMetrics(BaseModel):
    timestamp: str = Field(description="Timestamp de la medición")
    network_io_counters: NetworkIOCounters
    network_io_rates: NetworkIORates
    interfaces: Dict[str, NetworkInterface]


class ProcessMemoryInfo(BaseModel):
    rss: int = Field(description="Resident Set Size en bytes")
    vms: int = Field(description="Virtual Memory Size en bytes")


class ProcessIOCounters(BaseModel):
    read_count: int = Field(description="Número de operaciones de lectura")
    write_count: int = Field(description="Número de operaciones de escritura")
    read_bytes: int = Field(description="Bytes leídos")
    write_bytes: int = Field(description="Bytes escritos")


class ProcessInfo(BaseModel):
    pid: int = Field(description="Process ID")
    name: str = Field(description="Nombre del proceso")
    status: str = Field(description="Estado del proceso")
    create_time: float = Field(description="Tiempo de creación del proceso")
    cpu_percent: float = Field(description="Porcentaje de CPU usado por el proceso")
    memory_info: ProcessMemoryInfo
    memory_percent: float = Field(description="Porcentaje de memoria usado por el proceso")
    num_threads: int = Field(description="Número de hilos")
    num_fds: Optional[int] = Field(None, description="Número de file descriptors")
    connections: int = Field(description="Número de conexiones de red")
    cmdline: List[str] = Field(description="Línea de comandos")
    io_counters: Optional[ProcessIOCounters] = Field(None, description="Contadores de E/S")


class ProcessMetrics(BaseModel):
    timestamp: str = Field(description="Timestamp de la medición")
    process: ProcessInfo


class User(BaseModel):
    name: str = Field(description="Nombre del usuario")
    terminal: Optional[str] = Field(None, description="Terminal")
    host: Optional[str] = Field(None, description="Host")
    started: float = Field(description="Tiempo de inicio de sesión")


class SystemSummary(BaseModel):
    timestamp: str = Field(description="Timestamp de la medición")
    cpu: CPUMetrics
    memory: MemoryMetrics
    disk_io: DiskIOMetrics
    network_io: NetworkIOMetrics
    boot_time: float = Field(description="Tiempo de arranque del sistema")
    users: List[User] = Field(description="Usuarios conectados")


class ProfilingRequest(BaseModel):
    target_function: str = Field(description="Nombre de la función a perfilar")
    duration: int = Field(default=10, description="Duración del perfilado en segundos")
    profiler_type: str = Field(default="cProfile", description="Tipo de perfilador: cProfile, memory_profiler, py-spy")


class ProfilingResult(BaseModel):
    timestamp: str = Field(description="Timestamp del perfilado")
    profiler_type: str = Field(description="Tipo de perfilador usado")
    duration: int = Field(description="Duración del perfilado")
    result: str = Field(description="Resultado del perfilado")
    success: bool = Field(description="Si el perfilado fue exitoso")
    error: Optional[str] = Field(None, description="Error si el perfilado falló")


class APIResponse(BaseModel):
    success: bool = Field(description="Si la operación fue exitosa")
    data: Optional[Any] = Field(None, description="Datos de respuesta")
    error: Optional[str] = Field(None, description="Mensaje de error")
    timestamp: str = Field(description="Timestamp de la respuesta")


class HealthCheck(BaseModel):
    status: str = Field(description="Estado de la API")
    timestamp: str = Field(description="Timestamp del health check")
    version: str = Field(description="Versión de la API")
    uptime: float = Field(description="Tiempo activo en segundos") 