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

    @commands.bot_has_permissions(attach_files=True)
    @commands.guild_only()
    @commands.command(description='Mostra as informações da música no spotify que você está ouvindo.',usage='c.spotify @TOBIAS',aliases=['sptfy','musica'])
    async def spotify(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        presence = next(filter(lambda activity: activity.type.name == 'listening', member.activities)) if len(member.activities) > 0 else None
        if presence is None:
            embed = self.bot.erEmbed(ctx, 'Sem Músicas.')
            embed.description = f'**{ctx.author.name}** você não está ouvindo nenhuma música no momento.'
            return await ctx.send(embed=embed)

        ########################################################
        
        async with aiohttp.ClientSession() as session:
            async with session.get(str(presence.album_cover_url)) as resp:
                if resp.status == 200:
                    response = BytesIO(await resp.read())
                else:
                    return

            thumbnail = Image.open(response).resize((415, 415), Image.ANTIALIAS)
            base = Image.new('RGBA', (1100, 415), (0,0,0,0))
            base.paste(thumbnail, (0, 0))
            borrado = Image.open(response).resize((715, 615), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(radius = 8)) 
            if borrado.mode != 'RGBA':
                borrado = borrado.convert('RGBA')

            width, height = borrado.size
            gradient = Image.new('L', (1, height), color=0xFF)

            for y in range(height):
                gradient.putpixel((0, y), int(255 * (1 - 1.5 * float(y)/width)))
            
            gradient = gradient.rotate(180)
            alpha = gradient.resize(borrado.size)

            black_im = Image.new('RGBA', (width, height), color=0)
            black_im.putalpha(alpha)

            gradient_im = Image.alpha_composite(borrado, black_im)
            base.paste(gradient_im, (415,-150))

            ########################################################
            logo = Image.open('cogs/img/spotlogo.png').resize((100, 100), Image.ANTIALIAS)
            base.paste(logo, (420,10), logo.convert('RGBA'))
            ########################################################          
            end = datetime.utcnow() - presence.start
            decorrido = end.seconds
            ########################################################
            total = int(presence.duration.seconds)

            x = (700 * decorrido) / total   
            ########################################################

            end = presence.end - datetime.utcnow()
            end = str(presence.duration - end)[2:7]
            dur = str(presence.duration)[2:7]

            ########################################################

            fonte = ImageFont.truetype('cogs/img/American Captain.ttf', 35)
            escrever = ImageDraw.Draw(base)
            escrever.text(xy=(430,250), text=str(presence.title.capitalize()),fill=(240,248,255),font=fonte)
            escrever.rectangle([(415,400), (1100,415)], fill=(40,40,40))
            escrever.rectangle([(415, 400), (x + 400, 415)], fill=(0,255,0))
            escrever.text(xy=(430,300), text=str(presence.artist),fill=(46, 189, 89),font=fonte)
            ########################################################
            escrever.text(xy=(430,360), text=str(end),fill=(0,255,0),font=fonte)
            escrever.text(xy=(1020,360), text=str(dur),fill=(240,248,255),font=fonte)
            ########################################################
            arr = BytesIO()
            base.save(arr, format='PNG')
            arr.seek(0)
            file = discord.File(arr, filename='imagem1.png')
            await ctx.send(file=file)

   
def setup(bot):
    bot.add_cog(bemvindo(bot))
