# Partie 2 · « Qui est cet homme » (41,7 s), calée sur la voix (VO_complete 63,5 → 105,2 s ; vidéo finale 0:51,5 → 1:33,2).
# Usage : python -I montage_partie2.py [final]   (brouillon par défaut : 960×402, 15 i/s)
# Plans [CODE] : scenes.html capturé par outils/capture/capture.js (silkroad, tor, dpr, compteur).
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
STOCK = {'colis': '10472351-hd_1920_1080_25fps.mp4', 'bitcoin': '7634144-hd_1920_1080_25fps.mp4',
         'campus': '7969427-uhd_2160_3840_30fps.mp4', 'ecran_nuit': '14614656_3840_2160_30fps.mp4'}
VO0, VO1 = 63.5, 105.2

def run(a): subprocess.run([F, '-v', 'error', '-y'] + a, check=True)

def texte(nom, petit, grand):
    petit, grand = T(petit), T(grand)
    """Calque transparent : petit sur-titre espacé + grand texte fin (style des titres validés)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = W / 1920
    fp = ImageFont.truetype('C:/Windows/Fonts/segoeuil.ttf', int(24 * k)); fg = ImageFont.truetype('C:/Windows/Fonts/segoeuisl.ttf', int(64 * k))
    d.text((int(120 * k), H - int(190 * k)), ' '.join(petit.upper()), font=fp, fill=(200, 200, 200, 230))
    d.text((int(118 * k), H - int(150 * k)), grand, font=fg, fill=(245, 245, 245, 255))
    p = os.path.join(DOS, nom + '.png'); im.save(p); return p

base = f"fps={FPS},setsar=1"
cadre = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
plans = []   # (fichier, durée)
def plan(nom, d, entree, vf):
    out = os.path.join(DOS, f'p{len(plans):02d}_{nom}.mp4')
    run(entree + ['-t', str(d), '-filter_complex', vf, '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out]); plans.append((out, d))

# Calé sur les phrases réelles (p2.mp3 = VO_complete 66,0 → 103,7 s), à partir de 63,5 s (fin de la minute validée).
# 1 · « Il s'appelle Ross Ulbricht. Vingt-neuf ans. »
t = texte('t_ross', 'Ross Ulbricht', '29 ans')
plan('portrait', 5.9, ['-loop', '1', '-i', r'C:/Users/HP/Documents/Remotion/depot/assets3d/silk-road/archives/ross_carreaux.png', '-i', t],
     f"[0]scale={W*2}:-2,zoompan=z='1.0+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih*0.42-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},eq=saturation=.85:contrast=1.05[v];[v][1]overlay,fade=in:d=1.2,{base}")
# 2 · « Diplômé en physique, passionné d'économie. » : campus (vidéo verticale sur fond flouté)
t = texte('t_etudes', 'Diplômé en', 'physique · économie')
plan('campus', 4.4, ['-i', os.path.join(DL, STOCK['campus']), '-i', t],
     f"[0]split[a][b];[a]{cadre},boxblur=20[f];[b]scale=-2:{H}[c];[f][c]overlay=(W-w)/2:0,eq=saturation=.7[v];[v][1]overlay,{base}")
# 3 · « En 2011, il lance un site invisible, caché derrière le réseau Tor… » (Three.js)
plan('tor', 4.6, ['-i', os.path.join(DOS, 'tor.mp4')], f"[0]{cadre},{base}")
# 4 · « … Silk Road. On y achète de la drogue comme on achète un livre. »
plan('silkroad', 5.0, ['-i', os.path.join(DOS, 'silkroad.mp4')], f"[0]{cadre},{base}")
# 5 · « Livrée par la poste. »
plan('colis', 2.0, ['-ss', '1', '-i', os.path.join(DL, STOCK['colis'])], f"[0]{cadre},eq=saturation=.75:brightness=-.04,{base}")
# 6 · « Payée en bitcoins. »
plan('bitcoin', 2.3, ['-ss', '2', '-i', os.path.join(DL, STOCK['bitcoin'])], f"[0]{cadre},eq=saturation=.8,{base}")
# 7 · « Sur le site, personne ne connaît son vrai nom. On l'appelle seulement… Dread Pirate Roberts. »
plan('dpr', 8.1, ['-i', os.path.join(DOS, 'dpr.mp4')], f"[0]{cadre},{base}")
# 8 · « En deux ans, plus d'un milliard de dollars de ventes passent par Silk Road. »
plan('compteur', 4.2, ['-i', os.path.join(DOS, 'compteur.mp4')], f"[0]{cadre},{base}")
# 9 · « Et quelque part, une équipe du FBI cherche l'homme derrière le masque. »
plan('fbi', 5.2, ['-ss', '1', '-i', os.path.join(DL, STOCK['ecran_nuit'])], f"[0]{cadre},eq=saturation=.45:brightness=-.08,colorbalance=bs=.12:bm=.06,fade=out:st=4.6:d=0.6,{base}")

liste = os.path.join(DOS, 'liste.txt'); open(liste, 'w').write(''.join(f"file '{p}'\n" for p, _ in plans))
TOTAL = sum(d for _, d in plans)
vo = os.path.join(V, 'voix', 'VO_complete_SilkRoad.mp3'); mus = os.path.join(V, 'montage', 'elements', 'musique.wav')
sortie = os.path.join(V, 'rendu', 'silk-road_partie2' + ('' if FINAL else '_brouillon') + SUF + '.mp4')
run(['-f', 'concat', '-safe', '0', '-i', liste, '-i', vo, '-i', mus, '-filter_complex',
     # voix + lit musical (pulsation/tic-tac de la musique validée, 18 → 48 s, en boucle) qui s'efface sous la voix
     f"[1]atrim={VO0}:{VO1},asetpts=N/SR/TB,aformat=channel_layouts=stereo,volume=1.15,asplit[vo][sc];"
     f"[2]atrim=18:48,asetpts=N/SR/TB,aloop=loop=2:size=1440000,atrim=0:{TOTAL},volume=0.45[m];"
     f"[m][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];[vo][md]amix=2:normalize=0,alimiter=limit=0.9[a]",
     '-map', '0:v', '-map', '[a]', '-vf', f"noise=alls=2:allf=t,vignette=PI/6,pad={W}:{W*9//16}:0:({W*9//16}-{H})/2:black",
     '-c:v', 'libx264', '-crf', '18' if not FINAL else '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', str(TOTAL), sortie])
print('OK', sortie, round(TOTAL, 1), 's')
