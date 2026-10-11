# Cartons [CODE] de la minute : titre (0.8), date (0.9), zoom dans l'écran (1.2).
# Sortie : montage/elements/*.mp4 (1280×536, 30 i/s). Usage : python -I cartons.py
import subprocess, os
F = r"C:\ffmpeg\bin\ffmpeg.exe"
HERE = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(HERE, 'elements'); os.makedirs(E, exist_ok=True)
GRAS = 'gras.ttf'; MONO = 'mono.ttf'   # copiées depuis C:/Windows/Fonts (ffmpeg n'aime pas « C: » dans les filtres)
import shutil; shutil.copy('C:/Windows/Fonts/bahnschrift.ttf', os.path.join(E, GRAS)); shutil.copy('C:/Windows/Fonts/consola.ttf', os.path.join(E, MONO))

def txt(nom, s):
    """Texte dans un fichier (évite l'échappement des apostrophes dans drawtext)."""
    p = os.path.join(E, nom + '.txt'); open(p, 'w', encoding='utf8').write(s)
    return nom + '.txt'   # chemin relatif : ffmpeg tourne dans elements/

def run(args): subprocess.run([F, '-v', 'error', '-y'] + args, check=True, cwd=E)

# 0.8 Titre : noir, apparition sèche, petit trait rouge
t1 = txt('t1', "L'EMPIRE À UN MILLIARD"); t2 = txt('t2', "PIÉGÉ DANS UNE BIBLIOTHÈQUE")
run(['-f', 'lavfi', '-i', 'color=black:s=1280x536:r=30:d=4', '-vf',
     f"drawtext=fontfile={GRAS}:textfile='{t1}':fontcolor=white:fontsize=58:x=(w-tw)/2:y=h/2-66:enable='gte(t,.15)',"
     f"drawtext=fontfile={GRAS}:textfile='{t2}':fontcolor=white:fontsize=58:x=(w-tw)/2:y=h/2+8:enable='gte(t,.15)',"
     "drawbox=x=(iw-120)/2:y=ih/2+90:w=120:h=3:color=0xd01818:t=fill:enable='gte(t,.4)',fade=out:st=3.5:d=0.5",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(E, 'titre.mp4')])

# 0.9 Date : machine à écrire
ligne = "SAN FRANCISCO  ·  MARDI 1ER OCTOBRE 2013"; dt = .06; f = []
for k in range(1, len(ligne) + 1):
    p = txt(f'd{k:02d}', ligne[:k]); fin = 99 if k == len(ligne) else .4 + k * dt
    f.append(f"drawtext=fontfile={MONO}:textfile='{p}':fontcolor=0xe8e8e8:fontsize=30:x=(w-{len(ligne)}*16.5)/2:y=(h-th)/2"
             f":enable='between(t,{.4 + (k - 1) * dt:.2f},{fin:.2f})'")
run(['-f', 'lavfi', '-i', 'color=black:s=1280x536:r=30:d=3.5', '-vf', ','.join(f) + ',fade=out:st=3.1:d=0.4',
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(E, 'date.mp4')])

# 1.2 Zoom lent dans l'écran, vers le tableau de bord, 7 s
z = "(1.25+.35*t/7)"
run(['-stream_loop', '1', '-i', os.path.join(HERE, '..', 'ecran', 'ecran.mp4'), '-t', '7', '-vf',
     f"fps=30,scale=w='trunc(1280*{z}/2)*2':h=-2:eval=frame,crop=1280:536:x='(iw-ow)*(.5+.35*t/7)':y='(ih-oh)/2',setsar=1",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(E, 'ecran_zoom.mp4')])
print('OK')
