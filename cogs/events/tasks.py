from discord.ext import commands, tasks
from cogs.utils.Utils import avatars
from random import choice
from datetime import datetime
import pytz



class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._change_icon.start()


    @tasks.loop(minutes=1)
    async def _change_icon(self):
        horas = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%H:%M")
        print("executado as :", horas)
        if horas == "13:01":
            print("cheguei no horario definido:", horas)
            try:
                print("tentando trocar icon", horas)
                info = choice(avatars)
                avatar = open(info['path'], 'rb').read()
                await self.bot.get_guild(self.bot.guild).edit(icon=avatar)
                print("Icone do servidor alterado")
            except Exception as e:
                print("Erro encontado:\n", e)



def setup(bot):
    bot.add_cog(Tasks(bot))