import discord
import os
import sqlite3
import json

from discord.ext import commands
from discord.ext.commands import when_mentioned_or

with open("db/config.json", mode='r', encoding='utf8') as c:
    cf = json.load(c)

intents = discord.Intents.all()

def get_prefix(bot, message):
    setting = sqlite3.connect('db/setting.db')
    cursor = setting.cursor()
    cursor.execute(f"SELECT prefix FROM settings WHERE guild_id = '{message.guild.id}'")
    result = cursor.fetchone()
    if result is None:
        prefix = '>'
    if str(result[0]) == '>':
        prefix = '>'
    if str(result[0]) is None:
        prefix = '>'
    if str(result[0]) is not None:
        prefix = str(result[0])

    return when_mentioned_or(prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle,
    activity=discord.Activity(type=discord.ActivityType.watching, name=f"🌙"))
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
    bot.run(cf['TOKEN])
