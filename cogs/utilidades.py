import discord
from discord.ext import commands
from datetime import datetime

class Utilidades(commands.Cog):
    """
    Modulo de herramientas y utilidades matematicas.
    Agrupa funciones auxiliares de conversion de datos y el directorio de comandos.
    """

    def __init__(self, bot):
        self.bot = bot
        # Encapsulamiento de limites constantes como atributos de la clase
        # Esto previene modificaciones accidentales desde el exterior y desbordamientos
        self.min_numero_binario = 0
        self.max_numero_binario = 1000000

    @commands.command(name='binario')
    async def binario(self, ctx, numero: int):
        """
        Transforma un numero de base 10 (decimal) a base 2 (binario).
        Implementa validacion de rango para asegurar la estabilidad de la conversion.
        """
        # Validacion de entrada de datos (Input validation)
        if numero < self.min_numero_binario or numero > self.max_numero_binario:
            await ctx.send(f"Error de validacion: El valor debe estar comprendido entre {self.min_numero_binario} y {self.max_numero_binario}.")
            return

        # Se utiliza la funcion built-in de Python y se formatea la cadena resultante
        resultado = bin(numero).replace("0b", "")
        longitud_bits = len(resultado)

        embed = discord.Embed(
            title="Conversion de Base Numerica",
            color=discord.Color.purple()
        )
        embed.add_field(name="Decimal (Base 10)", value=f"`{numero}`", inline=True)
        embed.add_field(name="Binario (Base 2)", value=f"`{resultado}`", inline=True)
        embed.add_field(name="Longitud de palabra", value=f"{longitud_bits} bits requeridos", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='unidades')
    async def unidades(self, ctx, cantidad: float, unidad_origen: str):
        """
        Realiza la conversion de unidades de almacenamiento digital.
        Emplea un diccionario como estructura de datos para mapear los factores de conversion.
        """
        unidad = unidad_origen.upper()

        if cantidad < 0:
            await ctx.send("Error de logica: La magnitud no puede ser un valor negativo.")
            return

        # Diccionario para busqueda en tiempo constante O(1) de los multiplicadores base
        conversiones = {
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4
        }

        if unidad not in conversiones:
            await ctx.send(f"Error de sintaxis: Unidad '{unidad_origen}' no reconocida. Unidades validas: KB, MB, GB, TB.")
            return

        # Se normaliza la entrada convirtiendo primero todo a la unidad fundamental (bytes)
        bytes_totales = cantidad * conversiones[unidad]

        mensaje = "**CONVERSION DE ALMACENAMIENTO**\n\n"
        mensaje += f"Entrada procesada: {cantidad} {unidad}\n\n"

        for nombre_unidad, factor in conversiones.items():
            if nombre_unidad != unidad:
                valor = bytes_totales / factor
                mensaje += f"- **{nombre_unidad}**: {valor:.4f}\n"

        await ctx.send(mensaje)

    @commands.command(name='comandos')
    async def comandos_personalizados(self, ctx):
        """
        Genera e imprime el directorio de comandos del sistema.
        Sustituye a la funcion help por defecto de discord.py para mayor control de formato.
        """
        embed = discord.Embed(
            title="Directorio de Comandos",
            description="Listado de modulos y subrutinas disponibles en el sistema",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Modulo Academico",
            value=(
                "`!materias` - Retorna malla curricular\n"
                "`!entregas` - Consulta de tareas pendientes\n"
                "`!tutor <consulta>` - Interfaz con IA\n"
                "`!cuota_ia` - Metricas del uso de API\n"
                "`!proyectar <notas>` - Proyeccion de promedio academico\n"
            ),
            inline=False
        )

        embed.add_field(
            name="Modulo de Utilidades",
            value=(
                "`!binario <numero>` - Conversion base 10 a base 2\n"
                "`!unidades <cantidad> <unidad>` - Conversion de memoria\n"
                #"`!sys_info` - Diagnostico de hardware\n"
                "`!health` - Estado de salud del nodo"
            ),
            inline=False
        )

        embed.set_footer(text=f"Prefijo configurado: {self.bot.command_prefix} | Sistema UPS")
        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)

# Funcion de enlace estandar para la carga de extensiones
async def setup(bot):
    await bot.add_cog(Utilidades(bot))