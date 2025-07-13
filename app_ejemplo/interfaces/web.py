#!/usr/bin/env python3
"""
Interfaz web con FastAPI para la aplicación de ejemplo
"""

import sys
import os
from typing import Dict, List, Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import asyncio

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.operaciones import OperacionesEjemplo, ResultadoOperacion
from core.utils import MonitorRendimiento, generar_reporte_html


# Modelos Pydantic para las respuestas
class RespuestaOperacion(BaseModel):
    nombre: str
    tiempo_ejecucion: float
    resultado: dict
    memoria_usada_mb: Optional[float] = None
    cpu_porcentaje: Optional[float] = None


class RespuestaEstadisticas(BaseModel):
    contador_operaciones: int
    memoria_acumulada_elementos: int
    memoria_acumulada_mb: float
    threads_activos: int
    running: bool


class RespuestaMetricas(BaseModel):
    cpu_porcentaje: float
    memoria_porcentaje: float
    memoria_usada_mb: float
    memoria_total_mb: float
    disco_lectura_mb: float
    disco_escritura_mb: float
    red_enviado_mb: float
    red_recibido_mb: float
    timestamp: float


# Instancia global de la aplicación
operaciones_global = OperacionesEjemplo()
monitor_global = MonitorRendimiento()

# Crear la aplicación FastAPI
app = FastAPI(
    title="Aplicación de Ejemplo para Monitoreo",
    description="Aplicación web con operaciones intensivas para probar el analizador de rendimiento",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/", response_class=HTMLResponse)
async def pagina_principal():
    """Página principal con interfaz web"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aplicación de Ejemplo - Monitoreo de Rendimiento</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .header { text-align: center; color: #333; border-bottom: 2px solid #007bff; padding-bottom: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
            .card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; }
            .card h3 { color: #007bff; margin-top: 0; }
            .btn { background: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #0056b3; }
            .btn-danger { background: #dc3545; }
            .btn-danger:hover { background: #c82333; }
            .btn-success { background: #28a745; }
            .btn-success:hover { background: #218838; }
            .result { margin-top: 10px; padding: 10px; background: #e9ecef; border-radius: 5px; }
            .loading { display: none; color: #007bff; }
        </style>
        <script>
            async function ejecutarOperacion(endpoint, params = {}) {
                const resultDiv = document.getElementById('resultado');
                const loadingDiv = document.getElementById('loading');
                
                loadingDiv.style.display = 'block';
                resultDiv.innerHTML = '';
                
                try {
                    const url = new URL(endpoint, window.location.origin);
                    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result">
                                <h4>✅ ${data.nombre}</h4>
                                <p><strong>Tiempo:</strong> ${data.tiempo_ejecucion.toFixed(2)}s</p>
                                <p><strong>Resultado:</strong> ${JSON.stringify(data.resultado, null, 2)}</p>
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="result" style="background: #f8d7da; color: #721c24;">❌ Error: ${data.detail}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result" style="background: #f8d7da; color: #721c24;">❌ Error: ${error.message}</div>`;
                } finally {
                    loadingDiv.style.display = 'none';
                }
            }
            
            async function obtenerEstadisticas() {
                const response = await fetch('/estadisticas');
                const data = await response.json();
                
                document.getElementById('stats').innerHTML = `
                    <h4>📊 Estadísticas</h4>
                    <p>Operaciones: ${data.contador_operaciones}</p>
                    <p>Memoria acumulada: ${data.memoria_acumulada_mb.toFixed(1)} MB</p>
                    <p>Threads activos: ${data.threads_activos}</p>
                `;
            }
            
            async function obtenerMetricas() {
                const response = await fetch('/metricas');
                const data = await response.json();
                
                document.getElementById('metrics').innerHTML = `
                    <h4>📈 Métricas del Sistema</h4>
                    <p>CPU: ${data.cpu_porcentaje.toFixed(1)}%</p>
                    <p>Memoria: ${data.memoria_porcentaje.toFixed(1)}%</p>
                    <p>Disco Lectura: ${data.disco_lectura_mb.toFixed(1)} MB</p>
                    <p>Disco Escritura: ${data.disco_escritura_mb.toFixed(1)} MB</p>
                `;
            }
            
            // Actualizar métricas cada 5 segundos
            setInterval(() => {
                obtenerEstadisticas();
                obtenerMetricas();
            }, 5000);
            
            // Cargar datos iniciales
            window.onload = () => {
                obtenerEstadisticas();
                obtenerMetricas();
            };
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔧 Aplicación de Ejemplo para Monitoreo de Rendimiento</h1>
                <p>Interfaz web para ejecutar operaciones intensivas y monitorear el rendimiento</p>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>🔥 Operaciones CPU</h3>
                    <button class="btn" onclick="ejecutarOperacion('/cpu-intensivo', {iteraciones: 500000})">CPU Intensiva (500K)</button>
                    <button class="btn" onclick="ejecutarOperacion('/cpu-intensivo', {iteraciones: 1000000})">CPU Intensiva (1M)</button>
                    <button class="btn" onclick="ejecutarOperacion('/fibonacci', {max_n: 30})">Fibonacci (30)</button>
                    <button class="btn" onclick="ejecutarOperacion('/fibonacci', {max_n: 35})">Fibonacci (35)</button>
                </div>
                
                <div class="card">
                    <h3>💾 Operaciones Memoria</h3>
                    <button class="btn" onclick="ejecutarOperacion('/memoria-intensivo', {tamaño_mb: 50})">Memoria (50 MB)</button>
                    <button class="btn" onclick="ejecutarOperacion('/memoria-intensivo', {tamaño_mb: 100})">Memoria (100 MB)</button>
                    <button class="btn" onclick="ejecutarOperacion('/memory-leak', {incremento_mb: 10, iteraciones: 3})">Memory Leak</button>
                    <button class="btn btn-success" onclick="ejecutarOperacion('/limpiar-memoria')">Limpiar Memoria</button>
                </div>
                
                <div class="card">
                    <h3>💿 Operaciones E/S</h3>
                    <button class="btn" onclick="ejecutarOperacion('/io-intensivo', {archivos: 5, tamaño_kb: 512})">E/S (5 archivos)</button>
                    <button class="btn" onclick="ejecutarOperacion('/io-intensivo', {archivos: 10, tamaño_kb: 1024})">E/S (10 archivos)</button>
                    <button class="btn" onclick="ejecutarOperacion('/multithreading', {num_threads: 2, trabajo: 50000})">Multithreading</button>
                </div>
                
                <div class="card">
                    <h3>⏰ Operaciones Especiales</h3>
                    <button class="btn" onclick="ejecutarOperacion('/operacion-lenta', {segundos: 3})">Operación Lenta (3s)</button>
                    <button class="btn" onclick="ejecutarOperacion('/operacion-lenta', {segundos: 5})">Operación Lenta (5s)</button>
                    <button class="btn btn-danger" onclick="ejecutarOperacion('/benchmark-completo')">Benchmark Completo</button>
                </div>
                
                <div class="card">
                    <h3>📊 Información del Sistema</h3>
                    <div id="stats">Cargando estadísticas...</div>
                    <div id="metrics">Cargando métricas...</div>
                </div>
                
                <div class="card">
                    <h3>📄 Reportes</h3>
                    <button class="btn" onclick="window.open('/docs', '_blank')">API Docs</button>
                    <button class="btn" onclick="window.open('/reporte-html', '_blank')">Generar Reporte</button>
                </div>
            </div>
            
            <div id="loading" class="loading">
                <h3>⏳ Ejecutando operación...</h3>
            </div>
            
            <div id="resultado"></div>
        </div>
    </body>
    </html>
    """
    return html_content


@app.get("/cpu-intensivo", response_model=RespuestaOperacion)
async def operacion_cpu_intensiva(iteraciones: int = 1000000):
    """Operación que consume mucho CPU"""
    try:
        resultado = operaciones_global.operacion_cpu_intensiva(iteraciones)
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado={"valor": resultado.resultado, "iteraciones": iteraciones}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memoria-intensivo", response_model=RespuestaOperacion)
async def operacion_memoria_intensiva(tamaño_mb: int = 100):
    """Operación que consume mucha memoria"""
    try:
        resultado = operaciones_global.operacion_memoria_intensiva(tamaño_mb)
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado=resultado.resultado,
            memoria_usada_mb=resultado.memoria_usada_mb
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/io-intensivo", response_model=RespuestaOperacion)
async def operacion_io_intensiva(archivos: int = 10, tamaño_kb: int = 1024):
    """Operación que realiza muchas operaciones de E/S"""
    try:
        resultado = operaciones_global.operacion_io_intensiva(archivos, tamaño_kb)
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado=resultado.resultado
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fibonacci", response_model=RespuestaOperacion)
async def operacion_fibonacci(max_n: int = 35):
    """Operación recursiva ineficiente usando Fibonacci"""
    try:
        if max_n > 40:
            raise HTTPException(status_code=400, detail="max_n no puede ser mayor a 40 (demasiado lento)")
        
        resultado = operaciones_global.operacion_fibonacci(max_n)
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado={"fibonacci": resultado.resultado, "n": max_n}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/multithreading", response_model=RespuestaOperacion)
async def operacion_multithreading(num_threads: int = 4, trabajo: int = 100000):
    """Operación que usa múltiples hilos"""
    try:
        resultado = operaciones_global.operacion_multithreading(num_threads, trabajo)
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado=resultado.resultado
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory-leak", response_model=RespuestaOperacion)
async def simulacion_memory_leak(incremento_mb: int = 10, iteraciones: int = 5):
    """Simula una fuga de memoria"""
    try:
        resultado = operaciones_global.simulacion_memory_leak(incremento_mb, iteraciones)
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado=resultado.resultado,
            memoria_usada_mb=resultado.memoria_usada_mb
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/limpiar-memoria", response_model=RespuestaOperacion)
async def limpiar_memoria():
    """Limpia la memoria acumulada"""
    try:
        resultado = operaciones_global.limpiar_memoria()
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado=resultado.resultado
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/operacion-lenta", response_model=RespuestaOperacion)
async def operacion_deliberadamente_lenta(segundos: int = 5):
    """Operación que simplemente espera"""
    try:
        resultado = operaciones_global.operacion_deliberadamente_lenta(segundos)
        return RespuestaOperacion(
            nombre=resultado.nombre,
            tiempo_ejecucion=resultado.tiempo_ejecucion,
            resultado=resultado.resultado
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/benchmark-completo")
async def benchmark_completo(background_tasks: BackgroundTasks):
    """Ejecuta un benchmark completo con todas las operaciones"""
    try:
        resultados = operaciones_global.benchmark_completo()
        
        # Convertir resultados a formato serializable
        resultados_serializables = {}
        for nombre, resultado in resultados.items():
            resultados_serializables[nombre] = {
                "nombre": resultado.nombre,
                "tiempo_ejecucion": resultado.tiempo_ejecucion,
                "resultado": resultado.resultado
            }
        
        return {
            "mensaje": "Benchmark completo ejecutado",
            "total_operaciones": len(resultados),
            "tiempo_total": sum(r.tiempo_ejecucion for r in resultados.values()),
            "resultados": resultados_serializables
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/estadisticas", response_model=RespuestaEstadisticas)
async def obtener_estadisticas():
    """Obtiene estadísticas actuales de la aplicación"""
    try:
        stats = operaciones_global.obtener_estadisticas()
        return RespuestaEstadisticas(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metricas", response_model=RespuestaMetricas)
async def obtener_metricas():
    """Obtiene métricas actuales del sistema"""
    try:
        metricas = monitor_global.obtener_metricas_actuales()
        return RespuestaMetricas(
            cpu_porcentaje=metricas.cpu_porcentaje,
            memoria_porcentaje=metricas.memoria_porcentaje,
            memoria_usada_mb=metricas.memoria_usada_mb,
            memoria_total_mb=metricas.memoria_total_mb,
            disco_lectura_mb=metricas.disco_lectura_mb,
            disco_escritura_mb=metricas.disco_escritura_mb,
            red_enviado_mb=metricas.red_enviado_mb,
            red_recibido_mb=metricas.red_recibido_mb,
            timestamp=metricas.timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reporte-html")
async def generar_reporte():
    """Genera un reporte HTML de las operaciones ejecutadas"""
    try:
        # Ejecutar un benchmark rápido para tener datos
        resultados = operaciones_global.benchmark_completo()
        
        archivo_reporte = "reporte_web_rendimiento.html"
        generar_reporte_html(resultados, archivo_reporte)
        
        return FileResponse(
            archivo_reporte,
            media_type='text/html',
            filename=archivo_reporte
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Función principal para ejecutar el servidor web"""
    print("🚀 Iniciando servidor web...")
    print("📱 Interfaz web disponible en: http://localhost:8000")
    print("📚 Documentación API en: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main() 