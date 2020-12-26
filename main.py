import discord
import os
import json
from config import secrets
from database import adicionar_user
from discord.ext import commands
from cogs.utils.role import emojis
from cogs.utils.role import cargos
from pymongo import MongoClient
from cogs.utils.Utils import random_color

intents = discord.Intents.default()
intents.members = True
intents.presences = True


class main(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(secrets.PREFIXO),
                        case_insensitive=True,
                        pm_help=None,
                        shard_count=1,
                        shard_ids=[0],
                        #activity=discord.Activity(type=discord.ActivityType.watching, name='instagram.com/gostosazapi', status=discord.Status.do_not_disturb),
                        intents=intents)
        
        self.remove_command('help')
        self.cargo = cargos
        self._emojis = emojis
        self.dono = secrets.DONO
        self.adms = secrets.ADMS
        self.database = secrets.DATAB
        self.errado = "<:errado:761205727841746954>"
        self.correto = "<:correto:761205727670829058>"
        
        
        self.adicionar_user = adicionar_user
        self.logschannels = 772494035063275520
        self.logsroles = 772494035063275520
        self.logsusers = 772494035063275520
        self.logscargos = 772494035063275520
        self.sugestao = 791131875988733963

        self.canais = ["791131878090080257"]
        self.logs = 772494035063275520
        
        self.bans = 772494035063275520
        self.guild = 635624989193666591
        self.regras = 791131860520534036

        
        
        self.token = 'blz,talvez outro dia.'
        self.color = 0x36393F
        self.cor = random_color()

        print("( * ) | Tentando se conectar ao banco de dados...")
        try:
            mongo = MongoClient(self.database)
        except Exception as e:
            print(f"\n<---------------->\n( ! ) | Erro na tentativa de conexão com o banco de dados!\n<----------->\n{e}\n<---------------->\n")
            exit()
        self.db = mongo['insiders']

        print(f"( > ) | Conectado ao banco de dados!")
        

    async def on_message(self, message):
        if message.guild is None:
          return 

        if message.author.bot or not message.channel.permissions_for(message.guild.me).send_messages:
          return
       
        ctx = await self.get_context(message)    
        try:
            await self.invoke(ctx)
        except Exception as e:
            self.dispatch('command_error', ctx, e)

    async def on_ready(self):
        print('---------- Bot Online -----------')
        print(f"[OK] - {self.user.name} ({self.user.id}) - (Status - Online)")
        print(f"Modulos ativos: {len(bot.cogs)}")
        print(f'Usuários: {len(self.users) - len([c for c in self.users if c.bot])}')
        print(f'Bots: {len([c for c in self.users if c.bot])}')
        print(f'Guilds: {len(self.guilds)}')
        print('---------------------------------')
        
    def embed(self, ctx, invisible=False):
        color = self.cor if invisible else self.color
        emb = discord.Embed(color=color)
        emb.set_footer(text=self.user.name+" © 2020", icon_url=self.user.avatar_url_as())
        emb.timestamp = ctx.message.created_at
        return emb

    def erEmbed(self, ctx, error='Erro!'):
        emb = discord.Embed(title=f':x: | {error}', color=0xDD2E44)
        emb.set_footer(text=self.user.name+" © 2020", icon_url=self.user.avatar_url_as())
        emb.timestamp = ctx.message.created_at
        return emb


bot = main()

if __name__ == '__main__':
    for filename in [c for c in os.listdir("cogs/cmds") if c.endswith(".py")]: 
            name = filename[:-3]
            try:    
                bot.load_extension(f'cogs.cmds.{name}') 
                #print(f'MÓDULO [{filename}] CARREGADO')
            except commands.NoEntryPointError:
                print(f'⚠ - Módulo {filename[:-3]} ignorado! "def setup" não encontrado!!')
            except Exception as e:
                print(f'⚠ - Módulo {filename[:-3]} deu erro na hora de carregar!\nerro: {e}')

    for filename in [c for c in os.listdir("cogs/events") if c.endswith(".py")]:  
            name = filename[:-3]  
            try:                # 
                bot.load_extension(f'cogs.events.{filename[:-3]}') 
                #print(f'EVENTO [{filename}] CARREGADO')
            except commands.NoEntryPointError:
                pass  
            except:
                print(f'⚠ - Módulo {filename[:-3]} não foi carregado!')
    try:

        bot.run(secrets.TOKEN, reconnect=True, bot=True)
    except KeyboardInterrupt: 
        pass
