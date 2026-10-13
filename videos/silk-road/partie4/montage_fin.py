# Parties 4 (la diversion), 5 (le procès) et 6 (clôture) — VO_complete 191,5 → 304,6 s + carton final.
# Calé sur la transcription voix/transcription_192-305.md. Usage : python -I montage_fin.py [final]
import subprocess, os, sys, json
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'outils'))
from etalonnage import ETALONNAGE as E, FINITION
F = r"C:\ffmpeg\bin\ffmpeg.exe"; HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..')
FINAL = 'final' in sys.argv; W, H, FPS = (1920, 804, 30) if FINAL else (960, 402, 15)
DOS = os.path.join(HERE, 'final' if FINAL else 'brouillon'); os.makedirs(DOS, exist_ok=True)
DL = r"C:\Users\HP\Downloads\TRU Stories"
V4 = r"C:\Users\HP\Documents\Codex\2026-10-12\files-mentioned-by-the-user-silk\outputs\production_v4\silk-road_minute_v4.mp4"
ECRAN = os.path.join(V, 'montage', 'elements', 'ecran_zoom.mp4')
VO0 = 191.5; k = W / 1920
ETIQ = json.load(open(os.path.join(HERE, 'etiquettes.json'), encoding='utf8')) if os.path.exists(os.path.join(HERE, 'etiquettes.json')) else {}

def run(a): subprocess.run([F, '-v', 'error', '-y'] + a, check=True)
def police(n, s): return ImageFont.truetype('C:/Windows/Fonts/' + n, max(10, int(s * k)))
def calque(nom, dessin):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dessin(ImageDraw.Draw(im)); p = os.path.join(DOS, nom + '.png'); im.save(p); return p
def bas_gauche(nom, petit, grand, rouge=False):
    return calque(nom, lambda d: (d.text((int(120 * k), H - int(190 * k)), ' '.join(petit.upper()), font=police('segoeuil.ttf', 24), fill=(215, 215, 215, 235)),
                                  d.text((int(118 * k), H - int(150 * k)), grand, font=police('segoeuisl.ttf', 62), fill=(225, 50, 40, 255) if rouge else (245, 245, 245, 255))))
def carton(nom, petit, grand, sous=None):
    def dessin(d):
        d.rectangle((0, 0, W, H), fill=(11, 12, 14, 255))
        d.text((W / 2, H * .38), ' '.join(petit.upper()), font=police('segoeuil.ttf', 24), fill=(150, 150, 150, 255), anchor='ms')
        d.text((W / 2, H * .55), grand, font=police('georgiai.ttf', 78), fill=(238, 238, 238, 255), anchor='ms')
        if sous: d.text((W / 2, H * .68), sous, font=police('georgiai.ttf', 44), fill=(200, 200, 200, 255), anchor='ms')
    return calque(nom, dessin)
def etiquettes(nom, plan):
    """Étiquettes noires à bord blanc déchiré, aux positions calculées dans Blender (etiquettes.json)."""
    def dessin(d):
        f = police('consolab.ttf', 30)
        for texte, x, y in ETIQ.get(plan, []):
            cx, cy = x * W, y * H - 46 * k; tw = d.textlength(texte, font=f); pad = 16 * k
            r = (cx - tw / 2 - pad, cy - 26 * k, cx + tw / 2 + pad, cy + 26 * k)
            d.rectangle((r[0] - 6 * k, r[1] - 6 * k, r[2] + 6 * k, r[3] + 6 * k), fill=(244, 244, 244, 255))
            d.rectangle(r, fill=(17, 17, 17, 255)); d.text((cx, cy), texte, font=f, fill=(242, 242, 242, 255), anchor='mm')
            d.polygon([(cx - 12 * k, r[3] + 6 * k), (cx + 12 * k, r[3] + 6 * k), (cx, r[3] + 22 * k)], fill=(244, 244, 244, 255))
    return calque(nom, dessin)
def liste(nom, lignes):
    """Une ligne de la liste (✓ blanc / ✗ rouge) — calques cumulés."""
    def dessin(d):
        for i, (txt, ok) in enumerate(lignes):
            y = H * .32 + i * 74 * k
            d.text((W * .30, y), '✓' if ok else '✗', font=police('seguisym.ttf', 54), fill=(240, 240, 240, 255) if ok else (225, 50, 40, 255), anchor='lm')
            d.text((W * .36, y), txt, font=police('segoeuisl.ttf', 50), fill=(240, 240, 240, 255), anchor='lm')
    return calque(nom, dessin)

