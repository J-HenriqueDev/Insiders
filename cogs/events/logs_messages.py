import discord
import pytz
import asyncio, re
from datetime import datetime
from discord.ext import commands
aviso1 = []
aviso2 = []
aviso3 = []


class logs_messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    #ok
    @commands.Cog.listener()
    async def on_message_delete(self,message):
            if message.author.bot == False:
                if message.channel.id == 772972558605090836:
                    return
                elif message.channel.id == 772972570752319488:
                    return
                else:
                    embed = discord.Embed(color=self.bot.cor)
                    embed.set_author(name="Logs (Mensagem Apagada)", icon_url=message.author.avatar_url)
                    if len(message.attachments) >= 1:
                        link = message.attachments[0].url
                        url = str(link).replace("https://cdn.discordapp.com/", "https://media.discordapp.net/")
                        embed.set_image(url=url)
                    else:
                        pass
                    if len(message.content) >= 1:
                        embed.add_field(name="Mensagem", value=f"``{message.content[:900]}``", inline=True)
                    else:
                        pass
                    embed.add_field(name="Usuário", value=f"``{message.author}`` - (<@{message.author.id}>)", inline=True)
                    embed.add_field(name="Canal", value=f"``{message.channel.name}`` - (<#{message.channel.id}>)",
                                        inline=True)
                    timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
                    time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))
                    embed.add_field(name="Horário", value=f"``{time}``", inline=True)
                    canal = message.guild.get_channel(self.bot.logs)
                    if canal is None:
                        return
                    await canal.send(embed=embed)


    # ok
    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        if before.author.bot == False:
            if before.guild.id == self.bot.guild:
                if before.content != after.content:
                    embed = discord.Embed(color=self.bot.cor)
                    embed.set_author(name="Logs (Mensagem editada)", icon_url=before.author.avatar_url)
                    if len(before.attachments) >= 1:
                        link = before.attachments[0].url
                        url = str(link).replace("https://cdn.discordapp.com/", "https://media.discordapp.net/")
                        embed.set_image(url=url)
                    else:
                        pass
                    if len(before.content) >= 1:
                        embed.add_field(name="Mensagem (Antes)", value=f"``{before.content[:900]}``", inline=True)
                        embed.add_field(name="Mensagem (Depois)", value=f"``{after.content[:900]}``", inline=True)

                    else:
                        pass
                    embed.add_field(name="Usuário:", value=f"``{before.author}`` - (<@{before.author.id}>)",
                                        inline=True)
                    embed.add_field(name="Canal:", value=f"``{before.channel.name}`` - (<#{before.channel.id}>)",
                                        inline=True)

                    timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
                    time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))
                    embed.add_field(name="Horário", value=f"``{time}``", inline=True)
                    canal = before.guild.get_channel(self.bot.logs)
                    if canal is None:
                        return
                    await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if re.search(r'discord(?:app\\?[\s\S]com\\?\/invite|\\?[\s\S]gg|\\?[\s\S]me)\/', message.content) or re.search(r'invite\\?[\s\S]gg\\?\/[\s\S]', message.content) or "privatepage" in message.content.lower() or "naked" in message.content.lower():
            if str("💼┃Parceiro") in [r.name for r in message.author.roles if r.name != "@everyone"] and str("👑┃Owner") in [r.name for r in message.author.roles if r.name != "@everyone"]:
                print("OK")
            if message.author is message.guild.owner:    
                print("OK")
            if message.author.guild_permissions.manage_guild:
                print("OK")
                
            else:
                if not message.author.id in aviso1:
                    aviso1.append(message.author.id)
                    await message.delete()
                    embed=discord.Embed(description=f" <:unlike:760197986592096256> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **ADMINISTRADORES** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **1° Strike**.\nNo **3° Strike** você será banido.", color=self.bot.cor)
                    msg = await message.channel.send(embed=embed)
                    await asyncio.sleep(10)
                    await msg.delete()
                elif not message.author.id in aviso2:
                    aviso2.append(message.author.id)
                    await message.delete()
                    embed=discord.Embed(description=f" <:unlike:760197986592096256> **|** Olá {message.author.mention}, não é permitido **CONVITES** de outros servidores sem a permissão dos **ADMINISTRADORES** segundo as regras.\nTendo isso em mente irei avisa-lo esse é seu **2° Strike**.\nNo **3° Strike** você será banido.", color=self.bot.cor)
                    msg = await message.channel.send(embed=embed)
                    await asyncio.sleep(10)
                    await msg.delete()
                else:
                    await message.delete()
                    aviso1.remove(message.author.id)     
                    aviso2.remove(message.author.id)       
                    print('ban')
                    #await message.author.send("pow pra que divulgar mano?\n\n~~não responda essa mensagem~~")
                    await message.author.ban(reason="Divulgando.")



def setup(bot):
    bot.add_cog(logs_messages(bot))