from datetime import datetime
from asyncio import sleep
import pytz
from datetime import datetime
import discord
from discord.ext import commands

class Atualizar(commands.Cog):
    def __init__(self, lab):
        self.lab = lab
        self.users = lab.db.users

    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot:
            return
        else:
            db = self.lab.db.users
            user = db.find_one({"_id": after.id})
            if user is None:
                return self.lab.adicionar_user(db, after)
        atualizado = True

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

        if atualizado:
            db.save(user)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.guild.id != self.lab.guild:
            return
        cat = member.created_at.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone('America/Sao_Paulo')).strftime('`%d/%m/%Y`')
        dias = (datetime.utcnow() - member.created_at).days
        embed = discord.Embed(color=self.lab.cor, description=f'**{member.mention}(`{member.id}`) entrou no servidor, com a conta criada em {cat}({dias} dias).**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=self.lab.user.name+" © 2020", icon_url=self.lab.user.avatar_url_as())
        await self.lab.get_channel(773567922526355496).send(embed=embed)

        if member.bot:
            return
        else:
            user = self.users.find_one({"_id": member.id})
            if user is None:
                return self.lab.adicionar_user(self.users, member)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.guild.id != self.lab.guild:
            return

        user = self.users.find_one({"_id": member.id})
        if user is None:
            return self.lab.adicionar_user(self.users, member)

        
def setup(lab):
    lab.add_cog(Atualizar(lab))