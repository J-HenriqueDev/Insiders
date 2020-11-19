import discord
from discord.ext import commands
import random
import time
import asyncio
from pymongo import MongoClient
import pymongo
import json
from datetime import datetime, timedelta

python = ['python', 'py']
javascript = ['javascript', 'js']
kotlin = ['kotlin', 'kt']
java = ['java']
ruby = ['ruby', 'rb']
go = ['golang', 'go']

prefixos = ["c.", "!", "@", "/"]
linguagem = ["python", "javascript"]
blocklist = []


class addbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def addbot(self, ctx):
        if not str(
                ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
            await ctx.message.add_reaction(self.bot._emojis['incorreto'].replace("<", " ").replace(">", " "))
            return
        dias_servidor = (datetime.utcnow() - ctx.author.joined_at).days
        if dias_servidor < 5:
            embed = discord.Embed(colour=self.bot.cor)
            embed = discord.Embed(
                description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, você precisa ser membro desse servidor há mais de **`5`** dias para poder adicionar um bot.",
                color=self.bot.cor)
            return await ctx.send(embed=embed)
        try:
            embed = discord.Embed(
                description=f":envelope_with_arrow:  **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).",
                color=self.bot.cor)
            msg = await ctx.send(embed=embed)
            txs = f"<:newDevs:573629564627058709> **|** Então você quer adicionar o seu **BOT** em nosso servidor?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu **BOT** em nosso sistema e discord.\n\n{self.bot._emojis['bots']} **|** Insira o **ID** do bot que deseja adicionar: \n{self.bot._emojis['timer']} **|** **2 minutos**"
            embed = discord.Embed(description=txs, color=self.bot.cor)
            msg = await ctx.author.send(embed=embed)

            def pred(m):
                return m.author == ctx.author and m.guild is None

            id_bot = await self.bot.wait_for('message', check=pred, timeout=120.0)
            if id_bot.content.isnumeric() == False:
                await msg.delete()
                embed = discord.Embed(
                    description=f"{self.bot._emojis['incorreto']}  **|** Olá **{ctx.author.name}**, o argumento que você inseriu não é um **ID** e por isso o cadastramento foi cancelado.",
                    color=self.bot.cor)
                await ctx.author.send(embed=embed, delete_after=30)

            else:
                try:
                    usuario = await self.bot.fetch_user(id_bot.content)
                    if usuario.bot == True:
                        if usuario in ctx.guild.members:
                            gg = 1
                            texto = f"{self.bot._emojis['incorreto']}  **|** o **ID** que você forneceu corresponde a de um **BOT** chamado `{usuario}`, é o bot já está no servidor e por isso a cadastramento foi cancelado."
                        else:
                            gg = 2
                            texto = f"<:newDevs:573629564627058709> **|** o **ID** que você forneceu corresponde a de um **BOT** chamado `{usuario}`.\n\n{self.bot._emojis['incorreto']}  : Não é meu **BOT**\n:correto:761205727670829058> : É meu **BOT**\n\n{self.bot._emojis['timer']} **|** **2 minutos**"
                    else:
                        gg = 1
                        texto = f"{self.bot._emojis['incorreto']}  **|** o **ID** que você forneceu corresponde a de um usuário chamado `{usuario}` não é possível adiciona-lo ao servidor por que ele não e um usuário **BOT** e por isso a cadastramento foi cancelado."
                except:
                    usuario = None
                if usuario == None:
                    embed = discord.Embed(
                        description=f"{self.bot._emojis['incorreto']}  **|** Olá **{ctx.author.name}**, o **ID** que você inseriu é invalído e por isso o cadastramento foi cancelado",
                        color=self.bot.cor)
                    msg = await ctx.author.send(embed=embed, delete_after=30)
              
                else:
                    embed = discord.Embed(description=texto, color=self.bot.cor)
                    msg = await ctx.author.send(embed=embed)
                    if gg == 1:
                        await asyncio.sleep(30)
                        await msg.delete()
                    else:
                        reactions = [":errado:761205727841746954", ':like:760197986609004584']
                        user = ctx.message.author
                        if user == ctx.message.author:
                            for reaction in reactions:
                                await msg.add_reaction(reaction)

                        def check(reaction, user):
                            return user == ctx.message.author and str(reaction.emoji)

                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120.0)

                        if reaction.emoji.name == 'errado':
                            await msg.delete()
                            embed = discord.Embed(
                                description=f"{self.bot._emojis['incorreto']}  **|** o **ID** que você forneceu corresponde a de um **BOT** chamado `{usuario}`, já que **BOT** não é seu o cadastramento foi cancelado.",
                                color=self.bot.cor)
                            msg = await ctx.author.send(embed=embed)
                            await asyncio.sleep(30)
                            await msg.delete()
                        if reaction.emoji.name == 'like':
                            await msg.delete()
                            txs = f"{self.bot._emojis['nome']} **|** Diga-nos agora o prefixo do seu **BOT** (máximo 8 caracteres)\n:no_entry_sign: Prefixo banidos **|** **[c.],[!],[/][@],[#]**\n{self.bot._emojis['timer']} **|** **2 minutos**"
                            embed = discord.Embed(description=txs, color=self.bot.cor)
                            msg = await ctx.author.send(embed=embed)

                            prefix = await self.bot.wait_for('message', check=pred, timeout=120.0)
                            if len(prefix.content) + 1 >= 8:
                                await msg.delete()
                                embed = discord.Embed(
                                    description=f"{self.bot._emojis['incorreto']}  **|** Olá **{ctx.author.name}**, o prefixo que você forneceu execedeu o limite máximo **(8)** caracteres e por isso ação foi cancelada.",
                                    color=self.bot.cor)
                                msg = await ctx.author.send(embed=embed)
                                await asyncio.sleep(30)
                                await msg.delete()
                            elif str(prefix.content) in prefixos:
                                await msg.delete()
                                embed = discord.Embed(
                                    description=f"{self.bot._emojis['incorreto']}  **|** Olá **{ctx.author.name}**, o prefixo que você forneceu está banido e por isso ação foi cancelada.",
                                    color=self.bot.cor)
                                msg = await ctx.author.send(embed=embed)
                                await asyncio.sleep(30)
                                await msg.delete()
                            else:
                                await msg.delete()
                                lang = ", ".join(linguagem)
                                txs = f"<:newDevs:573629564627058709> **|** Diga-nos agora o linguagem do seu **BOT** foi criado.\n{self.bot._emojis['api']}Linguagens **|** **{lang}**\n{self.bot._emojis['timer']} **|** **2 minutos**"
                                embed = discord.Embed(description=txs, color=self.bot.cor)
                                msg = await ctx.author.send(embed=embed)
                                lang = await self.bot.wait_for('message', check=pred, timeout=120.0)
                                if not str(lang.content) in linguagem:
                                    await msg.delete()
                                    embed = discord.Embed(
                                        description=f"{self.bot._emojis['incorreto']}  **|** Olá **{ctx.author.name}**, a linguagem que você forneceu é invalida e por isso ação foi cancelada.",
                                        color=self.bot.cor)
                                    msg = await ctx.author.send(embed=embed)
                                    await asyncio.sleep(30)
                                    await msg.delete()
                                elif str(lang.content) in linguagem:
                                    await msg.delete()
                                    embed = discord.Embed(
                                        description=f"<:newDevs:573629564627058709> **|** Olá **{ctx.author.name}**, abaixo está localizado as informações do **BOT** caso tenha alguma coisa errada clique na reação ({self.bot._emojis['incorreto']} ) para recusar e deletar, caso esteja certo clique na reação (<:correto:761205727670829058>).",
                                        color=self.bot.cor)
                                    embed.set_author(name="SOLICITAÇÂO DE ADD(BOT)",
                                                     icon_url=ctx.author.avatar_url_as())
                                    embed.add_field(name=f"{self.bot._emojis['bots']} Bot",
                                                    value="``" + str(usuario) + "``", inline=True)
                                    embed.add_field(name=f"{self.bot._emojis['ip']} Id",
                                                    value="``" + str(usuario.id) + "``", inline=True)
                                    embed.add_field(name=f"{self.bot._emojis['texto']} Prefixo",
                                                    value="``" + str(prefix.content) + "``", inline=True)
                                    embed.add_field(name=f"{self.bot._emojis['api']} Linguagem",
                                                    value="``" + str(lang.content) + "``", inline=True)
                                    embed.set_thumbnail(url=usuario.avatar_url_as())
                                    embed.set_footer(text=self.bot.user.name + " © 2020",
                                                     icon_url=self.bot.user.avatar_url_as())
                                    msg = await ctx.author.send(embed=embed)
                                    reactions = [":errado:761205727841746954", ':like:760197986609004584']
                                    user = ctx.message.author
                                    if user == ctx.message.author:
                                        for reaction in reactions:
                                            await msg.add_reaction(reaction)

                                    def _check(reaction, user):
                                        return user == ctx.message.author and str(reaction.emoji)

                                    reaction, user = await self.bot.wait_for('reaction_add', check=_check,
                                                                              timeout=120.0)
                                    if reaction.emoji.name == 'errado':
                                        await msg.delete()
                                        embed = discord.Embed(
                                            description=f"{self.bot._emojis['incorreto']}  **|** A solicitação foi cancelada.. tente novamente caso queira adicionar o bot novamente ao servidor.",
                                            color=self.bot.cor)
                                        msg = await ctx.author.send(embed=embed)
                                        await asyncio.sleep(30)
                                        await msg.delete()
                                    if reaction.emoji.name == 'like':
                                        await msg.delete()
                                        embed = discord.Embed(
                                            description=f"{self.bot._emojis['correto']} **|** A solicitação foi realizada com sucesso, agora aguarde algum staff convidar seu bot para o servidor.",
                                            color=self.bot.cor)
                                        msg = await ctx.author.send(embed=embed)
                                        await asyncio.sleep(10)
                                        await msg.delete()
                                        embed = discord.Embed(color=self.bot.cor)
                                        embed.set_author(name="SOLICITAÇÂO DE ADD(BOT)",
                                                         icon_url=ctx.author.avatar_url_as())
                                        embed.add_field(name=f"{self.bot._emojis['bots']} Bot",
                                                        value="``" + str(usuario) + "``", inline=True)
                                        embed.add_field(name=f"{self.bot._emojis['ip']} Id",
                                                        value="``" + str(usuario.id) + "``", inline=True)
                                        embed.add_field(name=f"{self.bot._emojis['texto']} Prefixo",
                                                        value="``" + str(prefix.content) + "``", inline=True)
                                        embed.add_field(name=f"{self.bot._emojis['api']} Linguagem",
                                                        value="``" + str(lang.content) + "``", inline=True)
                                        embed.add_field(name=f"{self.bot._emojis['mention']} Dono",
                                                        value="``" + str(ctx.author) + "``" + " (" + str(
                                                            ctx.author.mention) + ")", inline=True)
                                        embed.add_field(name=f"{self.bot._emojis['mention']} Convite",
                                                        value=f"[Link](https://discordapp.com/api/oauth2/authorize?client_id={usuario.id}&permissions=0&scope=bot)",
                                                        inline=True)
                                        embed.set_thumbnail(url=usuario.avatar_url_as())
                                        embed.set_footer(text=self.bot.user.name + " © 2020",
                                                         icon_url=self.bot.user.avatar_url_as())
                                        # servidor
                                        server = self.bot.get_guild(self.bot.guild)
                                        # canal solicitação
                                        channel = discord.utils.get(server.channels, id=772972566402826242)
                                        msg = await channel.send(embed=embed, content="<@&571015748517101578>")
                                        reactions = [":incorreto:571040727643979782", ':like:760197986609004584']
                                        user = ctx.message.author
                                        if user == ctx.message.author:
                                            for reaction in reactions:
                                                await msg.add_reaction(reaction)

                                            def check(reaction, user):
                                                return user.id != 760196609161822219 and reaction.message.id == msg.id

                                            reaction, author = await self.bot.wait_for('reaction_add', check=check)
                                            if reaction.emoji.name == 'like':
                                                db = self.bot.db.bots
                                                bot = db.find_one({"_id": ctx.author.id})
                                                if bot is None:
                                                    print("[Bot] : inserido")
                                                    serv = {"_id": str(usuario.id), "prefixo": str(prefix.content),
                                                            "dono": str(ctx.author.id), "tags": "Não definidas",
                                                            "linguagem": str(lang.content.lower()),
                                                            "aceito por": str(author.id), "reputação": "0"}
                                                    db.insert_one(serv).inserted_id
                                                else:
                                                    print("[Bot] : Atualizado")
                                                    db.update_many({'_id': str(usuario.id)}, {
                                                        '$set': {"prefixo": str(prefix.content),
                                                                 "dono": str(ctx.author.id), "tags": "Não definidas",
                                                                 "linguagem": str(lang.content.lower()),
                                                                 "aceito por": str(author.id), "reputação": "0"}})

                                                await msg.delete()
                                                embed = discord.Embed(color=self.bot.cor)
                                                embed.set_author(name="BOT ACEITO", icon_url=ctx.author.avatar_url_as())
                                                embed.add_field(name=f"{self.bot._emojis['bots']} Bot",
                                                                value="``" + str(usuario) + "``", inline=True)
                                                embed.add_field(name=f"{self.bot._emojis['ip']} Id",
                                                                value="``" + str(usuario.id) + "``", inline=True)
                                                embed.add_field(name=f"{self.bot._emojis['texto']} Prefixo",
                                                                value="``" + str(prefix.content) + "``", inline=True)
                                                embed.add_field(name=f"{self.bot._emojis['api']} Linguagem",
                                                                value="``" + str(lang.content) + "``", inline=True)
                                                embed.add_field(name=f"{self.bot._emojis['mention']} Dono",
                                                                value="``" + str(ctx.author) + "``" + " (" + str(
                                                                    ctx.author.mention) + ")", inline=True)
                                                embed.add_field(name=f"{self.bot._emojis['mention']} Aceito por",
                                                                value=f"<@{author.id}>", inline=True)
                                                embed.set_thumbnail(url=usuario.avatar_url_as())
                                                embed.set_footer(text=self.bot.user.name + " © 2020",
                                                                 icon_url=self.bot.user.avatar_url_as())
                                                server = self.bot.get_guild(self.bot.guild)
                                                channel = discord.utils.get(server.channels, id=778654724860805141)
                                                await channel.send(embed=embed)
                                                link = f"{self.bot._emojis['correto']} **|** Convite do **BOT** ``{str(usuario)} ({str(usuario.id)})`` - https://discordapp.com/api/oauth2/authorize?client_id={usuario.id}&permissions=0&scope=bot"
                                                embed = discord.Embed(description=link, color=self.bot.cor)
                                                usuario = await self.bot.fetch_user(author.id)
                                                await usuario.send(embed=embed)

                                            if reaction.emoji.name == 'errado':
                                                try:
                                                    await msg.delete()
                                                    server = self.bot.get_guild(self.bot.guild)
                                                    channel = discord.utils.get(server.channels, id=772972566402826242)
                                                    embed = discord.Embed(
                                                        description=f"{self.bot._emojis['incorreto']}  **|** Diga-me o motivo da recusa do **BOT** ``{str(usuario)}``",
                                                        color=self.bot.cor)
                                                    msg = await channel.send(embed=embed)
                                                    recused = await self.bot.wait_for('message')
                                                    if recused.content.lower().startswith("motivo :"):
                                                        await msg.delete()
                                                        embed = discord.Embed(color=self.bot.cor)
                                                        embed.set_author(name="BOT RECUSADO",
                                                                         icon_url=ctx.author.avatar_url_as())
                                                        embed.add_field(name=f"{self.bot._emojis['bots']} Bot",
                                                                        value="``" + str(usuario) + "``", inline=True)
                                                        embed.add_field(name=f"{self.bot._emojis['ip']} Id",
                                                                        value="``" + str(usuario.id) + "``",
                                                                        inline=True)
                                                        embed.add_field(name=f"{self.bot._emojis['texto']} Prefixo",
                                                                        value="``" + str(prefix.content) + "``",
                                                                        inline=True)
                                                        embed.add_field(name=f"{self.bot._emojis['api']} Linguagem",
                                                                        value="``" + str(lang.content) + "``",
                                                                        inline=True)
                                                        embed.add_field(name=f"{self.bot._emojis['mention']} Dono",
                                                                        value="``" + str(
                                                                            ctx.author) + "``" + " (" + str(
                                                                            ctx.author.mention) + ")", inline=True)
                                                        embed.add_field(
                                                            name=f"{self.bot._emojis['mention']} Recusado por",
                                                            value=f"<@{author.id}>", inline=True)
                                                        texto = str(recused.content).replace("motivo :", "")
                                                        embed.add_field(name=f"{self.bot._emojis['incorreto']}  Motivo",
                                                                        value=f"``{texto}``", inline=True)
                                                        embed.set_thumbnail(url=usuario.avatar_url_as())
                                                        embed.set_footer(text=self.bot.user.name + " © 2020",
                                                                         icon_url=self.bot.user.avatar_url_as())
                                                        server = self.bot.get_guild(self.bot.guild)
                                                        channel = discord.utils.get(server.channels,
                                                                                    id=778654724860805141)
                                                        await channel.send(embed=embed)
                                                except Exception as e:
                                                    print(e)

        except asyncio.TimeoutError:
            await msg.delete()
            embed = discord.Embed(colour=self.bot.cor)
            embed = discord.Embed(
                description=f"{self.bot._emojis['timer']} **|** Olá **{ctx.author.name}**, passou do tempo limite e por isso a cadastramento foi cancelado.",
                color=self.bot.cor)
            msg = await ctx.author.send(embed=embed)
            await asyncio.sleep(30)
            await msg.delete()


        except discord.errors.Forbidden:
            await msg.delete()
            embed = discord.Embed(colour=self.bot.cor)
            embed = discord.Embed(
                description=f":envelope_with_arrow: **|** Olá **{ctx.author.name}**, para iniciar o processo precisamos que você libere suas mensagens privadas.",
                color=self.bot.cor)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(30)
            await msg.delete()


def setup(bot):
    print("[Bot] : Cmd (addbot) ")
    bot.add_cog(addbot(bot))
