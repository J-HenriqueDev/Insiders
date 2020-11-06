import asyncio
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
            captchac = member.guild.get_role(772972516817895484)
            await member.add_roles(captchac)
        if member.guild.id == self.bot.guild and not member.bot:
            canal = self.bot.get_channel(772972557015711744)
            membros = len(member.guild.members)
            texto = "<a:emoji:760195465727180852> | **Membros** : "+str(membros).replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣")
            txt = f"{member} entrou no servidor."
            await canal.edit(topic=texto, reason=txt)
        
        #########################################




        #########################################


        cat = member.created_at.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone('America/Sao_Paulo')).strftime('`%d/%m/%Y`')
        dias = (datetime.utcnow() - member.created_at).days
        embed = discord.Embed(color=self.bot.cor, description=f'**{member.mention}(`{member.id}`) entrou no servidor, com a conta criada em {cat}({dias} dias).**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
        await self.bot.get_channel(773567922526355496).send(embed=embed)
        
        ###################################################################
        print(f"{member} disparou ")
        canal = discord.utils.get(member.guild.channels, id=772972570752319488)
        #await member.add_roles(member.guild.get_role(772972516817895484))
        try:
            numeros = randint(1000,10000)
            image = ImageCaptcha()
            image.generate('12345')
            image.write(str(numeros), 'out.png')
            mention = await canal.send(member.mention)
            embed = discord.Embed(description="",color=0x7289da)
            embed.set_author(name="🔑| Captcha")
            embed.add_field(name='Por favor escreva os números a baixo (sem espaço) ',value= f"**--Tempo maximo de 5 minutos--**")
            embed.set_image(url="attachment://out.png")
            embed_enviado = await canal.send(embed=embed, file=discord.File('out.png'))

            check=lambda m: m.author == member            

            tentativas = 0
            tentativas_max = 2
            while tentativas <= tentativas_max:
                tentativas += 1
                msg = await self.bot.wait_for('message', check=check, timeout=300)
                if msg.content == str(numeros):
                    msg_sucesso = await canal.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**',delete_after=60)
                    await member.remove_roles(member.guild.get_role(772972516817895484))
                    await member.add_roles(member.guild.get_role(772972512711409725)) 
                    await asyncio.sleep(10)
                    await mention.delete()
                    await msg_sucesso.delete()
                    await msg.delete()
                    await embed_enviado.delete()
                    break
                else:
                    if tentativas <= tentativas_max:
                        await canal.send(f'Resposta errada, você tem mais ``{tentativas_max - tentativas}`` tentativa(s)',delete_after=60)
                    else:
                        await member.guild.kick(member, reason=f'{member} falhou durante o captcha.')

        except Exception as e:
            print(e)
        
        
        
        print(f"{member} entrou ")
        url = requests.get(member.avatar_url_as(format="png"))
        avatar = Image.open(BytesIO(url.content))
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
        fundo.save("cogs/img/welcome.png")   
   


        canal = self.bot.get_channel(772972552393981972)
        await canal.send(f"Olá {member.mention}, seja bem vindo ao servidor **{self.bot.get_user(self.bot.user.id).name}**, leia as <#772972551713587210> para ficar por dentro do servidor.", file=discord.File('cogs/img/welcome.png'))
 


        



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
