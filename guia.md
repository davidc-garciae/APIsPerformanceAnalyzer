# Proyecto Final

**Curso:** Sistemas Operativos y Laboratorio  
**Estado:** ✅ **COMPLETADO**

---

## Título del proyecto

Analizador de Rendimiento de Aplicaciones Web y APIs mediante Python

## Miembros del equipo

- David García (Líder de proyecto)
- \[Nombre Integrante 2]
- \[Nombre Integrante 3]

---

## Resumen

Este proyecto **desarrolló exitosamente** un sistema completo en Python para monitorizar y analizar el rendimiento tanto de aplicaciones web como de APIs REST. La solución **implementa** medición de métricas de CPU, memoria y dispositivos de E/S, **incluye** perfiles detallados de funciones específicas, y **proporciona** dos interfaces principales: monitoreo del sistema operativo y análisis de rendimiento de APIs. Los datos se **exponen** mediante visualizaciones coloridas en terminal y se **garantiza** compatibilidad multiplataforma.

---

## Introducción

### Necesidad o problema

Las aplicaciones web modernas requieren un monitoreo continuo de recursos para garantizar su estabilidad y escalabilidad. Sin herramientas adecuadas, los desarrolladores tienen dificultad para identificar cuellos de botella y optimizar funciones críticas.

### Importancia tecnológica

En un entorno donde la eficiencia y la experiencia de usuario son primordiales, disponer de métricas precisas en tiempo real y perfiles de funciones facilita la toma de decisiones y mejora la calidad del software.

---

## Antecedentes o marco teórico

### Aspectos teóricos clave

- Conceptos de planificación y asignación de CPU en sistemas operativos.
- Gestión de memoria y detección de fugas.
- I/O subsystems: controladores, buffers y colas en discos y redes.
- Principios de perfilado de código: muestreo vs determinístico.
- Análisis de rendimiento de APIs REST y métricas de red.

### Relación con el curso de Sistemas Operativos

- En la parte teórica, se aplicaron conceptos de scheduling y administración de memoria vistos en clase.
- En laboratorio, se experimentó con herramientas de monitoreo y se profundizó en psutil, cProfile y otras utilidades de Python.
- Se implementaron versiones programáticas de herramientas como `top`, `htop`, `iotop` y `netstat`.

---

## Objetivos

### Objetivo principal

✅ **COMPLETADO:** Desarrollar un sistema completo en Python que recolecte, exponga y permita analizar métricas de rendimiento de aplicaciones web y APIs en tiempo real.

### Objetivos específicos

1. ✅ **COMPLETADO:** Implementar módulos de monitoreo de CPU, memoria y E/S usando bibliotecas multiplataforma.
2. ✅ **COMPLETADO:** Diseñar interfaces de terminal coloridas para exponer métricas sistematizadas.
3. ✅ **COMPLETADO:** Integrar perfiladores de funciones (cProfile, memory_profiler, py-spy) con mecanismos de activación.
4. ✅ **COMPLETADO:** Desarrollar sistema de monitoreo de APIs con tests de carga y análisis de rendimiento.
5. ✅ **COMPLETADO:** Documentar y validar el funcionamiento en entornos multiplataforma.

---

## Metodología

### Herramientas utilizadas

- **Python 3.8+** como lenguaje principal.
- **Rich** para interfaces de terminal coloridas y visualizaciones.
- **psutil** para métricas de sistema operativo.
- **aiohttp** para peticiones HTTP asíncronas.
- **cProfile**, **memory_profiler** y **py-spy** para perfilado.
- **click** para interfaces de línea de comandos.
- **FastAPI** para aplicaciones de ejemplo.

### Actividades realizadas

1. ✅ Revisión bibliográfica y selección de librerías.
2. ✅ Diseño de arquitectura modular (monitoreo, perfilado, visualización).
3. ✅ Implementación de módulos de monitoreo del sistema.
4. ✅ Desarrollo de sistema de monitoreo de APIs.
5. ✅ Integración de perfiladores y visualizaciones.
6. ✅ Implementación de demos y casos de uso.
7. ✅ Documentación completa y limpieza del proyecto.

---

## Funcionalidades Implementadas

### 🖥️ Sistema de Monitoreo del Sistema

- **Monitoreo en tiempo real** con actualización automática
- **Métricas completas**: CPU, memoria, disco, red, procesos
- **Visualización colorida** con paneles y barras de progreso
- **Profiling integrado** con cProfile y memory_profiler
- **Interfaz interactiva** con Rich library

### 🌐 Sistema de Monitoreo de APIs

- **Tests de endpoints individuales** con métricas detalladas
- **Tests de carga personalizados** con concurrencia configurable
- **Demo específica de PokéAPI** con 6 endpoints diferentes
- **Análisis de rendimiento** con estadísticas completas
- **Reportes visuales** con tablas y gráficos coloridos

### 📊 Características Técnicas

- **Arquitectura modular** con separación clara de responsabilidades
- **Compatibilidad multiplataforma** (Windows, Linux, macOS)
- **Interfaces asíncronas** para mejor rendimiento
- **Manejo de errores robusto** con reintentos automáticos
- **Documentación completa** con ejemplos de uso

