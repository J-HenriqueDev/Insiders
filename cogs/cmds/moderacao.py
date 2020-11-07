import discord
from datetime import datetime, timedelta
import pytz, typing
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord.ext import commands
from asyncio import sleep
import requests


mutedRole = '</Mutado>' # Put here the name of muted members role
memberRole = '👤┃Membro' # Put here the name of members default role

class moderacao(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    @commands.command(no_pm=True,hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cores(self, ctx):
            color_roles = [
                {
                    "name": "──── Colors ────"
                },
                {
                    "name": "Black",
                    "color": discord.Color(0)
                },
                {
                    "name": "Blue",
                    "color": discord.Color(0x4363D8)
                },
                {
                    "name": "Brown",
                    "color": discord.Color(0x9A6324)
                },
                {
                    "name": "Cyan",
                    "color": discord.Color(0x42D4F4)
                },
                {
                    "name": "Green",
                    "color": discord.Color(0x3CB44B)
                },
                {
                    "name": "Grey",
                    "color": discord.Color(0xA9A994)
                },
                {
                    "name": "Lavender",
                    "color": discord.Color(0xE6BEFF)
                },
                {
                    "name": "Lime",
                    "color": discord.Color(0xBFE743)
                },
                {
                    "name": "Magenta",
                    "color": discord.Color(0xF032E6)
                },
                {
                    "name": "Maroon",
                    "color": discord.Color(0x800014)
                },
                {
                    "name": "Mint",
                    "color": discord.Color(0xAAFFC3)
                },
                {
                    "name": "Navy",
                    "color": discord.Color(0x000075)
                },
                {
                    "name": "Olive",
                    "color": discord.Color(0x808012)
                },
                {
                    "name": "Orange",
                    "color": discord.Color(0xF58231)
                },
                {
                    "name": "Pink",
                    "color": discord.Color(0xF4BCBE)
                },
                {
                    "name": "Purple",
                    "color": discord.Color(0x911EB4)
                },
                {
                    "name": "Red",
                    "color": discord.Color(0xE62345)
                },
                {
                    "name": "Teal",
                    "color": discord.Color(0x469990)
                },
                {
                    "name": "White",
                    "color": discord.Color(0xFFFFFF)
                },
                {
                    "name": "Yellow",
                    "color": discord.Color(0xFFE119)
                },
            ]

            for kwargs in color_roles:
                await ctx.guild.create_role(**kwargs, reason="hehe")

    @commands.command(usage='{}ban [membro] (motivo)', description='Bane um membro que está no servidor (ou não). [Banir Membros]', aliases=['banir'])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, membro:typing.Union[discord.Member, str], *, reason="Não informado."):
        if type(membro) == discord.Member:
            erro = self.bot.erEmbed(ctx, 'Sem permissão.')

            if membro == ctx.author:
                erro.description = 'Você não pode se banir, bobinho!'

            if membro == ctx.me:
                erro.description = 'Não posso me banir...'

            if membro.top_role.position >= ctx.author.top_role.position or membro == ctx.guild.owner:
                erro.description = f'Você não tem permissão para banir **{membro.name}** (seu cargo é menor ou igual que o dele)'

            if membro.top_role.position >= ctx.me.top_role.position:
                erro.description = f'Eu não tenho permissão para banir **{membro.name}** (cargo dele é maior ou igual que o meu)'

            if type(erro.description) != discord.Embed.Empty: # isinstance não funcionaria
                return await ctx.send(embed=erro)
            await membro.ban(reason=f'Por {ctx.author} || Motivo: {reason}')

            # Não vou usar o self.bot.embed, já que esse embed sobescreve tudo.
            embed = self.bot.embed(ctx)
            embed.title = f'{self.bot.emotes["sora_ban"]} | Ban'
            embed.description = 'Desrespeitou as regras, deu nisso aí.'
            embed.add_field(name=f'Usuário:', value=f'Tag: `{membro}`\nId: `{membro.id}`', inline=False)
            embed.add_field(name=f'Staffer:', value=f'Tag: `{ctx.author}`\nCargo: `{ctx.author.top_role.name}`', inline=False)
            embed.add_field(name=f'Motivo:', value=reason, inline=False)
            embed.set_footer(text=f'Banido: {membro.name}', icon_url=membro.avatar_url)
            return await ctx.send(embed=embed)

        else:
            try:
                int(membro)
            except ValueError:
                embed = self.bot.erEmbed(ctx, 'Inválido')
                embed.description = 'O "id" que você digitou não é um número!'
                return await ctx.send(embed=embed)

            member = discord.Object(id=membro)

            embed = self.bot.embed(ctx, invisible=True)
            embed.description = 'Banindo...'
            m = await ctx.send(embed=embed)

            try:
                await ctx.guild.ban(member, reason=f'Por {ctx.author} || Motivo: {reason}')
            except discord.NotFound:
                embed = self.bot.erEmbed(ctx, 'Id inválido')
                embed.description = f'O id que você digitou ({member.id}) não pertence à algum membro.\nVerifique erros de escrita.'
                return await m.edit(embed=embed)

            embed.description = 'Membro banido, carregando embed...'
            await m.edit(embed=embed)

            member = await self.bot.fetch_user(member.id)
            embed = self.bot.embed(ctx)
            embed.title = f'{self.bot.emotes["sora_ban"]} | Ban'
            embed.description = 'Desrespeitou as regras deu nisso ai.'
            embed.add_field(name=f'Usuário:', value=f'Tag: `{member}`\nId: `{member.id}`', inline=False)
            embed.add_field(name=f'Staffer:', value=f'Menção: {ctx.author.mention}\nCargo: `{ctx.author.top_role.name}`', inline=False)
            embed.add_field(name=f'Motivo:', value=reason)
            embed.set_footer(text=f'Banido: {member.name}', icon_url=member.avatar_url)

            await m.edit(embed=embed)

    @commands.command(usage='{}softban [membro] (motivo)', description='Bane e desbane um membro, util para limpar as mensagens rapidamente.')
    @commands.has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, membro:discord.Member, *, reason="Não informado."):
        erro = self.bot.erEmbed(ctx, 'Sem permissão.')

        if membro == ctx.author:
            erro.description = 'Você não pode se banir, bobinho!'

        if membro == ctx.me:
            erro.description = 'Não posso me banir...'

        if membro.top_role.position >= ctx.author.top_role.position:
            erro.description = f'Você não tem permissão para banir **{membro.name}** (seu cargo é menor ou igual que o dele)'

        if membro.top_role.position >= ctx.me.top_role.position:
            erro.description=f'Eu não tenho permissão para banir **{membro.name}** (cargo dele é maior ou igual que o meu)'

        if type(erro.description) != discord.Embed.Empty: # isinstance não funciona aqui
            return await ctx.send(embed=erro)

        await membro.ban(reason=f'Por {ctx.author} || Motivo: {reason}')
        await membro.unban(reason=f'Por {ctx.author} || Motivo: {reason}')
        
        embed = self.bot.embed(ctx)
        embed.title = f'{self.bot.emotes["sora_ban"]} | SoftBan'
        embed.description = 'Desrespeitou as regras, deu nisso aí.'
        embed.add_field(name=f'Usuário:', value=f'Tag: `{membro}`\nId: `{membro.id}`', inline=False)
        embed.add_field(name=f'Staffer:', value=f'Tag: `{ctx.author}`\nCargo: `{ctx.author.top_role.name}`', inline=False)
        embed.add_field(name=f'Motivo:', value=reason, inline=False)
        embed.set_footer(text=f'Punido: {membro.name}', icon_url=membro.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(usage='{}kick [membro] (motivo)', description='Expulsa um membro do servidor. [Expulsar Membros]')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, membro:discord.Member, *, reason="Não informado."):
        erro = self.bot.erEmbed(ctx, 'Sem permissão.')
        if membro.top_role.position >= ctx.author.top_role.position:
            erro.description = f'Você não tem permissão para expulsar **{membro.name}** (seu cargo é menor ou igual que o dele)'

        if membro.top_role.position >= ctx.me.top_role.position:
            erro.description = f'Eu não tenho permissão para expulsar **{membro.name}** (cargo dele é maior ou igual que o meu)'

        if not isinstance(erro.description, type(discord.Embed.Empty)):
            return await ctx.send(embed=erro)

        await membro.kick(reason=f'Por {ctx.author} || Motivo: {reason}')

        embed = self.bot.embed(ctx)
        embed.title = f'{self.bot.emotes["sora_ban"]} | Kick'
        embed.description = f'{membro} foi expulso por: `{reason}`'
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(kick_members = True)
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, member: discord.Member = None, *, reason: str = 'Motivo não informado.'): # Mute command
        # Discord return
        if member is None:
            e = discord.Embed(description = f'Você não informou o usuário a ser mutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
            e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
            await ctx.send(embed = e)
            await ctx.message.add_reaction('❌')
        else:
            role = discord.utils.get(ctx.guild.roles, name = mutedRole)
            if role in member.roles:
                e = discord.Embed(description = f'O usuário já está mutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.add_reaction('❌')
            else:
                muted = discord.utils.get(ctx.guild.roles, name = mutedRole)
                if muted is None:
                    await ctx.guild.create_role()
                default = discord.utils.get(ctx.guild.roles, name = memberRole)
                await member.add_roles(muted)
                await member.remove_roles(default)

                e = discord.Embed(colour = 0xFEA900, timestamp = datetime.utcnow())
                e.add_field(name = ':bust_in_silhouette: Usuário', value = f'{member.mention}')
                e.add_field(name = ':crown: Moderador', value = f'{ctx.author.mention}')
                e.add_field(name = ':grey_question: Motivo', value = f'{reason}')
                e.set_author(name = 'MUTADO', icon_url = member.avatar_url)
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.delete()

                # Console return
                print('\n', f'-'*30)
                print(f'\n[+] A mute command has been called!\n\nLog: Author: {ctx.author}, Target: {member}')

    @commands.command()
    @commands.bot_has_permissions(kick_members = True)
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member: discord.Member = None):
        # Discord return
        if member is None:
            e = discord.Embed(description = f'Você não informou o usuário a ser desmutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
            e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
            await ctx.send(embed = e)
            await ctx.message.add_reaction('❌')
        else:
            role = discord.utils.get(ctx.guild.roles, name = mutedRole)
            if role not in member.roles:
                e = discord.Embed(description = f'O usuário não está mutado, {ctx.author.mention}!', colour = self.bot.cor, timestamp = datetime.utcnow())
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.add_reaction('❌')
            else:
                muted = discord.utils.get(ctx.guild.roles, name = mutedRole)
                default = discord.utils.get(ctx.guild.roles, name = memberRole)
                await member.add_roles(default)
                await member.remove_roles(muted)

                e = discord.Embed(colour = 0x3AFE00, timestamp = datetime.utcnow())
                e.add_field(name = ':bust_in_silhouette: Usuário', value = f'{member.mention}')
                e.add_field(name = ':crown: Moderador', value = f'{ctx.author.mention}')
                e.set_author(name = 'DESMUTADO', icon_url = member.avatar_url)
                e.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                await ctx.send(embed = e)
                await ctx.message.delete()

                # Console return
                print('\n', f'-'*30)
                print(f'\n[+] A mute command has been called!\n\nLog: Author: {ctx.author}, Target: {member}')


   
def setup(bot):
    bot.add_cog(moderacao(bot))