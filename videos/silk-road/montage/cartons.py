# Cartons [CODE] de la minute : titre (0.8), date (0.9), zoom dans l'écran (1.2).
# Sortie : montage/elements/ecran_zoom.mp4 (1920×804, 30 i/s). Usage : python -I cartons.py
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

# (titre et date : voir titres.py)

# 1.2 Zoom lent dans l'écran, vers le tableau de bord, 7 s
z = "(1.25+.35*t/7)"
run(['-stream_loop', '1', '-i', os.path.join(HERE, '..', 'ecran', 'ecran.mp4'), '-t', '7', '-vf',
     f"fps=30,scale=w='trunc(1920*{z}/2)*2':h=-2:eval=frame,crop=1920:804:x='(iw-ow)*(.5+.35*t/7)':y='(ih-oh)/2',setsar=1",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(E, 'ecran_zoom.mp4')])
print('OK')
