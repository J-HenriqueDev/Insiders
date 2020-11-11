from discord.ext.commands import Bot, Cog, Context
from discord import Message, Member, Game, Reaction, Embed
from discord.ext.commands.errors import *
from discord.errors import *
from discord.utils import get, find   
    
class starboard(Cog):
    def __init__(self,bot):
        self.bot = bot
 
    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: Member):
        message = reaction.message

        starboard = get(message.guild.text_channels, name="「⭐」starboard")

        if not starboard:
            return

        if message.channel == starboard:
            return

        if str(reaction.emoji) == '⭐':
            reactions = message.reactions

            def make_check(emoji: str):
                def check(r):
                    return str(r.emoji) == emoji
                return check

            star_two_in_reactions = find(make_check('🌟'), reactions)
            if star_two_in_reactions:
                if star_two_in_reactions.me:
                    return

            star_in_reactions = find(make_check('⭐'), reactions)
            if star_in_reactions:
                stars = find(lambda r: str(r.emoji) == '⭐', reactions)
            else:
                return

            if stars.count <= 2:
                return

            await reaction.message.add_reaction('🌟')

            embed = Embed(
                title="Uma nova pérola apareceu!",
                description=f"Um [brilho]({message.jump_url}) está vindo do canal {message.channel.mention}!\n\n```{message.content}```",
                color=self.bot.cor,
                url=message.jump_url
            ).set_footer(
                icon_url=message.author.avatar_url,
                text=message.author.name + '#' + message.author.discriminator
            )

            attachments = message.attachments
            if attachments:
                for attachment in attachments:
                    if attachment.height and attachment.width:
                        embed.set_image(url=attachment.url)
                        break

            await starboard.send(embed=embed)


def setup(bot):
    bot.add_cog(starboard(bot))