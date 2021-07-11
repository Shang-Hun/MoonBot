import discord

from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.errors.CheckFailure):
            owner = await self.bot.fetch_user(617658847552864256)
            embed=discord.Embed(description=f'<:no:855127556737728533>Only **{owner}** can use this command!',
            color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed=discord.Embed(description=f'<:no:855127556737728533>You do not have permission to use this command!',
            color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.CommandNotFound):
            embed=discord.Embed(description=f'<:no:855127556737728533>I dont have this command!',
            color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)


def setup(bot):
    bot.add_cog(Error(bot))