"""
Archivo principal del Analizador de Rendimiento
Inicia la API con FastAPI y configura todos los endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.endpoints import router as api_router

# Crear instancia de FastAPI
app = FastAPI(
    title="Analizador de Rendimiento de Aplicaciones Web",
    description="API para monitorizar y analizar el rendimiento de aplicaciones web mediante métricas de CPU, memoria, E/S y perfilado de funciones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de la API
app.include_router(api_router, prefix="/api/v1")

# Endpoint raíz adicional
@app.get("/")
async def root():
    """
    Endpoint raíz que proporciona información básica de la API
    """
    return {
        "message": "Analizador de Rendimiento de Aplicaciones Web",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/api/v1/",
        "endpoints": {
            "cpu_metrics": "/api/v1/metrics/cpu",
            "memory_metrics": "/api/v1/metrics/memory",
            "disk_io_metrics": "/api/v1/metrics/disk-io",
            "network_io_metrics": "/api/v1/metrics/network-io",
            "process_metrics": "/api/v1/metrics/process",
            "system_summary": "/api/v1/metrics/system-summary",
            "live_cpu": "/api/v1/metrics/live-cpu",
            "comparison": "/api/v1/metrics/comparison",
            "system_info": "/api/v1/info/system"
        }
    }


if __name__ == "__main__":
    print("🚀 Iniciando Analizador de Rendimiento...")
    print("📊 API disponible en: http://localhost:8000")
    print("📖 Documentación en: http://localhost:8000/docs")
    print("🔍 ReDoc en: http://localhost:8000/redoc")
    print("\n✨ Endpoints principales:")
    print("   • CPU: http://localhost:8000/api/v1/metrics/cpu")
    print("   • Memoria: http://localhost:8000/api/v1/metrics/memory")
    print("   • E/S Disco: http://localhost:8000/api/v1/metrics/disk-io")
    print("   • E/S Red: http://localhost:8000/api/v1/metrics/network-io")
    print("   • Resumen: http://localhost:8000/api/v1/metrics/system-summary")
    print("\n⚡ Presiona Ctrl+C para detener el servidor")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 