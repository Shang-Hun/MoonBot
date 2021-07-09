# from os import strerror
# import discord
# import sqlite3
# import datetime
# import random
# import math
# import io
# import aiohttp

# from discord.ext import commands
# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw
# from io import BytesIO



# class Mod(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

# class TextLeveling(commands.Cog, name='Leveling'):
#     def __init__(self, bot):
#         self.bot = bot

#     async def ranking(self, message):
#         main = sqlite3.connect('db/main.db')
#         cursor = main.cursor()
#         cursor.execute(f"SELECT role_id, level FROM ranks WHERE guild_id = '{message.guild.id}'")
#         result = cursor.fetchall()
#         cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
#         result1 = cursor.fetchone()
#         lvl = int(result1[2])
#         for result in result:
#             role = message.guild.get_role(int(result[0]))
#             try:
#                 if lvl >= int(result[1]):
#                     await message.author.add_roles(role)
#             except:
#                 return

#     @commands.Cog.listener()
#     async def on_message(self, message):
#         if message.author.bot:
#             return
#         else:
#             main = sqlite3.connect('db/main.db')
#             cursor = main.cursor()
#             cursor.execute(f"SELECT enabled FROM glevel WHERE guild_id = '{message.guild.id}'")
#             result = cursor.fetchone()
#             if result is None:
#                 return
#             elif str(result[0]) == 'enabled':
#                 cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
#                 result1 = cursor.fetchone()
#                 if result1 is None:
#                     sql = ("INSERT INTO glevel(guild_id, user_id, exp, level) VALUES(?,?,?,?)")
#                     val = (str(message.guild.id), str(message.author.id), 0, 0)
#                     cursor.execute(sql, val)
#                     sql = ("INSERT INTO tlevel(guild_id, user_id, xp_time) VALUES(?,?,?)")
#                     val = (str(message.guild.id), str(message.author.id), datetime.datetime.utcnow())
#                     cursor.execute(sql, val)
#                     main.commit()
#                     await TextLeveling(self).ranking(message) 
#                 else:
#                     cursor.execute(f"SELECT xp_time FROM tlevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
#                     result2 = cursor.fetchone()
#                     datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
#                     time_diff = datetime.datetime.strptime(str(datetime.datetime.utcnow()), datetimeFormat)\
#                         - datetime.datetime.strptime(str(result2[0]), datetimeFormat)
#                     if time_diff.seconds >= 60:
#                         exp = int(result1[1])
#                         sql = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
#                         val = (int(exp + random.randint(15,26)), str(message.guild.id), str(message.author.id))
#                         cursor.execute(sql, val)
#                         sql = ("UPDATE tlevel SET xp_time = ? WHERE guild_id = ? and user_id = ?")
#                         val = (datetime.datetime.utcnow(), str(message.guild.id), str(message.author.id))
#                         cursor.execute(sql, val)
#                         main.commit()
#                         cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
#                         result2 = cursor.fetchone()
#                         xp_start = int(result2[1])
#                         lvl_start = int(result1[2])
                        
#                         xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
#                         if xp_end < xp_start:               
#                             await message.channel.send(f'{message.author.mention} has leveled up to level {lvl_start + 1}.')
#                             sql = ("UPDATE glevel SET level = ? WHERE guild_id = ? and user_id = ?")
#                             val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
#                             cursor.execute(sql, val)
#                             main.commit()
#                             sql1 = ("UPDATE glevel SET exp = ? WHERE guild_id = ? and user_id = ?")
#                             val1 = (xp_start - xp_end, str(message.guild.id), str(message.author.id))  
#                             cursor.execute(sql1, val1)
#                             main.commit()
#                             await TextLeveling(self).ranking(message)
#                         else:
#                             await TextLeveling(self).ranking(message) 
#             else:
#                 return

