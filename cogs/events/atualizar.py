from datetime import datetime
from asyncio import sleep
import pytz
from datetime import datetime
import discord
from discord.ext import commands

class Atualizar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bots = bot.db.bots
        self.users = bot.db.users

    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot:
            db = self.bots
            user = db.find_one({"_id": after.id})
            if user is None:
                return
        else:
            db = self.users
            user = db.find_one({"_id": after.id})
            if user is None:
                return self.bot.adicionar_user(db, after)

        atualizado = False

        if str(before) != str(after):
            user['nome'] = after.name
            user['discriminador'] = after.discriminator
            if db == self.users:
                user['histórico_nomes'].insert(
                    0, {
                        "nome": str(after),
                        "data": datetime.now()
                    }
                )
            else:
                user['histórico'].insert(
                    0, {
                        "ação": "Nome alterado",
                        "autor": after.id,
                        "motivo": None,
                        "data": datetime.now()
                    }
                )
            atualizado = True

        elif after.avatar != before.avatar:
            user['avatar'] = after.avatar
            atualizado = True

        elif db == self.users and after.roles != before.roles and after.guild.id == self.bot.guild:
            administrador = after.guild.get_role(772972507388444703) #adm
            moderador = after.guild.get_role(772972508344877057) #mod
            helper = after.guild.get_role(773517066803478589) #helper

            if helper in after.roles and helper not in before.roles:  # ganhou helper
                user['helper'] = True
                atualizado = True
            elif moderador in after.roles and moderador not in before.roles:  # ganhou sup
                user['moderador'] = True
                atualizado = True
            elif administrador in after.roles and administrador not in before.roles:  # ganhou administrador
                user['administrador'] = True
                atualizado = True

            elif helper not in after.roles and helper in before.roles:  # perdeu helper
                user['helper'] = False
                atualizado = True
            elif moderador not in after.roles and moderador in before.roles:  # perdeu sup
                user['moderador'] = False
                atualizado = True
            elif administrador not in after.roles and administrador in before.roles:  # perdeu administrador
                user['administrador'] = False
                atualizado = True


        if atualizado:
            db.save(user)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            bot = self.bots.find_one({"_id": member.id})
            if bot is None:
                return await member.add_roles(discord.Object(772972514418753586))

            if bot['pendente_discord']:
                cargo_bot_pendente = member.guild.get_role(778736824503238676)
                await member.add_roles(cargo_bot_pendente, reason=f'[{self.bot.user}] Bot Pendente para aprovação')

            cat = member.created_at.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone('America/Sao_Paulo')).strftime(
                '`%d/%m/%Y`')
            dias = (datetime.utcnow() - member.created_at).days
            embed = discord.Embed(color=self.bot.cor,
                                  description=f'**{member.mention}(`{member.id}`) entrou no servidor, {cat}({dias} dias).**')
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
            await self.bot.get_channel(773567922526355496).send(embed=embed)

        else:
            user = self.users.find_one({"_id": member.id})
            if user is None:
                return self.bot.adicionar_user(self.users, member)




    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != self.bot.guild:
            return

        if member.bot:
            bot = self.bots.find_one({"_id": member.id})
            if bot is None:
                return

            if 'Recusado' in bot['histórico'][0]['ação']:
                return

            bot['pendente_discord'] = False
            bot['aprovado_discord'] = False
            bot['suspenso'] = True
            bot['suspenso_info'] = {
                "autor": self.bot.user.id,
                "data": datetime.now(),
                "motivo": "Bot saiu do servidor"
            }
            return self.bots.save(bot)

        user = self.users.find_one({"_id": member.id})
        if user is None:
            return self.bot.adicionar_user(self.users, member)

        bots = self.bots.find({"donos": [member.id]})
        if bots:
            for b in bots:
                bo = member.guild.get_member(b['_id'])
                if bo:
                    b['histórico'].insert(
                        0, {
                            "ação": "Suspenso",
                            "autor": self.bot.user.id,
                            "motivo": "Dono saiu do servidor",
                            "data": datetime.now()
                        }
                    )
                    self.bots.save(b)
                    await bo.kick(reason=f"[{self.bot.user}] Auto-Kick || Motivo: Dono saiu do servidor")

        if user['administrador']: user['administrador'] = False
        if user['moderador']: user['moderador'] = False
        if user['helper']: user['helper'] = False
        self.users.save(user)


def setup(bot):
    bot.add_cog(Atualizar(bot))