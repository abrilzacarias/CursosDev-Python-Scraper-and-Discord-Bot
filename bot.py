import discord
from discord.ext import commands
import json
from cursosdev import scrape_if_empty
# Crear un objeto de intenciones con las intenciones predeterminadas
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, description='This bot returns courses')

def load_courses():
    try:
        with open('courses.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        scrape_if_empty()
        load_courses()

courses = load_courses()

def load_secrets():
    with open('secrets.json', 'r') as f:
        return json.load(f)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def search(ctx, searchTerm: str):
    results = [course for course in courses if searchTerm.lower() in course['name'].lower()]
    
    if results:
        for course in results:
            await ctx.send(f"**{course['name']}**\nCreator: {course['creator']}\nLink: {course['url']}")
    else:
        await ctx.send("No courses matching the keyword were found.")
#events
@bot.event
async def on_ready():
    print('Bot ready!')

secrets = load_secrets()
token = secrets['DISCORD_TOKEN']
bot.run(token)