# 📊 Analizador de Rendimiento - Sistemas Operativos

> **Sistema completo de monitoreo y análisis de rendimiento**  
> Monitoreo del sistema operativo + Análisis de APIs REST

## 🎯 Descripción

Proyecto educativo desarrollado para el curso de **Sistemas Operativos** que implementa un sistema completo de monitoreo y análisis de rendimiento con dos componentes principales:

1. **🖥️ Monitor del Sistema**: Métricas de CPU, memoria, disco, red y procesos
2. **🌐 Monitor de APIs**: Análisis de rendimiento, tests de carga y monitoreo continuo

Desarrollado con Python, utiliza interfaces de terminal coloridas e interactivas mediante Rich library.

## ✨ Características Principales

### 🖥️ Monitoreo del Sistema

- ⚡ **Monitoreo en tiempo real** con visualización colorida
- 📊 **Métricas completas**: CPU, memoria, disco, red, procesos
- 🔍 **Profiling de código**: cProfile, memory_profiler, py-spy
- 📈 **Comparación temporal** de métricas
- 🎨 **Interfaz rica** con paneles, barras de progreso y tablas

### 🌐 Monitoreo de APIs

- 🔍 **Tests de endpoints individuales** con métricas detalladas
- 🔥 **Tests de carga** con usuarios concurrentes
- 📊 **Monitoreo continuo** de disponibilidad
- 📈 **Estadísticas avanzadas**: latencia, throughput, percentiles
- 🐱 **Demo integrada** con PokéAPI para ejemplos prácticos

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

- Python 3.8 o superior
- Windows, Linux o macOS

### 2. Instalación

```bash
# Clonar o descargar el proyecto
cd SistemasOperativos

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Verificar Instalación

```bash
# Probar monitor del sistema
python ejecutar_monitor.py

# Probar monitor de APIs
python ejecutar_api_monitor.py
```

## 🎮 Inicio Rápido

### 🖥️ Monitor del Sistema

```bash
python ejecutar_monitor.py
```

**Opciones disponibles:**

- 📊 Resumen del sistema
- ⚡ Monitoreo en tiempo real
- 🔍 Demo de profiling
- 📈 Comparación de métricas

### 🌐 Monitor de APIs

```bash
python ejecutar_api_monitor.py
```

**Funcionalidades:**

- 🔍 Probar endpoints individuales
- 🔥 Tests de carga personalizados
- 📊 Monitoreo continuo
- 🐱 Tests específicos de PokéAPI

### 🎪 Demo Completa

```bash
# Demo completa del sistema
python demo_completo.py

# Demo específica de APIs con PokéAPI
python demo_pokeapi.py

# Aplicación de ejemplo para monitorear
python app_a_monitorear/main.py
```

## 📁 Estructura del Proyecto

```
SistemasOperativos/
├── 🆕 analizador_rendimiento/           # Sistema principal
│   ├── core/
│   │   ├── monitoring.py              # Monitoreo del sistema
│   │   ├── api_monitor.py             # Monitoreo de APIs
│   │   ├── api_visualizer.py          # Visualización de APIs
│   │   ├── visualizacion.py           # Visualización del sistema
│   │   └── profiling.py               # Herramientas de profiling
│   └── api_monitor_app.py             # App principal de APIs
├── 🚀 ejecutar_monitor.py              # [PRINCIPAL] Monitor del sistema
├── 🚀 ejecutar_api_monitor.py          # [PRINCIPAL] Monitor de APIs
├── 🎮 demo_pokeapi.py                  # Demo completa de PokéAPI
├── 🎪 demo_completo.py                 # Demo completa del sistema
├── 📱 app_a_monitorear/                # Aplicación de ejemplo
├── 📊 ejemplos_uso.md                  # Documentación detallada
├── 📁 api/ + core/                     # Sistema legacy (compatible)
└── 📦 requirements.txt                 # Dependencias
```

## 🎯 Casos de Uso

### 📚 Educativo - Sistemas Operativos

**Conceptos demostrados:**

- Gestión de procesos y memoria
- E/S de dispositivos (disco, red)
- Planificación de CPU
- Herramientas de monitoreo del SO
- Profiling y optimización

### 🔧 Profesional - DevOps

**Aplicaciones prácticas:**

- Monitoreo de servidores
- Tests de carga de APIs
- Detección de cuellos de botella
- Análisis de rendimiento
- Alertas automáticas

## 📊 Ejemplos de Salida

### Monitor del Sistema

```
╔══════════════════════ 🖥️ MONITOR DE RENDIMIENTO ══════════════════════╗
║                        Actualizado: 2025-07-13 11:30:15                ║
╚════════════════════════════════════════════════════════════════════════╝

