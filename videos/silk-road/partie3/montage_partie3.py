# Partie 3 · « La traque : deux erreurs » (86,3 s) — p3.mp3 = VO_complete 105,2 → 191,5 s.
# Usage : python -I montage_partie3.py [final]   (brouillon : 960×402, 15 i/s)
# Prérequis : captures Three.js/HTML dans brouillon/ (decors.html : mur1, mur2, bureau, couloir ; forum.html : forum).
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
F = r"C:\ffmpeg\bin\ffmpeg.exe"; HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..')
FINAL = 'final' in sys.argv; W, H, FPS = (2560, 1072, 30) if FINAL else (960, 402, 15)   # final en 2K
LANG = os.environ.get('TRU_LANG')   # TRU_LANG=en → textes traduits (trad_en.json), sorties *_EN
import json as _j
_TR = _j.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', f'trad_{LANG}.json'), encoding='utf8')) if LANG else {}
T = lambda s: _TR.get(s, s)
SUF = '_' + LANG.upper() if LANG else ''
PNG = os.path.join(HERE, 'final' if FINAL else 'brouillon')   # images Blender (communes aux langues)
DOS = PNG + (('_' + LANG) if LANG else ''); os.makedirs(DOS, exist_ok=True)
DL = r"C:\Users\HP\Downloads\TRU Stories"
VO0, VO1 = 105.2, 191.5
k = W / 1920

def run(a): subprocess.run([F, '-v', 'error', '-y'] + a, check=True)
def police(n, s): return ImageFont.truetype('C:/Windows/Fonts/' + n, int(s * k))
def calque(nom, dessin):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dessin(ImageDraw.Draw(im)); p = os.path.join(DOS, nom + '.png'); im.save(p); return p
def bas_gauche(nom, petit, grand):
    petit, grand = T(petit), T(grand)
    return calque(nom, lambda d: (d.text((int(120 * k), H - int(190 * k)), ' '.join(petit.upper()), font=police('segoeuil.ttf', 24), fill=(215, 215, 215, 235)),
                                  d.text((int(118 * k), H - int(150 * k)), grand, font=police('segoeuisl.ttf', 62), fill=(245, 245, 245, 255))))
def carton(nom, petit, grand):
    petit, grand = T(petit), T(grand)
    def dessin(d):
        d.rectangle((0, 0, W, H), fill=(11, 12, 14, 255))
        d.text((W / 2, H * .42), ' '.join(petit.upper()), font=police('segoeuil.ttf', 24), fill=(150, 150, 150, 255), anchor='ms')
        d.text((W / 2, H * .58), grand, font=police('georgiai.ttf', 80), fill=(238, 238, 238, 255), anchor='ms')
    return calque(nom, dessin)

