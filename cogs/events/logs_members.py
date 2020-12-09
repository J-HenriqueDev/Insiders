import discord
import pytz
import asyncio
from datetime import datetime
from discord.ext import commands



def difference_between_lists(list1: list, list2: list) -> list:
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))


class logs_members(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        if member.guild.id == self.bot.guild:
            server = member.guild
            if after.channel != None and before.channel != None:
                s = discord.Embed(description="**{}** acabou de mudar os canais de voz".format(member.name),
                                colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name='{}'.format(member),icon_url = "{}".format(member.avatar_url))
                s.add_field(name="Antes", value="`{}`".format(before.channel), inline=False)
                s.add_field(name="Depois", value="`{}`".format(after.channel))
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)
            if after.channel == None:
                s = discord.Embed(
                    description="**{}** acabou de sair do canal de voz `{}`".format(member.name, before.channel),
                    colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=member, icon_url=member.avatar_url)
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)
            if before.channel == None:
                s = discord.Embed(
                    description="**{}** acabou de entrar no canal de voz `{}`".format(member.name, after.channel),
                    colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=member, icon_url=member.avatar_url)
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)
            if before.mute and not after.mute:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.member_update:
                        action = x.user
                s = discord.Embed(description="**{}** foi desmutado por **{}**".format(member.name, action),
                                colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=member, icon_url=member.avatar_url)
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)
            if not before.mute and after.mute:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.member_update:
                        action = x.user
                s = discord.Embed(description="**{}** foi mutado por **{}**".format(member.name, action), colour=0xf84b50,
                                timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=member, icon_url=member.avatar_url)
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)
            if before.deaf and not after.deaf:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.member_update:
                        action = x.user
                s = discord.Embed(description="**{}** desativado de ouvir por **{}**".format(member.name, action),
                                colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=member, icon_url=member.avatar_url)
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)
            if not before.deaf and after.deaf:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.member_update:
                        action = x.user
                s = discord.Embed(description="**{}** foi ensurdecido por **{}**".format(member.name, action),
                                colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=member, icon_url=member.avatar_url)
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)


    #ok
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id == self.bot.guild:
            if after.bot: return
            if not self.bot.is_ready(): return
            if before.nick != after.nick:
                if not before.nick:
                    before.nick = after.name
                if not after.nick:
                    after.nick = after.name
                s = discord.Embed(description="o usuário **{}** mudou de apelido.".format(after.name),
                                colour=self.bot.cor, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=after, icon_url=after.avatar_url)
                s.add_field(name="Antes:", value=f"``{before.nick}``", inline=False)
                s.add_field(name="Depois:", value=f"``{after.nick}``")
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                try:
                    await canal.send(embed=s)
                except Exception as e:
                    print(f"Erro ao enviar log : {e}")

            if before.name != after.name:
                s = discord.Embed(description="o usuário **{}** mudou seu nome de usuário.".format(before.name),
                                colour=self.bot.cor, timestamp=datetime.now())
                s.set_author(name=after, icon_url=after.avatar_url)
                s.add_field(name="Antes:", value=f"``{before}``", inline=False)
                s.add_field(name="Depois:", value=f"``{after}``")
                canal = self.bot.get_channel(self.bot.logsusers)
                if canal is None:
                    return
                await canal.send(embed=s)
            if before.roles != after.roles:
                    cargos = [f'<@&{c.id}>' for c in difference_between_lists (before.roles, after.roles)]
                    if len(before.roles) < len(after.roles):
                        desc = None
                        if len(cargos) == 1:
                            desc = f'Novo cargo: {cargos[0]}'
                        elif len(cargos) > 1:
                            desc = 'Novos cargo: ' + ', '.join(cargos)
                    else:  
                        desc = None
                        if len(cargos) == 1:
                            desc = f'Cargo removido: ``{cargos[0]}``'
                        elif len(cargos) > 1:
                            desc = 'Cargos removidos: ' + ', '.join(cargos)
                    embed = discord.Embed(title='Cargos alterados',
                                            colour=self.bot.cor,
                                            description=f'O(A) ``{after.name}`` sofreu alteração nos cargos!\n'
                                                        f'User: ``{after.mention}``\n'
                                                        f'ID: ``{after.id}``\n'
                                                        f'{desc}',
                                            timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=str(after.avatar_url))
                    channel_cargos = self.bot.get_channel(self.bot.logscargos)
                    await channel_cargos.send(embed=embed)
            if (before.premium_since is None) and (after.premium_since is not None):
                    embed = discord.Embed(title='Novo booster',
                                            colour=self.bot.cor,
                                            description=f'**{after.name}** começou a dar boost!\n'
                                                        f'User: {after.mention}\n'
                                                        f'Id: ``{after.id}``\n',
                                            timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=str(after.avatar_url))
                    logsboost = self.bot.get_channel(772972566402826242)
                    await logsboost.send(embed=embed)

    #ok
    @commands.Cog.listener()
    async def on_member_ban(self , guild, member):
        if guild.id == self.bot.guild:
            await asyncio.sleep(3)
            async for entry in guild.audit_logs(action=discord.AuditLogAction.ban ,limit=1):
                moderator = entry.user
                if moderator is None:
                    moderator = "NADA"
                reason = entry.reason
                if reason is None:
                    reason = "Não informada."
            embed = discord.Embed(color=self.bot.cor,timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            embed.set_author(name=f"MEMBRO BANIDO", icon_url=guild.icon_url)
            embed.add_field(name=f"Usuário:", value=f"`{member.name}`")
            embed.add_field(name=f"Autor:",value=f"`{moderator}`")
            embed.add_field(name="Motivo:",value=f"``{reason}``")
            embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
            embed.set_thumbnail(url=member.avatar_url_as(format='png'))
            logs_bans = guild.get_channel(self.bot.bans)
            await logs_bans.send(embed=embed, content="@here")
    #ok
    @commands.Cog.listener()
    async def on_member_unban(self , guild, member):
        if guild.id == self.bot.guild:
            await asyncio.sleep(3)
            moderator = 'Não encontrado.'
            async for entry in guild.audit_logs(action=discord.AuditLogAction.unban ,limit=1):
                moderator = entry.user
            embed = discord.Embed(color=self.bot.cor,timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            embed.set_author(name=f"MEMBRO DESBANIDO", icon_url=guild.icon_url)
            embed.add_field(name=f"Usuário:", value=f"`{member.name}`")
            embed.add_field(name=f"Autor:",value=f"`{moderator}`")
            embed.set_footer(text=self.bot.user.name+" © 2020", icon_url=self.bot.user.avatar_url_as())
            embed.set_thumbnail(url=member.avatar_url_as(format='png'))
            logs_bans = guild.get_channel(self.bot.bans)
            await logs_bans.send(embed=embed, content="@here")


   


def setup(bot):
    bot.add_cog(logs_members(bot))