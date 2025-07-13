# 📊 Ejemplos de Uso del Analizador de Rendimiento

> **Sistema completo de monitoreo para Sistemas Operativos**
> Incluye monitoreo del sistema y análisis de rendimiento de APIs

## 🚀 Inicio Rápido

### Sistema de Monitoreo del Sistema

```bash
# Monitor principal con interfaz rica
python ejecutar_monitor.py

# Monitor simplificado
python monitor_terminal.py
```

### Sistema de Monitoreo de APIs

```bash
# Monitor completo de APIs
python ejecutar_api_monitor.py

# Demo específica de PokéAPI
python demo_pokeapi.py
```

### Aplicaciones de Ejemplo

```bash
# Aplicación de ejemplo para monitorear
python app_a_monitorear/main.py

# Demo completa del sistema
python demo_completo.py
```

## 🖥️ Monitoreo del Sistema

### 1. Monitor Principal Interactivo

```bash
python ejecutar_monitor.py
```

**Funcionalidades disponibles:**

- 📊 **Resumen del sistema**: Métricas generales de CPU, memoria, disco
- ⚡ **Monitoreo en tiempo real**: Visualización continua con actualización automática
- 🔍 **Demo de profiling**: Análisis de rendimiento de código Python
- 📈 **Comparación de métricas**: Comparar mediciones antes/después
- 🚪 **Interfaz rica**: Paneles coloridos con Rich library

**Ejemplo de métricas mostradas:**

```
🔥 CPU
├─ Uso Total: 15.2%
├─ Frecuencia: 2.4 GHz
├─ Núcleos: 8 lógicos, 4 físicos
└─ [████████████████░░░░] 75%

💾 MEMORIA
├─ RAM Usado: 8.2 GB / 16.0 GB (51.2%)
├─ SWAP: 0 MB usado
└─ [████████████████████████░░░░] 80%

💿 DISCO
├─ Lecturas: 1.2 MB/s
├─ Escrituras: 850 KB/s
└─ Total transferido: 2.1 GB

🌐 RED
├─ Enviado: 245 MB
├─ Recibido: 1.2 GB
└─ Velocidad: 125 Mbps
```

### 2. Métricas del Sistema Programáticamente

```python
from analizador_rendimiento.core.monitoring import SystemMonitor

# Crear monitor
monitor = SystemMonitor()

# Obtener métricas específicas
cpu_metrics = monitor.get_cpu_metrics()
memory_metrics = monitor.get_memory_metrics()
disk_metrics = monitor.get_disk_metrics()
network_metrics = monitor.get_network_metrics()

print(f"CPU: {cpu_metrics['cpu_percent_total']:.1f}%")
print(f"RAM: {memory_metrics['virtual_memory']['percent']:.1f}%")
```

### 3. Profiling de Aplicaciones

```python
from analizador_rendimiento.core.profiling import ProfilerManager

# Perfilado de CPU
profiler = ProfilerManager()
result = profiler.profile_cpu_intensive_function()

# Perfilado de memoria
memory_result = profiler.profile_memory_usage()

# Análisis con py-spy (si está instalado)
pyspy_result = profiler.run_pyspy_profiling(pid=1234, duration=10)
```

## 🌐 Monitoreo de APIs

### 1. Monitor Principal de APIs

```bash
python ejecutar_api_monitor.py
```

**Menú de opciones:**

1. **🔍 Probar endpoint individual**
2. **🔥 Test de carga personalizado**
3. **📊 Monitoreo continuo**
4. **🐱 Tests específicos de PokéAPI**
5. **📈 Ver reportes y estadísticas**
6. **🔄 Comparar tests**
7. **🧹 Limpiar métricas**

### 2. Ejemplo: Probar un Endpoint

```
🌐 Ingresa la URL del endpoint: https://api.github.com/users/octocat
📝 Método HTTP [GET/POST/PUT/DELETE] (GET): GET
🚀 Probando: https://api.github.com/users/octocat

✅ Resultado:
├─ Tiempo de respuesta: 0.245s
├─ Código de estado: 200
├─ Tamaño de respuesta: 1,234 bytes
└─ Estado: Exitoso
```

### 3. Test de Carga Personalizado

