import os
import time
import platform
import psutil
import discord
from discord.ext import commands
from datetime import datetime

class Sistema(commands.Cog):
    """
    Modulo encargado de la telemetria y diagnostico del hardware del servidor.
    Interactua con el nucleo del sistema operativo para extraer metricas de rendimiento.
    """

    def __init__(self, bot):
        # Inyeccion de dependencias: se recibe la instancia principal del bot
        self.bot = bot
        # Almacenamiento del timestamp (tiempo Unix) en el momento de instanciacion
        self.inicio_tiempo = time.time()

    @commands.command(name='sys_info')
    async def sys_info(self, ctx):
        """
        Extrae y formatea informacion a nivel de hardware y sistema operativo.
        Utiliza la libreria psutil para acceder a los descriptores de rendimiento.
        """
        # Interfaz con el sistema operativo
        so_nombre = platform.system()
        so_version = platform.release()
        arquitectura = platform.machine()

        # Muestreo de la unidad central de procesamiento (CPU)
        # El parametro interval=1 bloquea la subrutina por 1 segundo para promediar el uso real
        uso_cpu = psutil.cpu_percent(interval=1)
        hilos_procesamiento = psutil.cpu_count()

        # Muestreo de memoria de acceso aleatorio (RAM)
        memoria = psutil.virtual_memory()
        
        # Conversion de bytes a Megabytes (MB) usando division entera para evitar flotantes
        ram_usada_mb = memoria.used // (1024 ** 2)
        ram_total_mb = memoria.total // (1024 ** 2)

        embed = discord.Embed(
            title="Informacion del Sistema",
            description="Metricas de rendimiento y configuracion del hardware"
        )
        # ... (final del comando health, dentro de la clase) ...
        embed.set_footer(text=f"Identificador del proceso: {self.bot.user.id}")
        await ctx.send(embed=embed)

# ==========================================
# FUNCION DE ENLACE GLOBAL (Fuera de la clase)
# ==========================================
async def setup(bot):
    await bot.add_cog(Sistema(bot))