#     @commands.command()
#     async def rank(self, ctx, user:discord.User=None):
#         main = sqlite3.connect('db/main.db')
#         cursor = main.cursor()
#         cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
#         result1 = cursor.fetchone()
#         lvl_start = int(result1[2])
#         xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
#         user = ctx.author or id if not user else user
#         if user is None:
#             main = sqlite3.connect('db/main.db')
#             cursor = main.cursor()
#             cursor.execute(f"SELECT exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
#             result = cursor.fetchone()
#             if result is None:
#                 async with aiohttp.ClientSession() as session:
#                     async with session.get(str(ctx.author.avatar_url)) as response:
#                         image = await response.read()
#                 final_xp = xp_end
#                 xp = 0
#                 user_name = user.name
#                 discriminator = user.discriminator
#                 background = Image.new("RGB", (1000, 240))
#                 logo = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
#                 bigsize = (logo.size[0] * 3, logo.size[1] * 3)
#                 mask = Image.new("L", bigsize, 0)


#                 draw = ImageDraw.Draw(mask)
#                 draw.ellipse((0, 0) + bigsize, 255)


#                 # Black Circle
#                 draw.ellipse((140 * 3, 140 * 3, 189 * 3, 189 * 3), 0)

#                 mask = mask.resize(logo.size, Image.ANTIALIAS)
#                 logo.putalpha(mask)

#                 background.paste(logo, (20, 20), mask=logo)

#                 # # Black Circle
#                 draw = ImageDraw.Draw(background, "RGB")
#                 draw.ellipse((160, 160, 208, 208), fill="#000")

#                 # Green Circle (Discord Status Colours)
#                 if str(ctx.author.status) =='online':
#                     draw.ellipse((162, 162, 206, 206), fill="#43b581")
#                 elif str(ctx.author.status) =='idle':
#                     draw.ellipse((162, 162, 206, 206), fill="#faa61a")
#                 elif str(ctx.author.status) =='dnd':
#                     draw.ellipse((162, 162, 206, 206), fill="#f04747")
#                 elif str(ctx.author.status) =='streaming':
#                     draw.ellipse((162, 162, 206, 206), fill="#643da7")
#                 elif str(ctx.author.status) =='invisible':
#                     draw.ellipse((162, 162, 206, 206), fill="#747f8d")
#                 elif str(ctx.author.status) =='offline':
#                     draw.ellipse((162, 162, 206, 206), fill="#636b75")

#                 # Working with Fonts
#                 big_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 60)
#                 medium_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 40)
#                 small_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 30)

#                 # Placing Right Upper Part
#                 text_size = draw.textsize("0", font=big_font)
#                 offset_x = 1000 - 15 - text_size[0]
#                 offset_y = 10
#                 draw.text((offset_x, offset_y), "0", font=big_font, fill="#11ebf2")

#                 text_size = draw.textsize("LEVEL", font=small_font)
#                 offset_x -= text_size[0] + 5
#                 draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#11ebf2")

#                 # text_size = draw.textsize(f"#1", font=big_font) #here
#                 # offset_x -= text_size[0] + 15
#                 # draw.text((offset_x, offset_y), f"#1", font=big_font, fill="#fff") #here

#                 # text_size = draw.textsize("RANK", font=small_font)
#                 # offset_x -= text_size[0] + 5
#                 # draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")

#                 # Empty Progress Bar (Gray)
#                 bar_offset_x = 320
#                 bar_offset_y = 160
#                 bar_offset_x_1 = 950
#                 bar_offset_y_1 = 200
#                 circle_size = bar_offset_y_1 - bar_offset_y  # Diameter

#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")

#                 # Left Circle
#                 draw.ellipse(
#                     (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )

#                 # Right Circle
#                 draw.ellipse(
#                     (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )


#                 # Filling Bar
#                 bar_length = bar_offset_x_1 - bar_offset_x
#                 progress = (final_xp - xp) * 100 / final_xp
#                 progress = 100 - progress
#                 progress_bar_length = round(bar_length * progress / 100)
#                 bar_offset_x_1 = bar_offset_x + progress_bar_length


#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")

#                 text_size = draw.textsize(f"/ 0 XP", font=small_font)

#                 offset_x = 950 - text_size[0]
#                 offset_y = bar_offset_y - text_size[1] - 10

#                 draw.text((offset_x, offset_y), f"/ 0 XP", font=small_font, fill="#727175")

#                 text_size = draw.textsize(f"0", font=small_font)
#                 offset_x -= text_size[0] + 8
#                 draw.text((offset_x, offset_y), f"0", font=small_font, fill="#fff")


