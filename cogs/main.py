import discord
import time
import datetime
import psutil
import os

from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

start_time = time.time()
invite = 'https://bit.ly/3hMdZHI'
Support_Server = 'https://google.com/404'


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        t = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.trigger_typing()
        bot = round((t2 - t) * 1000)
        ws = int(self.bot.latency * 1000)
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        
        
        embed=discord.Embed(title=f'PING', description=f'🕒Uptime: {text}\n \n⌛Latency: `{bot}` (ms)\n \n🌐Websocket: `{ws}` (ms)',
         color=0xacacc1, timestamp= datetime.datetime.now())
        embed.set_footer(text=f'By {owner}', icon_url=ownera)
        await ctx.send(embed=embed)

    @commands.command(aliases=['bi'])
    async def botinfo(self, ctx):
        ramUsage = self.process.memory_full_info().rss / 1024**2
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url

        embed=discord.Embed(title="About Me", description=f"**{self.bot.user}** is a bot with **leveling** and **moderator** functions!",
         color=0xacacc1)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="🆔ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="<:py:748251108253630524>Power By", value="Discord.py {}".format(discord.__version__), inline=True)
        embed.add_field(name="<:Ram2:858372413384818700>RAM", value=f"{ramUsage:.2f} MB", inline=True)
        embed.set_footer(text=f'By {owner}', icon_url=ownera)
        await ctx.send(
                embed=embed,
                components = [
                    [Button(style=ButtonStyle.gray, label = "🔗 Invite", disabled=True),
                    Button(style=ButtonStyle.gray, label = "Support Server", disabled=True, emoji="⚔"),
                    Button(style=ButtonStyle.gray, label = "Vote", disabled=True, emoji="🎟")]
                ]
            )


def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(Main(bot))