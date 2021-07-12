import discord
import os
import datetime
import sqlite3
import typing

from discord.ext import commands
from discord.ext.commands.core import command


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ld'])
    @commands.is_owner()
    async def load(self, ctx, extension):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        self.bot.load_extension(f'cogs.{extension}')
        embed=discord.Embed(title=f"<a:loading:748251106970435604> Load -- **{extension}**",
         description="Succeeded Load<a:verify:748461028253368412>", color=discord.Color.gold(), timestamp=datetime.datetime.now())
        embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['ud'])
    @commands.is_owner()
    async def unload(self, ctx, extension):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        self.bot.unload_extension(f'cogs.{extension}')
        embed=discord.Embed(title=f"<a:loading:748251106970435604> Unload -- **{extension}**",
         description="Succeeded Unload<a:verify:748461028253368412>", color=discord.Color.gold(), timestamp=datetime.datetime.now())
        embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
        await ctx.send(embed=embed)
    

    @commands.command(aliases=['rd'])
    @commands.is_owner()
    async def reload(self, ctx, extension):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        if extension == '*':
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.bot.reload_extension(f'cogs.{filename[:-3]}')
            embed=discord.Embed(title=f"<a:loading:748251106970435604> Reload -- **All Extension**",
            description="Succeeded Reload All Extension<a:verify:748461028253368412>", color=discord.Color.gold(), timestamp=datetime.datetime.now())
            embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
            await ctx.send(embed=embed)
        else:
            self.bot.reload_extension(f'cogs.{extension}')
            embed=discord.Embed(title=f"<a:loading:748251106970435604> Reload -- **{extension}**",
            description="Succeeded Reload<a:verify:748461028253368412>", color=discord.Color.gold(), timestamp=datetime.datetime.now())
            embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def oslc(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT log_channel FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            sql = ("UPDATE settings SET log_channel = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'{channel.mention} has been set as a log channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET log_channel = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Log channel changed to {channel.mention}!')
        cursor.close()
        setting.close()

    @commands.command()
    @commands.is_owner()
    async def orlc(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT log_channel FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            await ctx.send(f'This server not have log channel!')
            return
        elif str(result[0]) is not None:
            g_channel = str(channel)
            g_guild = str(guild.id)
            sql = (f"DELETE FROM settings WHERE log_channel = '{g_channel}' and guild_id = '{g_guild}'")
            cursor.execute(sql)
            setting.commit()
            await ctx.send(f'Deleted Log channel!')
        cursor.close()
        setting.close()

    @commands.command()
    @commands.is_owner()
    async def oagp(self ,ctx, *, g=None):
        guild = self.bot.get_guild(int(g))
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        sql = ("INSERT INTO settings(guild_id, log_channel, welcome, leave, prefix) VALUES(?,?,?,?,?)")
        val = (str(guild.id), None, None, None, '//')
        cursor.execute(sql, val)
        setting.commit()
        await ctx.send(f'Added setting data for {guild}!')

        cursor.close()
        setting.close()

    @commands.command()
    @commands.is_owner()
    async def osp(self, ctx, *, p=None):
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT prefix FROM settings WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchone()
        if p is None:
            p = '>'
            if p == str(result[0]):
                await ctx.send(f'`{p}` is already the prefix of this server!')
            else:
                sql = ("UPDATE settings SET prefix = ? WHERE guild_id = ?")
                val = ('>', str(ctx.guild.id))
                cursor.execute(sql, val)
                setting.commit()
                await ctx.send(f'Prefix has reverted to `>`!')
        else:
            if p == str(result[0]):
                await ctx.send(f'`{p}` is already the prefix of this server!')
            else:
                pf = str(p)
                sql = ("UPDATE settings SET prefix = ? WHERE guild_id = ?")
                val = (str(pf), str(ctx.guild.id))
                cursor.execute(sql, val)
                setting.commit()
                await ctx.send(f'Prefix has been changed to `{p}` on this server')
            cursor.close()
            setting.close()

    @commands.command()
    @commands.is_owner()
    async def cac(self, ctx, cac=None, *, t=None):
        if cac is None:
            await ctx.send(f'Please enter something to change avtivity!')
        if t is None:
            await ctx.send(f'Please enter type to change avtivity type!')
        else:
            if t == 'play':
                await self.bot.change_presence(status=discord.Status.idle,
                activity=discord.Activity(type=discord.ActivityType.playing, name=cac))
                await ctx.send(f'changed!')
            if t == 'watch':
                await self.bot.change_presence(status=discord.Status.idle,
                activity=discord.Activity(type=discord.ActivityType.watching, name=cac))
                await ctx.send(f'changed!')
            if t == 'listen':
                await self.bot.change_presence(status=discord.Status.idle,
                activity=discord.Activity(type=discord.ActivityType.listening, name=cac))
                await ctx.send(f'changed!')

    @commands.command()
    @commands.is_owner()
    async def osw(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT welcome FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            sql = ("UPDATE settings SET welcome = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'{channel.mention} has been set as a welcome channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET welcome = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Welcome channel changed to {channel.mention}!')
        cursor.close()
        setting.close()

    @commands.command()
    @commands.is_owner()
    async def odw(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT welcome FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            await ctx.send(f'This server not have welcome channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET welcome = ? WHERE guild_id = ?")
            val = (None, str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Deleted welcome channel!')
        cursor.close()
        setting.close()

    @commands.command()
    @commands.is_owner()
    async def osl(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT leave FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            sql = ("UPDATE settings SET leave = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'{channel.mention} has been set as a leave channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET leave = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Leave channel changed to {channel.mention}!')
        cursor.close()
        setting.close()

    @commands.command()
    @commands.is_owner()
    async def odl(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT leave FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            await ctx.send(f'This server not have leave channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET leave = ? WHERE guild_id = ?")
            val = (None, str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Deleted leave channel!')
        cursor.close()
        setting.close()


def setup(bot):
    bot.add_cog(Owner(bot))