🔥 CPU                               💾 MEMORIA
├─ Uso Total: 15.2%                  ├─ RAM: 8.2 GB / 16.0 GB (51.2%)
├─ Frecuencia: 2.4 GHz               ├─ SWAP: 0 MB usado
└─ [████████░░░░] 65%                └─ [████████████████████░░░░] 80%

💿 DISCO                             🌐 RED
├─ Lecturas: 1.2 MB/s                ├─ Enviado: 245 MB
├─ Escrituras: 850 KB/s              ├─ Recibido: 1.2 GB
└─ Total: 2.1 GB                     └─ Velocidad: 125 Mbps

⚡ TOP PROCESOS
┌─────┬──────────────────┬────────┬───────────┐
│ PID │ Nombre           │ CPU %  │ Memoria % │
├─────┼──────────────────┼────────┼───────────┤
│ 1234│ python.exe       │ 15.2%  │ 2.1%      │
│ 5678│ chrome.exe       │ 8.7%   │ 12.3%     │
└─────┴──────────────────┴────────┴───────────┘
```

### Monitor de APIs

```
╔═══════════════════════ 🔍 PRUEBA DE ENDPOINT ═══════════════════════╗
║ https://pokeapi.co/api/v2/pokemon/pikachu                           ║
╚═════════════════════════════════════════════════════════════════════╝

✅ Resultado:
├─ ⏱️  Tiempo de respuesta: 0.124s
├─ 📊 Código de estado: 200
├─ 📦 Tamaño de respuesta: 245.2 KB
├─ 🌐 Estado: Exitoso
└─ 🔗 Endpoint: GET /pokemon/pikachu

📈 Test de Carga - 50 peticiones, 10 concurrentes:
├─ ✅ Peticiones exitosas: 50/50 (100%)
├─ ⚡ Throughput: 21.4 req/s
├─ 📊 Tiempo promedio: 0.118s
├─ ⏱️  P95: 0.267s
└─ 🎯 Disponibilidad: 100.0%
```

## 🛠️ Comandos Principales

| Comando                           | Descripción                      | Uso                          |
| --------------------------------- | -------------------------------- | ---------------------------- |
| `python ejecutar_monitor.py`      | 🖥️ Monitor principal del sistema | Estudiantes, administradores |
| `python ejecutar_api_monitor.py`  | 🌐 Monitor de APIs completo      | Desarrolladores, DevOps      |
| `python demo_pokeapi.py`          | 🐱 Demo educativa con PokéAPI    | Aprendizaje, ejemplos        |
| `python app_a_monitorear/main.py` | 🎯 App de ejemplo                | Testing, simulación          |

## 🔧 Solución de Problemas

### Error: "cannot import name 'system_monitor'"

```bash
# ❌ No usar:
python main.py

# ✅ Usar en su lugar:
python ejecutar_monitor.py      # Sistema
python ejecutar_api_monitor.py  # APIs
```

### Error: "Module not found"

```bash
pip install -r requirements.txt
```

### Puerto ocupado

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
sudo lsof -i :8000
sudo kill -9 <PID>
```

## 📚 Documentación Adicional

- **📊 [Ejemplos de Uso Detallados](ejemplos_uso.md)**: Guía completa con casos prácticos
- **📖 [Guía del Proyecto](guia.md)**: Información técnica detallada
- **🚀 [Guía de Ejecución](README_EJECUCION.md)**: Instrucciones paso a paso

## 🎓 Conceptos de Sistemas Operativos

Este proyecto implementa y demuestra:

1. **⚡ Gestión de Procesos**: Monitoreo en tiempo real, jerarquías de procesos
2. **💾 Gestión de Memoria**: RAM, SWAP, detección de fugas
3. **💿 E/S de Dispositivos**: Disco, red, performance de I/O
4. **🖥️ Planificación de CPU**: Distribución entre núcleos, context switches
5. **🔧 Herramientas del SO**: Implementación de `top`, `htop`, `netstat`

## 🤝 Contribuciones

Proyecto educativo desarrollado para:

- **Universidad**: [Tu Universidad]
- **Curso**: Sistemas Operativos
- **Semestre**: [Semestre/Año]

## 📄 Licencia

Proyecto educativo - Libre uso para fines académicos

---

### 🚀 **Comenzar Ahora**

```bash
# Clonar el proyecto
git clone [URL-del-repositorio]
cd SistemasOperativos

# Instalar dependencias
pip install -r requirements.txt

# ¡Ejecutar!
python ejecutar_monitor.py
```

**¡Listo para explorar el rendimiento del sistema!** 🎉
