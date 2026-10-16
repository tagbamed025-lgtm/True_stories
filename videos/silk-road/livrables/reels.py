# Reels / Shorts 9:16 (1080×1920) découpés dans le montage final CapCut de Mo (« Modifier et finale/Ross ulbrich.mp4 », 4K).
# Mise en page : fond flouté, image recadrée au centre (3:4), accroche en haut (style étiquettes TRU Stories), signature en bas.
# Usage : python -I reels.py   → livrables/reels/reel_1..4.mp4
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
F = r"C:\ffmpeg\bin\ffmpeg.exe"; HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'reels'); os.makedirs(OUT, exist_ok=True)
SRC = r"C:\Users\HP\Downloads\TRU Stories\Modifier et finale\Ross ulbrich.mp4"
# (début, fin) dans le montage CapCut — repérés par corrélation avec la voix ; accroche (2 lignes)
REELS = [(18.0, 53.3, "IL DIRIGEAIT UN EMPIRE À 1 MILLIARD $", "…DEPUIS UNE BIBLIOTHÈQUE"),
         (114.2, 154.0, "2 ERREURS.", "C'EST TOUT CE QU'IL A FALLU AU FBI"),
         (208.1, 244.3, "LE FBI A SIMULÉ UNE DISPUTE", "POUR L'ARRÊTER"),
         (254.6, 294.9, "PERPÉTUITÉ…", "PUIS LA GRÂCE PRÉSIDENTIELLE")]

def calque(i, l1, l2):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype('C:/Windows/Fonts/seguibl.ttf', 52); f2 = ImageFont.truetype('C:/Windows/Fonts/seguibl.ttf', 44)
    for j, (t, f, fond, encre) in enumerate([(l1, f1, (216, 38, 28), (255, 255, 255)), (l2, f2, (17, 17, 17), (245, 245, 245))]):
        tw = d.textlength(t, font=f); y = 120 + j * 112; x = (1080 - tw) / 2
        if fond == (17, 17, 17): d.rectangle((x - 30, y - 16, x + tw + 30, y + 80), fill=(244, 244, 244))
        d.rectangle((x - 22, y - 8, x + tw + 22, y + 72), fill=fond); d.text((x, y), t, font=f, fill=encre)
    f3 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 40); t = "TRU STORIES · l'histoire complète sur la chaîne"
    d.text((540, 1800), t, font=f3, fill=(235, 235, 235), anchor='mm')
    p = os.path.join(OUT, f'_calque{i}.png'); im.save(p); return p

for i, (a, b, l1, l2) in enumerate(REELS, 1):
    c = calque(i, l1, l2)
    vf = ("[0]crop=3840:1608:0:276,split[x][y];"
          "[x]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-.25[fond];"
          "[y]crop=1206:1608:(iw-1206)/2:0,scale=1080:1440[img];"
          "[fond][img]overlay=0:300[v];[v][1]overlay,fade=in:d=0.4,fade=out:st=" + str(round(b - a - .5, 2)) + ":d=0.5[out]")
    subprocess.run([F, '-v', 'error', '-y', '-ss', str(a), '-t', str(b - a), '-i', SRC, '-i', c, '-filter_complex', vf,
                    '-map', '[out]', '-map', '0:a', '-af', f"afade=t=in:d=0.3,afade=t=out:st={b - a - .6}:d=0.6",
                    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '192k',
                    os.path.join(OUT, f'reel_{i}.mp4')], check=True)
    print('OK reel', i, round(b - a, 1), 's')
