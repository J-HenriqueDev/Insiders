from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import aiohttp
member = "Neo_#0666"
   
end = "01:23"
dur = "04:23"
thumbnail = Image.open('cogs/img/avatar.png').resize((415, 415), Image.ANTIALIAS)
base = Image.new('RGBA', (1100, 415), (0,0,0,0))
base.paste(thumbnail, (0, 0))
borrado = Image.open('cogs/img/avatar.png').resize((815, 615), Image.ANTIALIAS)
im2 = borrado.filter(ImageFilter.GaussianBlur(radius = 8)) 
base.paste(im2, (400,0))
   
titulo = "monstro da selva"
cantor = "neo"

x = (700 * 105) / 209
print(x)    

print(base.size)

fonte = ImageFont.truetype('cogs/img/college.ttf', 35)
escrever = ImageDraw.Draw(base)
escrever.text(xy=(410,250), text=str(titulo.capitalize()),fill=(240,248,255),font=fonte)
escrever.rectangle([(400,400), (1100,415)], fill=(0,191,255))
#escrever.rectangle([(400,400), (800,415)], fill=(0,255,0))
escrever.rectangle([(400, 400), (x + 400, 415)], fill=(0,255,0))



escrever.text(xy=(410,360), text="04:31",fill=(0,255,0),font=fonte)
escrever.text(xy=(1000,360), text="04:31",fill=(0,191,255),font=fonte)

escrever.text(xy=(410,300), text=str(cantor),fill=(75,0,130),font=fonte)

width, height = borrado.size
alpha_gradient = Image.new('L', (width, 1), color=0xFF)
for x in range(width):
    a = int((1 * 255.) * (1. - 1 * float(x)/width))
    if a > 0:
        alpha_gradient.putpixel((x, 0), a)
    else:
        alpha_gradient.putpixel((x, 0), 0)
alpha = alpha_gradient.resize(borrado.size)

# create black image, apply gradient
black_im = Image.new('RGBA', (width, height), color=0) # i.e. black
black_im.putalpha(alpha)


sombra = Image.alpha_composite(borrado, black_im)
#sombra.save('cogs/img/sombra.png')
sombra.show()
#base.save('cogs/img/imagem1.png')
#base.show()