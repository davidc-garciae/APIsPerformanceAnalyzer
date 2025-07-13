"""
Módulo de monitoreo de recursos del sistema
Utiliza psutil para recolectar métricas de CPU, memoria y E/S
"""

import psutil
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import platform
import os


class SystemMonitor:
    """Monitor del sistema para recopilar métricas de rendimiento"""
    
    def __init__(self):
        self.previous_disk_io = None
        self.previous_network_io = None
        self.last_measurement_time = None

    def get_cpu_metrics(self) -> Dict:
        """
        Obtiene métricas de CPU
        Returns:
            Dict con información de CPU, frecuencia y uso por núcleo
        """
        try:
            # CPU total
            cpu_percent_total = psutil.cpu_percent(interval=1, percpu=False)
            
            # CPU por núcleo
            cpu_percent_per_core = psutil.cpu_percent(interval=None, percpu=True)
            
            # Información de frecuencia
            cpu_freq = psutil.cpu_freq()
            cpu_frequency = {
                "current": cpu_freq.current if cpu_freq else 0,
                "min": cpu_freq.min if cpu_freq else 0,
                "max": cpu_freq.max if cpu_freq else 0
            }
            
            # Conteo de núcleos
            cpu_count = {
                "logical": psutil.cpu_count(logical=True),
                "physical": psutil.cpu_count(logical=False)
            }
            
            # Estadísticas de CPU
            cpu_stats = psutil.cpu_stats()
            cpu_statistics = {
                "ctx_switches": cpu_stats.ctx_switches,
                "interrupts": cpu_stats.interrupts,
                "soft_interrupts": cpu_stats.soft_interrupts,
                "syscalls": cpu_stats.syscalls if hasattr(cpu_stats, 'syscalls') else 0
            }
            
            # Tiempos de CPU
            cpu_times = psutil.cpu_times()
            cpu_times_data = {
                "user": cpu_times.user,
                "system": cpu_times.system,
                "idle": cpu_times.idle
            }
            
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent_total": cpu_percent_total,
                "cpu_percent_per_core": cpu_percent_per_core,
                "cpu_frequency": cpu_frequency,
                "cpu_count": cpu_count,
                "cpu_statistics": cpu_statistics,
                "cpu_times": cpu_times_data
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo métricas de CPU: {str(e)}"}

    def get_memory_metrics(self) -> Dict:
        """
        Obtiene métricas de memoria
        Returns:
            Dict con información de memoria RAM y SWAP
        """
        try:
            # Memoria virtual (RAM)
            virtual_memory = psutil.virtual_memory()
            ram_data = {
                "total": virtual_memory.total,
                "available": virtual_memory.available,
                "used": virtual_memory.used,
                "free": virtual_memory.free,
                "percentage": virtual_memory.percent
            }
            
            # Memoria SWAP
            swap_memory = psutil.swap_memory()
            swap_data = {
                "total": swap_memory.total,
                "used": swap_memory.used,
                "free": swap_memory.free,
                "percentage": swap_memory.percent,
                "sin": swap_memory.sin,  # Bytes swapped in from disk
                "sout": swap_memory.sout  # Bytes swapped out to disk
            }
            
            return {
                "timestamp": datetime.now().isoformat(),
                "ram": ram_data,
                "swap": swap_data
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo métricas de memoria: {str(e)}"}

    def get_disk_io_metrics(self) -> Dict:
        """
        Obtiene métricas de E/S de disco
        Returns:
            Dict con información de lectura/escritura de disco
        """
        try:
            current_time = time.time()
            
            # Obtener contadores de E/S actuales
            disk_io = psutil.disk_io_counters()
            
            # Información básica de particiones
            disk_partitions = []
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    disk_partitions.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": partition_usage.total,
                        "used": partition_usage.used,
                        "free": partition_usage.free,
                        "percentage": partition_usage.percent
                    })
                except PermissionError:
                    continue
            
            disk_io_counters = {
                "read_count": disk_io.read_count if disk_io else 0,
                "write_count": disk_io.write_count if disk_io else 0,
                "read_bytes": disk_io.read_bytes if disk_io else 0,
                "write_bytes": disk_io.write_bytes if disk_io else 0,
                "read_time": disk_io.read_time if disk_io else 0,
                "write_time": disk_io.write_time if disk_io else 0
            }
            
            # Calcular tasas si tenemos medición anterior
            disk_io_rates = {"read_bytes_per_sec": 0, "write_bytes_per_sec": 0}
            
            if self.previous_disk_io and self.last_measurement_time:
                time_delta = current_time - self.last_measurement_time
                if time_delta > 0:
                    read_delta = disk_io_counters["read_bytes"] - self.previous_disk_io["read_bytes"]
                    write_delta = disk_io_counters["write_bytes"] - self.previous_disk_io["write_bytes"]
                    
                    disk_io_rates = {
                        "read_bytes_per_sec": read_delta / time_delta,
                        "write_bytes_per_sec": write_delta / time_delta
                    }
            
            # Actualizar valores anteriores
            self.previous_disk_io = disk_io_counters.copy()
            self.last_measurement_time = current_time
            
            return {
                "timestamp": datetime.now().isoformat(),
                "disk_io_counters": disk_io_counters,
                "disk_io_rates": disk_io_rates,
                "disk_partitions": disk_partitions
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo métricas de disco: {str(e)}"}

    def get_network_io_metrics(self) -> Dict:
        """
        Obtiene métricas de E/S de red
        Returns:
            Dict con información de envío/recepción de red
        """
        try:
            current_time = time.time()
            
            # Obtener contadores de red actuales
            network_io = psutil.net_io_counters()
            
            network_io_counters = {
                "bytes_sent": network_io.bytes_sent,
                "bytes_recv": network_io.bytes_recv,
                "packets_sent": network_io.packets_sent,
                "packets_recv": network_io.packets_recv,
                "errin": network_io.errin,
                "errout": network_io.errout,
                "dropin": network_io.dropin,
                "dropout": network_io.dropout
            }
            
            # Calcular tasas si tenemos medición anterior
            network_io_rates = {"bytes_sent_per_sec": 0, "bytes_recv_per_sec": 0}
            
            if self.previous_network_io and self.last_measurement_time:
                time_delta = current_time - self.last_measurement_time
                if time_delta > 0:
                    sent_delta = network_io_counters["bytes_sent"] - self.previous_network_io["bytes_sent"]
                    recv_delta = network_io_counters["bytes_recv"] - self.previous_network_io["bytes_recv"]
                    
                    network_io_rates = {
                        "bytes_sent_per_sec": sent_delta / time_delta,
                        "bytes_recv_per_sec": recv_delta / time_delta
                    }
            
            # Información de interfaces de red
            network_interfaces = {}
            try:
                for interface, addrs in psutil.net_if_addrs().items():
                    interface_info = []
                    for addr in addrs:
                        interface_info.append({
                            "family": str(addr.family),
                            "address": addr.address,
                            "netmask": addr.netmask,
                            "broadcast": addr.broadcast
                        })
                    network_interfaces[interface] = interface_info
            except Exception:
                network_interfaces = {}
            
            # Actualizar valores anteriores
            self.previous_network_io = network_io_counters.copy()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "network_io_counters": network_io_counters,
                "network_io_rates": network_io_rates,
                "network_interfaces": network_interfaces
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo métricas de red: {str(e)}"}

    def get_process_metrics(self, pid: Optional[int] = None) -> Dict:
        """
        Obtiene métricas de un proceso específico o de todos los procesos
        Args:
            pid: ID del proceso (opcional)
        Returns:
            Dict con información del proceso o lista de procesos
        """
        try:
            if pid:
                # Métricas de un proceso específico
                process = psutil.Process(pid)
                return {
                    "timestamp": datetime.now().isoformat(),
                    "pid": process.pid,
                    "name": process.name(),
                    "status": process.status(),
                    "cpu_percent": process.cpu_percent(),
                    "memory_info": process.memory_info()._asdict(),
                    "memory_percent": process.memory_percent(),
                    "create_time": process.create_time(),
                    "num_threads": process.num_threads()
                }
            else:
                # Lista de todos los procesos
                processes = []
                for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        processes.append(process.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                return {
                    "timestamp": datetime.now().isoformat(),
                    "processes": processes,
                    "total_processes": len(processes)
                }
                
        except psutil.NoSuchProcess:
            return {"error": f"No existe el proceso con PID {pid}"}
        except psutil.AccessDenied:
            return {"error": f"Acceso denegado al proceso con PID {pid}"}
        except Exception as e:
            return {"error": f"Error obteniendo métricas del proceso: {str(e)}"}
    
    def get_top_processes_by_cpu(self, limit: int = 5) -> List[Dict]:
        """
        Obtiene los procesos que más CPU consumen
        Args:
            limit: Número máximo de procesos a devolver
        Returns:
            Lista de procesos ordenados por uso de CPU
        """
        try:
            processes = []
            for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    # Obtener información del proceso
                    pinfo = process.info
                    if pinfo['cpu_percent'] is None:
                        pinfo['cpu_percent'] = 0.0
                    if pinfo['memory_percent'] is None:
                        pinfo['memory_percent'] = 0.0
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Ordenar por CPU y tomar los primeros 'limit'
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:limit]
            
        except Exception as e:
            return [{"error": f"Error obteniendo procesos: {str(e)}"}]
    
    def get_system_summary(self) -> Dict:
        """
        Obtiene un resumen completo del sistema
        Returns:
            Dict con resumen de todas las métricas
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(),
            "disk_io": self.get_disk_io_metrics(),
            "network_io": self.get_network_io_metrics(),
            "boot_time": psutil.boot_time(),
            "users": [{"name": user.name, "terminal": user.terminal, "host": user.host, "started": user.started} 
                     for user in psutil.users()]
        }


# Instancia global del monitor
system_monitor = SystemMonitor() 