"""
Aplicación de Ejemplo para Monitoreo de Rendimiento
Paquete con operaciones intensivas para demostrar análisis de rendimiento
"""

__version__ = "2.0.0"
__author__ = "Sistema de Monitoreo de Rendimiento"
__description__ = "Aplicación con operaciones intensivas para pruebas de rendimiento"

from .core.operaciones import OperacionesEjemplo, ResultadoOperacion
from .core.utils import MonitorRendimiento, MetricasRendimiento

__all__ = [
    "OperacionesEjemplo",
    "ResultadoOperacion", 
    "MonitorRendimiento",
    "MetricasRendimiento"
] 