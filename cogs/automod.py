import discord
import sqlite3
import datetime
import time

from discord.ext import commands

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        dt = datetime.datetime.now()
        ddt = dt.__format__("%Y/%m/%d %H:%M:%S %p")
        guild = message.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT log_channel FROM settings WHERE guild_id = {guild.id}")
        result = cursor.fetchone()
        if str(result[0]) is None:
            return
        elif str(result[0]) is not None:
            log = str(result[0])
            get_channel = discord.utils.get(guild.channels, name=log)
            channel_id = get_channel.id
            channel = self.bot.get_channel(channel_id)
            embed1=discord.Embed(title="DELTED MESSAGE", description=f"Deleted Time: {ddt}",
            color=message.author.color)
            embed1.add_field(name="Author", value='{}'.format(message.author), inline=True)
            embed1.add_field(name="Channel", value='{}'.format(message.channel), inline=True)
            embed1.set_footer(text="Message:\n{}".format(message.content))
            msg = await channel.send(embed=embed1)

            async for entry in message.guild.audit_logs(limit=100, action=discord.AuditLogAction.message_delete):
                if entry.target == message.author:
                    if -10 < (entry.created_at - datetime.datetime.utcnow()).total_seconds() < 10:
                        embed2=discord.Embed(title="DELTED MESSAGE", description=f"Deleted Time: {ddt}",
                        color=message.author.color, timestamp=datetime.datetime.now())
                        embed2.add_field(name="Deleted By", value='{}'.format(entry.user), inline=True)
                        embed2.add_field(name="Author", value='{}'.format(message.author), inline=True)
                        embed2.add_field(name="Channel", value='{}'.format(message.channel), inline=True)
                        embed2.set_footer(text="Message:\n{}".format(message.content))
                        await msg.edit(embed=embed2)
                        return
        else:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        dt = datetime.datetime.now()
        ddt = dt.__format__("%Y/%m/%d %H:%M:%S %p")
        guild = before.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT log_channel FROM settings WHERE guild_id = {guild.id}")
        result = cursor.fetchone()
        if str(result[0]) is None:
            return
        if before.clean_content == after.clean_content:
            return
        elif str(result[0]) is not None:
            log = str(result[0])
            get_channel = discord.utils.get(guild.channels, name=log)
            channel_id = get_channel.id
            channel = self.bot.get_channel(channel_id)
            embed=discord.Embed(title="EDIT MESSAGE", description=f"Edit Time: {ddt}",
            color=before.author.color, timestamp=datetime.datetime.now())
            embed.add_field(name="Edit By", value=f'{before.author}', inline=True)
            embed.add_field(name="Channel", value=f'{before.channel}', inline=True)
            embed.add_field(name="Before", value=f'{before.clean_content}', inline=True)
            embed.add_field(name="After", value=f'{after.clean_content}', inline=True)
            await channel.send(embed=embed)
        else:
            return


def setup(bot):
    bot.add_cog(Automod(bot))