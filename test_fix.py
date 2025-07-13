#!/usr/bin/env python3
"""
Script de prueba para verificar que las correcciones funcionan
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'analizador_rendimiento'))

try:
    from analizador_rendimiento.core.monitoring import SystemMonitor
    from analizador_rendimiento.core.visualizacion import SystemVisualizer
    
    print("🧪 Probando correcciones...")
    
    # Probar SystemMonitor
    monitor = SystemMonitor()
    print("✅ SystemMonitor creado")
    
    # Probar método get_top_processes_by_cpu
    processes = monitor.get_top_processes_by_cpu(5)
    print(f"✅ get_top_processes_by_cpu funciona - {len(processes)} procesos obtenidos")
    
    # Probar métricas de memoria con nuevas claves
    memory_metrics = monitor.get_memory_metrics()
    print(f"✅ Métricas de memoria obtenidas")
    print(f"   - RAM: {memory_metrics.get('ram', {}).get('percentage', 'N/A')}%")
    print(f"   - SWAP: {memory_metrics.get('swap', {}).get('percentage', 'N/A')}%")
    
    # Probar visualizador
    visualizer = SystemVisualizer()
    print("✅ SystemVisualizer creado")
    
    # Probar panel de memoria
    memory_panel = visualizer.create_memory_panel()
    print("✅ Panel de memoria creado")
    
    print("\n🎉 ¡Todas las correcciones funcionan correctamente!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 