```
🌐 URL del endpoint: https://pokeapi.co/api/v2/pokemon/pikachu
📊 Número de peticiones (100): 50
👥 Usuarios concurrentes (10): 5
⏱️ Retraso entre peticiones en segundos (0.1): 0.05

🚀 Iniciando test de carga: 50 peticiones con 5 concurrentes
████████████████████████████████ 100% (50/50)
✅ Test completado en 2.34s

📈 Resultados:
├─ Peticiones exitosas: 50/50 (100%)
├─ Tiempo promedio: 0.124s
├─ Tiempo mínimo: 0.089s
├─ Tiempo máximo: 0.267s
├─ Throughput: 21.4 peticiones/segundo
└─ Disponibilidad: 100.0%
```

### 4. Demo de PokéAPI

```bash
python demo_pokeapi.py
```

**Fases de la demo:**

1. **🎮 Fase 1**: Test de endpoints comunes (pokemon, types, abilities)
2. **🔥 Fase 2**: Test de carga con 50 peticiones concurrentes
3. **📊 Fase 3**: Análisis detallado de resultados
4. **📈 Fase 4**: Reporte completo con estadísticas

**Resultado ejemplo:**

```
🏆 RESULTADOS FINALES
✅ Total de peticiones: 56
⚡ Tiempo promedio: 0.116s
📊 Disponibilidad: 100.00%
🚀 Throughput: 17.68 req/s
📦 Datos transferidos: 13.35 MB

💡 Conclusiones:
• PokéAPI es 🟢 muy confiable
• Tiempo de respuesta 🟢 excelente
• Maneja bien la carga concurrente
```

## 🧪 Escenarios de Prueba

### Escenario 1: Detectar Uso Alto de CPU

1. **Ejecutar aplicación de ejemplo:**

```bash
python app_a_monitorear/main.py
```

2. **Generar carga CPU en otra terminal:**

```bash
# Visitar en navegador o usar curl
curl "http://localhost:8001/cpu-intensivo?iteraciones=2000000"
```

3. **Monitorear en tiempo real:**

```bash
python ejecutar_monitor.py
# Seleccionar opción 2: Monitoreo en tiempo real
```

**Resultado esperado:**

- 📈 Incremento visible en uso de CPU
- 🔥 Barras de progreso mostrando la carga
- ⚡ Lista de procesos top actualizándose

### Escenario 2: Análisis de Performance de API

1. **Probar API lenta:**

```python
# En ejecutar_api_monitor.py, probar:
# URL: https://httpbin.org/delay/2
# Método: GET
```

2. **Comparar con API rápida:**

```python
# URL: https://httpbin.org/get
# Método: GET
```

3. **Ver comparación:**

- Opción 6 en el menú: "🔄 Comparar tests"

### Escenario 3: Test de Carga de API Real

1. **Configurar test de estrés:**

```
URL: https://api.github.com/users
Peticiones: 100
Concurrencia: 20
Retraso: 0.1s
```

2. **Analizar resultados:**

- Tiempo de respuesta promedio
- Rate limiting (código 429)
- Disponibilidad del servicio

## 📊 Interpretación de Métricas

### Métricas del Sistema

| Métrica       | Descripción           | Valores Normales              |
| ------------- | --------------------- | ----------------------------- |
| **CPU %**     | Uso del procesador    | < 70% para uso normal         |
| **RAM %**     | Memoria utilizada     | < 80% para rendimiento óptimo |
| **SWAP**      | Memoria virtual usada | Idealmente 0%                 |
| **Disco I/O** | Lectura/escritura     | Varía según aplicación        |
| **Red**       | Tráfico de red        | Depende del ancho de banda    |

### Métricas de APIs

| Métrica                 | Descripción              | Valores Deseables                    |
| ----------------------- | ------------------------ | ------------------------------------ |
| **Tiempo de Respuesta** | Latencia de la API       | < 200ms excelente, < 1s aceptable    |
| **Disponibilidad**      | % de peticiones exitosas | > 99.9% para producción              |
| **Throughput**          | Peticiones por segundo   | Depende de la capacidad del servidor |
| **Códigos de Error**    | 4xx, 5xx                 | < 1% para APIs estables              |

### Códigos de Estado HTTP

- **2xx** ✅ Exitoso
- **3xx** 🔄 Redirección
- **4xx** ❌ Error del cliente
- **5xx** 💥 Error del servidor

## 🛠️ Integración y Automatización

### Script de Monitoreo Continuo

