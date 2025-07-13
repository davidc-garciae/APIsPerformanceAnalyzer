# 📊 Analizador de Rendimiento de APIs - Sistemas Operativos

> **Sistema completo de monitoreo y análisis de rendimiento**  
> Monitoreo del sistema operativo + Análisis de APIs REST + Aplicación de ejemplo

## 🎯 Descripción

Proyecto educativo desarrollado para el curso de **Sistemas Operativos** que implementa un sistema completo de monitoreo y análisis de rendimiento con **arquitectura limpia** y dos componentes principales:

1. **🌐 Monitor de APIs**: Análisis de rendimiento, tests de carga y monitoreo continuo de APIs REST
2. **🎯 Aplicación de Ejemplo**: Interfaz de consola y web con operaciones intensivas para pruebas de rendimiento

Desarrollado con Python, utiliza interfaces de terminal coloridas e interactivas mediante Rich library y FastAPI para la interfaz web.

## ✨ Características Principales

### 🌐 Monitoreo de APIs

- 🔍 **Tests de endpoints individuales** con métricas detalladas
- 🔥 **Tests de carga** con usuarios concurrentes
- 📊 **Monitoreo continuo** de disponibilidad
- 📈 **Estadísticas avanzadas**: latencia, throughput, percentiles
- 🌐 **Análisis de conectividad** con ping, DNS y traceroute
- 🛡️ **Tests de resiliencia** bajo diferentes condiciones
- 🔥💻 **Tests de estrés** con monitoreo del sistema operativo
- 🐱 **Demo integrada** con PokéAPI para ejemplos prácticos

### 🎯 Aplicación de Ejemplo

- 💻 **Interfaz de consola** con menú interactivo (12 operaciones)
- 🌐 **Interfaz web** con FastAPI y dashboard moderno
- 🔥 **Operaciones intensivas**: CPU, memoria, E/S, multithreading
- 📊 **Métricas en tiempo real** con monitoreo integrado
- 📄 **Generación de reportes** HTML automáticos
- 🖥️ **Monitoreo del sistema**: CPU, memoria, disco, red y procesos

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
# Probar monitor de APIs
python ejecutar_api_monitor.py

# Probar aplicación de ejemplo
python ejecutar_app_ejemplo.py
```

## 🎮 Inicio Rápido

### 🌐 Monitor de APIs

```bash
python ejecutar_api_monitor.py
```

**Funcionalidades disponibles:**

- 🧪 Test de endpoint individual
- 🔥 Test de carga personalizado
- 🌐 Test de conectividad de red
- 🔥💻 Test de estrés con monitoreo del sistema
- 🛡️ Test de resiliencia de API
- 🐱💎 Análisis completo de PokéAPI
- 👀 Monitoreo continuo

### 🎯 Aplicación de Ejemplo

```bash
python ejecutar_app_ejemplo.py
```

**Opciones disponibles:**

- 💻 **Interfaz de consola**: Menú interactivo con operaciones intensivas
- 🌐 **Interfaz web**: Dashboard en http://localhost:8000
- ❓ **Ayuda**: Información detallada del sistema

**Operaciones intensivas incluidas:**

- 🔥 CPU Intensiva: Cálculos matemáticos complejos
- 🧠 Memoria Intensiva: Grandes estructuras de datos
- 💿 E/S Intensiva: Operaciones de archivo
- 🔢 Fibonacci Recursivo: Algoritmo ineficiente
- 🧵 Multithreading: Operaciones con múltiples hilos
- 💧 Memory Leak: Simulación de fuga de memoria
- ⏱️ Operación Lenta: Esperas deliberadas
- 📊 Benchmark Completo: Todas las operaciones

## 📁 Estructura del Proyecto

```
SistemasOperativos/
├── 🌐 ejecutar_api_monitor.py          # [PRINCIPAL] Monitor de APIs
├── 🎯 ejecutar_app_ejemplo.py          # [PRINCIPAL] Aplicación de ejemplo
├── 📊 analizador_rendimiento/          # Sistema de monitoreo
│   └── core/
│       ├── api_monitor.py             # Monitoreo de APIs
│       ├── api_visualizer.py          # Visualización de APIs
│       ├── monitoring.py              # Monitoreo del sistema
│       ├── visualizacion.py           # Visualización del sistema
│       └── profiling.py               # Herramientas de profiling
├── 🎮 app_ejemplo/                     # Aplicación de ejemplo
│   ├── core/
│   │   ├── operaciones.py             # Operaciones intensivas
│   │   └── utils.py                   # Utilidades
│   ├── interfaces/
│   │   ├── consola.py                 # Interfaz de consola
│   │   └── web.py                     # Interfaz web FastAPI
│   ├── tests/                         # Tests unitarios
│   └── main.py                        # Punto de entrada
├── 📖 guia.md                          # Documentación técnica
├── 📦 requirements.txt                 # Dependencias
└── 📄 README.md                        # Este archivo
```

## 🎯 Casos de Uso

### 📚 Educativo - Sistemas Operativos

**Conceptos demostrados:**

- Gestión de procesos y memoria
- E/S de dispositivos (disco, red)
- Planificación de CPU
- Herramientas de monitoreo del SO
- Profiling y optimización
- Análisis de rendimiento de red
- Tests de carga y estrés

### 🔧 Profesional - DevOps

**Aplicaciones prácticas:**

- Monitoreo de APIs REST
- Tests de carga automatizados
- Detección de cuellos de botella
- Análisis de conectividad de red
- Tests de resiliencia
- Alertas de rendimiento

## 📊 Ejemplos de Salida

### Monitor de APIs

```
╔═══════════════════════ 🔍 PRUEBA DE ENDPOINT ═══════════════════════╗
║ https://pokeapi.co/api/v2/pokemon/pikachu                           ║
╚═════════════════════════════════════════════════════════════════════╝

