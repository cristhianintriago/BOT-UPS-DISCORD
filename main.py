import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# CONFIGURACION DE LOGS (DEBUGGING)

# Se crea  sistema de logs que escribe en un archivo 'bot.log' y tambien muestra en consola.
# para rastrear el flujo de ejecucion y errores sin depender de la consola.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# DEFINICION DE LA CLASE PRINCIPAL
class BotUPS(commands.Bot):
    """
    Clase principal del bot que aplica herencia.
    Heredamos de commands.Bot para obtener todos los metodos de red de Discord
    y sobrescribimos metodos especificos para adaptar el comportamiento.
    """

    def __init__(self):
        # 1. Definicion de permisos (Intents)
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        
        # 2. Llamada al constructor de la superclase (commands.Bot)
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None # Desactivamos la ayuda por defecto para implementar una personalizada luego
        )

    async def setup_hook(self):
        """
        Metodo sobrescrito. Pertenece al ciclo de vida interno de discord.py.
        Se ejecuta una unica vez antes de que el bot inicie conexion web.
        Su responsabilidad exclusiva es cargar los modulos (Cogs).
        """
        logger.info("Iniciando carga de modulos (Cogs)...")
        
        # Iteracion sobre el directorio local de cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    # Se carga la extension usando la notacion de punto de Python (carpeta.archivo)
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f"Modulo cargado en memoria: {filename}")
                except Exception as e:
                    logger.error(f"Fallo al cargar el modulo {filename}. Causa: {e}")

    # EVENTOS DEL SISTEMA (Sobrescritura de eventos base)
    async def on_ready(self):
        # Confirma que el socket TCP/IP con Discord se establecio correctamente
        logger.info("-" * 50)
        logger.info("SISTEMA ONLINE Y OPERATIVO")
        logger.info(f"Instancia de usuario: {self.user.name} | ID de proceso: {self.user.id}")
        logger.info("-" * 50)

    async def on_member_join(self, member):
        # Encapsula la logica de control de acceso al servidor
        logger.info(f"Nueva conexion entrante: {member.name}")
        
        canal_bienvenida = discord.utils.get(member.guild.channels, name="bienvenida")
        if canal_bienvenida:
            await canal_bienvenida.send(f"ALERTA DE SISTEMA: Nueva conexion detectada. Acceso concedido a {member.mention}.")

        rol_basico = discord.utils.get(member.guild.roles, name="Read_Only")
        if rol_basico:
            await member.add_roles(rol_basico)

    async def on_command_error(self, ctx, error):
        # Interceptor global de excepciones para evitar que el bot colapse por errores de usuario
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Error de sintaxis: Falta el parametro obligatorio '{error.param.name}'.")
        elif isinstance(error, commands.CommandNotFound):
            # Se ignora silenciosamente para no generar redundancia en el canal
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Limite de peticiones alcanzado. Por favor, espere antes de enviar una nueva solicitud.")
        else:
            logger.error(f"Excepcion no controlada en el contexto {ctx.command}: {error}")

# PUNTO DE ENTRADA DEL PROGRAMA
if __name__ == "__main__":
    # La validacion de variables de entorno se mantiene en el bloque principal
    # garantizando que no se instancie la clase si faltan dependencias criticas.
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.critical("Error fatal: Variable de entorno DISCORD_TOKEN no encontrada. Abortando ejecucion.")
        exit(1)
    # Instanciacion del objeto principal y ejecucion del bucle de eventos
    bot_instancia = BotUPS()
    bot_instancia.run(token)