import discord
import os
import datetime
import sqlite3
import typing

from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def dev(self, ctx, funcion=None, extension=None, *, cac=None, t=None):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        if extension is None:
            if funcion is None:
                await ctx.send(f'Please enter the function you want to execute!')
            if funcion is not None:
                if funcion == 'guilds':
                    text = f'I have joined `{len(self.bot.guilds)}` servers!'
                    embed=discord.Embed(title='Name/Owner/ID/Members')
                    for guild in self.bot.guilds:
                        try:
                            embed.add_field(name=f"**{guild.name}**", value=f"Owner `{guild.owner}`\n`{guild.id}`\n`{len(guild.members)}` members", inline=True)
                        except:
                            pass
                    await ctx.send(text, embed=embed)
            else:
                await ctx.send(f'I dont have this funcion!')
        if extension is not None:
            if funcion is not None:
                if funcion == 'cac':
                    if cac is None:
                        await ctx.send(f'Please enter something to change avtivity!')
                    if cac == 'reset':
                        await self.bot.change_presence(status=discord.Status.idle,
                        activity=discord.Activity(type=discord.ActivityType.watching, name='🌙'))
                        await ctx.send(f'Activity has been reset!\n**OriginalName:**🌙\n**OriginalType:**watching')
                        return
                    if cac == 'updating':
                        await self.bot.change_presence(status=discord.Status.idle,
                        activity=discord.Activity(type=discord.ActivityType.playing, name='Updating! 🌙'))
                        await ctx.send(f'Activity has been updating mode!\n**Name:**Updating! 🌙\n**OriginalType:**playing')
                        return
                    if t is None:
                        await ctx.send(f'Please enter type to change avtivity type!')
                    else:
                        if t == 'play':
                            await self.bot.change_presence(status=discord.Status.idle,
                            activity=discord.Activity(type=discord.ActivityType.playing, name=cac))
                            await ctx.send(f'Activity has been changed!\n**Name:**{cac}\n**Type:**playing')
                        if t == 'watch':
                            await self.bot.change_presence(status=discord.Status.idle,
                            activity=discord.Activity(type=discord.ActivityType.watching, name=cac))
                            await ctx.send(f'Activity has been changed!\n**Name:**{cac}\n**Type:**watching')
                        if t == 'listen':
                            await self.bot.change_presence(status=discord.Status.idle,
                            activity=discord.Activity(type=discord.ActivityType.listening, name=cac))
                            await ctx.send(f'Activity has been changed!\n**Name:**{cac}\n**Type:**listening')
                        if funcion == 'ld':
                            self.bot.load_extension(f'cogs.{extension}')
                            embed=discord.Embed(title=f"<a:loading:748251106970435604> Load -- **{extension}**",
                            description="Succeeded Load<a:verify:748461028253368412>", color=discord.Color.gold(), timestamp=datetime.datetime.now())
                            embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
                            await ctx.send(embed=embed)
                        if funcion == 'ud':
                            self.bot.unload_extension(f'cogs.{extension}')
                            embed=discord.Embed(title=f"<a:loading:748251106970435604> Unload -- **{extension}**",
                            description="Succeeded Unload<a:verify:748461028253368412>", color=discord.Color.gold(), timestamp=datetime.datetime.now())
                            embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
                            await ctx.send(embed=embed)
            if funcion == 'rd':
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
    async def black(self, ctx, bw=None, user:discord.Member=None):
        blacklist = sqlite3.connect('db/ud.db')
        cursor = blacklist.cursor()
        cursor.execute(f"SELECT blacklist FROM users WHERE user_id = '{user.id}'")
        result = cursor.fetchone()
        if bw is None:
            await ctx.send(f'Please enter black or unblack!')
        elif bw is not None:
            if bw == 'black':
                if result is None:
                    sql = ("INSERT INTO users(user_id, blacklist) VALUES(?,?)")
                    val = (str(user.id), 'true')
                    cursor.execute(sql, val)
                    blacklist.commit()
                    await ctx.send(f'{user} has been add to blacklist!')
                elif result is not None:
                    await ctx.send(f'{user} is already in blacklist!')
            if bw == 'unblack':
                if result is None:
                    await ctx.send(f'{user} doesnt in blacklist!')
                elif result is not None:
                    sql = ("DELETE FROM users WHERE user_id = ? and blacklist = ?")
                    val = (str(user.id), 'true')
                    cursor.execute(sql, val)
                    blacklist.commit()
                    await ctx.send(f'{user} has been remove to blacklist!')
        else:
            await ctx.send(f'Please enter black or unblack!')
        cursor.close()
        blacklist.close()

def setup(bot):
    bot.add_cog(Owner(bot))