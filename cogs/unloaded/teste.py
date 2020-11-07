from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import aiohttp
member = "Neo_#0666"

async def bem_vindo():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cdn.discordapp.com/avatars/478266814204477448/a_7e2d0bc5528080fa33436c450a3b3ec6.webp?size=1024") as resp:
            if resp.status == 200:
                response = BytesIO(await resp.read())
            else:
                return
    avatar = Image.open(response)
    avatar = avatar.resize((210, 210));
    bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(avatar.size, Image.ANTIALIAS)
    avatar.putalpha(mask)

    saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    saida.putalpha(mask)

    fundo = Image.open('cogs/img/bem-vindo.png')
    fonte = ImageFont.truetype('cogs/img/college.ttf',42)
    escrever = ImageDraw.Draw(fundo)
    nome_user = str(member) if len(str(member)) <= 50 else str(member)[:50]
    fundo_x, _ = fundo.size
    texto_x, _ = escrever.textsize(nome_user, font=fonte)
    escrever.text(xy=((fundo_x - texto_x)/2, 345), text=nome_user,fill=(0,0,0),font=fonte)
    fundo.paste(saida, (357, 39), saida)
    arr = BytesIO()
    fundo.save(arr, format='PNG')
    arr.seek(0)
