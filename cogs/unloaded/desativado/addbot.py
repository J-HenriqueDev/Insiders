import discord

from discord.ext import commands
from asyncio import TimeoutError as Timeout
from datetime import datetime


prefixos = ["c.", "!", "@", "/"]

class Cadastro(commands.Cog):
    def __init__(self, lab):
        self.bot = lab
        self.forms = []

    @commands.command(
        name='adicionarbot', 
        aliases=['addbot', 'registrarbot', 'cadastrarbot', 'cadastrar', 'enviarbot'],
        description='Adiciona um bot no sistema',
        usage='c.-adicionarbot'
    )
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _adicionarbot(self, ctx):
        if not str(
            ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
            await ctx.message.add_reaction(self.bot._emojis['incorreto'].replace("<", " ").replace(">", " "))
            return
        '''
        dias_servidor = (datetime.utcnow() - ctx.author.joined_at).days
        if dias_servidor < 5:
            embed = discord.Embed(colour=self.bot.cor)
            embed = discord.Embed(
                description=f"{self.bot._emojis['incorreto']} **|** Olá **{ctx.author.name}**, você precisa ser membro desse servidor há mais de **`5`** dias para poder adicionar um bot.",
                color=self.bot.cor)
            return await ctx.send(embed=embed)
        '''

        if ctx.author.id in self.forms:
            return await ctx.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, ainda existe um formulário sendo executado no seu privado.", delete_after=30)

        if not str(
                ctx.channel.id) in self.bot.canais and not ctx.author.id in self.bot.dono and not ctx.author.id in self.bot.adms:
            await ctx.message.add_reaction(self.bot._emojis['incorreto'].replace("<", " ").replace(">", " "))
            return

        txs = f"{self.bot._emojis['api']} **|** Então você quer adicionar o seu **BOT** em nosso servidor?\nPara isso precisamos que você preencha um pequeno formulário para cadastramento de seu **BOT** em nosso sistema e discord.\n\n{self.bot._emojis['bots']} **|** Insira o **ID** do bot que deseja adicionar: \n{self.bot._emojis['timer']} **|** **2 minutos**"
        embed = discord.Embed(description=txs, color=self.bot.cor)
            
        try:
            m_opt = await ctx.author.send(embed=embed)
        except discord.Forbidden:
            return await ctx.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, ative as Mensagens Diretas para que eu possa prosseguir com o registro.")

        self.forms.append(ctx.author.id)

        await ctx.send(embed=discord.Embed(
            description=f":envelope_with_arrow:  **|** Olá **{ctx.author.name}**, verifique sua mensagens diretas (DM).",
            color=self.bot.cor))
        

        def opt_check(reaction, user):
            return reaction.message.id == m_opt.id and user == ctx.author 


        max_tentativas = 3


        def id_check_canal(m):
            return m.author == ctx.author and m.channel.id == m_opt.channel.id

        botID = None
        id_tentativas = 1
        while not botID:
            try:
                _botID = await self.bot.wait_for("message", check=id_check_canal, timeout=120)
            except Timeout:
                await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você demorou demais para responder!", delete_after=20)
                break
            else:
                if len(_botID.content) <= 32 and _botID.content.isdigit():
                    botID = int(_botID.content)
                else:
                    if id_tentativas == max_tentativas:
                        await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você atingiu o limite de tentativas! `(3/3)`", delete_after=20)
                        break

                    await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, esse não é um valor válido, forneça outro! `(Tentativa {id_tentativas}/{max_tentativas})`", delete_after=20)
                    id_tentativas += 1

        await m_opt.delete()

        if not botID:
            self.forms.remove(ctx.author.id)
        try:
            bot = await self.bot.fetch_user(botID)
        except (discord.Forbidden, discord.HTTPException):
            self.forms.remove(ctx.author.id)
            return await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, não foi possível encontrar nenhuma conta com o `ID` fornecido.", delete_after=20)
        
        if not bot.bot:
            self.forms.remove(ctx.author.id)
            return await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, o `ID` fornecido não pertence a um Bot.", delete_after=20)
        
        db = self.bot.db.bots
        _bot = db.find_one({"_id": bot.id})
        if _bot:
            if ctx.author.id not in _bot['donos']:
                self.forms.remove(ctx.author.id)
                return await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, o `ID` fornecido pertence ao bot **`{bot}`** e **VOCÊ NÃO É DONO** dele.", delete_after=20)
            elif _bot['banido']:
                self.forms.remove(ctx.author.id)
                return await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, o `ID` fornecido pertence ao bot **`{bot}`** que foi **BANIDO** do meu sistema.", delete_after=20)
            elif _bot['suspenso']:
                self.forms.remove(ctx.author.id)
                return await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, o `ID` fornecido pertence ao bot **`{bot}`** que foi **SUSPENSO** do meu sistema.", delete_after=20)
            elif _bot['pendente_discord']:
                self.forms.remove(ctx.author.id)
                return await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, o `ID` fornecido pertence ao bot **`{bot}`** que já está **PENDENTE** para aprovação.", delete_after=20)
            elif _bot['aprovado_discord']:
                self.forms.remove(ctx.author.id)
                return await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, o `ID` fornecido pertence ao bot **`{bot}`** que já foi **ADICIONADO** no Discord do **`Insider's`**.", delete_after=20)
        
        txs = f"{self.bot._emojis['nome']} **|** Diga-nos agora o prefixo do seu **BOT** (máximo 8 caracteres)\n\n:no_entry_sign: Prefixo banidos **|** **[c.],[!],[/][@],[#]**\n\n{self.bot._emojis['timer']} **|** **2 minutos**"
        embed_prefix = discord.Embed(description=txs, color=self.bot.cor)
        m_prefixo = await ctx.author.send(embed=embed_prefix)

        def prefixo_check_canal(m):
            return m.author == ctx.author and m.channel.id == m_prefixo.channel.id

        botPrefixo = None
        prefixo_tentativas = 1
        while not botPrefixo:
            try:
                _botPrefixo = await self.bot.wait_for("message", check=prefixo_check_canal, timeout=120)
            except Timeout:
                await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você demorou demais para fornecer o prefixo do bot!", delete_after=20)
                break
                 
            if 0 < len(_botPrefixo.content) <= 8:
                botPrefixo = _botPrefixo.content
            else:
                if prefixo_tentativas == max_tentativas:
                    await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você atingiu o limite de tentativas permitidas! `(3/3)`", delete_after=20)
                    break
                
                await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, só permitimos prefixos com até ``8`` caracteres, tente novamente! `(Tentativa {prefixo_tentativas}/{max_tentativas})`", delete_after=20)
                prefixo_tentativas += 1
        
        await m_prefixo.delete()

        if not botPrefixo:
            self.forms.remove(ctx.author.id)
            return

        botDescricao = None
        m_descricao = await ctx.author.send(f"{self.bot._emojis['api']} | **Digite uma curta descrição sobre seu bot**. Ela ficará visível no comando de informações do seu bot. `(5 minutos)`\n**OBS**: O texto precisa conter no mínimo ``100`` caracteres e no máximo ``180``.")

        def descricao_check_canal(m):
            return m.author == ctx.author and m.channel.id == m_descricao.channel.id

        descricao_tentativas = 1
        while not botDescricao:
            try:
                _botDescricao = await self.bot.wait_for("message", check=descricao_check_canal, timeout=300)
            except Timeout:
                await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você demorou demais para fornecer uma descrição!", delete_after=20)
                break
            
            if 180 >= len(_botDescricao.content) >= 100:
                botDescricao = _botDescricao.content
            else:
                if descricao_tentativas == max_tentativas:
                    await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você atingiu o limite de tentativas permitidas! `(3/3)`", delete_after=20)
                    break
                
                await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, descrição fornecida precisa ter no mínimo ``100`` e no máximo ``180`` caracteres. `(Tentativa {descricao_tentativas}/{max_tentativas})`", delete_after=20)
                descricao_tentativas += 1
        
        await m_descricao.delete()

        if not botDescricao:
            self.forms.remove(ctx.author.id)
            return

        bibliotecas = ["Python", "JavaScript"]
        

        
        txs = f"{self.bot._emojis['canais']} **|** Diga-nos agora o linguagem do seu **BOT** foi criado.\n{self.bot._emojis['api']} Linguagens **|** **{', '.join([f'`{lib}`' for lib in bibliotecas])}**\n{self.bot._emojis['timer']} **|** **2 minutos**"
        embed = discord.Embed(description=txs, color=self.bot.cor)
        m_biblioteca = await ctx.author.send(embed=embed)

        def biblioteca_check_canal(m):
            return m.author == ctx.author and m.channel.id == m_biblioteca.channel.id

        botBiblioteca = None
        biblioteca_tentativas = 1
        while not botBiblioteca:
            try:
                _botBiblioteca = await self.bot.wait_for("message", check=biblioteca_check_canal, timeout=120)
            except Timeout:
                await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você demorou demais para responder!", delete_after=20)
                break
            
            bibli = [bibli for bibli in bibliotecas if bibli.lower() == _botBiblioteca.content.lower()]
            if bibli != []:
                botBiblioteca = bibli[0]
            else:
                if biblioteca_tentativas == max_tentativas:
                    await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você atingiu o limite de tentativas permitidas! `(3/3)`", delete_after=20)
                    break
                
                await ctx.author.send(f"{self.bot._emojis['errado']} | **{ctx.author.name}**, você forneceu uma biblioteca inválida! Certifique-se de digitar uma das bibliotecas listadas acima `(Tentativa {biblioteca_tentativas}/{max_tentativas})`\n**OBS**: Se você utilizou outra biblioteca para codar seu bot, digite \"Outros\"", delete_after=20)
                biblioteca_tentativas += 1
        
        await m_biblioteca.delete()

        if not botBiblioteca:
            self.forms.remove(ctx.author.id)
            return


        embed = discord.Embed(color=self.bot.cor)
        embed.set_author(name="SOLICITAÇÂO DE ADD(BOT)",
                            icon_url=ctx.author.avatar_url_as())
        embed.add_field(name=f"{self.bot._emojis['bots']} Bot",
                        value="``" + str(bot) + "``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['ip']} ID",
                        value="``" + str(bot.id) + "``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['notas']} Criado em",
                        value=f"`{bot.created_at.strftime('%d/%m/20%y')}`", inline=True)
        embed.add_field(name=f"{self.bot._emojis['texto']} Prefixo",
                        value="``" + str(botPrefixo) + "``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['api']} Linguagem",
                        value="``" + str(botBiblioteca) + "``", inline=True)
        embed.add_field(name=f"{self.bot._emojis['mention']} Dono",
                        value="``" + str(ctx.author) + "``" + " (" + str(
                            ctx.author.mention) + ")", inline=True)
        embed.add_field(name=f"{self.bot._emojis['mention']} Convite",
                        value=f"[Link](https://discordapp.com/api/oauth2/authorize?client_id={bot.id}&permissions=0&scope=bot)",
                        inline=True)
        embed.add_field(name=f"{self.bot._emojis['tipo']} | **Descrição:**",
                        value=f"```diff\n{botDescricao}\n```", inline=False)
        embed.set_thumbnail(url=bot.avatar_url)
        embed.set_footer(text=self.bot.user.name + " © 2020",
                        icon_url=self.bot.user.avatar_url_as())


        addbot = self.bot.get_channel(778728930156609556)
        pendenteMsg = await addbot.send(content="**NOVO BOT PENDENTE PARA APROVAÇÃO** (@here)", embed=embed)

        for e in [self.bot._emojis['correto'], self.bot._emojis['errado']]:
            await pendenteMsg.add_reaction(e.replace("<", "").replace(">", ""))

        if _bot:
                _bot['pendente_discord'] = True
                _bot['data_enviado_discord'] = datetime.now()
                _bot['enviado_por_discord'] = ctx.author.id
                _bot['pendente_msg'] = pendenteMsg.id
                _bot['biblioteca'] = botBiblioteca.lower()
                _bot['prefixo'] = botPrefixo
                db.save(_bot)
        else:
            db.insert_one({
                "_id": bot.id,
                "nome": bot.name,
                "discriminador": bot.discriminator,
                "avatar": bot.avatar,
                "donos": [ctx.author.id],
                "votos_mensais": 0,
                "votos_totais": 0,
                "prefixo": botPrefixo,
                "biblioteca": botBiblioteca.lower(),
                "descrição": botDescricao,
                "pendente_msg": pendenteMsg.id,
                "aprovado_discord": False,
                "pendente_discord": True,
                "pendente_verificar": False,
                "data_aprovado_discord": None,
                "data_enviado_discord": datetime.now(),
                "data_enviado_verificado": None,
                "aprovado_por_discord": None,
                "verificado_por": None,
                "enviado_por_discord": ctx.author.id,
                "enviado_por_verificado": None,
                "banido": False,
                "suspenso": False,
                "ban_info": {
                    "autor": None,
                    "data": None,
                    "motivo": None
                },
                "suspenso_info": {
                    "autor": None,
                    "data": None,
                    "motivo": None
                }, 
                "histórico": [
                    {"ação": f"Enviado Discord", "autor": ctx.author.id, "motivo": None, "data": datetime.now()}, {"ação": "Nome alterado", "autor": bot.id, "motivo": str(bot), "data": datetime.now()}
                ]
            })

        logs = self.bot.get_channel(778654724860805141)
        await logs.send(f"{self.bot._emojis['texto']} {ctx.author.mention} **enviou** o bot **`{bot}`** para verificação e está aguardando analise.")
        
        
        embed_concluido = discord.Embed(
            description=f"{self.bot._emojis['correto']} **|** **{ctx.author.name}**, você completou o formulário para adicionar seu bot `{bot}` no **INSIDER'S**.\n**OBS**: O bot será sujeito a avaliação, podendo ser aprovado ou rejeitado.",
            color=self.bot.cor)
        
        await ctx.author.send(embed=embed_concluido)
        self.forms.remove(ctx.author.id)


def setup(lab):
    lab.add_cog(Cadastro(lab))