✅ Resultado:
├─ ⏱️  Tiempo de respuesta: 0.124s
├─ 📊 Código de estado: 200
├─ 📦 Tamaño de respuesta: 245.2 KB
├─ 💻 Uso de CPU: 2.3%
├─ 🧠 Memoria utilizada: 45.2 MB
├─ 🔗 Conexiones activas: 8
└─ 🌐 Estado: Exitoso

🔥 Test de Estrés con Monitoreo del Sistema:
├─ 📈 Tasa de éxito: 98.5%
├─ ⚡ Req/seg: 21.4
├─ 🔥 CPU pico: 45.2%
├─ 🧠 Memoria pico: 78.1%
└─ 🌐 Red: 15.8 MB transferidos
```

### Aplicación de Ejemplo - Consola

```
🔧 APLICACIÓN DE EJEMPLO PARA MONITOREO DE RENDIMIENTO
======================================================================
Seleccione la interfaz que desea usar:

1. 💻 Interfaz de Consola (Menú interactivo)
2. 🌐 Interfaz Web (Servidor FastAPI)
3. ❓ Ayuda
0. ❌ Salir

🔥 OPERACIONES DISPONIBLES:
├─ CPU Intensiva: Cálculos matemáticos complejos
├─ Memoria Intensiva: Grandes estructuras de datos
├─ E/S Intensiva: Operaciones de archivo
├─ Fibonacci Recursivo: Algoritmo ineficiente
├─ Multithreading: Múltiples hilos
└─ Benchmark Completo: Todas las operaciones
```

## 🛠️ Comandos Principales

| Comando                          | Descripción                 | Uso                     |
| -------------------------------- | --------------------------- | ----------------------- |
| `python ejecutar_api_monitor.py` | 🌐 Monitor completo de APIs | Desarrolladores, DevOps |
| `python ejecutar_app_ejemplo.py` | 🎯 Aplicación de ejemplo    | Testing, aprendizaje    |

## 🔧 Solución de Problemas

### Error: "Module not found"

```bash
pip install -r requirements.txt
```

### Error: "cannot import name"

```bash
# Verificar que estás en el directorio correcto
cd SistemasOperativos

# Verificar la estructura de archivos
ls -la
```

### Puerto ocupado (interfaz web)

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
sudo lsof -i :8000
sudo kill -9 <PID>
```

## 🧪 Tests y Demos Incluidos

### 🐱 Demo de PokéAPI

La aplicación incluye tests específicos para PokéAPI que demuestran:

- Análisis de conectividad completo
- Tests de múltiples endpoints
- Tests de carga bajo diferentes condiciones
- Análisis de resiliencia
- Monitoreo del impacto en el sistema

### 🔥 Tests de Estrés

Incluye tests que combinan:

- Carga de trabajo intensa en APIs
- Monitoreo del sistema operativo en tiempo real
- Análisis del impacto en CPU, memoria y red
- Medición de overhead de conexiones

## 🎓 Conceptos de Sistemas Operativos

Este proyecto implementa y demuestra:

1. **⚡ Gestión de Procesos**: Monitoreo en tiempo real, jerarquías de procesos
2. **💾 Gestión de Memoria**: RAM, detección de fugas, profiling
3. **💿 E/S de Dispositivos**: Disco, red, performance de I/O
4. **🖥️ Planificación de CPU**: Distribución entre núcleos, multithreading
5. **🌐 Redes**: Conectividad, latencia, throughput, análisis de tráfico
6. **🔧 Herramientas del SO**: Implementación de utilidades de monitoreo

## 📦 Dependencias Principales

- **fastapi**: Framework web moderno y rápido
- **psutil**: Información del sistema y procesos
- **rich**: Interfaces de terminal coloridas
- **aiohttp**: Cliente HTTP asíncrono
- **memory-profiler**: Análisis de uso de memoria
- **py-spy**: Profiling de aplicaciones Python

## 🤝 Contribuciones

Proyecto educativo desarrollado para:

- **Universidad**: Universidad de Antioquia
- **Curso**: Sistemas Operativos
- **Semestre**: 2025-1

## 📄 Licencia

Proyecto educativo - Libre uso para fines académicos

---

### 🚀 **Comenzar Ahora**

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Probar monitor de APIs
python ejecutar_api_monitor.py

# 3. Probar aplicación de ejemplo
python ejecutar_app_ejemplo.py
```

**¡Listo para explorar el rendimiento del sistema!** 🎉

### 💡 **Flujo de Trabajo Recomendado**

1. **Inicia el monitor de APIs** para entender el análisis de rendimiento de red
2. **Ejecuta la aplicación de ejemplo** para generar carga de trabajo
3. **Combina ambos** para análisis completo del sistema
4. **Revisa los reportes** generados automáticamente

---

**🔥 Características destacadas:**

- ✅ Solo 2 archivos de ejecución principales
- ✅ Interfaces tanto de consola como web
- ✅ Monitoreo completo del sistema operativo
- ✅ Tests de APIs con métricas avanzadas
- ✅ Documentación completa y ejemplos prácticos