---

## Cronograma (Completado)

| Actividad                                    | Fecha de inicio | Fecha de fin | Estado |
| -------------------------------------------- | --------------- | ------------ | ------ |
| 1. Selección de bibliotecas y diseño inicial | 20/05/2025      | 26/05/2025   | ✅     |
| 2. Implementación de monitoreo de recursos   | 27/05/2025      | 09/06/2025   | ✅     |
| 3. Desarrollo de visualizaciones y UI        | 10/06/2025      | 23/06/2025   | ✅     |
| 4. Integración de perfiladores               | 24/06/2025      | 01/07/2025   | ✅     |
| 5. Sistema de monitoreo de APIs              | 02/07/2025      | 07/07/2025   | ✅     |
| 6. Documentación y limpieza final            | 08/07/2025      | 13/07/2025   | ✅     |

---

## Resultados y Logros

### 🎯 Métricas de Éxito

- **100% de objetivos completados**
- **Sistema completamente funcional** en ambos componentes
- **Interfaz rica y profesional** con Rich library
- **Documentación completa** con ejemplos prácticos
- **Código limpio y modular** después de refactorización

### 🚀 Comandos Principales

```bash
# Sistema de monitoreo del sistema
python ejecutar_monitor.py

# Sistema de monitoreo de APIs
python ejecutar_api_monitor.py

# Aplicación unificada de ejemplo (NUEVA ARQUITECTURA)
python ejecutar_app_ejemplo.py

# Demo específica de PokéAPI
python ejecutar_api_monitor.py  # Opción 6: Análisis completo de PokéAPI
```

### 📈 Casos de Uso Demostrados

1. **Monitoreo de sistema** con visualización en tiempo real
2. **Análisis de APIs** con PokéAPI (56 peticiones, 100% éxito)
3. **Tests de carga** con concurrencia (50 peticiones, 10 usuarios)
4. **Profiling de aplicaciones** con herramientas integradas
5. **Aplicación unificada** con interfaz de consola y web (arquitectura limpia)

---

## Referencias

1. Repositorio oficial de `psutil`: [https://github.com/giampaolo/psutil](https://github.com/giampaolo/psutil)
2. Documentación de Rich: [https://rich.readthedocs.io/](https://rich.readthedocs.io/)
3. Documentación de aiohttp: [https://docs.aiohttp.org/](https://docs.aiohttp.org/)
4. PokéAPI Documentation: [https://pokeapi.co/docs/v2](https://pokeapi.co/docs/v2)
5. Guía de perfiladores en Python: cProfile, memory_profiler, py-spy
6. Artículos académicos y manuales de Sistemas Operativos relacionados con scheduling, gestión de memoria e I/O.

### 📌 Ejemplos prácticos implementados: **¿Cuál es la necesidad y/o problema que aborda el desafío?**

1.  **Sobreuso de CPU por parte de una función mal optimizada** ✅

    > **Implementado:** El sistema detecta automáticamente procesos con alto uso de CPU y los muestra en el panel de "Top 5 Procesos". Durante las pruebas, se observó que Cursor.exe consumía 37.9% de CPU.

2.  **Fugas de memoria en aplicaciones persistentes** ✅

    > **Implementado:** El monitor muestra en tiempo real el uso de memoria RAM y SWAP, permitiendo detectar incrementos progresivos. Se incluye profiling de memoria con memory_profiler.

3.  **Bloqueo de recursos por acceso de E/S concurrente** ✅

    > **Implementado:** El panel de disco muestra tasas de lectura/escritura en tiempo real, y el de red muestra tráfico de envío/recepción. Permite identificar cuellos de botella de I/O.

4.  **Dificultad para determinar qué parte del código ralentiza una API** ✅

    > **Implementado:** El sistema de monitoreo de APIs mide tiempos de respuesta específicos por endpoint, identifica los más lentos, y proporciona estadísticas detalladas. En PokéAPI, se detectó que pokemon/1 tardaba 0.327s vs 0.063s de generation/1.

---

### 🔧 Ejemplos prácticos implementados: **¿Qué relación tiene esta teoría con los temas del curso de Sistemas Operativos?**

1.  **Planificación de procesos y hilos (Scheduling)** ✅

    > **Implementado:** El sistema muestra en tiempo real cómo se distribuye el uso de CPU entre procesos, permitiendo observar la efectividad de algoritmos de planificación como Round Robin.

2.  **Administración de memoria** ✅

    > **Implementado:** Se monitorea memoria virtual vs física, uso de SWAP, y se pueden detectar patrones de paginación. El sistema mostró 51.2% de uso de RAM durante las pruebas.

3.  **Sistemas de archivos e I/O buffering** ✅

    > **Implementado:** Se mide latencia de E/S de disco y red, mostrando cómo el sistema operativo gestiona buffers y colas. Se observaron velocidades de 1.2 MB/s en lecturas y 850 KB/s en escrituras.

4.  **Herramientas del laboratorio** ✅

    > **Implementado:** Se creó una versión programática de herramientas como `top`, `htop`, `iotop` y `netstat`, aplicando los mismos principios pero con visualización moderna y rica.
