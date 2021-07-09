import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='//', intents=intents)
bot.remove_command('help')
load_dotenv()
token = getenv("TOKEN")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle,
    activity=discord.Activity(type=discord.ActivityType.playing, name=f"🌙"))
    print('------')
    print('Online! botinfo:')
    print(f'Bot Owner: ShangHun✧‧₊˚#4475')
    print(f"Bot: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    print('------')
  

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(os.environ['token'])