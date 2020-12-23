import discord
from discord.ext import commands
from datetime import datetime
import random

suck = ["https://media.giphy.com/media/l1J3sQY4zwxtvZpoA/giphy.gif",
        "https://media.giphy.com/media/2UOeg2XGEZine/giphy.gif",
        "https://media.giphy.com/media/KQdp5OCj44AG4/giphy.gif",
        "https://media.giphy.com/media/orSmv7XcL4R2w/giphy.gif",
        "https://media.giphy.com/media/xT0xexBaEUZZzkB1Di/giphy.gif",
        "https://media.giphy.com/media/iVxMwQW4pHpL2/giphy.gif",
        "https://media.giphy.com/media/zb3hfgWiHO3Yc/giphy.gif"]

class Insiders(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.users = [734580029849206874,731878461748281436]

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(description= "dê uma bela mamada em alguém",aliases=['suck'], hidden=True,usage=f"c.mamada @user")
    async def mamada(self, ctx, member: discord.Member):
        if not str(
                ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
            await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<", " ").replace(">", " "))
            return

        if not ctx.author.id in self.users and not ctx.author.id in self.bot.adms and not ctx.author.id in self.bot.dono:
            #await ctx.message.add_reaction(self.bot._emojis["incorreto"].replace("<", " ").replace(">", " "))
            embebo = discord.Embed(timestamp=datetime.utcnow(), color=self.bot.cor,
                                   description=f"Para utilizar esse comando é necessario pagar uma taxa de 15000 sonhos para @Neo_#0291.\n\nUtilize +pay @Neo_#0291 15k")
            embebo.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
            return await ctx.send(content=f"a", embed=embebo)

        if ctx.author == member:
            return await ctx.send(content=f"{ctx.author.mention}", embed=discord.Embed(timestamp=datetime.utcnow(),color=self.bot.cor,
                                                                                       description=f"Você não pode se mamar, tente fazer isso em casa mas não force a coluna demais.")).set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        gif = random.choice(suck)

        mamada_text = '<:zerotwoLewd:776245467453456404> {} **deu uma mamada em** {}.'.format(ctx.author.mention, member.mention)

        embed = discord.Embed(colour=self.bot.cor,
                              description="{}".format(mamada_text), timestamp=datetime.utcnow())

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=12)
        except:
            return
        else:
            #await msg.delete()
            if member.id not in self.users:
                embebo1 = discord.Embed(coluor=self.bot.cor,
                                       description=f"Para utilizar esse comando é necessario pagar uma taxa de 15000 sonhos para @Neo_#0291.\n\nUtilize +pay @Neo_#0291 15k")
                embebo1.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
                return await ctx.send(content=f"{member.mention}",embed=embebo1)
            author = ctx.author
            ctx.author = member
            await ctx.invoke(ctx.command, member=author)



def setup(bot):
    bot.add_cog(Insiders(bot))