import discord
from datetime import datetime
import pytz
from discord.ext import commands
import aiohttp
from io import BytesIO
import aiohttp
import requests

class logs_roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()    
    
    #ok
    @commands.Cog.listener()
    async def on_guild_role_create(self,role):
        if role.guild.id == self.bot.guild:
            server = role.guild
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.role_create:
                    user = x.user
            s = discord.Embed(description="O cargo **{}** foi criado por **{}**".format(role.name, user),
                            colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel(self.bot.logsroles)
            if canal is None:
                return
            await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_role_delete(self,role):
        if role.guild.id == self.bot.guild:
            server = role.guild
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.role_delete:
                    user = x.user
                s = discord.Embed(description="o cargo **{}** foi deletado por  **{}**".format(role.name, user),
                            colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                canal = self.bot.get_channel(self.bot.logsroles)
                if canal is None:
                    return
                await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_role_update(self,before, after):
        if before.guild.id == self.bot.guild:
            server = before.guild
            for x in await server.audit_logs(limit=1, action=discord.AuditLogAction.role_update).flatten():
                user = x.user
            if before.name != after.name:
                s = discord.Embed(description="o  cargo **{}** foi renomeado por **{}**".format(after.name, user),
                                colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                s.add_field(name="Antes", value=before)
                s.add_field(name="Depois", value=after)
                s.set_author(name=server, icon_url=server.icon_url)
                canal = self.bot.get_channel(self.bot.logsroles)
                if canal is None:
                    return
                await canal.send(embed=s)
            if before.permissions != after.permissions:
                permissionadd = list(map(lambda x: "+ " + x[0].replace("_", " ").title(), filter(
                    lambda x: x[0] in map(lambda x: x[0], filter(lambda x: x[1] == True, after.permissions)),
                    filter(lambda x: x[1] == False, before.permissions))))
                permissionremove = list(map(lambda x: "- " + x[0].replace("_", " ").title(), filter(
                    lambda x: x[0] in map(lambda x: x[0], filter(lambda x: x[1] == False, after.permissions)),
                    filter(lambda x: x[1] == True, before.permissions))))
                s = discord.Embed(
                    description="O  cargo **{}** teve suas permissões alteradas por **{}**\n```diff\n{}\n{}```".format(
                        before.name, user, "\n".join(permissionadd), "\n".join(permissionremove)), colour=0xe6842b,
                    timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                canal = self.bot.get_channel(self.bot.logsroles)
                if canal is None:
                    return
                await canal.send(embed=s)


def setup(bot):
    bot.add_cog(logs_roles(bot))