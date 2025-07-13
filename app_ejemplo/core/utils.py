#!/usr/bin/env python3
"""
Utilidades comunes para la aplicación de ejemplo
"""

import time
import psutil
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class MetricasRendimiento:
    """Métricas de rendimiento del sistema"""
    cpu_porcentaje: float
    memoria_porcentaje: float
    memoria_usada_mb: float
    memoria_total_mb: float
    disco_lectura_mb: float
    disco_escritura_mb: float
    red_enviado_mb: float
    red_recibido_mb: float
    timestamp: float


class MonitorRendimiento:
    """Monitor de rendimiento del sistema"""
    
    def __init__(self):
        self.metricas_historial: List[MetricasRendimiento] = []
        self.inicio_monitoreo = time.time()
    
    def obtener_metricas_actuales(self) -> MetricasRendimiento:
        """Obtiene las métricas actuales del sistema"""
        # CPU
        cpu_porcentaje = psutil.cpu_percent(interval=0.1)
        
        # Memoria
        memoria = psutil.virtual_memory()
        memoria_porcentaje = memoria.percent
        memoria_usada_mb = memoria.used / (1024 * 1024)
        memoria_total_mb = memoria.total / (1024 * 1024)
        
        # Disco (E/S)
        disco_io = psutil.disk_io_counters()
        disco_lectura_mb = disco_io.read_bytes / (1024 * 1024) if disco_io else 0
        disco_escritura_mb = disco_io.write_bytes / (1024 * 1024) if disco_io else 0
        
        # Red
        red_io = psutil.net_io_counters()
        red_enviado_mb = red_io.bytes_sent / (1024 * 1024) if red_io else 0
        red_recibido_mb = red_io.bytes_recv / (1024 * 1024) if red_io else 0
        
        metricas = MetricasRendimiento(
            cpu_porcentaje=cpu_porcentaje,
            memoria_porcentaje=memoria_porcentaje,
            memoria_usada_mb=memoria_usada_mb,
            memoria_total_mb=memoria_total_mb,
            disco_lectura_mb=disco_lectura_mb,
            disco_escritura_mb=disco_escritura_mb,
            red_enviado_mb=red_enviado_mb,
            red_recibido_mb=red_recibido_mb,
            timestamp=time.time()
        )
        
        self.metricas_historial.append(metricas)
        
        # Mantener solo las últimas 100 métricas
        if len(self.metricas_historial) > 100:
            self.metricas_historial = self.metricas_historial[-100:]
        
        return metricas
    
    def obtener_resumen_rendimiento(self) -> Dict:
        """Obtiene un resumen del rendimiento"""
        if not self.metricas_historial:
            return {}
        
        cpu_promedio = sum(m.cpu_porcentaje for m in self.metricas_historial) / len(self.metricas_historial)
        memoria_promedio = sum(m.memoria_porcentaje for m in self.metricas_historial) / len(self.metricas_historial)
        
        cpu_max = max(m.cpu_porcentaje for m in self.metricas_historial)
        memoria_max = max(m.memoria_porcentaje for m in self.metricas_historial)
        
        tiempo_monitoreo = time.time() - self.inicio_monitoreo
        
        return {
            "tiempo_monitoreo_segundos": tiempo_monitoreo,
            "muestras_tomadas": len(self.metricas_historial),
            "cpu": {
                "promedio": cpu_promedio,
                "maximo": cpu_max,
                "actual": self.metricas_historial[-1].cpu_porcentaje
            },
            "memoria": {
                "promedio": memoria_promedio,
                "maximo": memoria_max,
                "actual": self.metricas_historial[-1].memoria_porcentaje
            }
        }


def formatear_tiempo(segundos: float) -> str:
    """Formatea tiempo en segundos a formato legible"""
    if segundos < 1:
        return f"{segundos*1000:.1f}ms"
    elif segundos < 60:
        return f"{segundos:.2f}s"
    else:
        minutos = int(segundos // 60)
        segundos_restantes = segundos % 60
        return f"{minutos}m {segundos_restantes:.1f}s"


def formatear_bytes(bytes_cantidad: int) -> str:
    """Formatea cantidad de bytes a formato legible"""
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_cantidad < 1024.0:
            return f"{bytes_cantidad:.1f} {unidad}"
        bytes_cantidad /= 1024.0
    return f"{bytes_cantidad:.1f} PB"


def mostrar_tabla_resultados(resultados: Dict) -> None:
    """Muestra una tabla formateada de resultados"""
    print("\n" + "="*80)
    print("📊 RESULTADOS DE OPERACIONES")
    print("="*80)
    
    print(f"{'Operación':<20} {'Tiempo':<12} {'Estado':<10} {'Detalles'}")
    print("-" * 80)
    
    for nombre, resultado in resultados.items():
        tiempo_str = formatear_tiempo(resultado.tiempo_ejecucion)
        estado = "✅ OK" if resultado.tiempo_ejecucion > 0 else "❌ ERROR"
        
        # Extraer detalle relevante del resultado
        detalle = ""
        if isinstance(resultado.resultado, dict):
            if 'suma' in resultado.resultado:
                detalle = f"Suma: {resultado.resultado['suma']:,}"
            elif 'archivos_procesados' in resultado.resultado:
                detalle = f"Archivos: {resultado.resultado['archivos_procesados']}"
            elif 'num_threads' in resultado.resultado:
                detalle = f"Threads: {resultado.resultado['num_threads']}"
        elif isinstance(resultado.resultado, (int, float)):
            detalle = f"Resultado: {resultado.resultado:,}"
        
        print(f"{nombre:<20} {tiempo_str:<12} {estado:<10} {detalle}")
    
    print("="*80)


def generar_reporte_html(resultados: Dict, archivo: str = "reporte_rendimiento.html") -> None:
    """Genera un reporte HTML de los resultados"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reporte de Rendimiento</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .ok {{ color: green; }}
            .error {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>📊 Reporte de Rendimiento</h1>
        <p>Generado el: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <table>
            <tr>
                <th>Operación</th>
                <th>Tiempo de Ejecución</th>
                <th>Estado</th>
                <th>Resultado</th>
            </tr>
    """
    
    for nombre, resultado in resultados.items():
        tiempo_str = formatear_tiempo(resultado.tiempo_ejecucion)
        estado_class = "ok" if resultado.tiempo_ejecucion > 0 else "error"
        estado_text = "✅ Completado" if resultado.tiempo_ejecucion > 0 else "❌ Error"
        
        resultado_str = str(resultado.resultado)
        if len(resultado_str) > 100:
            resultado_str = resultado_str[:100] + "..."
        
        html_content += f"""
            <tr>
                <td>{nombre}</td>
                <td>{tiempo_str}</td>
                <td class="{estado_class}">{estado_text}</td>
                <td>{resultado_str}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📄 Reporte HTML generado: {archivo}") 