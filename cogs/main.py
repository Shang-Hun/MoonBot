import discord
import time
import datetime
import psutil
import os
import sqlite3

from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


start_time = datetime.datetime.utcnow()
invite = 'https://bit.ly/3hMdZHI'
Support_Server = 'https://google.com/404'


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    def get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @commands.command(name="ping", description='View my latency and websocket', usage='>ping')
    async def ping(self, ctx):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        t = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.trigger_typing()
        bot = round((t2 - t) * 1000)
        ws = int(self.bot.latency * 1000)
        text = self.get_bot_uptime(brief=True)
        
        
        embed=discord.Embed(title=f'PING', description=f'🕒Uptime: {text}\n \n⌛Latency: `{bot}` (ms)\n \n🌐Websocket: `{ws}` (ms)',
         color=0xacacc1, timestamp= datetime.datetime.now())
        embed.set_footer(text=f'By {owner}', icon_url=ownera)
        await ctx.send(embed=embed)

    @commands.command(name="botinfo", description='Information about me', usage='>botinfo | >bi', aliases=['bi'])
    async def botinfo(self, ctx):
        ramUsage = self.process.memory_full_info().rss / 1024**2
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url

        embed=discord.Embed(title="About Me", description=f"**{self.bot.user}** is a bot with **leveling** and **moderator** functions!",
         color=0xacacc1, timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="🏆Leveling",
         value=f"My leveling system is currently in a beta version, there may be bugs and it is only enabled and cannot be disabled.",
         inline=False)
        embed.add_field(name="⚖️Moderator",
         value=f"My moderator system can currently set prefix(1) log channel (message deletion and message editing) welcome channel leave channel",
         inline=False)
        embed.add_field(name="🆔ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="<:py:748251108253630524>Power By", value="Discord.py {}".format(discord.__version__), inline=True)
        embed.add_field(name="<:Ram2:858372413384818700>RAM", value=f"{ramUsage:.2f} MB", inline=True)
        embed.set_footer(text=f'By {owner}', icon_url=ownera)
        await ctx.send(
                embed=embed,
                components = [
                    [Button(style=ButtonStyle.URL, label = "🔗 Invite", url=invite),
                    Button(style=ButtonStyle.gray, label = "Support Server", disabled=True, emoji="⚔"),
                    Button(style=ButtonStyle.gray, label = "Vote", disabled=True, emoji="🎟")]
                ]
            )

    @commands.command(name="report", description='Report my bug or problem', usage='>report')
    async def report(self, ctx, *, msg:str=None):
        blacklist = sqlite3.connect('db/ud.db')
        cursor = blacklist.cursor()
        cursor.execute(f"SELECT blacklist FROM users WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            receive_channel = await self.bot.fetch_channel(864448286714626068)
            owner = await self.bot.fetch_user(617658847552864256)
            datatime = datetime.datetime.now()
            report_time = datatime.__format__("%Y/%m/%d %H:%M:%S %p")
            text = f'{owner.mention}\n__**Report**__\n**Reporter:**{ctx.author}\n**Report content**:{msg}\n**Report time**:{report_time}'
            await receive_channel.send(text)
            await ctx.send(f'{ctx.author.mention}, Report to {owner} successfully!')
        elif str(result[0]) == 'true':
            await ctx.send(f'{ctx.author.mention} You are a member of the blacklist and cannot use this command!')
        cursor.close()
        blacklist.close()


def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(Main(bot))