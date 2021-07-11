import discord
import sqlite3
import datetime
import aiohttp
import textwrap

from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _circle_border(self, circle_img_size: tuple):
        border_size = []
        for i in range(len(circle_img_size)):
            border_size.append(circle_img_size[0] + 8)
        return tuple(border_size)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        main = sqlite3.connect('db/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        setting = sqlite3.connect('db/setting.db')
        cursor1 = setting.cursor()
        cursor1.execute(f"SELECT prefix FROM settings WHERE guild_id = '{guild.id}'")
        result2 = cursor1.fetchone()
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
        if result2 is None:
            sql = ("INSERT INTO settings(guild_id, log_channel, welcome, leave, prefix) VALUES(?,?,?,?,?)")
            val = (str(guild.id), None, None, None, '>')
            cursor1.execute(sql, val)
            setting.commit()
        # for channel in guild.text_channels:
        #     if channel.permissions_for(guild.me).send_messages:
        #         await channel.send(f'Hi i am {self.bot.user}! If you want disabled levelsys Please Enter `//disabled`\n`Need administrator authority`')
        #     break
        cursor.close()
        main.close()
        cursor1.close()
        setting.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        main = sqlite3.connect('db/main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{member.guild.id}'")
        result = cursor.fetchone()
        setting = sqlite3.connect('db/setting.db')
        cursor1 = setting.cursor()
        cursor1.execute(f"SELECT welcome FROM settings WHERE guild_id = '{member.guild.id}'")
        result2 = cursor1.fetchone()
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
                pass
            if str(result2[0]) is None:
                pass
            if str(result2[0]) is not None:
                welcomec = str(result2[0])
                get_channel = discord.utils.get(member.guild.channels, name=welcomec)
                channel_id = get_channel.id
                channel = self.bot.get_channel(channel_id)
                background = Image.new("RGBA", (500, 150))
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(str(member.avatar_url_as(format="png"))) as res:
                        imgdata = await res.read()

                welcome_picture = ImageOps.fit(background, (500, 150), centering=(0.5, 0.5))
                welcome_picture.paste(background)
                welcome_picture = welcome_picture.resize((500, 150), Image.NEAREST)

                profile_area = Image.new("L", (512, 512), 0)
                draw = ImageDraw.Draw(profile_area)
                draw.ellipse(((0, 0), (512, 512)), fill=255)
                profile_area = profile_area.resize((128, 128), Image.ANTIALIAS)
                profile_picture = Image.open(BytesIO(imgdata))
                profile_area_output = ImageOps.fit(profile_picture, (128, 128), centering=(0, 0))
                profile_area_output.putalpha(profile_area)

                mask = Image.new('L', (512, 512), 0)
                draw_thumb = ImageDraw.Draw(mask)
                draw_thumb.ellipse((0, 0) + (512, 512), fill=255, outline=0)
                circle = Image.new("RGBA", (512, 512))
                draw_circle = ImageDraw.Draw(circle)
                if str(member.status) =='online':
                    draw_circle.ellipse([0, 0, 512, 512], fill="#43b581", outline=(255, 255, 255, 250))
                elif str(member.status) =='idle':
                    draw_circle.ellipse([0, 0, 512, 512], fill="#faa61a", outline=(255, 255, 255, 250))
                elif str(member.status) =='dnd':
                    draw_circle.ellipse([0, 0, 512, 512], fill="#f04747", outline=(255, 255, 255, 250))
                elif str(member.status) =='streaming':
                    draw_circle.ellipse([0, 0, 512, 512], fill="#643da7", outline=(255, 255, 255, 250))
                elif str(member.status) =='offline':
                    draw_circle.ellipse([0, 0, 512, 512], fill="#636b75", outline=(255, 255, 255, 250))
                elif str(member.status) =='invisible':
                    draw_circle.ellipse([0, 0, 512, 512], fill="#747f8d", outline=(255, 255, 255, 250))
                circle_border_size = self._circle_border((128, 128))
                circle = circle.resize((circle_border_size), Image.ANTIALIAS)
                circle_mask = mask.resize((circle_border_size), Image.ANTIALIAS)
                circle_pos = (7 + int((136 - circle_border_size[0]) / 2))
                border_pos = (11 + int((136 - circle_border_size[0]) / 2))
                drawtwo = ImageDraw.Draw(welcome_picture)
                welcome_picture.paste(circle, (circle_pos, circle_pos), circle_mask)
                welcome_picture.paste(profile_area_output, (border_pos, border_pos), profile_area_output)

                uname = (str(member.name) + "#" + str(member.discriminator))

                def _outline(original_position: tuple, text: str, pixel_displacement: int, font, textoutline):
                    op = original_position
                    pd = pixel_displacement

                    left = (op[0] - pd, op[1])
                    right = (op[0] + pd, op[1])
                    up = (op[0], op[1] - pd)
                    down = (op[0], op[1] + pd)

                    drawtwo.text(left, text, font=font, fill=(textoutline))
                    drawtwo.text(right, text, font=font, fill=(textoutline))
                    drawtwo.text(up, text, font=font, fill=(textoutline))
                    drawtwo.text(down, text, font=font, fill=(textoutline))

                    drawtwo.text(op, text, font=font, fill=(textoutline))

                welcome_font = ImageFont.truetype("db/setofont.otf", 50)

                _outline((150, 16), "Welcome", 1, welcome_font, (0, 0, 0, 255))
                drawtwo.text((150, 16), "Welcome", font=welcome_font, fill=(255, 255, 255, 230))
                name_font = ImageFont.truetype("db/setofont.otf", 30)
                name_font_medium = ImageFont.truetype("db/setofont.otf", 22)
                name_font_small = ImageFont.truetype("db/setofont.otf", 18)
                name_font_smallest = ImageFont.truetype("db/setofont.otf", 12)
                server_font = ImageFont.truetype("db/setofont.otf", 22)

                if len(str(uname)) <= 17:
                    _outline((152, 63), str(uname), 1, name_font, (0, 0, 0, 255))
                    drawtwo.text((152, 63), str(uname), font=name_font, fill=(255, 255, 255, 230))

                if len(str(uname)) > 17:
                    if len(str(uname)) <= 23:
                        _outline((152, 66), str(uname), 1, name_font_medium, (0, 0, 0, 255))
                        drawtwo.text((152, 66), str(uname), font=name_font_medium, fill=(255, 255, 255, 230))

                if len(str(uname)) >= 24:
                    if len(str(uname)) <= 32:
                        _outline((152, 70), str(uname), 1, name_font_small, (0, 0, 0, 255))
                        drawtwo.text((152, 70), str(uname), font=name_font_small, fill=(255, 255, 255, 230))

                if len(str(uname)) >= 33:
                    drawtwo.text((152, 73), str(uname), 1, name_font_smallest, (0, 0, 0, 255))
                    drawtwo.text((152, 73), str(uname), font=name_font_smallest, fill=(255, 255, 255, 230))

                server_text = "\n".join(textwrap.wrap(f"Welcome to {member.guild.name}!", 25))
                _outline((152, 100), server_text, 1, server_font, (0, 0, 0, 255))
                drawtwo.text((152, 100), server_text, font=server_font, fill=(255, 255, 255, 230))

                welcome_picture.save("db/welcome.png")
                content = "**{}** | Welcome {} to {}!".format(len(member.guild.members), member.mention, member.guild.name)

                file = discord.File("db/welcome.png")
                await channel.send(file=file, content=content)
        cursor.close()
        main.close()
        cursor1.close()
        setting.close()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        setting = sqlite3.connect('db/setting.db')
        cursor1 = setting.cursor()
        cursor1.execute(f"SELECT leave FROM settings WHERE guild_id = '{member.guild.id}'")
        result2 = cursor1.fetchone()
        if str(result2[0]) is None:
            pass
        if str(result2[0]) is not None:
            leavec = str(result2[0])
            get_channel = discord.utils.get(member.guild.channels, name=leavec)
            channel_id = get_channel.id
            channel = self.bot.get_channel(channel_id)
            background = Image.new("RGBA", (500, 150))
            async with aiohttp.ClientSession() as cs:
                async with cs.get(str(member.avatar_url_as(format="png"))) as res:
                    imgdata = await res.read()

            leave_picture = ImageOps.fit(background, (500, 150), centering=(0.5, 0.5))
            leave_picture.paste(background)
            leave_picture = leave_picture.resize((500, 150), Image.NEAREST)

            profile_area = Image.new("L", (512, 512), 0)
            draw = ImageDraw.Draw(profile_area)
            draw.ellipse(((0, 0), (512, 512)), fill=255)
            profile_area = profile_area.resize((128, 128), Image.ANTIALIAS)
            profile_picture = Image.open(BytesIO(imgdata))
            profile_area_output = ImageOps.fit(profile_picture, (128, 128), centering=(0, 0))
            profile_area_output.putalpha(profile_area)

            mask = Image.new('L', (512, 512), 0)
            draw_thumb = ImageDraw.Draw(mask)
            draw_thumb.ellipse((0, 0) + (512, 512), fill=255, outline=0)
            circle = Image.new("RGBA", (512, 512))
            draw_circle = ImageDraw.Draw(circle)
            if str(member.status) =='online':
                draw_circle.ellipse([0, 0, 512, 512], fill="#43b581", outline=(255, 255, 255, 250))
            elif str(member.status) =='idle':
                draw_circle.ellipse([0, 0, 512, 512], fill="#faa61a", outline=(255, 255, 255, 250))
            elif str(member.status) =='dnd':
                draw_circle.ellipse([0, 0, 512, 512], fill="#f04747", outline=(255, 255, 255, 250))
            elif str(member.status) =='streaming':
                draw_circle.ellipse([0, 0, 512, 512], fill="#643da7", outline=(255, 255, 255, 250))
            elif str(member.status) =='offline':
                draw_circle.ellipse([0, 0, 512, 512], fill="#636b75", outline=(255, 255, 255, 250))
            elif str(member.status) =='invisible':
                draw_circle.ellipse([0, 0, 512, 512], fill="#747f8d", outline=(255, 255, 255, 250))
            circle_border_size = self._circle_border((128, 128))
            circle = circle.resize((circle_border_size), Image.ANTIALIAS)
            circle_mask = mask.resize((circle_border_size), Image.ANTIALIAS)
            circle_pos = (7 + int((136 - circle_border_size[0]) / 2))
            border_pos = (11 + int((136 - circle_border_size[0]) / 2))
            drawtwo = ImageDraw.Draw(leave_picture)
            leave_picture.paste(circle, (circle_pos, circle_pos), circle_mask)
            leave_picture.paste(profile_area_output, (border_pos, border_pos), profile_area_output)

            uname = (str(member.name) + "#" + str(member.discriminator))

            def _outline(original_position: tuple, text: str, pixel_displacement: int, font, textoutline):
                op = original_position
                pd = pixel_displacement

                left = (op[0] - pd, op[1])
                right = (op[0] + pd, op[1])
                up = (op[0], op[1] - pd)
                down = (op[0], op[1] + pd)

                drawtwo.text(left, text, font=font, fill=(textoutline))
                drawtwo.text(right, text, font=font, fill=(textoutline))
                drawtwo.text(up, text, font=font, fill=(textoutline))
                drawtwo.text(down, text, font=font, fill=(textoutline))

                drawtwo.text(op, text, font=font, fill=(textoutline))

            leave_font = ImageFont.truetype("db/setofont.otf", 50)

            _outline((150, 16), "Leave", 1, leave_font, (0, 0, 0, 255))
            drawtwo.text((150, 16), "Leave", font=leave_font, fill=(255, 255, 255, 230))
            name_font = ImageFont.truetype("db/setofont.otf", 30)
            name_font_medium = ImageFont.truetype("db/setofont.otf", 22)
            name_font_small = ImageFont.truetype("db/setofont.otf", 18)
            name_font_smallest = ImageFont.truetype("db/setofont.otf", 12)
            server_font = ImageFont.truetype("db/setofont.otf", 22)

            if len(str(uname)) <= 17:
                _outline((152, 63), str(uname), 1, name_font, (0, 0, 0, 255))
                drawtwo.text((152, 63), str(uname), font=name_font, fill=(255, 255, 255, 230))

            if len(str(uname)) > 17:
                if len(str(uname)) <= 23:
                    _outline((152, 66), str(uname), 1, name_font_medium, (0, 0, 0, 255))
                    drawtwo.text((152, 66), str(uname), font=name_font_medium, fill=(255, 255, 255, 230))

            if len(str(uname)) >= 24:
                if len(str(uname)) <= 32:
                    _outline((152, 70), str(uname), 1, name_font_small, (0, 0, 0, 255))
                    drawtwo.text((152, 70), str(uname), font=name_font_small, fill=(255, 255, 255, 230))

            if len(str(uname)) >= 33:
                drawtwo.text((152, 73), str(uname), 1, name_font_smallest, (0, 0, 0, 255))
                drawtwo.text((152, 73), str(uname), font=name_font_smallest, fill=(255, 255, 255, 230))

            server_text = "\n".join(textwrap.wrap(f"Leave to {member.guild.name}!", 25))
            _outline((152, 100), server_text, 1, server_font, (0, 0, 0, 255))
            drawtwo.text((152, 100), server_text, font=server_font, fill=(255, 255, 255, 230))

            leave_picture.save("db/leave.png")
            content = "**{}** | {} Leave to {}!".format(len(member.guild.members), member.mention, member.guild.name)

            file = discord.File("db/leave.png")
            await channel.send(file=file, content=content)
        cursor1.close()
        setting.close()



def setup(bot):
    bot.add_cog(Log(bot))