base = f"fps={FPS},setsar=1"; cadre = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
plans = []
def plan(nom, d, entree, vf):
    out = os.path.join(DOS, f'p{len(plans):02d}_{nom}.mp4')
    run(entree + ['-t', str(d), '-filter_complex', vf, '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out]); plans.append((out, d))

# A · « Silk Road est conçu pour être introuvable. Les serveurs sont cachés. Les paiements, anonymes. Les messages, chiffrés. »
mots = [bas_gauche('m1', 'Les serveurs', 'cachés'), bas_gauche('m2', 'Les paiements', 'anonymes'), bas_gauche('m3', 'Les messages', 'chiffrés')]
plan('serveurs', 11.75, ['-ss', '3', '-i', os.path.join(DL, '5028622-uhd_3840_2160_25fps.mp4')] + sum((['-i', m] for m in mots), []),
     f"[0]{cadre},eq=saturation=.35:brightness=-.1:contrast=1.1,colorbalance=bs=.08[v];"
     "[v][1]overlay=enable='between(t,5.1,6.7)'[a];[a][2]overlay=enable='between(t,6.7,8.6)'[b];[b][3]overlay=enable='between(t,8.6,11.75)',"
     f"{base}")
# B · « Alors les enquêteurs ne cherchent pas une faille dans le code. Ils cherchent une faille… dans l'homme. »
plan('mur1', 7.55, ['-i', os.path.join(DOS, 'mur1.mp4')], f"[0]{cadre},{base}")
# C · « Première erreur… » forum de 2011, l'e-mail avec son vrai nom
plan('forum', 22.7, ['-i', os.path.join(DOS, 'forum.mp4')], f"[0]{cadre},{base}")
# D · « Des années plus tard, un enquêteur du fisc américain, Gary Alford, retrouve ce vieux message. »
plan('alford', 5.9, ['-i', os.path.join(DOS, 'bureau.mp4')], f"[0]{cadre},{base}")
# E · « Deuxième erreur. Juillet 2013. À la frontière canadienne, un colis est intercepté… neuf faux papiers… même visage. »
plan('erreur2', 2.0, ['-loop', '1', '-i', carton('c_err2', 'Deuxième erreur', 'Juillet 2013')], f"[0]fade=in:d=0.3,{base}")
t = bas_gauche('t_frontiere', 'Frontière canadienne', 'un colis intercepté')
plan('colis', 3.5, ['-ss', '4', '-i', os.path.join(DL, '10472351-hd_1920_1080_25fps.mp4'), '-i', t], f"[0]{cadre},eq=saturation=.6:brightness=-.05[v];[v][1]overlay,{base}")
plan('faux_papiers', 8.8, ['-loop', '1', '-i', os.path.join(DL, 'Screenshot 2026-10-12 223447.png')],
     f"[0]scale={W*2}:-2,zoompan=z='1.0+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih/zoom/2)+on*0.6':d=1:s={W}x{H}:fps={FPS},eq=contrast=1.05,{base}")
# F · « L'adresse de livraison… mène à un appartement de San Francisco. Des agents frappent à sa porte. Le visage correspond. »
t = bas_gauche('t_sf', 'San Francisco', '15th Avenue')
plan('rue_sf', 4.0, ['-ss', '2', '-i', os.path.join(DL, '12604103_3840_2160_30fps.mp4'), '-i', t], f"[0]{cadre},eq=saturation=.7[v];[v][1]overlay,{base}")
plan('couloir', 6.7, ['-i', os.path.join(DOS, 'couloir.mp4')], f"[0]{cadre},{base}")
# G · « Ce jour-là, personne ne fait le lien… Et en septembre, les deux fils se rejoignent. Le FBI a désormais un nom. Mais un nom ne suffit pas. »
plan('mur2', 13.4, ['-i', os.path.join(DOS, 'mur2.mp4')], f"[0]{cadre},fade=out:st=12.9:d=0.5,{base}")

liste = os.path.join(DOS, 'liste.txt'); open(liste, 'w').write(''.join(f"file '{p}'\n" for p, _ in plans))
TOTAL = sum(d for _, d in plans)
vo = os.path.join(V, 'voix', 'VO_complete_SilkRoad.mp3'); mus = os.path.join(V, 'montage', 'elements', 'musique.wav')
sortie = os.path.join(V, 'rendu', 'silk-road_partie3' + ('' if FINAL else '_brouillon') + SUF + '.mp4')
run(['-f', 'concat', '-safe', '0', '-i', liste, '-i', vo, '-i', mus, '-filter_complex',
     f"[1]atrim={VO0}:{VO1},asetpts=N/SR/TB,aformat=channel_layouts=stereo,volume=1.15,asplit[vo][sc];"
     f"[2]atrim=18:48,asetpts=N/SR/TB,aloop=loop=3:size=1440000,atrim=0:{TOTAL},volume=0.45[m];"
     f"[m][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];[vo][md]amix=2:normalize=0,alimiter=limit=0.9[a]",
     '-map', '0:v', '-map', '[a]', '-vf', f"noise=alls=2:allf=t,vignette=PI/6,pad={W}:{W*9//16}:0:({W*9//16}-{H})/2:black",
     '-c:v', 'libx264', '-crf', '18' if not FINAL else '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', str(TOTAL), sortie])
print('OK', sortie, round(TOTAL, 1), 's')
