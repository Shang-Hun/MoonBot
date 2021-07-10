import discord
import sqlite3
import typing

from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def enabled(self, ctx):
    #     guild = ctx.guild
    #     main = sqlite3.connect('db/main.db')
    #     cursor = main.cursor()
    #     cursor.execute(f"DELECT enabled FROM glevel WHERE guild_id = '{guild.id}'")
    #     sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
    #     val = (str(guild.id), 'enabled')
    #     cursor.execute(sql, val)
    #     main.commit()
    #     await ctx.send(f"enabled levelsys in this server!")
    #     cursor.close()
    #     main.close()

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def disabled(self, ctx):
    #     guild = ctx.guild
    #     main = sqlite3.connect('db/main.db')
    #     cursor = main.cursor()
    #     cursor.execute(f"DELECT enabled FROM glevel WHERE guild_id = '{guild.id}'")
    #     sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
    #     val = (str(guild.id), 'disabled')
    #     cursor.execute(sql, val)
    #     main.commit()
    #     await ctx.send(f"disabled levelsys in this server!")
    #     cursor.close()
    #     main.close()

    @commands.command(aliases=['slog'])
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
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

    @commands.command(aliases=['rlog'])
    @commands.has_permissions(administrator=True)
    async def remove_log_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
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
            

def setup(bot):
    bot.add_cog(Mod(bot))