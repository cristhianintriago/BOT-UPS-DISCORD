import os
import json
import logging
import asyncio
import datetime
from datetime import datetime
import discord  
from discord.ext import commands
from google import genai

logger = logging.getLogger(__name__)

class Academia(commands.Cog):
    """
    Modulo que gestiona las funcionalidades academicas del bot.
    Aplica encapsulamiento para el manejo de credenciales y lectura de archivos.
    """

    def __init__(self, bot):
        self.bot = bot
        
        # Atributos de instancia para configuracion interna
        self.archivo_entregas = "entregas.json"
        self.modelo_ia = 'gemini-2.0-flash'
        self.max_reintentos = 3
        
        # Inicializacion segura del cliente de IA
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            self.cliente_ia = genai.Client(api_key=api_key)
        else:
            self.cliente_ia = None
            logger.warning("Fallo en inicializacion: GEMINI_API_KEY no detectada.")

    def _cargar_entregas(self):
        """
        Metodo de uso interno (privado) para procesar el archivo de tareas.
        """
        try:
            with open(self.archivo_entregas, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            entregas = {}
            for materia, fecha_str in datos.items():
                entregas[materia] = datetime.fromisoformat(fecha_str)
            return entregas
            
        except FileNotFoundError:
            logger.warning(f"Archivo de persistencia {self.archivo_entregas} no localizado. Aplicando datos mock.")
            return {
                "Sistemas Operativos (Proyecto)": datetime(2026, 4, 10, 23, 59),
                "POO (Primer Parcial)": datetime(2026, 5, 15, 8, 0),
                "Algoritmos (Tarea 1)": datetime(2026, 3, 20, 20, 0),
                "Calculo (Examen)": datetime(2026, 6, 2, 10, 0)
            }
        except Exception as error_lectura:
            logger.error(f"Error de E/S al leer entregas: {error_lectura}")
            return {}

    async def _llamar_ia_con_reintentos(self, prompt):
        """
        Metodo privado asincrono para interactuar con Gemini.
        Implementa control de flujo (Exponential Backoff) para manejar latencia y cuotas.
        """
        if not self.cliente_ia:
            return None

        for intento in range(self.max_reintentos):
            try:
                # La llamada a la API requiere procesarse adecuadamente para no frenar el event loop
                respuesta = self.cliente_ia.models.generate_content(
                    model=self.modelo_ia,
                    contents=prompt
                )
                return respuesta
                
            except Exception as e:
                error_msg = str(e)
                if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
                    tiempo_espera = 2 ** (intento + 1)
                    logger.warning(f"Saturacion de API detectada. Retraso inyectado: {tiempo_espera}s (Intento {intento + 1}/{self.max_reintentos})")
                    
                    if intento < self.max_reintentos - 1:
                        # Uso obligatorio de asyncio.sleep en lugar de time.sleep en entornos asincronos
                        await asyncio.sleep(tiempo_espera)
                        continue
                    else:
                        logger.error("Timeout de peticion: Limites de reintentos agotados.")
                        return None
                else:
                    logger.error(f"Excepcion de red no identificada: {e}")
                    raise e
        return None

    @commands.command(name='materias')
    async def materias(self, ctx):
        embed = discord.Embed(
            title="Malla Curricular - Segundo Nivel UPS",
            description="Distribucion de carga horaria",
            color=discord.Color.blue()
        )
        embed.add_field(name="Programacion Orientada a Objetos", value="192 horas", inline=False)
        embed.add_field(name="Calculo", value="160 horas", inline=False)
        embed.add_field(name="Algoritmos y Estructura de Datos", value="144 horas", inline=False)
        embed.add_field(name="Sistemas Operativos", value="144 horas", inline=False)
        embed.add_field(name="Antropologia", value="80 horas", inline=False)
        embed.set_footer(text="Total: 720 horas academicas")
        
        await ctx.send(embed=embed)

    @commands.command(name='entregas')
    async def entregas(self, ctx):
        cronograma = self._cargar_entregas()
        
        if not cronograma:
            await ctx.send("Advertencia: Base de datos de entregas vacia.")
            return

        ahora = datetime.now()
        mensaje = "**CRONOGRAMA DE ENTREGAS**\n\n"
        
        entregas_ordenadas = sorted(cronograma.items(), key=lambda x: x[1])

        for materia, fecha in entregas_ordenadas:
            diferencia = fecha - ahora
            
            if diferencia.days < 0:
                mensaje += f"~~{materia}~~ (Plazo finalizado)\n"
            elif diferencia.days == 0:
                horas = diferencia.seconds // 3600
                mensaje += f"**{materia}**: FECHA LIMITE HOY ({horas}h restantes)\n"
            else:
                dias = diferencia.days
                horas = diferencia.seconds // 3600
                mensaje += f"- **{materia}**: {dias} dias y {horas} horas\n"

        await ctx.send(mensaje)

    @commands.command(name='tutor')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def tutor(self, ctx, *, consulta: str):
        if not self.cliente_ia:
            await ctx.send("Error de configuracion: El subsistema de IA esta fuera de linea.")
            return

        async with ctx.typing():
            prompt_contextualizado = (
                "Eres un profesor de Ingenieria de Software especializado en ensenar "
                "a estudiantes de segundo semestre. Responde de forma tecnica pero clara, "
                "usando ejemplos practicos. "
                "Si la pregunta requiere codigo, utiliza sintaxis estandar de Python o Java.\n\n"
                f"Consulta tecnica: {consulta}"
            )

            try:
                respuesta = await self._llamar_ia_con_reintentos(prompt_contextualizado)

                if respuesta is None:
                    await ctx.send("Limite de procesamiento alcanzado. Imposible establecer conexion con el servidor de IA.")
                    return

                texto_respuesta = respuesta.text

                # Logica de particion de strings para mitigar la limitacion de 2000 caracteres del socket de Discord
                if len(texto_respuesta) <= 2000:
                    await ctx.send(texto_respuesta)
                else:
                    fragmentos = [texto_respuesta[i:i + 1900] for i in range(0, len(texto_respuesta), 1900)]
                    for indice, fragmento in enumerate(fragmentos, 1):
                        await ctx.send(f"**Segmento {indice}/{len(fragmentos)}**\n{fragmento}")

            except Exception as e:
                logger.error(f"Fallo de tiempo de ejecucion en modulo tutor: {e}")
                await ctx.send("Error de procesamiento. Consulte los registros del servidor.")

    @commands.command(name='cuota_ia')
    async def cuota_ia(self, ctx):
        embed = discord.Embed(
            title="Telemetria de IA",
            description="Parametros de uso de la API",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="Parametros de control",
            value=(
                f"- Tasa de refresco (Cooldown): 60 segundos por servidor\n"
                f"- Motor inferencial: {self.modelo_ia}\n"
                f"- Tolerancia a fallos (Retries): {self.max_reintentos}"
            ),
            inline=False
        )
        
        embed.set_footer(text="Sujeto a limites de capa gratuita.")
        await ctx.send(embed=embed)
    #Calculadora de proyeccion promedio academico
    @commands.command(name="proyectar")
    async def proyectar(self, ctx, *notas: float):
        # 1. Validamos que el usuario haya ingresado al menos una nota
        if len(notas) == 0:
            await ctx.send("⚠️ Por favor, ingresa al menos una nota. Ejemplo: `!proyectar 70 85 90`")
            return

        # 2. Aplicamos cálculos dinámicos
        cantidad_notas = len(notas)
        suma_notas = sum(notas)
        promedio_actual = suma_notas / cantidad_notas

        # 3. Construcción del mensaje visual
        embed = discord.Embed(
            title="📊 Análisis de Calificaciones",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Notas Evaluadas", value=f"{cantidad_notas} nota(s)", inline=True)
        embed.add_field(name="Suma Total", value=f"{suma_notas:.2f}", inline=True)
        embed.add_field(name="Promedio Actual", value=f"**{promedio_actual:.2f}**", inline=False)
        
        # 4. Lógica de estado académico
        if promedio_actual >= 70.0:
            embed.description = "🎉 ¡Vas por muy buen camino con este promedio! Sigue así."
        else:
            embed.description = "💡 Necesitas subir este promedio en tus próximas evaluaciones para asegurar la materia."
            
        embed.set_footer(text="Calculadora Dinámica de Promedios - Sistema UPS")
        await ctx.send(embed=embed)
    
    #CITADOR DE NORMAS APA
    @commands.command(name="apa")
    async def apa(self, ctx, autor: str, año: str, titulo: str, editorial: str = "N/A"):
        # Limpieza básica de datos
        autor = autor.strip()
        titulo = titulo.strip()
        
        # Formateo según norma APA (Séptima Edición)
        # Formato: Apellido, N. (Año). Título del trabajo. Editorial.
        cita = f"{autor}. ({año}). *{titulo}*. {editorial}."

        embed = discord.Embed(
            title="📚 Generador de Citas APA",
            description="Aquí tienes tu referencia lista para copiar y pegar:",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Cita Generada", value=f"```{cita}```", inline=False)
        embed.set_footer(text="Normas APA 7ma Edición - Asistente UPS")
        
        await ctx.send(embed=embed)
        if not autor or not año or not titulo:
            await ctx.send("⚠️ Error: Faltan datos. Uso: `!apa \"Autor\" \"Año\" \"Título\" \"Editorial\"`")
            return
        
async def setup(bot):
    await bot.add_cog(Academia(bot))