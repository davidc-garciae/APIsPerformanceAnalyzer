# Proyecto Final

**Curso:** Sistemas Operativos y Laboratorio

---

## Título del proyecto

Análisis de Rendimiento de Aplicaciones Web través de una API en Python

## Miembros del equipo

- David García (Líder de proyecto)
- \[Nombre Integrante 2]
- \[Nombre Integrante 3]

---

## Resumen

Este proyecto propone el desarrollo de una API en Python para monitorizar y analizar el rendimiento de aplicaciones web. La solución medirá métricas de CPU, memoria y dispositivos de E/S, y permitirá la creación de perfiles detallados de funciones específicas. Los datos se expondrán mediante endpoints REST y se garantizará compatibilidad multiplataforma.

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

### Relación con el curso de Sistemas Operativos

- En la parte teórica, se aplican conceptos de scheduling y administración de memoria vistos en clase.
- En laboratorio, se experimenta con herramientas de monitoreo y se profundiza en psutil, cProfile y otras utilidades de Python.

---

## Objetivos

### Objetivo principal

Desarrollar una API en Python que recolecte, exponga y permita analizar métricas de rendimiento de aplicaciones web en tiempo real.

### Objetivos específicos

1. Implementar módulos de monitoreo de CPU, memoria y E/S usando bibliotecas multiplataforma.
2. Diseñar endpoints REST para exponer métricas sistematizadas.
3. Integrar perfiladores de funciones (cProfile, memory_profiler, py-spy) con mecanismos de activación remota.
4. Documentar y validar el funcionamiento en entornos Windows, Linux y macOS.

---

## Metodología

### Herramientas propuestas

- **Python 3.8+** como lenguaje principal.
- **FastAPI** o **Flask** para la capa REST.
- **psutil** para métricas de sistema.
- **cProfile**, **memory_profiler** y **py-spy** para perfilado.
- **Prometheus Client** (opcional) para integración con herramientas de visualización.

### Actividades principales

1. Revisión bibliográfica y selección de librerías.
2. Diseño de arquitectura modular (monitoreo, perfilado, API).
3. Implementación de módulos de monitoreo.
4. Desarrollo de endpoints REST.
5. Integración de perfiladores y pruebas unitarias.
6. Pruebas multiplataforma y ajustes.
7. Documentación y presentación final.

---

## Cronograma

| Actividad                                    | Fecha de inicio | Fecha de fin |
| -------------------------------------------- | --------------- | ------------ |
| 1. Selección de bibliotecas y diseño inicial | 20/05/2025      | 26/05/2025   |
| 2. Implementación de monitoreo de recursos   | 27/05/2025      | 09/06/2025   |
| 3. Desarrollo de API y endpoints REST        | 10/06/2025      | 23/06/2025   |
| 4. Integración de perfiladores               | 24/06/2025      | 01/07/2025   |
| 5. Pruebas multiplataforma                   | 02/07/2025      | 07/07/2025   |
| 6. Documentación y entrega final             | 08/07/2025      | 10/07/2025   |

> **Diagrama de Gantt:**
> (Se incluirá el diagrama de Gantt detallado en la versión final del documento.)

---

## Referencias

1. Repositorio oficial de `psutil`: [https://github.com/giampaolo/psutil](https://github.com/giampaolo/psutil)
2. Documentación de FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
3. Guía de perfiladores en Python: cProfile, memory_profiler, py-spy
4. Artículos académicos y manuales de Sistemas Operativos relacionados con scheduling, gestión de memoria e I/O.

### 📌 Ejemplos prácticos para la sección: **¿Cuál es la necesidad y/o problema que aborda el desafío?**

1.  **Sobreuso de CPU por parte de una función mal optimizada**

    > Un servicio web que ejecuta una función recursiva intensiva sin límite de profundidad puede saturar el CPU, afectando la capacidad de respuesta de toda la aplicación. Sin herramientas de monitoreo o perfilado, identificar esta función problemática puede tomar horas o días.

2.  **Fugas de memoria en aplicaciones persistentes**

    > En servidores que manejan múltiples peticiones web, una mala gestión de objetos en memoria puede acumular referencias sin liberar recursos, causando degradación progresiva. Esto afecta directamente el uso de RAM del sistema operativo y puede llevar al swapping.

3.  **Bloqueo de recursos por acceso de E/S concurrente**

    > Una API que accede simultáneamente a archivos de log en disco sin sincronización adecuada puede generar cuellos de botella en el subsistema de disco o errores de concurrencia. El análisis del uso de disco o de sockets permitiría detectar esta sobrecarga.

4.  **Dificultad para determinar qué parte del código ralentiza una API**

    > En una API que responde lentamente, puede no estar claro si la causa es el framework, la base de datos, o alguna función específica. Usar un perfilador remoto permitiría aislar y medir el tiempo exacto que consume cada bloque del código.

---

### 🔧 Ejemplos prácticos para: **¿Qué relación tiene esta teoría con los temas del curso de Sistemas Operativos?**

1.  **Planificación de procesos y hilos (Scheduling)**

    > Cuando se mide el uso de CPU por procesos, se puede observar cómo el sistema operativo asigna tiempo de CPU. Esto se relaciona directamente con los algoritmos de planificación como Round Robin o Multilevel Feedback Queue, vistos en clase.

2.  **Administración de memoria**

    > Al detectar picos en el uso de memoria de un proceso, se puede inferir cómo el sistema operativo maneja la segmentación o paginación. Se aplican conceptos como espacio de direcciones virtuales o swapping.

3.  **Sistemas de archivos e I/O buffering**

    > Analizar la latencia de E/S permite observar cómo el sistema operativo gestiona los buffers, colas de espera, y prioridades de acceso a disco o red. Esto conecta con temas de administración de dispositivos y uso de controladores.

4.  **Herramientas del laboratorio**

    > En el laboratorio se utilizan herramientas como `top`, `htop`, `iotop` o `ps`, que permiten observar estas métricas desde el sistema operativo. La API que se desarrollará funcionará como una versión programática de estas herramientas, aplicando los mismos principios.
