import discord
from unidecode import unidecode
from columnar import columnar
import asyncio
from asyncio import TimeoutError as Timeout
from datetime import datetime
import pytz
import requests, json, os
import re
from discord.ext import commands
aviso1 = []
aviso2 = []
aviso3 = []



class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.users = bot.db.users
        self.bots = bot.db.bots
        self.guilds = bot.db.guilds

    
    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.author.id in self.bot.dono and ctx.command.is_on_cooldown(ctx):
            ctx.command.reset_cooldown(ctx)


    @commands.Cog.listener()
    async def on_message(self,message):
        if message.channel.id == 772972553769713735:    
            await message.add_reaction(self.bot._emojis["correto"].replace("<"," ").replace(">"," "))
            return await message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        elif message.channel.id == 775080884138147850:
            await message.add_reaction(self.bot._emojis["correto"].replace("<"," ").replace(">"," "))
            return await message.add_reaction(self.bot._emojis["incorreto"].replace("<"," ").replace(">"," "))
        elif message.channel.id == 774389441456373761:
            content = message.content
            lvl = int(content[content.find('`') + 1:content.rfind('`')])
            if lvl == 20:
                await message.mentions[0].add_roles(message.guild.get_role(772972512065749013),reason=f"{message.mentions[0]} recebeu o cargo Membro Plus.")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        if payload.channel_id != 778728930156609556 or payload.user_id == self.bot.user.id:
         return

        guild_id = payload.guild_id
        user_id = payload.user_id
        if user_id == self.bot.user.id:
            return

        message_id = payload.message_id
        emoji = payload.emoji

        db = self.bot.db.bots
        bot = db.find_one({"pendente_msg": message_id})
        if bot is None:
            return

        servidor = self.bot.get_guild(guild_id)
        canal = servidor.get_channel(channel_id)
        mensagem = await canal.fetch_message(message_id)
        user = servidor.get_member(user_id)
        logs = servidor.get_channel(778654724860805141)
        botmember = servidor.get_member(bot['_id'])
        dono = servidor.get_member(bot['donos'][0])

        
        if str(emoji) == self.bot._emojis['correto']:
            if dono is None:
                await mensagem.delete()

                bot['pendente_site'] = False
                bot['pendente_discord'] = False
                if bot['aprovado_discord']: bot['aprovado_discord'] = False
                bot['historico'].append({"ação": f"Recusado pro Discord", "autor": self.bot.user.id, "motivo": "Dono saiu do servidor", "data": datetime.now()})
                db.save(bot)

                if botmember:
                    await botmember.kick(reason=f"[{self.bot.user}] Bot auto-rejeitado || Motivo: Dono saiu do servidor")

                return await logs.send(f"{self.bot._emojis['errado']} O **bot `{bot['nome']}#{bot['discriminador']}`** de <@{bot['donos'][0]}> **foi recusado por** {servidor.me.mention}.\n```Motivo: Dono saiu do servidor.```")

            if botmember is None:
                await mensagem.remove_reaction(emoji, user)
                return await canal.send(f"{self.bot._emojis['errado']} | {user.mention}, **você não adicionou o bot `{bot['nome']}#{bot['discriminador']}` no servidor**.", delete_after=20)

            await mensagem.delete()


            

            cargo_dev = servidor.get_role(778732782968504360)
            cargo_bot_pendente = servidor.get_role(778736824503238676) #Pendenterole

            if bot['biblioteca'] == "python":
                cargo_bot = servidor.get_role(773702429279649822) #Python
            elif bot['biblioteca'] == "javascript":
                cargo_bot = servidor.get_role(773702428692316160) # Javascript


            if cargo_dev not in dono.roles: await dono.add_roles(cargo_dev, reason=f"[{user}] Bot aprovado no Discord")
            if cargo_bot_pendente in botmember.roles: await botmember.remove_roles(cargo_bot_pendente, reason=f"[{user}] Bot aprovado no Discord")
            if cargo_bot not in botmember.roles: await botmember.add_roles(cargo_bot, reason=f"[{user}] Bot aprovado no Discord")

            
            bot['pendente_discord'] = False
            bot['aprovado_discord'] = True
            bot['data_aprovado_discord'] = datetime.now()
            bot['aprovado_por_discord'] = user_id
            
            bot['histórico'].insert(0,
                {
                    "ação": "Aprovado no " + "Servidor",
                    "data": datetime.now(),
                    "autor": user_id,
                    "motivo": None
                }
            )

            db.save(bot)

            await logs.send(f"{self.bot._emojis['correto']} O BOT **`{botmember}`** enviado por {dono.mention} foi **`ACEITO`** por **{user.name}**.")
            try:
                await dono.send(f"{self.bot._emojis['correto']} | Seu bot **`{botmember}`** foi **`ACEITO`** no **Insider's** por **{user}**.\nAgora você pode editar as informações dele usando o comando `c.editbot`.")
            except:
                pass
        elif str(emoji) == self.bot._emojis['errado']:
            try:
                q = await user.send(f"{self.bot._emojis['api']} | **Digite o motivo pelo qual você está recusando o bot `{botmember}`**. **`(5 minutos)`**")
            except:
                await mensagem.remove_reaction(emoji, user)
                return await canal.send(f"{self.bot._emojis['errado']} | {user.mention}, **o envio de Mensagem Direta está desativado na sua conta\nAtive para poder continuar com a rejeição desse bot**.", delete_after=25)

            def check(m):
                return m.channel.id == q.channel.id and m.author.id == user_id

            try:
                motivo = await self.bot.wait_for("message", check=check, timeout=300)
            except Timeout:
                await mensagem.remove_reaction(emoji, user)
                return await user.send(f"{self.bot._emojis['errado']} | **Você demorou demais para fornecer um motivo**!")

            await mensagem.delete()

            bot['pendente_discord'] = False
            bot['histórico'].insert(0,
                {
                    "ação": "Recusado pro " + "Insiders",
                    "data": datetime.now(),
                    "autor": user_id,
                    "motivo": motivo.content
                }
            )

            db.save(bot)

            if botmember and not bot['aprovado_discord']:
                await botmember.kick(reason=f"[{user}] Bot rejeitado pro servidor || Motivo: {motivo.content}")
            
            await logs.send(f"{self.bot._emojis['errado']} **`{bot['nome']}#{bot['discriminador']}`** enviado por <@{bot['donos'][0]}> foi **recusado** por **{user.name}**.\n```Motivo: {motivo.content}```")
            await user.send(f"{self.bot._emojis['correto']} | **Você recusou o bot `{bot['nome']}#{bot['discriminador']}`**")
            if dono:
                try:
                    await dono.send(f"{self.bot._emojis['errado']} | **Seu bot `{bot['nome']}#{bot['discriminador']}` foi recusado por {user}**.\n```Motivo: {motivo.content}```")
                except:
                    pass


def setup(bot):
    bot.add_cog(events(bot))
