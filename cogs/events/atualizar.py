from database import adicionar_user
from datetime import datetime
from asyncio import sleep
import discord
from discord.ext import commands

class Atualizar(commands.Cog):
    def __init__(self, lab):
        self.lab = lab
        self.users = lab.db.users
        self.bots = lab.db.bots
        self.guilds = lab.db.guilds
    
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
                return adicionar_user(db, after)

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
            
        
        
        
        elif db == self.bots and after.status != before.status:
            user['status'] = str(after.status).replace("dnd", "ocupado").replace("idle", "ausente")
            atualizado = True

        if atualizado:
            db.save(user)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.guild.id != self.lab.guild:
            return


        if not member.bot:
            return
        
        bot = self.bots.find_one({"_id": member.id})
        if bot is None:
            return
        
        user = self.users.find_one({"_id": member.id})
        if user is None:
            return adicionar_user(self.users, member)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.guild.id != self.lab.guild:
            return


        
        if member.bot:
            bot = self.bots.find_one({"_id": member.id})
            if bot is None:
                return
            
            if 'Recusado' in bot['histórico'][0]['ação']:
                return 

            bot['pendente_discord'] = False
            bot['pendente_site'] = False
            bot['aprovado_site'] = False
            bot['aprovado_discord'] = False
            bot['suspenso'] = True
            bot['suspenso_info'] = {
                "autor": self.lab.user.id,
                "data": datetime.now(),
                "motivo": "Bot saiu do servidor"
            }
            
            return self.bots.save(bot)
        
        user = self.users.find_one({"_id": member.id})
        if user is None:
            return adicionar_user(self.users, member)

        bots = self.bots.find({"donos": [member.id]})
        if bots:
            for b in bots:
                bo = member.guild.get_member(b['_id']) 
                if bo:
                    b['histórico'].insert(
                        0, {
                            "ação": "Suspenso",
                            "autor": self.lab.user.id,
                            "motivo": "Dono saiu do servidor",
                            "data": datetime.now()
                        }
                    )
                    self.bots.save(b)
                    await bo.kick(reason=f"[{self.lab.user}] Auto-Kick || Motivo: Dono saiu do servidor")

        if user['devmod']: user['devmod'] = False
        if user['supervisor']: user['supervisor'] = False
        if user['devhelper']: user['devhelper'] = False
        if user['cooperador']: user['cooperador'] = False
        self.users.save(user)


        
def setup(lab):
    lab.add_cog(Atualizar(lab))