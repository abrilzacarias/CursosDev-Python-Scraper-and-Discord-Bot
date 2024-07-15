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
    if results:
        for course in results:
            name, creator, url = course
            await ctx.send(f"**{name}**\nCreator: {creator}\nLink: {url}")
    else:
        await ctx.send("No courses matching the keyword and today's date were found.")

@search.error
async def searchError(ctx, error):
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


@bot.command()
async def search_creator(ctx, creator: str):
    results = searchCoursesByCreator(creator)
    if results:
        for course in results:
            name, creator, url = course
            await ctx.send(f"**{name}**\nCreator: {creator}\nLink: {url}")
    else:
        await ctx.send(f"No courses found for the creator: {creator}")

@search_creator.error
async def search_creator_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide a creator name. Usage: `!search_creator <creator_name>`')

async def scheduleDeleteOldCourses():
    while True:
        deleteOldCourses()
        await asyncio.sleep(86400)  # Revisa cada 24 horas (86400 segundos)

async def runDaily():
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), datetime.strptime("12:00:00", "%H:%M:%S").time())
        
        if now > target_time:
            target_time += timedelta(days=1)
        
        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time) 
        
        run()  
        
        await asyncio.sleep(86400)

#events
@bot.event
async def on_ready():
    print('Bot ready!')
    bot.loop.create_task(scheduleDeleteOldCourses())
    bot.loop.create_task(runDaily())

token = os.getenv('DISCORD_TOKEN')
bot.run(token)