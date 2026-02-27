# Guía de Contribución - Bot Asistente Académico

¡Gracias por tu interés en mejorar este proyecto! Este bot está diseñado para ser una herramienta colaborativa para los estudiantes. Si tienes ideas para nuevos comandos o mejoras en el código, tu ayuda es bienvenida.

## Cómo configurar el proyecto localmente

Para probar o modificar el código en tu propia máquina sin afectar el bot principal, sigue estos pasos:

1. **Haz un Fork del repositorio** haciendo clic en el botón "Fork" en la esquina superior derecha de esta página.

2. **Clona tu Fork** a tu computadora:
   ```bash
   git clone [https://github.com/cristhianintriago/BOT-UPS-DISCORD.git](https://github.com/cristhianintriago/BOT-UPS-DISCORD.git)
   
3. **Crea un entorno virtual** e instala las dependencias:

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   
4. **Configura tus credenciales:**
   - Duplica el archivo `.env.example`.
   - Renombra la copia a `.env`.
   - Coloca tu propio token de prueba de Discord.

## Estructura Modular (Cogs)

Este proyecto utiliza la arquitectura de Cogs de discord.py. Si vas a crear un comando nuevo, por favor añádelo en el archivo correspondiente dentro de la carpeta /cogs:
- `academia.py`: Para funciones relacionadas con la universidad, materias y la IA.
- `utilidades.py`: Para conversores o calculadoras.
- `sistema.py`: Para métricas del bot.

## Cómo enviar tus cambios (Pull Requests)

1. Crea una rama para tu nueva función: `git checkout -b nueva-funcion`
2. Escribe tu código y pruébalo localmente.
3. Haz un commit con un mensaje claro: `git commit -m "Añadido comando de recordatorio de clases"`
4. Sube tu rama: `git push origin nueva-funcion`
5. Abre un **Pull Request** en este repositorio original para que el código sea revisado e integrado.

## Regla de Oro de Seguridad
Bajo ninguna circunstancia modifiques el archivo `.gitignore` ni subas tu archivo `.env` personal. Cualquier Pull Request que contenga credenciales expuestas será rechazado inmediatamente.   