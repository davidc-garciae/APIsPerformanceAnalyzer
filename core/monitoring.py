"""
Módulo de monitoreo de recursos del sistema
Utiliza psutil para recolectar métricas de CPU, memoria y E/S
"""

import psutil
import time
from typing import Dict, List, Optional
from datetime import datetime


class SystemMonitor:
    """Clase principal para monitorear recursos del sistema"""

    def __init__(self):
        self.last_io_counters = None
        self.last_net_counters = None
        self.last_check_time = None

    def get_cpu_metrics(self) -> Dict:
        """
        Obtiene métricas de CPU
        Returns:
            Dict con métricas de CPU (porcentaje total, por núcleo, frecuencia)
        """
        try:
            # Obtener porcentaje de CPU (promedio en 1 segundo)
            cpu_percent = psutil.cpu_percent(interval=1)

            # Obtener porcentaje por núcleo
            cpu_percent_per_core = psutil.cpu_percent(interval=0.1, percpu=True)

            # Obtener frecuencia de CPU
            cpu_freq = psutil.cpu_freq()

            # Obtener información de núcleos
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_count_physical = psutil.cpu_count(logical=False)

            # Obtener estadísticas de CPU
            cpu_stats = psutil.cpu_stats()

            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent_total": cpu_percent,
                "cpu_percent_per_core": cpu_percent_per_core,
                "cpu_frequency": {
                    "current": cpu_freq.current if cpu_freq else None,
                    "min": cpu_freq.min if cpu_freq else None,
                    "max": cpu_freq.max if cpu_freq else None
                },
                "cpu_count": {
                    "logical": cpu_count_logical,
                    "physical": cpu_count_physical
                },
                "cpu_stats": {
                    "ctx_switches": cpu_stats.ctx_switches,
                    "interrupts": cpu_stats.interrupts,
                    "soft_interrupts": cpu_stats.soft_interrupts,
                    "syscalls": cpu_stats.syscalls if hasattr(cpu_stats, 'syscalls') else None
                }
            }
        except Exception as e:
            return {"error": f"Error obteniendo métricas de CPU: {str(e)}"}

    def get_memory_metrics(self) -> Dict:
        """
        Obtiene métricas de memoria
        Returns:
            Dict con métricas de memoria (virtual, swap)
        """
        try:
            # Memoria virtual
            virtual_memory = psutil.virtual_memory()

            # Memoria swap
            swap_memory = psutil.swap_memory()

            return {
                "timestamp": datetime.now().isoformat(),
                "virtual_memory": {
                    "total": virtual_memory.total,
                    "available": virtual_memory.available,
                    "used": virtual_memory.used,
                    "free": virtual_memory.free,
                    "percent": virtual_memory.percent,
                    "active": virtual_memory.active if hasattr(virtual_memory, 'active') else None,
                    "inactive": virtual_memory.inactive if hasattr(virtual_memory, 'inactive') else None,
                    "buffers": virtual_memory.buffers if hasattr(virtual_memory, 'buffers') else None,
                    "cached": virtual_memory.cached if hasattr(virtual_memory, 'cached') else None
                },
                "swap_memory": {
                    "total": swap_memory.total,
                    "used": swap_memory.used,
                    "free": swap_memory.free,
                    "percent": swap_memory.percent,
                    "sin": swap_memory.sin,
                    "sout": swap_memory.sout
                }
            }
        except Exception as e:
            return {"error": f"Error obteniendo métricas de memoria: {str(e)}"}

    def get_disk_io_metrics(self) -> Dict:
        """
        Obtiene métricas de E/S de disco
        Returns:
            Dict con métricas de E/S de disco
        """
        try:
            current_time = time.time()

            # Obtener contadores de E/S de disco
            disk_io = psutil.disk_io_counters()

            if disk_io is None:
                return {"error": "No se pudieron obtener métricas de E/S de disco"}

            # Calcular tasas si tenemos datos previos
            rates = {}
            if self.last_io_counters and self.last_check_time:
                time_delta = current_time - self.last_check_time
                if time_delta > 0:
                    rates = {
                        "read_bytes_per_sec": (disk_io.read_bytes - self.last_io_counters.read_bytes) / time_delta,
                        "write_bytes_per_sec": (disk_io.write_bytes - self.last_io_counters.write_bytes) / time_delta,
                        "read_count_per_sec": (disk_io.read_count - self.last_io_counters.read_count) / time_delta,
                        "write_count_per_sec": (disk_io.write_count - self.last_io_counters.write_count) / time_delta
                    }

            # Guardar datos actuales para próxima medición
            self.last_io_counters = disk_io
            self.last_check_time = current_time

            # Obtener información de discos
            disk_partitions = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_partitions.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except PermissionError:
                    # Algunos puntos de montaje pueden no ser accesibles
                    continue

            return {
                "timestamp": datetime.now().isoformat(),
                "disk_io_counters": {
                    "read_count": disk_io.read_count,
                    "write_count": disk_io.write_count,
                    "read_bytes": disk_io.read_bytes,
                    "write_bytes": disk_io.write_bytes,
                    "read_time": disk_io.read_time,
                    "write_time": disk_io.write_time
                },
                "disk_io_rates": rates,
                "disk_partitions": disk_partitions
            }
        except Exception as e:
            return {"error": f"Error obteniendo métricas de E/S de disco: {str(e)}"}

    def get_network_io_metrics(self) -> Dict:
        """
        Obtiene métricas de E/S de red
        Returns:
            Dict con métricas de E/S de red
        """
        try:
            current_time = time.time()

            # Obtener contadores de red
            net_io = psutil.net_io_counters()

            if net_io is None:
                return {"error": "No se pudieron obtener métricas de red"}

            # Calcular tasas si tenemos datos previos
            rates = {}
            if self.last_net_counters and self.last_check_time:
                time_delta = current_time - self.last_check_time
                if time_delta > 0:
                    rates = {
                        "bytes_sent_per_sec": (net_io.bytes_sent - self.last_net_counters.bytes_sent) / time_delta,
                        "bytes_recv_per_sec": (net_io.bytes_recv - self.last_net_counters.bytes_recv) / time_delta,
                        "packets_sent_per_sec": (net_io.packets_sent - self.last_net_counters.packets_sent) / time_delta,
                        "packets_recv_per_sec": (net_io.packets_recv - self.last_net_counters.packets_recv) / time_delta
                    }

            # Guardar datos actuales para próxima medición
            self.last_net_counters = net_io

            # Obtener información por interfaz
            net_io_per_interface = {}
            for interface, stats in psutil.net_io_counters(pernic=True).items():
                net_io_per_interface[interface] = {
                    "bytes_sent": stats.bytes_sent,
                    "bytes_recv": stats.bytes_recv,
                    "packets_sent": stats.packets_sent,
                    "packets_recv": stats.packets_recv,
                    "errin": stats.errin,
                    "errout": stats.errout,
                    "dropin": stats.dropin,
                    "dropout": stats.dropout
                }

            return {
                "timestamp": datetime.now().isoformat(),
                "network_io_counters": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                    "errin": net_io.errin,
                    "errout": net_io.errout,
                    "dropin": net_io.dropin,
                    "dropout": net_io.dropout
                },
                "network_io_rates": rates,
                "interfaces": net_io_per_interface
            }
        except Exception as e:
            return {"error": f"Error obteniendo métricas de red: {str(e)}"}

    def get_process_metrics(self, pid: Optional[int] = None) -> Dict:
        """
        Obtiene métricas de un proceso específico o del proceso actual
        Args:
            pid: Process ID. Si es None, usa el proceso actual
        Returns:
            Dict con métricas del proceso
        """
        try:
            if pid is None:
                process = psutil.Process()
            else:
                process = psutil.Process(pid)

            # Información básica del proceso
            process_info = {
                "pid": process.pid,
                "name": process.name(),
                "status": process.status(),
                "create_time": process.create_time(),
                "cpu_percent": process.cpu_percent(interval=0.1),
                "memory_percent": process.memory_percent(),
                "memory_info": process.memory_info(),
                "io_counters": process.io_counters(),
                "threads": process.num_threads(),
                "connections": process.connections()
            }

            return process_info

        except psutil.NoSuchProcess:
            return {"error": f"Proceso con PID {pid} no encontrado"}
        except Exception as e:
            return {"error": f"Error obteniendo métricas del proceso: {str(e)}"}

    def get_top_processes_by_cpu(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene una lista de los procesos que más CPU consumen
        Args:
            limit: Número de procesos a devolver
        Returns:
            Lista de procesos
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Ordenar por uso de CPU
        sorted_processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
        return sorted_processes[:limit]

    def get_system_summary(self) -> Dict:
        """
        Obtiene un resumen completo del estado del sistema
        """
        try:
            return {
                "cpu": self.get_cpu_metrics(),
                "memory": self.get_memory_metrics(),
                "disk": self.get_disk_io_metrics(),
                "network": self.get_network_io_metrics(),
                "top_processes": self.get_top_processes_by_cpu(5)
            }
        except Exception as e:
            return {"error": f"Error al generar el resumen del sistema: {str(e)}"}