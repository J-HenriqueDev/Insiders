import discord
import pytz
from datetime import datetime
from discord.ext import commands


class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
          comma = error.args[0].split('"')[1]
          quantidade = len(comma)
          if quantidade > 13:
            return await ctx.send('não tente me bugar poha')
          embed = discord.Embed(title=f"{self.bot._emojis['incorreto']} | Comando não encontrado", color=self.bot.cor, description=f"O comando `{comma}` não existe.")
          await ctx.send(embed=embed)

        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument, commands.MissingRequiredArgument)):
          uso = ctx.command.usage if ctx.command.usage else "Não especificado."
          await ctx.send(f"{self.bot._emojis['incorreto']} **Oops**, **{ctx.author.name}**! Parece que você usou o comando **`{ctx.command.name}`** de forma errada!\nUso correto: **`{uso}`**")
        
        elif isinstance(error, commands.BotMissingPermissions):
            perms = '\n'.join([f"   {self.bot._emojis['incorreto']} **`{perm.upper()}`**" for perm in error.missing_perms])
            await ctx.send(f"**{ctx.author.name}**, eu preciso das seguintes permissões para poder executar o comando **`{ctx.invoked_with}`** nesse servidor:\n\n{perms}")
        
        elif isinstance(error, commands.MissingPermissions):
            perms = '\n'.join([f"   {self.bot._emojis['incorreto']} **`{perm.upper()}`**" for perm in error.missing_perms])
            await ctx.send(f"**{ctx.author.name}**, você precisa das seguintes permissões para poder usar o comando **`{ctx.invoked_with}`** nesse servidor:\n\n{perms}")

        elif isinstance(error, commands.CommandOnCooldown):
          s = divmod(error.retry_after, 60)
          return await ctx.send(f"**{ctx.author.name}**, aguarde **`{int(s)}`** segundo(s) para poder usar o comando **`{ctx.invoked_with}`** novamente.")
        
        elif isinstance(error, commands.CheckFailure):
            pass

        elif isinstance(error, commands.DisabledCommand):
          await ctx.send(f"{self.bot._emojis['incorreto']} | **{ctx.author.name}**, o comando **`{ctx.invoked_with}`** está temporariamente desativado.")
        
        elif isinstance(error, commands.MissingRequiredArgument):
          await ctx.send('faltando argumentos')


        elif isinstance(error, commands.CommandError):
            logs = self.bot.get_channel(773515801793134602)
            em = discord.Embed(
                colour=self.bot.cor,
                description=f"```py\n{error}```",
                timestamp=ctx.message.created_at
            ).set_author(
                name=str(ctx.author),
                icon_url=ctx.author.avatar_url
            )
            await logs.send(embed=em, content="**Usuário: `{0}` `{0.id}`** | **Comando:** `{1.name}`\n**Servidor: `{2.name}`** `{2.id}` | **Canal: `#{3.name}`** `{3.id}`\n**Mensagem:** `{4.content}`".format(ctx.author, ctx.command, ctx.guild, ctx.channel, ctx.message))
        
        else:
            pass


def setup(bot):
    bot.add_cog(errors(bot))