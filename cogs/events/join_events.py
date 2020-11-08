import asyncio
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz
from io import BytesIO
from captcha.image import ImageCaptcha
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageOps
from asyncio import sleep
import requests




class bemvindo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    

    @commands.Cog.listener()  
    async def on_member_join(self, member):
        if member.bot:
            dev = member.guild.get_role(772972514418753586)
            await member.add_roles(dev)
        else:
            captchac = member.guild.get_role(772972512711409725)
            await member.add_roles(captchac)
        if member.guild.id == self.bot.guild and not member.bot:
            canal = self.bot.get_channel(772972557015711744)
            membros = len(member.guild.members)
            texto = "<a:emoji:760195465727180852> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
            txt = f"{member} entrou no servidor."
            await canal.edit(topic=texto, reason=txt)
        
        if member.id == 493569647082209315: #ademira
            await member.add_roles(member.guild.get_role(772972507388444703))

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
            fonte = ImageFont.truetype('cogs/img/college.ttf',42)
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

            canal = self.bot.get_channel(772972552393981972)
            texto = f"Seja bem vindo ao servidor **{self.bot.get_user(self.bot.user.id).name}**, leia as <#772972551713587210> para ficar por dentro do servidor."
            embed = discord.Embed(author="BEM VINDO",description=texto,color=self.bot.cor)
            embed.set_image(url='attachment://welcome.png')
            await canal.send(embed=embed, file=file,content=f"{member.mention}")
            #await canal.send(f"Olá {member.mention}, seja bem vindo ao servidor **{self.bot.get_user(self.bot.user.id).name}**, leia as <#772972551713587210> para ficar por dentro do servidor.", file=discord.File('cogs/img/welcome.png'))
 


        



    @commands.Cog.listener()  
    async def on_member_remove(self, member):
       if member.guild.id == self.bot.guild:
        canal = self.bot.get_channel(772972557015711744)
        membros = len(member.guild.members)
        texto = "<a:emoji:760195465727180852> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
        txt = f"{member} saiu do servidor."
        await canal.edit(topic=texto, reason=txt)

   
def setup(bot):
    bot.add_cog(bemvindo(bot))
