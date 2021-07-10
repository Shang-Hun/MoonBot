import discord
import sqlite3
import datetime

from discord.ext import commands


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        main = sqlite3.connect('db/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO glevel(guild_id, enabled) VALUES(?,?)")
            val = (str(guild.id), 'enabled')
            cursor.execute(sql, val)
            main.commit()
        elif str(result[0]) == 'disabled':
            sql = ("UPDATE glevel SET enabled = ? WHERE guild_id = ?")
            val = ('enabled', str(guild.id))
            cursor.execute(sql, val)
            main.commit()
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f'Hi i am {self.bot.user}! If you want disabled levelsys Please Enter `//disabled`\n`Need administrator authority`')
            break
        cursor.close()
        main.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        main = sqlite3.connect('db/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{member.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            return
        elif str(result[0]) == 'enabled':
            cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{member.guild.id}' and user_id = '{member.id}'")
            result1 = cursor.fetchone()
            if result1 is None:
                sql = ("INSERT INTO glevel(guild_id, user_id, exp, level) VALUES(?,?,?,?)")
                val = (str(member.guild.id), str(member.id), 0, 0)
                cursor.execute(sql, val)
                sql = ("INSERT INTO tlevel(guild_id, user_id, xp_time) VALUES(?,?,?)")
                val = (str(member.guild.id), str(member.id), datetime.datetime.utcnow())
                cursor.execute(sql, val)
                main.commit()
            if result1 is not None:
                return
        else:
            return
        cursor.close()
        main.close()

    # @commands.Cog.listener()
    # async def on_message_delete(self, message):
    #     dt = datetime.datetime.now()
    #     ddt = dt.__format__("%Y/%m/%d %H:%M:%S %p")
    #     guild = message.guild
    #     main = sqlite3.connect('db/log.db')
    #     cursor = main.cursor()
    #     cursor.execute(f"SELECT channel FROM log WHERE guild = {guild.id}")
    #     result = cursor.fetchone()
    #     if result is None:
    #         return
    #     elif result is not None:
    #         log = str(result[0])
    #         # get_guild = str(result1[1])
    #         # guild1 = self.bot.get_guild(int(get_guild))
    #         get_channel = discord.utils.get(guild.channels, name=log)
    #         channel_id = get_channel.id
    #         channel = self.bot.get_channel(channel_id)
    #         async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
    #             deleter = entry.user

    #         embed=discord.Embed(title="DELTED MESSAGE", description=f"Deleted Time: {ddt}",
    #         color=message.author.color)
    #         embed.add_field(name="Deleted by", value=deleter, inline=True)
    #         embed.add_field(name="Author", value=message.author, inline=True)
    #         embed.add_field(name="Channel", value=message.channel, inline=True)
    #         embed.set_footer(text=f"Message:\n{message.content}")
    #         await channel.send(embed=embed)  
    #     else:
    #         return



def setup(bot):
    bot.add_cog(Log(bot))