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


def setup(bot):
    bot.add_cog(Log(bot))
