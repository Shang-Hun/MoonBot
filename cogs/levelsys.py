from sqlite3.dbapi2 import Timestamp
import discord
import sqlite3
import datetime
import random
import math

from discord.ext import commands



class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

class TextLeveling(commands.Cog, name='Leveling'):
    def __init__(self, bot):
        self.bot = bot

    async def ranking(self, message):
        main = sqlite3.connect('db/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT role_id, level FROM ranks WHERE guild_id = '{message.guild.id}'")
        result = cursor.fetchall()
        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
        result1 = cursor.fetchone()
        lvl = int(result1[2])
        for result in result:
            role = message.guild.get_role(int(result[0]))
            try:
                if lvl >= int(result[1]):
                    await message.author.add_roles(role)
            except:
                return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            main = sqlite3.connect('db/main.db')
            cursor = main.cursor()
            cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{message.guild.id}'")
            result = cursor.fetchone()
            if result is None:
                return
            elif str(result[0]) == 'enabled':
                cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
                result1 = cursor.fetchone()
                if result1 is None:
                    sql = ("INSERT INTO glevel(guild_id, user_id, exp, level) VALUES(?,?,?,?)")
                    val = (str(message.guild.id), str(message.author.id), 0, 0)
                    cursor.execute(sql, val)
                    sql = ("INSERT INTO tlevel(guild_id, user_id, xp_time) VALUES(?,?,?)")
                    val = (str(message.guild.id), str(message.author.id), datetime.datetime.utcnow())
                    cursor.execute(sql, val)
                    main.commit()
                    await TextLeveling(self).ranking(message) 
                else:
                    cursor.execute(f"SELECT xp_time FROM tlevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
                    result2 = cursor.fetchone()
                    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
                    time_diff = datetime.datetime.strptime(str(datetime.datetime.utcnow()), datetimeFormat)\
                        - datetime.datetime.strptime(str(result2[0]), datetimeFormat)
                    if time_diff.seconds >= 60:
                        exp = int(result1[1])
                        sql = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
                        val = (int(exp + random.randint(15,26)), str(message.guild.id), str(message.author.id))
                        cursor.execute(sql, val)
                        sql = ("UPDATE tlevel SET xp_time = ? WHERE guild_id = ? and user_id = ?")
                        val = (datetime.datetime.utcnow(), str(message.guild.id), str(message.author.id))
                        cursor.execute(sql, val)
                        main.commit()
                        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
                        result2 = cursor.fetchone()
                        xp_start = int(result2[1])
                        lvl_start = int(result1[2])
                        
                        xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
                        if xp_end < xp_start:               
                            await message.channel.send(f'{message.author.mention} has leveled up to level {lvl_start + 1}.')
                            sql = ("UPDATE glevel SET level = ? WHERE guild_id = ? and user_id = ?")
                            val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                            cursor.execute(sql, val)
                            main.commit()
                            sql1 = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
                            val1 = (xp_start - xp_end, str(message.guild.id), str(message.author.id))  
                            cursor.execute(sql1, val1)
                            main.commit()
                            await TextLeveling(self).ranking(message)
                        else:
                            await TextLeveling(self).ranking(message) 
            else:
                return

    @commands.command()
    @commands.guild_only()
    async def rank(self, ctx, user:discord.User=None):
        main = sqlite3.connect('db/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
        result1 = cursor.fetchone()
        lvl_start = int(result1[2])
        xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
        user = ctx.author or id if not user else user
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        if user is None:
            main = sqlite3.connect('db/main.db')
            cursor = main.cursor()
            cursor.execute(f"SELECT exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                xp = int(result[0])
                lvl = int(result[1])
                boxes = int((xp/(200*((1/2) * lvl)))*20)
                embed=discord.Embed(title="RANK", color=user.color, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="📛Name", value=user, inline=True)
                embed.add_field(name="🆔ID", value=user.id, inline=True)
                embed.add_field(name="📊Level", value=lvl, inline=True)
                embed.add_field(name=f"📈Progress bar {xp}/{xp_end}", value=boxes * ":blue_square:" + (15-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text=f'By {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            elif result is not None:
                xp = int(result[0])
                lvl = int(result[1])
                boxes = int((xp/(200*((1/2) * lvl)))*20)
                embed=discord.Embed(title="RANK", color=user.color, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="📛Name", value=user, inline=True)
                embed.add_field(name="🆔ID", value=user.id, inline=True)
                embed.add_field(name="📊Level", value=lvl, inline=True)
                embed.add_field(name=f"📈Progress bar {xp}/{xp_end}", value=boxes * ":blue_square:" + (15-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text=f'By {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            cursor.close()
            main.close()
        else:
            main = sqlite3.connect('db/main.db')
            cursor = main.cursor()
            cursor.execute(f"SELECT exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                xp = int(result[0])
                lvl = int(result[1])
                boxes = int((xp/(200*((1/2) * lvl)))*20)
                embed=discord.Embed(title="RANK", color=user.color, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="📛Name", value=user, inline=True)
                embed.add_field(name="🆔ID", value=user.id, inline=True)
                embed.add_field(name="📊Level", value=lvl, inline=True)
                embed.add_field(name=f"📈Progress bar {xp}/{xp_end}", value=boxes * ":blue_square:" + (15-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text=f'By {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            elif result is not None:
                xp = int(result[0])
                lvl = int(result[1])
                boxes = int((xp/(200*((1/2) * lvl)))*20)
                embed=discord.Embed(title="RANK", color=user.color, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="📛Name", value=user, inline=True)
                embed.add_field(name="🆔ID", value=user.id, inline=True)
                embed.add_field(name="📊Level", value=lvl, inline=True)
                embed.add_field(name=f"📈Progress bar {xp}/{xp_end}", value=boxes * ":blue_square:" + (15-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text=f'By {owner}', icon_url=ownera)
                await ctx.send(embed=embed)
            cursor.close()
            main.close()

    @commands.command(aliases=['lb'])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        main = sqlite3.connect('db/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' ORDER BY level DESC, exp DESC")
        result = cursor.fetchall()
        owner = await self.bot.fetch_user(617658847552864256)
        ownera = owner.avatar_url
        v = 1
        embed = discord.Embed(title="**Leaderboard Top 10**", description=f"Server: __{ctx.guild.name}__",
         color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f'By {owner}', icon_url=ownera)
        for result in result:
            if v > 10:
                break

            if result[0] == None:
                continue
            
            user = self.bot.get_user(int(result[0]))
            lvl = result[2]
            embed.add_field(name=f"**{v}.{str(user)}**", value=f"Lvl: {lvl}", inline=False)
            v += 1

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TextLeveling(bot))
    bot.add_cog(Leveling(bot))
