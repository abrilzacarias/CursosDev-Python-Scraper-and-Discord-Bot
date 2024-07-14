import discord
from discord.ext import commands
import os
from functions import *
import asyncio
from scraper import run

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, description='This bot returns courses')
    
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def search(ctx, searchTerm: str):
    results = searchCourses(searchTerm)
    #print(results)
    if results:
        for course in results:
            name, creator, url = course
            await ctx.send(f"**{name}**\nCreator: {creator}\nLink: {url}")
    else:
        await ctx.send("No courses matching the keyword and today's date were found.")

@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide a search term. Usage: `!search <term>`')

@bot.command()
async def today(ctx):
    results = getTodayCourses()
    
    if results:
        for course in results:
            name, creator, url = course
            await ctx.send(f"**{name}**\nCreator: {creator}\nLink: {url}")
    else:
        await ctx.send("No courses found for today's date.")


async def scheduleDeleteOldCourses():
    while True:
        deleteOldCourses()
        await asyncio.sleep(86400)  # Revisa cada 24 horas (86400 segundos)

# Función para ejecutar el scraper automáticamente a una hora predeterminada todos los días
async def runDaily():
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), datetime.strptime("03:00:00", "%H:%M:%S").time())
        
        # Si la hora objetivo ya ha pasado hoy, configúrala para mañana
        if now > target_time:
            target_time += timedelta(days=1)
        
        # Calcular el tiempo restante hasta la hora objetivo
        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)  # Esperar hasta la hora objetivo
        
        run()  # Ejecutar el scraper
        
        # Esperar 24 horas antes de volver a ejecutar
        await asyncio.sleep(86400)

#events
@bot.event
async def on_ready():
    print('Bot ready!')
    bot.loop.create_task(scheduleDeleteOldCourses())
    bot.loop.create_task(runDaily())

token = os.getenv('DISCORD_TOKEN')
bot.run(token)