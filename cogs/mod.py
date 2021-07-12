import discord
import sqlite3
import typing
import datetime
import asyncio

from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", description='kick a member', usage='>kick [member] (reason)')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user:discord.Member=None, *, reason=None):
        if user is ctx.author:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>You cant kick youself!", color=discord.Color.red()))
        elif user is None:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Enter a member!", color=discord.Color.red()))
        else:
            embed=discord.Embed(description=f'**Moderator**: {ctx.author}\n**Reason** {reason}', timestamp=datetime.datetime.now())
            embed.set_author(name=f'{user} has been kicked!', icon_url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.kick()

    @commands.command(name="ban", description='ban a member', usage='p/ban [member] (reason)\n`EX:p/ban @user No reason`')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, user:discord.Member=None, *, reason=None):
        if user is ctx.author:
            await ctx.message.delete()
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>You cant ban youself!", color=discord.Color.red()))
        elif user is None:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Enter a member!", color=discord.Color.red()))
        else:
            embed=discord.Embed(description=f'**Moderator**: {ctx.author}\n**Reason** {reason}', timestamp=datetime.datetime.now())
            embed.set_author(name=f'{user} has been banned!', icon_url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.kick()

    @commands.command(name="unban", description='unban a user', usage='>unban [user] (reason)\n`EX:>unban user#0000 No reason` __User is not mention is only username+tag!__')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member, reason=None):
        if member is ctx.author:
            await ctx.message.delete()
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>You cant unban youself!", color=discord.Color.red()))
        elif member is None:
            await ctx.message.delete()
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Enter a member!", color=discord.Color.red()))
        else:
            await ctx.message.delete()
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed=discord.Embed(description=f'**Moderator**: {ctx.author}\n**Reason** {reason}', timestamp=datetime.datetime.now())
                    embed.set_author(name=f'{user} has been unban!', icon_url=user.avatar_url)
                    await ctx.send(embed=embed)

    @commands.command(name="clear", description='Delete channel message', usage='>clear [num]')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, num:int=None):
        if num is None:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Please specify the number of messages to clear!", color=discord.Color.red()))

        deleted = await ctx.channel.purge(limit=num+1)
        msg = await ctx.channel.send(embed=discord.Embed(description="deleted {} messages!".format(len(deleted) - 1),
         color=discord.Color.gold(), timestamp=datetime.datetime.now()))

        await asyncio.sleep(3)
        await msg.delete()

    @commands.command(name="slowmode", description='set channel slowmode', usage='>slowmode [seconds]')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def slowmode(self, ctx, seconds:int=None):
        if seconds is None:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Please enter seconds", color=discord.Color.red()))
        elif seconds < 0:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Minimum upper limit 0s", color=discord.Color.red()))
        elif seconds > 21600:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Maximum upper limit 21600s(6hr)", color=discord.Color.red()))
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=discord.Embed(description=f"Channel slow mode has been set to {seconds} seconds!)", color=discord.Color.green(), timestamp=datetime.datetime.utcnow()))
    
    @commands.command(name="mute", description='mute a member', usage='p/mute [member] (reason)\n`EX:p/mute @user No reason`')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, user:discord.Member=None, *, reason=None):
        if user is ctx.author:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>You cant mute youself!", color=discord.Color.red()))
        elif user is None:
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Enter a member!", color=discord.Color.red()))

        role = discord.utils.get(ctx.guild.roles, name="Muted") 
        if not role:
            Muted = await ctx.guild.create_role(name="Muted", reason="use for mute")
            for channel in ctx.guild.channels:
                await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        else:
            await user.add_roles(role)
            embed=discord.Embed(description=f'**Moderator**: {ctx.author}\n**Reason** {reason}', timestamp=datetime.datetime.now())
            embed.set_author(name=f'{user} has been muted!', icon_url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name="unmute", description='unmute a member', usage='p/unmute [member] (reason)\n`EX:p/unmute @user No reason`')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, user:discord.Member=None, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted") 
        if user is ctx.author:
            await ctx.message.delete()
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>You cant mute youself!", color=discord.Color.red()))
        elif user is None:
            await ctx.message.delete()
            return await ctx.send(embed=discord.Embed(description="<:no:855127556737728533>Enter a member!", color=discord.Color.red()))
        else:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await user.remove_roles(role)
            embed=discord.Embed(description=f'**Moderator**: {ctx.author}\n**Reason** {reason}', timestamp=datetime.datetime.now())
            embed.set_author(name=f'{user} has been unmute!', icon_url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name="set_log_channel", description='Set up or change a log channel on this server', usage='>set_log_channel [channel]| >slog [channel]', aliases=['slog'])
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT log_channel FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            sql = ("UPDATE settings SET log_channel = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'{channel.mention} has been set as a log channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET log_channel = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Log channel changed to {channel.mention}!')
        cursor.close()
        setting.close()

    @commands.command(name="remove_log_channel", description='Remove log channel on this server', usage='>remove_log_channel [channel]| >rlog [channel]',aliases=['rlog'])
    @commands.has_permissions(administrator=True)
    async def remove_log_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT log_channel FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            await ctx.send(f'This server not have log channel!')
            return
        elif str(result[0]) is not None:
            g_channel = str(channel)
            g_guild = str(guild.id)
            sql = (f"DELETE FROM settings WHERE log_channel = '{g_channel}' and guild_id = '{g_guild}'")
            cursor.execute(sql)
            setting.commit()
            await ctx.send(f'Deleted Log channel!')
        cursor.close()
        setting.close()

    @commands.command(name="set_prefix", description='Set up or change prefix on this server', usage='>set_prefix [prefix]')
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, *, p=None):
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT prefix FROM settings WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchone()
        if p is None:
            p = '>'
            if p == str(result[0]):
                await ctx.send(f'`{p}` is already the prefix of this server!')
            else:
                sql = ("UPDATE settings SET prefix = ? WHERE guild_id = ?")
                val = ('>', str(ctx.guild.id))
                cursor.execute(sql, val)
                setting.commit()
                await ctx.send(f'Prefix has reverted to `>`!')
        else:
            if p == str(result[0]):
                await ctx.send(f'`{p}` is already the prefix of this server!')
            else:
                pf = str(p)
                sql = ("UPDATE settings SET prefix = ? WHERE guild_id = ?")
                val = (str(pf), str(ctx.guild.id))
                cursor.execute(sql, val)
                setting.commit()
                await ctx.send(f'Prefix has been changed to `{p}` on this server')
                
            cursor.close()
            setting.close()

    @commands.command(name="set_welcome_channel", description='Set up or change welcome channel on this server', usage='>set_welcome_channel [channel] | >swc [channel]', aliases=['swc'])
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT welcome FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            sql = ("UPDATE settings SET welcome = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'{channel.mention} has been set as a Welcome channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET welcome = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Welcome channel changed to {channel.mention}!')
        cursor.close()
        setting.close()

    @commands.command(name="remove_welcome_channel", description='Remove welcome channel on this server', usage='>remove_welcome_channel [channel] | >rwc [channel]', aliases=['rwc'])
    @commands.has_permissions(administrator=True)
    async def remove_welcome_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT welcome FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            await ctx.send(f'This server not have Welcome channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET welcome = ? WHERE guild_id = ?")
            val = (None, str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Deletd welcome channel!')
        cursor.close()
        setting.close()

    @commands.command(name="set_leave_channel", description='Set up or change leave channel on this server', usage='>set_leave_channel [channel] | >slc [channel]', aliases=['slc'])
    @commands.has_permissions(administrator=True)
    async def set_leave_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT leave FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            sql = ("UPDATE settings SET leave = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'{channel.mention} has been set as a leave channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET leave = ? WHERE guild_id = ?")
            val = (str(channel), str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Leave channel changed to {channel.mention}!')
        cursor.close()
        setting.close()

    @commands.command(name="remove_leave_channel", description='Remove leave channel on this server', usage='>remove_leave_channel [channel] | >mlc [channel]', aliases=['mlc'])
    @commands.has_permissions(administrator=True)
    async def remove_leave_channel(self, ctx, channel: typing.Union[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel or id
        guild = ctx.guild
        setting = sqlite3.connect('db/setting.db')
        cursor = setting.cursor()
        cursor.execute(f"SELECT leave FROM settings WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if str(result[0]) is None:
            await ctx.send(f'This server not have leave channel!')
        elif str(result[0]) is not None:
            sql = ("UPDATE settings SET leave = ? WHERE guild_id = ?")
            val = (None, str(guild.id))
            cursor.execute(sql, val)
            setting.commit()
            await ctx.send(f'Deleted leave channel!')
        cursor.close()
        setting.close()
            

def setup(bot):
    bot.add_cog(Mod(bot))
