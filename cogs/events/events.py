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


def setup(bot):
    bot.add_cog(events(bot))
