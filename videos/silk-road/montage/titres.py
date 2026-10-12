# Titres « bande-annonce » (style de la référence 1011.mp4) : minuscules élégantes, initiales en serif italique,
# apparition floue → nette avec aberration chromatique qui se résorbe, léger zoom arrière, fondu de sortie.
# Sortie : elements/titre.mp4 (3,5 s) et elements/date.mp4 (3 s), 1920×804, 30 i/s.
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(HERE, 'elements'); FF = r"C:\ffmpeg\bin\ffmpeg.exe"
W, H, FPS = 1920, 804, 30
FONTS = 'C:/Windows/Fonts/'
SANS = lambda s: ImageFont.truetype(FONTS + 'segoeuisl.ttf', s)      # Segoe UI Semilight
FIN = lambda s: ImageFont.truetype(FONTS + 'segoeuil.ttf', s)        # Segoe UI Light
SERIF_I = lambda s: ImageFont.truetype(FONTS + 'georgiaz.ttf', s)    # Georgia gras italique
SERIF = lambda s: ImageFont.truetype(FONTS + 'georgiai.ttf', s)      # Georgia italique

def ligne_mixte(draw, y, mots, taille, couleur=(242, 242, 242)):
    """Une ligne centrée où l'initiale de chaque mot est en serif italique, le reste en sans fin."""
    morceaux = []
    for i, m in enumerate(mots):
        if i: morceaux.append((' ', SANS(taille)))
        morceaux.append((m[0], SERIF_I(int(taille * 1.08)))); morceaux.append((m[1:], SANS(taille)))
    larg = sum(draw.textlength(s, font=f) for s, f in morceaux); x = (W - larg) / 2
    for s, f in morceaux:
        draw.text((x, y), s, font=f, fill=couleur, anchor='ls'); x += draw.textlength(s, font=f)

def centre(draw, y, s, f, couleur, espace=0):
    if espace:
        larg = sum(draw.textlength(c, font=f) for c in s) + espace * (len(s) - 1); x = (W - larg) / 2
        for c in s: draw.text((x, y), c, font=f, fill=couleur, anchor='ls'); x += draw.textlength(c, font=f) + espace
    else: draw.text((W / 2, y), s, font=f, fill=couleur, anchor='ms')

def carton_titre():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    centre(d, 300, 'TRU STORIES', FIN(22), (150, 150, 150), espace=9)
    ligne_mixte(d, 430, ["l'empire", 'à', 'un', 'milliard'], 92)
    centre(d, 505, 'piégé dans une bibliothèque', SERIF(40), (200, 200, 200))
    return im

def carton_date():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    centre(d, 360, 'San Francisco  ·  Glen Park', FIN(28), (170, 170, 170))
    centre(d, 450, '1er octobre 2013', SANS(76), (240, 240, 240))
    return im

def animer(base, duree, nom, entree=.9, sortie=.6):
    n = int(duree * FPS); dossier = os.path.join(E, '_' + nom); os.makedirs(dossier, exist_ok=True)
    a = np.asarray(base).astype(np.float32)
    for i in range(n):
        t = i / FPS; k = min(t / entree, 1); ease = 1 - (1 - k) ** 3
        op = ease * (1 - max(0, (t - (duree - sortie)) / sortie))
        ech = 1.035 - .035 * ease + .01 * t / duree                    # léger recul puis lente avancée
        im = Image.fromarray(a.astype(np.uint8)).resize((int(W * ech), int(H * ech)), Image.LANCZOS)
        ox, oy = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((ox, oy, ox + W, oy + H))
        flou = 6 * (1 - ease)
        if flou > .2: im = im.filter(ImageFilter.GaussianBlur(flou))
        r, g, b = im.split(); dec = int(round(10 * (1 - ease) + 1.5))   # aberration chromatique résiduelle
        r = r.transform(r.size, Image.AFFINE, (1, 0, dec, 0, 1, 0)); b = b.transform(b.size, Image.AFFINE, (1, 0, -dec, 0, 1, 0))
        im = Image.merge('RGB', (r, g, b))
        im = Image.fromarray((np.asarray(im).astype(np.float32) * op).astype(np.uint8))
        im.save(os.path.join(dossier, f'{i:04d}.png'))
    subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(dossier, '%04d.png'),
                    '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', os.path.join(E, nom + '.mp4')], check=True)

animer(carton_titre(), 3.0, 'titre')
animer(carton_date(), 2.0, 'date', entree=.6, sortie=.4)
print('OK')
