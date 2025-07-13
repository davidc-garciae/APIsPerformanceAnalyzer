# 🖥️ Analizador de Rendimiento del Sistema - Interfaz Terminal

## 🚀 Cómo Ejecutar la Aplicación

### Opción 1: Monitor Simple

```bash
python ejecutar_monitor.py
```

- Interfaz simplificada con funcionalidades básicas
- Ideal para demostraciones rápidas

### Opción 2: Aplicación Completa

```bash
python ejecutar_app_completa.py
```

- Interfaz completa con todas las funcionalidades avanzadas
- Incluye herramientas de profiling, comparación de métricas, etc.

### Opción 3: Ejecución Directa

```bash
cd analizador_rendimiento
python monitor_terminal.py
```

## 📋 Funcionalidades Disponibles

### 📊 **Resumen del Sistema**

- Vista general de CPU, memoria, disco y red
- Métricas actuales del sistema
- Información de procesos activos

### ⚡ **Monitoreo en Tiempo Real**

- Actualización continua de métricas
- Visualizaciones coloridas con barras de progreso
- Panel dividido con CPU, memoria, E/O y procesos

### 🔍 **Profiling de Código**

- **cProfile**: Análisis detallado de funciones
- **Memory Profiler**: Monitoreo de uso de memoria
- **Profiling Personalizado**: Para tu propio código
- **Monitoreo Continuo**: Seguimiento en tiempo real

### 📈 **Comparación de Métricas**

- Captura múltiples mediciones
- Tabla comparativa de rendimiento
- Análisis de diferencias entre ejecuciones

### 🔧 **Herramientas Avanzadas**

- Lista detallada de procesos
- Búsqueda de procesos específicos
- Información de discos y particiones
- Estadísticas de red detalladas
- Información detallada de CPU

## 🎮 **Aplicación de Ejemplo**

También puedes ejecutar la aplicación de ejemplo para ver el profiling en acción:

```bash
cd analizador_rendimiento/app_a_monitorear
python main.py
```

Esta aplicación incluye:

- Operaciones CPU intensivas
- Consumo de memoria
- Operaciones de E/O
- Multithreading
- Algoritmos ineficientes (para demostración)

## 🎨 **Características de la Interfaz**

- ✨ **Colores vibrantes** usando Rich
- 📊 **Barras de progreso** en tiempo real
- 🎯 **Paneles organizados** para diferentes métricas
- 🔄 **Actualizaciones en vivo** sin parpadeo
- 📱 **Interfaz responsiva** en terminal
- 🎪 **Emojis y símbolos** para mejor experiencia visual

## 🛠️ **Requisitos**

Todas las dependencias ya están instaladas en `requirements.txt`:

- `rich==13.7.0` - Interfaz terminal colorida
- `click==8.1.7` - CLI avanzada
- `psutil==5.9.6` - Monitoreo del sistema
- `memory-profiler==0.61.0` - Profiling de memoria
- `py-spy==0.3.14` - Profiling avanzado

## 🎯 **Casos de Uso**

1. **Estudiantes**: Aprender monitoreo de sistemas
2. **Desarrolladores**: Profiling de aplicaciones
3. **Administradores**: Monitoreo en tiempo real
4. **Investigación**: Análisis de rendimiento

## 💡 **Consejos de Uso**

- Usa `Ctrl+C` para salir en cualquier momento
- El monitoreo en tiempo real consume recursos mínimos
- Prueba diferentes funciones de profiling para comparar
- La aplicación de ejemplo está diseñada para ser ineficiente (propósito educativo)

---

_Desarrollado para el curso de Sistemas Operativos_ 🎓
