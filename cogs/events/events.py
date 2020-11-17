import discord
from unidecode import unidecode
from columnar import columnar
import asyncio
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
                await message.mentions[0].add_roles(message.guild.get_role(772972512065749013),reason=f"{message.mentions[0]} chegou ao level 20 e recebeu o cargo Membro Plus,")

            print("level:", lvl)



def setup(bot):
    bot.add_cog(events(bot))
