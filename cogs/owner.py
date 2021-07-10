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
         description="Succeeded Load<a:verify:748461028253368412>", color=discord.Color.gold())
        embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['ud'])
    @commands.is_owner()
    async def unload(self, ctx, extension):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        self.bot.unload_extension(f'cogs.{extension}')
        embed=discord.Embed(title=f"<a:loading:748251106970435604> Unload -- **{extension}**",
         description="Succeeded Unload<a:verify:748461028253368412>", color=discord.Color.gold())
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
            description="Succeeded Reload All Extension<a:verify:748461028253368412>", color=discord.Color.gold())
            embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
            await ctx.send(embed=embed)
        else:
            self.bot.reload_extension(f'cogs.{extension}')
            embed=discord.Embed(title=f"<a:loading:748251106970435604> Reload -- **{extension}**",
            description="Succeeded Reload<a:verify:748461028253368412>", color=discord.Color.gold())
            embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def oslc(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        main = sqlite3.connect('db/log.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT channel FROM log WHERE guild = '{guild.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO log(guild, channel) VALUES(?,?)")
            val = (str(guild.id), str(channel))
            cursor.execute(sql, val)
            main.commit()
            await ctx.send(f'{channel.mention} has been set as a log channel!')
        elif result is not None:
            sql = ("UPDATE log SET channel = ? WHERE guild = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            main.commit()
            await ctx.send(f'Log channel changed to {channel.mention}!')
        cursor.close()
        main.close()

    @commands.command()
    @commands.is_owner()
    async def orlc(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        main = sqlite3.connect('db/log.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT channel FROM log WHERE guild = '{guild.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f'This server not have log channel!')
            return
        elif result is not None:
            g_channel = str(channel)
            g_guild = str(guild.id)
            sql = (f"DELETE FROM log WHERE channel = '{g_channel}' and guild = '{g_guild}'")
            cursor.execute(sql)
            main.commit()
            await ctx.send(f'Deleted Log channel!')
        cursor.close()
        main.close()

    # @commands.command()
    # @commands.is_owner()
    # async def on(self, ctx):   
    #     guild = ctx.guild
    #     main = sqlite3.connect('db/main.db')
    #     cursor = main.cursor()
    #     cursor2 = main.cursor()
    #     cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{ctx.guild.id}'")
    #     result = cursor.fetchone()
    #     if result is None:
    #         sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
    #         val = (str(guild.id), 'enabled')
    #         cursor.execute(sql, val)
    #         main.commit()
    #     else:
    #         dsql = ("DELETE FROM glevel(guild_id, enabled) VALUES(?,?)")
    #         dval = (str(guild.id), 'disabled')
    #         sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
    #         val = (str(guild.id), 'enabled')
    #         cursor.execute(sql, val)
    #         cursor2.execute(dsql, dval)
    #         main.commit()
    #     await ctx.send(f"enabled levelsys in this server!")
    #     cursor.close()
    #     main.close()

    # @commands.command()
    # @commands.is_owner()
    # async def off(self, ctx):   
    #     guild = ctx.guild
    #     main = sqlite3.connect('db/main.db')
    #     cursor = main.cursor()
    #     cursor2 = main.cursor()
    #     cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{ctx.guild.id}'")
    #     result = cursor.fetchone()
    #     if result is None:
    #         sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
    #         val = (str(guild.id), 'disabled')
    #         cursor.execute(sql, val)
    #         main.commit()
    #     else:
    #         dsql = ("DELETE FROM glevel(guild_id, enabled) VALUES(?,?)")
    #         dval = (str(guild.id), 'enabled')
    #         sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
    #         val = (str(guild.id), 'disabled')
    #         cursor.execute(sql, val)
    #         cursor2.execute(dsql, dval)
    #         main.commit()
    #     await ctx.send(f"disabled levelsys in this server!")
    #     cursor.close()
    #     main.close()

    # @commands.command()
    # @commands.is_owner()
    # async def con(self, ctx):
    #     guild = ctx.guild
    #     main = sqlite3.connect('db/main.db')
    #     cursor = main.cursor()
    #     sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
    #     val = (str(guild.id), 'enabled')
    #     cursor.execute(sql, val)
    #     main.commit()
    #     await ctx.send(f'on!')
    #     cursor.close()
    #     main.close()


def setup(bot):
    bot.add_cog(Owner(bot))