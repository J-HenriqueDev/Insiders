import asyncio
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz
from io import BytesIO
from captcha.image import ImageCaptcha
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from asyncio import sleep
import requests




class bemvindo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    

    @commands.Cog.listener()  
    async def on_member_join(self, member):
        if member.guild.id == self.bot.guild and not member.bot:
            numbers = ['<:0black:786085813858336778>', '<:1black:786085813791227945>', '<:2black:786085813846409256>',
                       '<:3black:786085813829894144>', '<:4black:786085813901197312>', '<:5black:786085813829894164>',
                       '<:5black:786085813829894164>', '<:7black:786085813850472489>', '<:8black:786085813943140352>',
                       '<:9black:786085813854666772>']
            text = str(member.guild.member_count)
            list_ = list()
            for letter in text:
                list_.append(numbers[int(letter)])
            list_ = str(list_).replace('[', '').replace(']', '').replace(',', '.').replace("'","").replace(".","")
            canal = self.bot.get_channel(791131876697833483)
            txt = f"{member} entrou no servidor."
            await canal.edit(topic="<a:emoji:760195465727180852> **Membros:**  " + list_, reason=txt)


        #########################################
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.avatar_url_as(format="webp"))) as resp:
                if resp.status == 200:
                    response = BytesIO(await resp.read())
                else:
                    return
        
            print(f"{member} entrou ")
            avatar = Image.open(response)
            avatar = avatar.resize((210, 210));
            bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mask)

            saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
            saida.putalpha(mask)

            fundo = Image.open('cogs/img/bem-vindo.png')
            fonte = ImageFont.truetype('cogs/img/American Captain.ttf',42)
            escrever = ImageDraw.Draw(fundo)
            nome_user = str(member) if len(str(member)) <= 50 else str(member)[:50]
            fundo_x, _ = fundo.size
            texto_x, _ = escrever.textsize(nome_user, font=fonte)
            escrever.text(xy=((fundo_x - texto_x)/2, 345), text=nome_user,fill=(0,0,0),font=fonte)
            fundo.paste(saida, (357, 39), saida)
            arr = BytesIO()
            fundo.save(arr, format='PNG')
            arr.seek(0)
            file = discord.File(arr, filename='welcome.png')

            canal = self.bot.get_channel(791131862239543327)
            texto = f"Seja bem vindo ao servidor **{self.bot.get_user(self.bot.user.id).name}**, leia as <#783667565141426218> para ficar por dentro do servidor."
            embed = discord.Embed(author="BEM VINDO",description=texto,color=self.bot.cor)
            embed.set_image(url='attachment://welcome.png')
            await canal.send(embed=embed, file=file,content=f"{member.mention}")
            #await canal.send(f"Olá {member.mention}, seja bem vindo ao servidor **{self.bot.get_user(self.bot.user.id).name}**, leia as <#772972551713587210> para ficar por dentro do servidor.", file=discord.File('cogs/img/welcome.png'))


            if member.bot:
                return await member.add_roles(discord.Object(791131773945774080))
            else:
                await member.add_roles(discord.Object(791131770321895475))


    @commands.Cog.listener()  
    async def on_member_remove(self, member):
       if member.guild.id == self.bot.guild:
           numbers = ['<:0black:786085813858336778>', '<:1black:786085813791227945>', '<:2black:786085813846409256>',
                      '<:3black:786085813829894144>', '<:4black:786085813901197312>', '<:5black:786085813829894164>',
                      '<:5black:786085813829894164>', '<:7black:786085813850472489>', '<:8black:786085813943140352>',
                      '<:9black:786085813854666772>']
           text = str(member.guild.member_count)
           list_ = list()
           for letter in text:
               list_.append(numbers[int(letter)])
           list_ = str(list_).replace('[', '').replace(']', '').replace(',', '.').replace("'", "").replace(".", "")
           canal = self.bot.get_channel(791131876697833483)
           txt = f"{member} saiu no servidor."
           await canal.edit(topic="<a:emoji:760195465727180852> **Membros:**  " + list_, reason=txt)


def setup(bot):
    bot.add_cog(bemvindo(bot))
