"""
Módulo de perfilado de código
Integra cProfile, memory_profiler y py-spy para análisis avanzado
"""

import cProfile
import pstats
import io
import subprocess
import psutil
import time
import os
import tempfile
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading


class CodeProfiler:
    """Clase principal para el perfilado de código"""
    
    def __init__(self):
        self.active_profiles = {}
        self.profile_results = {}
    
    def profile_with_cprofile(self, target_function, duration: int = 10, *args, **kwargs) -> Dict[str, Any]:
        """
        Perfila una función usando cProfile
        
        Args:
            target_function: Función a perfilar
            duration: Duración máxima del perfilado
            *args, **kwargs: Argumentos para la función objetivo
        
        Returns:
            Dict con resultados del perfilado
        """
        try:
            profile = cProfile.Profile()
            
            start_time = time.time()
            profile.enable()
            
            # Ejecutar la función objetivo
            result = target_function(*args, **kwargs)
            
            profile.disable()
            end_time = time.time()
            
            # Crear buffer para capturar la salida de pstats
            output_buffer = io.StringIO()
            stats = pstats.Stats(profile, stream=output_buffer)
            
            # Configurar formato de salida
            stats.sort_stats('cumulative')
            stats.print_stats(50)  # Top 50 funciones
            
            # Obtener estadísticas adicionales
            stats_output = output_buffer.getvalue()
            
            # Estadísticas resumidas
            total_calls = stats.total_calls
            total_time = stats.total_tt
            
            return {
                "profiler_type": "cProfile",
                "timestamp": datetime.now().isoformat(),
                "execution_time": end_time - start_time,
                "total_calls": total_calls,
                "total_time": total_time,
                "result": result,
                "detailed_stats": stats_output,
                "success": True
            }
            
        except Exception as e:
            return {
                "profiler_type": "cProfile",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
    
    def profile_memory_usage(self, target_function, interval: float = 0.1, timeout: int = 60, *args, **kwargs) -> Dict[str, Any]:
        """
        Perfila el uso de memoria de una función usando memory_profiler
        
        Args:
            target_function: Función a perfilar
            interval: Intervalo de muestreo en segundos
            timeout: Timeout máximo para el perfilado
            *args, **kwargs: Argumentos para la función objetivo
        
        Returns:
            Dict con resultados del perfilado de memoria
        """
        try:
            from memory_profiler import memory_usage
            
            start_time = time.time()
            
            # Medir uso de memoria durante la ejecución
            mem_usage = memory_usage(
                (target_function, args, kwargs),
                interval=interval,
                timeout=timeout,
                include_children=True,
                multiprocess=True
            )
            
            end_time = time.time()
            
            if mem_usage:
                max_memory = max(mem_usage)
                min_memory = min(mem_usage)
                avg_memory = sum(mem_usage) / len(mem_usage)
                memory_delta = max_memory - min_memory
                
                return {
                    "profiler_type": "memory_profiler",
                    "timestamp": datetime.now().isoformat(),
                    "execution_time": end_time - start_time,
                    "memory_usage_mb": {
                        "max": max_memory,
                        "min": min_memory,
                        "average": avg_memory,
                        "delta": memory_delta,
                        "samples": len(mem_usage)
                    },
                    "memory_timeline": mem_usage,
                    "success": True
                }
            else:
                return {
                    "profiler_type": "memory_profiler",
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "error": "No se pudieron obtener mediciones de memoria"
                }
                
        except ImportError:
            return {
                "profiler_type": "memory_profiler",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": "memory_profiler no está instalado. Instala con: pip install memory-profiler"
            }
        except Exception as e:
            return {
                "profiler_type": "memory_profiler",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
    
    def profile_with_pyspy(self, pid: int, duration: int = 10, rate: int = 100) -> Dict[str, Any]:
        """
        Perfila un proceso usando py-spy
        
        Args:
            pid: Process ID del proceso a perfilar
            duration: Duración del perfilado en segundos
            rate: Frecuencia de muestreo por segundo
        
        Returns:
            Dict con resultados del perfilado con py-spy
        """
        try:
            # Verificar que el proceso existe
            if not psutil.pid_exists(pid):
                return {
                    "profiler_type": "py-spy",
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "error": f"No existe proceso con PID {pid}"
                }
            
            # Crear archivo temporal para la salida
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            try:
                # Comando py-spy
                cmd = [
                    'py-spy', 'record',
                    '--pid', str(pid),
                    '--duration', str(duration),
                    '--rate', str(rate),
                    '--output', temp_filename,
                    '--format', 'text'
                ]
                
                start_time = time.time()
                
                # Ejecutar py-spy
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=duration + 30  # Timeout un poco mayor que la duración
                )
                
                end_time = time.time()
                
                if result.returncode == 0:
                    # Leer resultados del archivo temporal
                    with open(temp_filename, 'r') as f:
                        profile_output = f.read()
                    
                    return {
                        "profiler_type": "py-spy",
                        "timestamp": datetime.now().isoformat(),
                        "execution_time": end_time - start_time,
                        "pid": pid,
                        "duration": duration,
                        "rate": rate,
                        "profile_output": profile_output,
                        "success": True
                    }
                else:
                    return {
                        "profiler_type": "py-spy",
                        "timestamp": datetime.now().isoformat(),
                        "success": False,
                        "error": f"py-spy error: {result.stderr}",
                        "returncode": result.returncode
                    }
                    
            finally:
                # Limpiar archivo temporal
                try:
                    os.unlink(temp_filename)
                except:
                    pass
                    
        except subprocess.TimeoutExpired:
            return {
                "profiler_type": "py-spy",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": f"py-spy timeout después de {duration + 30} segundos"
            }
        except FileNotFoundError:
            return {
                "profiler_type": "py-spy",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": "py-spy no está instalado. Instala con: pip install py-spy"
            }
        except Exception as e:
            return {
                "profiler_type": "py-spy",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
    
    def profile_function_comprehensive(self, target_function, duration: int = 10, *args, **kwargs) -> Dict[str, Any]:
        """
        Realiza un perfilado comprehensivo usando múltiples herramientas
        
        Args:
            target_function: Función a perfilar
            duration: Duración máxima del perfilado
            *args, **kwargs: Argumentos para la función objetivo
        
        Returns:
            Dict con resultados de todos los perfiladores
        """
        results = {
            "comprehensive_profile": True,
            "timestamp": datetime.now().isoformat(),
            "function_name": getattr(target_function, '__name__', 'unknown'),
            "profiles": {}
        }
        
        # cProfile
        cprofile_result = self.profile_with_cprofile(target_function, duration, *args, **kwargs)
        results["profiles"]["cprofile"] = cprofile_result
        
        # Memory profiler
        memory_result = self.profile_memory_usage(target_function, timeout=duration, *args, **kwargs)
        results["profiles"]["memory"] = memory_result
        
        # Intentar py-spy en el proceso actual (si es posible)
        current_pid = os.getpid()
        try:
            # Solo intentar py-spy si está disponible
            pyspy_result = self.profile_with_pyspy(current_pid, min(duration, 5))  # Duracion más corta para py-spy
            results["profiles"]["pyspy"] = pyspy_result
        except:
            results["profiles"]["pyspy"] = {
                "profiler_type": "py-spy",
                "success": False,
                "error": "py-spy no disponible o no se pudo ejecutar en el proceso actual"
            }
        
        return results
    
    def get_process_profile_snapshot(self, pid: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtiene un snapshot rápido del perfil de un proceso
        
        Args:
            pid: Process ID. Si es None, usa el proceso actual
        
        Returns:
            Dict con snapshot del proceso
        """
        try:
            if pid is None:
                pid = os.getpid()
            
            process = psutil.Process(pid)
            
            # Información básica
            process_info = {
                "pid": pid,
                "name": process.name(),
                "status": process.status(),
                "cpu_percent": process.cpu_percent(interval=1),
                "memory_info": {
                    "rss": process.memory_info().rss,
                    "vms": process.memory_info().vms,
                    "percent": process.memory_percent()
                },
                "threads": process.num_threads(),
                "files": process.num_fds() if hasattr(process, 'num_fds') else None,
                "connections": len(process.connections()),
                "cmdline": process.cmdline()
            }
            
            # Información de hilos
            try:
                threads_info = []
                for thread in process.threads():
                    threads_info.append({
                        "id": thread.id,
                        "user_time": thread.user_time,
                        "system_time": thread.system_time
                    })
                process_info["threads_detail"] = threads_info
            except (psutil.AccessDenied, AttributeError):
                process_info["threads_detail"] = None
            
            # Información de E/S
            try:
                io_counters = process.io_counters()
                process_info["io_counters"] = {
                    "read_count": io_counters.read_count,
                    "write_count": io_counters.write_count,
                    "read_bytes": io_counters.read_bytes,
                    "write_bytes": io_counters.write_bytes
                }
            except (psutil.AccessDenied, AttributeError):
                process_info["io_counters"] = None
            
            return {
                "snapshot_type": "process_profile",
                "timestamp": datetime.now().isoformat(),
                "process": process_info,
                "success": True
            }
            
        except psutil.NoSuchProcess:
            return {
                "snapshot_type": "process_profile",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": f"No existe proceso con PID {pid}"
            }
        except Exception as e:
            return {
                "snapshot_type": "process_profile",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
    
    def start_continuous_profiling(self, pid: int, duration: int = 60, interval: int = 5) -> str:
        """
        Inicia perfilado continuo de un proceso
        
        Args:
            pid: Process ID del proceso
            duration: Duración total del perfilado
            interval: Intervalo entre muestras
        
        Returns:
            ID del perfil para poder detenerlo después
        """
        profile_id = f"continuous_{pid}_{int(time.time())}"
        
        def continuous_profile():
            start_time = time.time()
            samples = []
            
            while time.time() - start_time < duration:
                try:
                    snapshot = self.get_process_profile_snapshot(pid)
                    samples.append(snapshot)
                    time.sleep(interval)
                except:
                    break
            
            # Guardar resultados
            self.profile_results[profile_id] = {
                "profile_type": "continuous",
                "pid": pid,
                "duration": duration,
                "interval": interval,
                "samples": samples,
                "start_time": start_time,
                "end_time": time.time()
            }
            
            # Remover de activos
            if profile_id in self.active_profiles:
                del self.active_profiles[profile_id]
        
        # Iniciar hilo de perfilado
        thread = threading.Thread(target=continuous_profile, daemon=True)
        thread.start()
        
        self.active_profiles[profile_id] = {
            "thread": thread,
            "start_time": time.time(),
            "pid": pid,
            "status": "running"
        }
        
        return profile_id
    
    def stop_continuous_profiling(self, profile_id: str) -> Dict[str, Any]:
        """
        Detiene un perfilado continuo
        
        Args:
            profile_id: ID del perfil a detener
        
        Returns:
            Dict con resultados del perfilado
        """
        if profile_id in self.active_profiles:
            # Marcar como detenido (el hilo se detendrá naturalmente)
            self.active_profiles[profile_id]["status"] = "stopped"
            
            # Esperar un poco para que termine
            time.sleep(1)
            
            # Retornar resultados si están disponibles
            if profile_id in self.profile_results:
                result = self.profile_results[profile_id]
                del self.profile_results[profile_id]  # Limpiar
                return result
            else:
                return {
                    "profile_id": profile_id,
                    "success": False,
                    "error": "Perfilado detenido pero resultados no disponibles aún"
                }
        else:
            return {
                "profile_id": profile_id,
                "success": False,
                "error": "Perfil no encontrado o ya finalizado"
            }
    
    def get_active_profiles(self) -> Dict[str, Any]:
        """
        Obtiene información sobre los perfiles activos
        
        Returns:
            Dict con información de perfiles activos
        """
        active_info = {}
        current_time = time.time()
        
        for profile_id, info in self.active_profiles.items():
            active_info[profile_id] = {
                "pid": info["pid"],
                "status": info["status"],
                "running_time": current_time - info["start_time"],
                "start_time": info["start_time"]
            }
        
        return {
            "active_profiles_count": len(active_info),
            "profiles": active_info
        }


# Instancia global del perfilador
code_profiler = CodeProfiler() 