#                 # Blitting Name
#                 text_size = draw.textsize(user_name, font=medium_font)

#                 offset_x = bar_offset_x
#                 offset_y = bar_offset_y - text_size[1] - 5
#                 draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")

#                 # Discriminator
#                 offset_x += text_size[0] + 5
#                 offset_y += 10

#                 draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#727175")
#                 background.save("db/result.png")
#                 file = discord.File("db/result.png")
#                 await ctx.send(file=file)
                
#             elif result is not None:
#                 async with aiohttp.ClientSession() as session:
#                     async with session.get(str(user.avatar_url)) as response:
#                         image = await response.read()          
#                 user_name = user.name
#                 discriminator = user.discriminator
#                 lvl = int(result[1])
#                 # rank = 
#                 final_xp = xp_end
#                 xp = int(result[0])
#                 background = Image.new("RGB", (1000, 240))
#                 logo = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
#                 bigsize = (logo.size[0] * 3, logo.size[1] * 3)
#                 mask = Image.new("L", bigsize, 0)


#                 draw = ImageDraw.Draw(mask)
#                 draw.ellipse((0, 0) + bigsize, 255)


#                 # Black Circle
#                 draw.ellipse((140 * 3, 140 * 3, 189 * 3, 189 * 3), 0)

#                 mask = mask.resize(logo.size, Image.ANTIALIAS)
#                 logo.putalpha(mask)

#                 background.paste(logo, (20, 20), mask=logo)

#                 # # Black Circle
#                 draw = ImageDraw.Draw(background, "RGB")
#                 draw.ellipse((160, 160, 208, 208), fill="#000")

#                 # Green Circle (Discord Status Colours)
#                 if str(ctx.author.status) =='online':
#                     draw.ellipse((162, 162, 206, 206), fill="#43b581")
#                 elif str(ctx.author.status) =='idle':
#                     draw.ellipse((162, 162, 206, 206), fill="#faa61a")
#                 elif str(ctx.author.status) =='dnd':
#                     draw.ellipse((162, 162, 206, 206), fill="#f04747")
#                 elif str(ctx.author.status) =='streaming':
#                     draw.ellipse((162, 162, 206, 206), fill="#643da7")
#                 elif str(ctx.author.status) =='invisible':
#                     draw.ellipse((162, 162, 206, 206), fill="#747f8d")
#                 elif str(ctx.author.status) =='offline':
#                     draw.ellipse((162, 162, 206, 206), fill="#636b75")

#                 # Working with Fonts
#                 big_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 60)
#                 medium_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 40)
#                 small_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 30)

#                 # Placing Right Upper Part
#                 text_size = draw.textsize(str(lvl), font=big_font)
#                 offset_x = 1000 - 15 - text_size[0]
#                 offset_y = 10
#                 draw.text((offset_x, offset_y), str(lvl), font=big_font, fill="#11ebf2")

#                 text_size = draw.textsize("LEVEL", font=small_font)
#                 offset_x -= text_size[0] + 5
#                 draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#11ebf2")

#                 # text_size = draw.textsize(f"#1", font=big_font) #here
#                 # offset_x -= text_size[0] + 15
#                 # draw.text((offset_x, offset_y), f"#1", font=big_font, fill="#fff") #here

#                 # text_size = draw.textsize("RANK", font=small_font)
#                 # offset_x -= text_size[0] + 5
#                 # draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")

#                 # Empty Progress Bar (Gray)
#                 bar_offset_x = 320
#                 bar_offset_y = 160
#                 bar_offset_x_1 = 950
#                 bar_offset_y_1 = 200
#                 circle_size = bar_offset_y_1 - bar_offset_y  # Diameter

#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")

#                 # Left Circle
#                 draw.ellipse(
#                     (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )

#                 # Right Circle
#                 draw.ellipse(
#                     (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )


#                 # Filling Bar
#                 bar_length = bar_offset_x_1 - bar_offset_x
#                 progress = (final_xp - xp) * 100 / final_xp
#                 progress = 100 - progress
#                 progress_bar_length = round(bar_length * progress / 100)
#                 bar_offset_x_1 = bar_offset_x + progress_bar_length


