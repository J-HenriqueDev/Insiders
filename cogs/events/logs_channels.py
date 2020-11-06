import discord
from datetime import datetime
import pytz
from discord.ext import commands
import aiohttp
from io import BytesIO
import aiohttp
import requests    
    

class logs_channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()       
    
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel):
        if channel.guild.id == self.bot.guild:
            server = channel.guild
            deletedby = "Inexistente"
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.channel_delete:
                    deletedby = x.user
            if isinstance(channel, discord.TextChannel):
                s = discord.Embed(description="o canal de texto **{}** foi deletado por **{}**.".format(channel.name, deletedby), colour=0xf84b50,
                                timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
            elif isinstance(channel, discord.VoiceChannel):
                s = discord.Embed(description="O canal de voz **{}** foi deletado por  **{}**.".format(channel.name, deletedby),
                                colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
            else:
                s = discord.Embed(description="A categoria **{}** foi deletada por **{}**.".format(channel.name, deletedby),
                                colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel(self.bot.logschannels)
            if canal is None:
                return
            await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        server = channel.guild
        createdby = "Indefinido"
        if channel.guild.id == self.bot.guild:
            for x in await server.audit_logs(limit=5).flatten():
                if x.action == discord.AuditLogAction.channel_create:
                    createdby = x.user
            if isinstance(channel, discord.TextChannel):
                s = discord.Embed(description="o canal <#{}> foi criado por  **{}**.".format(channel.id, createdby),
                                colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
            elif isinstance(channel, discord.VoiceChannel):
                s = discord.Embed(description="o canal de voz **{}** foi criado  por **{}**.".format(channel, createdby),
                                colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
            else:
                s = discord.Embed(
                    description="A categoria **{}** acaba de ser criada por **{}**.".format(channel, createdby),
                    colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel(self.bot.logschannels)
            if canal is None:
                return
            await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_update(self,before, after):
        server = before.guild
        editedby = "Indefinido"
        if before.guild.id == self.bot.guild:
            if isinstance(before, discord.TextChannel):
                if before.name != after.name:
                    for x in await server.audit_logs(limit=1).flatten():
                        if x.action == discord.AuditLogAction.channel_update:
                            editedby = x.user
                    s = discord.Embed(description="o canal <#{}> foi renomeado por **{}**".format(after.id, editedby),
                                    colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                    s.set_author(name=server, icon_url=server.icon_url)
                    s.add_field(name="Antes:", value="`{}`".format(before))
                    s.add_field(name="Depois:", value="`{}`".format(after))
                if before.slowmode_delay != after.slowmode_delay:
                    for x in await server.audit_logs(limit=1).flatten():
                        if x.action == discord.AuditLogAction.channel_update:
                            editedby = x.user
                    s = discord.Embed(
                        description="O slow mode de  {} foi editado por **{}**".format(after.mention, editedby),
                        colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                    s.set_author(name=server, icon_url=server.icon_url)
                    s.add_field(name="Antes", value="{} {}".format(before.slowmode_delay,
                                                                "second" if before.slowmode_delay == 1 else "seconds") if before.slowmode_delay != 0 else "Desativado")
                    s.add_field(name="Desativado", value="{} {}".format(after.slowmode_delay,
                                                                        "second" if after.slowmode_delay == 1 else "seconds") if after.slowmode_delay != 0 else "Desativado")
            if isinstance(before, discord.VoiceChannel):
                if before.name != after.name:
                    for x in await server.audit_logs(limit=1).flatten():
                        if x.action == discord.AuditLogAction.channel_update:
                            editedby = x.user
                    s = discord.Embed(description="O canal de voz **{}** foi renomeado por **{}**.".format(after, editedby),
                                    colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                    s.set_author(name=server, icon_url=server.icon_url)
                    s.add_field(name="Antes", value="`{}`".format(before))
                    s.add_field(name="Depois", value="`{}`".format(after))
            else:
                if before.name != after.name:
                    for x in await server.audit_logs(limit=1).flatten():
                        if x.action == discord.AuditLogAction.channel_update:
                            editedby = x.user
                    s = discord.Embed(description="A categoria  **{}** foi renomeada por **{}**.".format(after, editedby),
                                    colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                    s.set_author(name=server, icon_url=server.icon_url)
                    s.add_field(name="Antes", value="`{}`".format(before))
                    s.add_field(name="Depois", value="`{}`".format(after))
                    canal = self.bot.get_channel(self.bot.logschannels)
                    if canal is None:
                        return
                    await canal.send(embed=s)       


def setup(bot):
    bot.add_cog(logs_channels(bot))