from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import aiohttp
member = "Neo_#0666"


def test(im, gradient_magnitude=1.5):
    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    width, height = im.size
    gradient = Image.new('L', (1, height), color=0xFF)

    for y in range(height):
        gradient.putpixel((0, y), int(255 * (1 - gradient_magnitude * float(y)/width)))
    
    gradient = gradient.rotate(180)
    alpha = gradient.resize(im.size)

    black_im = Image.new('RGBA', (width, height), color=0)
    black_im.putalpha(alpha)

    gradient_im = Image.alpha_composite(im, black_im)
    gradient_im.save('cogs/img/out1.png')

    
   
end = "01:23"
dur = "04:23"
thumbnail = Image.open('cogs/img/avatar.png').resize((415, 415), Image.ANTIALIAS)
base = Image.new('RGBA', (1100, 415), (0,0,0,0))
base.paste(thumbnail, (0, 0))
borrado = Image.open('cogs/img/avatar.png').resize((815, 615), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(radius = 8))
test(borrado)
fundo_black = Image.open('cogs/img/out1.png')

base.paste(fundo_black, (415,-150))

base.save('cogs/img/base.png')  
base.show()

titulo = "monstro da selva"
cantor = "neo"

x = (700 * 105) / 209


fonte = ImageFont.truetype('cogs/img/college.ttf', 35)
escrever = ImageDraw.Draw(base)
escrever.text(xy=(410,250), text=str(titulo.capitalize()),fill=(240,248,255),font=fonte)
escrever.rectangle([(400,400), (1100,415)], fill=(0,191,255))
#escrever.rectangle([(400,400), (800,415)], fill=(0,255,0))
escrever.rectangle([(400, 400), (x + 400, 415)], fill=(0,255,0))



escrever.text(xy=(410,360), text="04:31",fill=(0,255,0),font=fonte)
escrever.text(xy=(1000,360), text="04:31",fill=(0,191,255),font=fonte)

escrever.text(xy=(410,300), text=str(cantor),fill=(75,0,130),font=fonte)





