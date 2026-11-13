# Miniatures façon Fern : rendu 3D rapproché + étalonnage sombre + 2-3 mots énormes (blanc, un mot en jaune).
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
D = '/home/claude/true_stories/videos/binance-hack/livrables/miniatures/'
F = ImageFont.truetype(D + 'img/anton.woff', 10)
def fabrique(src, lignes, sortie, x0=60, y0=50, taille=190):
    im = Image.open(src).convert('RGB').resize((1920, 1080), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.22); im = ImageEnhance.Color(im).enhance(1.35); im = ImageEnhance.Brightness(im).enhance(.9)
    W, H = im.size; vig = Image.new('L', im.size, 0); ImageDraw.Draw(vig).ellipse((-W * .2, -H * .3, W * 1.2, H * 1.3), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(200)); im = Image.composite(im, Image.new('RGB', im.size, (0, 0, 0)), vig)
    # assombrir le coin du texte pour la lisibilité
    om = Image.new('L', im.size, 0); ImageDraw.Draw(om).rectangle((0, 0, W * .55, H * .6), fill=170); om = om.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, om)
    d = ImageDraw.Draw(im); y = y0
    for morceaux in lignes:
        x = x0; f = ImageFont.truetype(D + 'img/anton.woff', taille)
        for txt, coul in morceaux:
            for dx, dy in ((0, 12), (6, 12)): d.text((x + dx, y + dy), txt, font=f, fill=(0, 0, 0))
            d.text((x, y), txt, font=f, fill=coul, stroke_width=6, stroke_fill=(0, 0, 0)); x += d.textlength(txt + ' ', font=f)
        y += int(taille * 1.02)
    im.resize((1280, 720), Image.LANCZOS).save(sortie, quality=94)
B, J = (250, 250, 250), (255, 196, 20)
src = sys.argv[1] if len(sys.argv) > 1 else ''
fabrique(D + f'3d/mini_C{src}.png', [[('VIDÉ EN', B)], [('20 MIN', J)]], D + 'miniature_fern_1.jpg')
fabrique(D + f'3d/mini_D{src}.png', [[('1 SEUL', B)], [('PC', J)]], D + 'miniature_fern_2.jpg', taille=210)