base = f"fps={FPS},setsar=1"; cadre = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
v4crop = f"crop=1920:804:0:138,scale={W}:{H}"
plans = []
def plan(nom, d, entree, vf):
    out = os.path.join(DOS, f'f{len(plans):02d}_{nom}.mp4')
    run(entree + ['-t', str(d), '-filter_complex', vf, '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out]); plans.append((out, d))
def blender(nom, d, calques=()):
    """Plan rendu par plans_blender.py (images PNG) + calques éventuels (étiquettes), avec leurs fenêtres d'affichage ENABLE[nom]."""
    src = ['-framerate', str(FPS), '-i', os.path.join(DOS, nom, '%04d.png')] + sum((['-i', c] for c in calques), [])
    vf, cur = f"[0]{cadre}", None
    for j, en in enumerate(ENABLE.get(nom, [''] * len(calques))):
        vf += f"[a{j}];[a{j}][{j + 1}]overlay" + (f"={en}" if en else '')
    plan(nom, d, src, vf + f",{base}")
ENABLE = {}

# ───────── PARTIE 4 · LA DIVERSION ─────────
# « 1er octobre 2013. Un mardi après-midi, » : retour à la plongée validée (v4)
t = bas_gauche('t_date', 'Glen Park · un mardi après-midi', '1er octobre 2013')
plan('plongee', 6.7, ['-ss', '9', '-t', '4', '-i', V4, '-i', t], f"[0]{v4crop},setpts=1.675*PTS[v];[v][1]overlay=enable='gte(t,0.6)',{base}")
# « Ross Ulbricht est connecté. Il gère son site depuis une table… » : épaule + écran (v4)
plan('epaule', 6.3, ['-ss', '23.5', '-t', '6', '-i', V4], f"[0]{v4crop},setpts=1.05*PTS,{base}")
# « Autour de lui, des agents du FBI, en civil. Ils attendent le bon moment. »
ENABLE['agents'] = ["enable='gte(t,1.3)'"]; blender('agents', 7.1, calques=[etiquettes('e_agents', 'agents')])
# « Il faut qu'il soit connecté. Il faut que l'ordinateur reste ouvert et il faut l'éloigner de son clavier. »
l1 = liste('l1', [('il est connecté', True)]); l2 = liste('l2', [('il est connecté', True), ("l'ordinateur est ouvert", True)])
l3 = liste('l3', [('il est connecté', True), ("l'ordinateur est ouvert", True), ('loin de son clavier', False)])
plan('conditions', 6.0, ['-i', ECRAN, '-i', l1, '-i', l2, '-i', l3],
     f"[0]{cadre},boxblur=12,eq=brightness=-.28:saturation=.4[v];[v][1]overlay=enable='between(t,0,1.7)'[a];[a][2]overlay=enable='between(t,1.7,3.7)'[b];[b][3]overlay=enable='gte(t,3.7)',{base}")
# « Alors, derrière lui, un homme et une femme se mettent à se disputer. Ce sont deux agents du FBI. »
ENABLE['dispute'] = ["enable='gte(t,5.2)'"]; blender('dispute', 7.7, calques=[etiquettes('e_dispute', 'dispute')])
# « Ross se retourne. Une seconde. Une seule. »
blender('retourne', 5.0)
# « Et pendant cette seconde, les agents le saisissent. L'ordinateur reste ouvert, déverrouillé. » (ralenti)
blender('saisie', 6.1)
# « Un agent spécialiste, Thomas Kiernan, le garde allumé pendant des heures pour que rien ne se chiffre. » (Three.js)
plan('kiernan', 6.7, ['-i', os.path.join(DOS, 'kiernan.mp4')], f"[0]{cadre},{base}")
# « Les lecteurs autour de lui se lèvent. Ce n'était pas des lecteurs. »
blender('debout', 5.8)
# « L'homme le plus recherché du dark web vient d'être arrêté… »
blender('cercle', 3.4)
# « … dans le rayon science-fiction. » : le panneau (v4)
plan('panneau', 2.5, ['-ss', '3.0', '-t', '2', '-i', V4], f"[0]{v4crop},setpts=1.25*PTS,{base}")
# « Sur l'écran, tout est là. Les comptes, les messages, le journal de bord de Silk Road. »
mots = [bas_gauche('w1', 'Sur l\'écran', 'les comptes'), bas_gauche('w2', 'Sur l\'écran', 'les messages'), bas_gauche('w3', 'Sur l\'écran', 'le journal de bord', True)]
plan('ecran', 9.3, ['-i', ECRAN] + sum((['-i', m] for m in mots), []),
     f"[0]{cadre},setpts=1.33*PTS,eq=brightness=-.06[v];[v][1]overlay=enable='between(t,2.7,4.1)'[a];[a][2]overlay=enable='between(t,4.1,5.8)'[b];[b][3]overlay=enable='gte(t,5.8)',fade=out:st=8.5:d=0.8,{base}")
# ───────── PARTIE 5 · LE PROCÈS ─────────
t = bas_gauche('t_ny', 'New York', 'février 2015')
plan('tribunal', 3.6, ['-ss', '2', '-i', os.path.join(DL, 'fb3d1c70e4969f2df7555cfe4095c753.mp4'), '-i', t], f"[0]{cadre},{E['nuit_enquete']}[v];[v][1]overlay,{base}")
plan('verdict', 4.2, ['-loop', '1', '-i', carton('c_verdict', 'Verdict', 'Coupable', 'des sept chefs d\'accusation')], f"[0]fade=in:d=0.3,{base}")
t = bas_gauche('t_peine', '29 mai 2015', 'perpétuité · sans libération', True)
plan('barreaux', 7.3, ['-ss', '1', '-i', os.path.join(DL, '5243246-hd_1920_1080_24fps.mp4'), '-i', t], f"[0]{cadre},{E['tech_froide']}[v];[v][1]overlay=enable='gte(t,1.4)',{base}")
t = bas_gauche('t_31', 'Ross Ulbricht', '31 ans')
plan('ross31', 2.7, ['-loop', '1', '-i', os.path.join(DL, 'portrait ross'), '-i', t],
     f"[0]scale={W*2}:-2,zoompan=z='1.1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih*0.4-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},hue=s=0,eq=contrast=1.1[v];[v][1]overlay,{base}")
# ───────── PARTIE 6 · CLÔTURE ─────────
t = bas_gauche('t_10ans', 'Pendant', 'plus de dix ans')
plan('prison', 4.1, ['-ss', '12', '-i', os.path.join(DL, '5243246-hd_1920_1080_24fps.mp4'), '-i', t], f"[0]{cadre},{E['tech_froide']},hue=s=0[v];[v][1]overlay,{base}")
t = bas_gauche('t_grace', '21 janvier 2025', 'grâce présidentielle')
plan('grace', 7.1, ['-loop', '1', '-i', os.path.join(DL, 'Screenshot 2026-10-12 223305.png'), '-i', t],
     f"[0]scale={W}:-2,pad={W}:{H*2}:0:(oh-ih)/3:color=white,zoompan=z='1.0+0.0007*on':x='iw/2-(iw/zoom/2)':y='ih*0.33-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}[v];[v][1]overlay=enable='gte(t,0.8)',{base}")
t = bas_gauche('t_libre', 'Ross Ulbricht', 'libre')
plan('libre', 4.0, ['-loop', '1', '-i', os.path.join(DL, 'Screenshot 2026-10-12 223252.png'), '-i', t],
     f"[0]scale={W*2}:-2,zoompan=z='1.0+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih*0.45-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},{E['souvenir']}[v];[v][1]overlay,{base}")
# « Mais une question reste : un empire bâti pour être invisible est tombé à cause d'une seconde d'inattention. »
blender('table_vide', 7.5)
plan('fin', 5.0, ['-loop', '1', '-i', carton('c_fin', 'TRU STORIES', 'Un empire invisible.', 'Une seconde d\'inattention.')], f"[0]fade=in:d=0.6,fade=out:st=4.2:d=0.8,{base}")

liste_f = os.path.join(DOS, 'liste_fin.txt'); open(liste_f, 'w').write(''.join(f"file '{p}'\n" for p, _ in plans))
TOTAL = sum(d for _, d in plans)
vo = os.path.join(V, 'voix', 'VO_complete_SilkRoad.mp3'); mus = os.path.join(V, 'montage', 'elements', 'musique.wav')
sortie = os.path.join(V, 'rendu', 'silk-road_fin' + ('' if FINAL else '_brouillon') + '.mp4')
run(['-f', 'concat', '-safe', '0', '-i', liste_f, '-i', vo, '-i', mus, '-filter_complex',
     f"[1]atrim={VO0},asetpts=N/SR/TB,aformat=channel_layouts=stereo,volume=1.15,apad,asplit[vo][sc];"
     f"[2]atrim=18:48,asetpts=N/SR/TB,aloop=loop=4:size=1440000,atrim=0:{TOTAL},volume=0.45,afade=t=out:st={TOTAL - 4}:d=4[m];"
     f"[m][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];[vo][md]amix=2:normalize=0,alimiter=limit=0.9,atrim=0:{TOTAL}[a]",
     '-map', '0:v', '-map', '[a]', '-vf', f"{FINITION},pad={W}:{W*9//16}:0:({W*9//16}-{H})/2:black",
     '-c:v', 'libx264', '-crf', '18' if not FINAL else '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', str(TOTAL), sortie])
print('OK', sortie, round(TOTAL, 1), 's')
