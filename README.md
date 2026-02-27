# Bot Discord UPS - Asistente Academico

Proyecto académico orientado al apoyo estudiantil. Implementa una arquitectura modular basada en Componentes (Cogs), sistema de logging, manejo global de excepciones y conexión asíncrona con la API de Google Gemini.

Python 3.8+ | Discord.py | Google Gemini

## Características Principales

- Modulo Académico: Consulta de malla curricular y cronograma automatizado de entregas.
- Modulo de IA: Tutor virtual para resolución de problemas de programación (Google Gemini).
- Modulo de Utilidades: Conversiones de bases numéricas y unidades de almacenamiento en memoria.
- Modulo de Sistema: Telemetría de hardware (uso de CPU, RAM, latencia de red y tiempo de actividad).
- Infraestructura: Sistema de registros (logs), manejo de errores, reintentos exponenciales y limites de peticiones (cooldowns).
- Configuración Dinámica: Lectura de archivos JSON para persistencia de datos y variables de entorno para seguridad de credenciales.

# Comandos Disponibles

### [ACADEMIA]

!materias          - Retorna malla curricular del semestre.

!entregas          - Consulta de tareas y exámenes pendientes.

!tutor <consulta>  - Interfaz asíncrona con Inteligencia Artificial.

!cuota_ia          - Métricas de uso y limites de la API.

### [UTILIDADES]

!binario <numero>    - Conversión de base 10 a base 2.

!unidades <cant> <U> - Conversión de almacenamiento (Ej: !unidades 2048 KB).

### [SISTEMA E INFORMACION]

!sys_info     - Diagnostico de hardware del nodo de ejecucion.

!health       - Estado de salud de los servicios lógicos.

!comandos     - Directorio general de subrutinas.

## Instrucciones de Despliegue

### Requisitos Previos
- Entorno de ejecución: Python 3.8 o superior.
- Credenciales: Token de Discord Developer y API Key de Google Gemini.

### 1. Clonación del repositorio
```bash
git clone [https://github.com/cristianintriago/bot-discord-ups.git](https://github.com/cristianintriago/bot-discord-ups.git)
cd bot-discord-ups
```
### 2. Preparación del entorno
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Configuración de credenciales
```bash
python main.py
```
# Estructura del Proyecto bot-discord-ups 🤖

## 📁 Árbol de Directorios


bot-discord-ups/

├── cogs/                 `#Módulos independientes (Arquitectura Cogs) 📁`

│   ├── academia.py       `#Lógica universitaria e integración de IA 🤖`

│   ├── sistema.py        `#Diagnostico de hardware (psutil) 💻`

│   └── utilidades.py     `#Herramientas de conversión matemática 🔢`

├── main.py               `#Archivo principal y arranque del bot 🚀`

├── entregas.json         `#Base de datos local en formato JSON 💾`

├── .env                  `#Variables de entorno (Excluido del repositorio) 🔒`

├── bot.log               `#Registros del sistema 📋`

├── requirements.txt      `#Archivo de dependencias 📦`

└── README.md             `#Documentación técnica 📖`

### Conceptos de Ingeniería Aplicados
Programación Orientada a Objetos: Implementación de clases, herencia (commands.Cog) y encapsulamiento de métodos.

Arquitectura Modular: Separación de responsabilidades (Separation of Concerns) dividiendo la lógica en módulos independientes.

Programación Asíncrona: Manejo de concurrencia mediante async/await.

Tolerancia a Fallos: Implementación de bloqueos try/except globales y algoritmo de "Exponential Backoff" para control de cuotas de red.

Telemetría de Sistema: Monitoreo de recursos a nivel de sistema operativo utilizando la librería psutil.

### Solución de Problemas


`ModuleNotFoundError: No module named 'discord':` Verificar activacion del entorno virtual e instalar dependencias.

`Error 429 / RESOURCE_EXHAUSTED,Saturacion de API.:` El sistema reintentara automaticamente o aplicara cooldown.

`Falla de arranque (LoginFailure):`Verificar integridad de DISCORD_TOKEN en el archivo .env.

`Comandos no responden:`Habilitar ""Message Content Intent"" en Discord Developer Portal."

### Licencia
Proyecto desarrollado con fines de investigación académica.

© 2026 Cristhian Intriago