#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#11ebf2")

#                 # Left Circle
#                 draw.ellipse(
#                     (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
#                 )

#                 # Right Circle
#                 draw.ellipse(
#                     (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
#                 )

#                 text_size = draw.textsize(f"/ {final_xp} XP", font=small_font)

#                 offset_x = 950 - text_size[0]
#                 offset_y = bar_offset_y - text_size[1] - 10

#                 draw.text((offset_x, offset_y), f"/ {final_xp:,} XP", font=small_font, fill="#727175")

#                 text_size = draw.textsize(f"{xp:,}", font=small_font)
#                 offset_x -= text_size[0] + 8
#                 draw.text((offset_x, offset_y), f"{xp:,}", font=small_font, fill="#fff")


#                 # Blitting Name
#                 text_size = draw.textsize(user_name, font=medium_font)

#                 offset_x = bar_offset_x
#                 offset_y = bar_offset_y - text_size[1] - 5
#                 draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")

#                 # Discriminator
#                 offset_x += text_size[0] + 5
#                 offset_y += 10

#                 draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#727175")
#                 background.save("db/result.png")
#                 file = discord.File("db/result.png")
#                 await ctx.send(file=file)
#             cursor.close()
#             main.close()

#         else:
#             main = sqlite3.connect('db/main.db')
#             cursor = main.cursor()
#             cursor.execute(f"SELECT exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}'")
#             result = cursor.fetchone()
#             if result is None:
#                 async with aiohttp.ClientSession() as session:
#                     async with session.get(str(ctx.author.avatar_url)) as response:
#                         image = await response.read()
#                 final_xp = xp_end
#                 xp = 0
#                 user_name = user.name
#                 discriminator = user.discriminator
#                 background = Image.new("RGB", (1000, 240))
#                 logo = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
#                 bigsize = (logo.size[0] * 3, logo.size[1] * 3)
#                 mask = Image.new("L", bigsize, 0)


#                 draw = ImageDraw.Draw(mask)
#                 draw.ellipse((0, 0) + bigsize, 255)


#                 # Black Circle
#                 draw.ellipse((140 * 3, 140 * 3, 189 * 3, 189 * 3), 0)

#                 mask = mask.resize(logo.size, Image.ANTIALIAS)
#                 logo.putalpha(mask)

#                 background.paste(logo, (20, 20), mask=logo)

#                 # # Black Circle
#                 draw = ImageDraw.Draw(background, "RGB")
#                 draw.ellipse((160, 160, 208, 208), fill="#000")

#                 # Green Circle (Discord Status Colours)
#                 if str(ctx.author.status) =='online':
#                     draw.ellipse((162, 162, 206, 206), fill="#43b581")
#                 elif str(ctx.author.status) =='idle':
#                     draw.ellipse((162, 162, 206, 206), fill="#faa61a")
#                 elif str(ctx.author.status) =='dnd':
#                     draw.ellipse((162, 162, 206, 206), fill="#f04747")
#                 elif str(ctx.author.status) =='streaming':
#                     draw.ellipse((162, 162, 206, 206), fill="#643da7")
#                 elif str(ctx.author.status) =='invisible':
#                     draw.ellipse((162, 162, 206, 206), fill="#747f8d")
#                 elif str(ctx.author.status) =='offline':
#                     draw.ellipse((162, 162, 206, 206), fill="#636b75")

#                 # Working with Fonts
#                 big_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 60)
#                 medium_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 40)
#                 small_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 30)

#                 # Placing Right Upper Part
#                 text_size = draw.textsize("0", font=big_font)
#                 offset_x = 1000 - 15 - text_size[0]
#                 offset_y = 10
#                 draw.text((offset_x, offset_y), "0", font=big_font, fill="#11ebf2")

#                 text_size = draw.textsize("LEVEL", font=small_font)
#                 offset_x -= text_size[0] + 5
#                 draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#11ebf2")

#                 # text_size = draw.textsize(f"#1", font=big_font) #here
#                 # offset_x -= text_size[0] + 15
#                 # draw.text((offset_x, offset_y), f"#1", font=big_font, fill="#fff") #here

#                 # text_size = draw.textsize("RANK", font=small_font)
#                 # offset_x -= text_size[0] + 5
#                 # draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")

