from datetime import datetime
import discord
import os
import datetime
import sqlite3

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


def setup(bot):
    bot.add_cog(Owner(bot))
