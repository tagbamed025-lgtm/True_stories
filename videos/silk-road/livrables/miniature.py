# Miniature YouTube 2560×1440 : rendu 3D Blender (partie4/plans_blender.py -- miniature) + étalonnage + titre.
# Usage : python -I miniature.py  → livrables/miniature_silk-road.png (+ version 1280×720 pour YouTube)
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'partie4', 'tests', 'miniature.png')
F = 'C:/Windows/Fonts/'
im = Image.open(SRC).convert('RGB').resize((2560, 1440), Image.LANCZOS)
W, H = im.size

# 1 · étalonnage « nuit_enquete » : plus sombre, plus contrasté, froid ; le rouge de Ross reste vif
im = ImageEnhance.Brightness(im).enhance(.62); im = ImageEnhance.Contrast(im).enhance(1.35); im = ImageEnhance.Color(im).enhance(.85)
froid = Image.new('RGB', im.size, (20, 40, 80)); im = Image.blend(im, froid, .12)
# lueur rouge derrière Ross (centre)
halo = Image.new('L', im.size, 0); ImageDraw.Draw(halo).ellipse((W * .36, H * .22, W * .64, H * .82), fill=150)
halo = halo.filter(ImageFilter.GaussianBlur(160)); rouge = Image.new('RGB', im.size, (230, 30, 25))
im = Image.composite(rouge, im, halo.point(lambda v: v * .45))
# vignette forte
vig = Image.new('L', im.size, 0); ImageDraw.Draw(vig).ellipse((-W * .15, -H * .25, W * 1.15, H * 1.25), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(220)); im = Image.composite(im, Image.new('RGB', im.size, (0, 0, 0)), vig)

d = ImageDraw.Draw(im)
def texte(xy, t, police, taille, couleur, ombre=14, anchor='la'):
    f = ImageFont.truetype(F + police, taille)
    for dx, dy in ((ombre, ombre), (0, ombre)): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0), anchor=anchor)
    d.text(xy, t, font=f, fill=couleur, anchor=anchor, stroke_width=4, stroke_fill=(0, 0, 0))
    return f
# 2 · titre : 3 mots maximum, très gros, à gauche ; montant en rouge
texte((120, 150), "PIÉGÉ", 'seguibl.ttf', 270, (245, 245, 245))
texte((128, 440), "EN 1 SECONDE", 'seguibl.ttf', 150, (245, 245, 245))
# bandeau rouge « 1 MILLIARD $ »
f = ImageFont.truetype(F + 'seguibl.ttf', 110); x0, y0 = 128, 650; tw = d.textlength("1 MILLIARD $", font=f)
d.rectangle((x0 - 20, y0 - 10, x0 + tw + 30, y0 + 140), fill=(216, 38, 28)); d.text((x0, y0), "1 MILLIARD $", font=f, fill=(255, 255, 255))
# étiquette style TRU Stories sur Ross
f = ImageFont.truetype(F + 'consolab.ttf', 64); t = "DREAD PIRATE ROBERTS"; tw = d.textlength(t, font=f); cx, cy = W * .5, H * .17
d.rectangle((cx - tw / 2 - 40, cy - 52, cx + tw / 2 + 40, cy + 52), fill=(244, 244, 244))
d.rectangle((cx - tw / 2 - 28, cy - 40, cx + tw / 2 + 28, cy + 40), fill=(17, 17, 17)); d.text((cx, cy), t, font=f, fill=(242, 242, 242), anchor='mm')
d.polygon([(cx - 26, cy + 52), (cx + 26, cy + 52), (cx, cy + 88)], fill=(244, 244, 244))
# logo discret
texte((W - 60, H - 60), "TRU STORIES", 'segoeuib.ttf', 54, (230, 230, 230), ombre=6, anchor='rs')

out = os.path.join(HERE, 'miniature_silk-road.png'); im.save(out)
im.resize((1280, 720), Image.LANCZOS).save(os.path.join(HERE, 'miniature_silk-road_1280.jpg'), quality=92)
print('OK', out)