#                 # Empty Progress Bar (Gray)
#                 bar_offset_x = 320
#                 bar_offset_y = 160
#                 bar_offset_x_1 = 950
#                 bar_offset_y_1 = 200
#                 circle_size = bar_offset_y_1 - bar_offset_y  # Diameter

#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")

#                 # Left Circle
#                 draw.ellipse(
#                     (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )

#                 # Right Circle
#                 draw.ellipse(
#                     (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )


#                 # Filling Bar
#                 bar_length = bar_offset_x_1 - bar_offset_x
#                 progress = (final_xp - xp) * 100 / final_xp
#                 progress = 100 - progress
#                 progress_bar_length = round(bar_length * progress / 100)
#                 bar_offset_x_1 = bar_offset_x + progress_bar_length


#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")

#                 text_size = draw.textsize(f"/ 0 XP", font=small_font)

#                 offset_x = 950 - text_size[0]
#                 offset_y = bar_offset_y - text_size[1] - 10

#                 draw.text((offset_x, offset_y), f"/ 0 XP", font=small_font, fill="#727175")

#                 text_size = draw.textsize(f"0", font=small_font)
#                 offset_x -= text_size[0] + 8
#                 draw.text((offset_x, offset_y), f"0", font=small_font, fill="#fff")


#                 # Blitting Name
#                 text_size = draw.textsize(user_name, font=medium_font)

#                 offset_x = bar_offset_x
#                 offset_y = bar_offset_y - text_size[1] - 5
#                 draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")

#                 # Discriminator
#                 offset_x += text_size[0] + 5
#                 offset_y += 10

#                 draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#727175")
#                 background.save("db/result.png")
#                 file = discord.File("db/result.png")
#                 await ctx.send(file=file)

#             elif result is not None:
#                 async with aiohttp.ClientSession() as session:
#                     async with session.get(str(user.avatar_url)) as response:
#                         image = await response.read()
#                 c = main.cursor()
#                 c.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}' ORDER BY level DESC, exp DESC")
#                 result1 = c.fetchall()
#                 user_name = user.name
#                 discriminator = user.discriminator
#                 lvl = int(result[1])
#                 rank = 0
#                 for result1 in result1:
#                     if result1[0] == None:
#                         continue
#                     rank += 1
#                 final_xp = xp_end
#                 xp = int(result[0])
#                 print(result1)
#                 background = Image.new("RGB", (1000, 240))
#                 logo = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
#                 bigsize = (logo.size[0] * 3, logo.size[1] * 3)
#                 mask = Image.new("L", bigsize, 0)


#                 draw = ImageDraw.Draw(mask)
#                 draw.ellipse((0, 0) + bigsize, 255)


#                 # Black Circle
#                 draw.ellipse((140 * 3, 140 * 3, 189 * 3, 189 * 3), 0)

#                 mask = mask.resize(logo.size, Image.ANTIALIAS)
#                 logo.putalpha(mask)

#                 background.paste(logo, (20, 20), mask=logo)

#                 # Black Circle
#                 draw = ImageDraw.Draw(background, "RGB")
#                 draw.ellipse((160, 160, 208, 208), fill="#000")

#                 # Green Circle (Discord Status Colours)
#                 if str(ctx.author.status) =='online':
#                     draw.ellipse((162, 162, 206, 206), fill="#43b581")
#                 elif str(ctx.author.status) =='idle':
#                     draw.ellipse((162, 162, 206, 206), fill="#faa61a")
#                 elif str(ctx.author.status) =='dnd':
#                     draw.ellipse((162, 162, 206, 206), fill="#f04747")
#                 elif str(ctx.author.status) =='streaming':
#                     draw.ellipse((162, 162, 206, 206), fill="#643da7")
#                 elif str(ctx.author.status) =='invisible':
#                     draw.ellipse((162, 162, 206, 206), fill="#747f8d")
#                 elif str(ctx.author.status) =='offline':
#                     draw.ellipse((162, 162, 206, 206), fill="#636b75")

#                 # Working with Fonts
#                 big_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 60)
#                 medium_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 40)
#                 small_font = ImageFont.FreeTypeFont("db/ABeeZee-Regular.otf", 30)

