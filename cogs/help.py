import discord
import random
import os
import datetime


from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord.ext import commands

invite = 'https://bit.ly/3hMdZHI'
Support_Server = 'https://google.com/404'


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description='View all my commands', usage=f'>help | >help cmd')
    async def help(self, ctx, cmd=None):
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        MoonColor = 0xacacc1
        if ctx.message.content.endswith("help"):
            if cmd is not None:
                if cmd == "help":
                    embed = discord.Embed()
                    embed.title = "HELP"
                    embed.description = "**help**"
                    embed.color = MoonColor
                    embed.timestamp=datetime.datetime.utcnow()
                    embed.add_field(name=f"Usage", value=f">help | >help [command]", inline=False)
                    embed.add_field(name=f"Alias", value=f"None", inline=False)
                    embed.add_field(name=f"Description", value=f"View all my commands or view the usage of command", inline=False)
                    embed.set_footer(text='By ShangHun#4475', icon_url=ownera)
                    await ctx.send(embed=embed)
                    return
                else:
                    for command in self.bot.commands:
                        if str(command) == cmd:
                            embed0 = discord.Embed()
                            embed0.title = "HELP"
                            embed0.description = f"**{command}**"
                            embed0.color = MoonColor
                            aliases = ",".join(command.aliases)
                            if str(command.aliases) == "[]":
                                aliases = "None"
                            if str(command) == "commands":
                                aliases = "None"
                            embed0.add_field(name=f"Usage", value=f"{command.usage}", inline=False)
                            embed0.add_field(name=f"Alias", value=f"{aliases}", inline=False)
                            embed0.add_field(name=f"Description", value=f"{command.description}", inline=False)
                            embed0.set_footer(text='By ShangHun#4475', icon_url=ownera)
                            await ctx.send(embed=embed0)
                            return
                    else:
                        await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>I dont have this command!", color=discord.Color.red()))
                        return
            else:
                embed1=discord.Embed()
                embed1.color = MoonColor
                embed1.title = "HELP"
                embed1.description = f"To get help on an command type >help [command]!\nIf your server has changed the prefix, the usage is\n`(your server prefix)[command]`"
                embed1.timestamp=datetime.datetime.utcnow()
                embed1.add_field(name="⚖️Moderator", value="`set_prefix` `set_log_channel` `remove_log_channel` `set_welcome_channel` `remove_welcome_channel` `set_leave_channel` `remove_leave_channel` `kick` `ban` `unban` `clear` `slowmode` `mute` `unmute`", inline=False)
                embed1.add_field(name="🏆Leveling", value="`rank` `leaderboard`", inline=False)
                embed1.add_field(name="🌎General", value="`ping` `help` `botinfo`", inline=False)
                embed1.set_footer(text='By ShangHun#4475', icon_url=ownera)
                await ctx.send(
                    embed=embed1,
                    components = [
                        [Button(style=ButtonStyle.gray, label = "🔗 Invite", disabled=True),
                        Button(style=ButtonStyle.gray, label = "Support Server", disabled=True, emoji="⚔"),
                        Button(style=ButtonStyle.gray, label = "Vote", disabled=True, emoji="🎟")]
                    ]
                )
                return
        if cmd is None:
            for filename in os.listdir('./cogs'):
                if filename[:-3] == "Error" or filename[:-3] == "Dm" or filename[:-3] == "Slash":
                    ...
                else:
                    if filename.endswith(".py"):
                        cogname = []
                        for command in self.bot.commands:
                            if str(command) == "load" or str(command) == "unload" or str(command) == "reload":
                                ...
                            else:
                                if command.cog_name == filename[:-3]:
                                    cogname.append(f'`{command}`')
                                    if command.cog_name == "Help":
                                        h = "`help`"
                                    else:
                                        h = ""
        else:
            if cmd == "help":
                    embed2 = discord.Embed()
                    embed2.title = "HELP"
                    embed2.description = "**help**"
                    embed2.color = MoonColor
                    embed2.timestamp=datetime.datetime.utcnow()
                    embed2.add_field(name=f"Usage", value=f">help | >help [command]", inline=False)
                    embed2.add_field(name=f"Alias", value=f"None", inline=False)
                    embed2.add_field(name=f"Description", value=f"View all my commands or view the usage of command", inline=False)
                    embed2.set_footer(text='By ShangHun#4475', icon_url=ownera)
                    await ctx.send(embed=embed2)
                    return
            else:
                for command in self.bot.commands:
                    if str(command) == cmd:
                        embed3 = discord.Embed()
                        embed3.title = "HELP"
                        embed3.description = f"**{command}**"
                        embed3.color = MoonColor
                        embed3.timestamp=datetime.datetime.utcnow()
                        aliases = ",".join(command.aliases)
                        if str(command.aliases) == "[]":
                            aliases = "None"
                        if str(command) == "commands":
                            aliases = "None"
                        embed3.add_field(name=f"Usage", value=f"{command.usage}", inline=False)
                        embed3.add_field(name=f"Alias", value=f"{aliases}", inline=False)
                        embed3.add_field(name=f"Description", value=f"{command.description}", inline=False)
                        embed3.set_footer(text='By ShangHun#4475', icon_url=ownera)
                        await ctx.send(embed=embed3)
                        return
                else:
                    await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>I dont have this command!", color=discord.Color.red()))
                    return


def setup(bot):
    bot.add_cog(Help(bot))