```python
import time
import json
from analizador_rendimiento.core.monitoring import SystemMonitor
from analizador_rendimiento.core.api_monitor import APIMonitor

def monitor_loop():
    system_monitor = SystemMonitor()
    api_monitor = APIMonitor()

    while True:
        # Métricas del sistema
        cpu = system_monitor.get_cpu_metrics()
        memory = system_monitor.get_memory_metrics()

        # Test de API crítica
        api_result = await api_monitor.test_single_endpoint("https://mi-api.com/health")

        # Alertas
        if cpu['cpu_percent_total'] > 80:
            print(f"🚨 CPU alta: {cpu['cpu_percent_total']:.1f}%")

        if not api_result.success:
            print(f"🚨 API caída: {api_result.error_message}")

        time.sleep(60)  # Revisar cada minuto

if __name__ == "__main__":
    monitor_loop()
```

### Exportar Métricas a JSON

```python
from analizador_rendimiento.core.monitoring import SystemMonitor
import json
import datetime

monitor = SystemMonitor()
report = monitor.get_system_summary()

# Agregar timestamp
report['timestamp'] = datetime.datetime.now().isoformat()

# Guardar en archivo
with open(f"system_report_{datetime.date.today()}.json", "w") as f:
    json.dump(report, f, indent=2)

print("📊 Reporte guardado en system_report.json")
```

## 🎓 Conceptos de Sistemas Operativos

Este proyecto demuestra conceptos fundamentales:

### 1. **Gestión de Procesos**

- Monitoreo de procesos en tiempo real
- Uso de CPU por proceso
- Jerarquía de procesos

### 2. **Gestión de Memoria**

- Memoria virtual vs física
- Uso de SWAP
- Detección de fugas de memoria

### 3. **E/S de Dispositivos**

- Monitoreo de disco (lecturas/escrituras)
- Tráfico de red
- Performance de I/O

### 4. **Planificación de CPU**

- Distribución de carga entre núcleos
- Context switches
- Load average

### 5. **Herramientas del Sistema**

- Implementación de `top`/`htop` en Python
- Profiling similar a `perf`
- Monitoreo de red como `netstat`

## 📝 Archivos de Configuración

### requirements.txt

```text
fastapi==0.104.1
uvicorn==0.24.0
psutil==5.9.6
requests==2.31.0
aiohttp==3.9.1
click==8.1.7
rich==13.7.0
memory-profiler==0.61.0
```

### Estructura del Proyecto

```
SistemasOperativos/
├── analizador_rendimiento/          # 🆕 Nuevo sistema
│   ├── core/
│   │   ├── monitoring.py           # Monitoreo del sistema
│   │   ├── api_monitor.py          # Monitoreo de APIs
│   │   ├── api_visualizer.py       # Visualización de APIs
│   │   ├── visualizacion.py        # Visualización del sistema
│   │   └── profiling.py            # Herramientas de profiling
│   └── api_monitor_app.py          # App principal de APIs
├── ejecutar_monitor.py             # 🚀 Monitor del sistema
├── ejecutar_api_monitor.py         # 🚀 Monitor de APIs
├── demo_pokeapi.py                 # 🎮 Demo de PokéAPI
├── app_a_monitorear/               # App de ejemplo
├── api/                            # 📁 Sistema legacy
├── core/                           # 📁 Sistema legacy
└── requirements.txt                # Dependencias
```

## 🔧 Solución de Problemas

### Error: "cannot import name 'system_monitor'"

Si aparece este error al ejecutar `python main.py`, usa en su lugar:

```bash
python ejecutar_monitor.py    # Para monitoreo del sistema
python ejecutar_api_monitor.py # Para monitoreo de APIs
```

### Error: "Module not found"

Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Puerto ocupado

Si aparece "port already in use":

```bash
# Cambiar puerto en el código o cerrar proceso
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 🏆 Resumen de Comandos

| Comando                           | Descripción                       |
| --------------------------------- | --------------------------------- |
| `python ejecutar_monitor.py`      | 🖥️ Monitor principal del sistema  |
| `python ejecutar_api_monitor.py`  | 🌐 Monitor principal de APIs      |
| `python demo_pokeapi.py`          | 🐱 Demo completa de PokéAPI       |
| `python app_a_monitorear/main.py` | 🎯 App de ejemplo para monitorear |
| `python demo_completo.py`         | 🎪 Demo completa del sistema      |

**¡El analizador está listo para usar como herramienta educativa y profesional!** 🚀