#                 # Placing Right Upper Part
#                 text_size = draw.textsize(str(lvl), font=big_font)
#                 offset_x = 1000 - 15 - text_size[0]
#                 offset_y = 10
#                 draw.text((offset_x, offset_y), str(lvl), font=big_font, fill="#11ebf2")

#                 text_size = draw.textsize("LEVEL", font=small_font)
#                 offset_x -= text_size[0] + 5
#                 draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#11ebf2")

#                 text_size = draw.textsize(f"#{rank}", font=big_font) #here
#                 offset_x -= text_size[0] + 15
#                 draw.text((offset_x, offset_y), f"#{rank}", font=big_font, fill="#fff") #here

#                 text_size = draw.textsize("RANK", font=small_font)
#                 offset_x -= text_size[0] + 5
#                 draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")

#                 # Empty Progress Bar (Gray)
#                 bar_offset_x = 320
#                 bar_offset_y = 160
#                 bar_offset_x_1 = 950
#                 bar_offset_y_1 = 200
#                 circle_size = bar_offset_y_1 - bar_offset_y  # Diameter

#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")

#                 # Left Circle
#                 draw.ellipse(
#                     (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )

#                 # Right Circle
#                 draw.ellipse(
#                     (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
#                 )


#                 # Filling Bar
#                 bar_length = bar_offset_x_1 - bar_offset_x
#                 progress = (final_xp - xp) * 100 / final_xp
#                 progress = 100 - progress
#                 progress_bar_length = round(bar_length * progress / 100)
#                 bar_offset_x_1 = bar_offset_x + progress_bar_length


#                 # Progress Bar
#                 draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#11ebf2")

#                 # Left Circle
#                 draw.ellipse(
#                     (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
#                 )

#                 # Right Circle
#                 draw.ellipse(
#                     (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
#                 )

#                 text_size = draw.textsize(f"/ {final_xp} XP", font=small_font)

#                 offset_x = 950 - text_size[0]
#                 offset_y = bar_offset_y - text_size[1] - 10

#                 draw.text((offset_x, offset_y), f"/ {final_xp:,} XP", font=small_font, fill="#727175")

#                 text_size = draw.textsize(f"{xp:,}", font=small_font)
#                 offset_x -= text_size[0] + 8
#                 draw.text((offset_x, offset_y), f"{xp:,}", font=small_font, fill="#fff")


#                 # Blitting Name
#                 text_size = draw.textsize(user_name, font=medium_font)

#                 offset_x = bar_offset_x
#                 offset_y = bar_offset_y - text_size[1] - 5
#                 draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")

#                 # Discriminator
#                 offset_x += text_size[0] + 5
#                 offset_y += 10

#                 draw.text((offset_x, offset_y), f'#{discriminator}', font=small_font, fill="#727175")
#                 background.save("db/result.png")
#                 file = discord.File("db/result.png")
#                 await ctx.send(file=file)
#                 await ctx.send(f'{rank}/{ctx.guild.member_count}')
#             cursor.close()
#             main.close()

#     @commands.command(aliases=['lb'])
#     async def leaderboard(self, ctx):
#         main = sqlite3.connect('db/main.db')
#         cursor = main.cursor()
#         cursor.execute(f"SELECT user_id, exp, level FROM glevel WHERE guild_id = '{ctx.guild.id}' ORDER BY level DESC, exp DESC")
#         result = cursor.fetchall()
#         desc = ''
#         v = 1
#         for result in result:
#             if v > 10:
#                 break

#             if result[0] == None:
#                 continue
            
#             user = self.bot.get_user(int(result[0]))
#             lvl = result[2]
#             desc += f'**{v}.{str(user)}** *(level {lvl})*\n '
#             v += 1
            
#         embed = discord.Embed(color=0xff003d)
#         embed.add_field(name='**Leaderboard Top 10**', value=desc)
#         embed.set_footer(text=f'{ctx.message.guild}')
#         embed.timestamp = datetime.datetime.utcnow()
#         await ctx.send(embed=embed)


# def setup(bot):
#     bot.add_cog(TextLeveling(bot))
#     bot.add_cog(Mod(bot))