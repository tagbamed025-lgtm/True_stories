# Assemble la première minute (cold open + section 1) sur la voix off. Usage : python -I montage_minute.py [final]
# Image : plans 3D (rendu/plans/<plan>[_apercu]/) + cartons (elements/), grain, vignette, bandes 2,39:1 dans un 16:9.
# Son : VO_complete (0 → 64 s) + ambiance de salle + nappe grave qui se coupe net à la fin de la plongée (0.7) + impact du titre.
import subprocess, os, sys
F = r"C:\ffmpeg\bin\ffmpeg.exe"; HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..')
FINAL = 'final' in sys.argv; W, H = (1920, 804) if FINAL else (1280, 536)
PLANS = os.path.join(V, 'rendu', 'plans'); E = os.path.join(HERE, 'elements')
# (source, durée en s) — cale sur les respirations de la voix (VO à 30,0 s ; « Parce que cet homme… » à 60,7 s)
SEQ = [('p01_entree', 8), ('p02_assis', 5), ('p03_visage', 4), ('p04_zenith', 6),
       ('titre.mp4', 4), ('date.mp4', 3.5),
       ('p07_travelling', 5.5), ('p08_epaule', 6), ('ecran_zoom.mp4', 7),
       ('p09_salle', 5.4), ('p10_poitrine', 6.1), ('p11_pousse', 3.5)]
TOTAL = sum(d for _, d in SEQ)
COUPE_NAPPE = 23.0   # fin du plan 0.7

def run(a): subprocess.run([F, '-v', 'error', '-y'] + a, check=True)
os.makedirs(os.path.join(HERE, 'tmp'), exist_ok=True); morceaux = []
for i, (src, d) in enumerate(SEQ):
    out = os.path.join(HERE, 'tmp', f'{i:02d}.mp4'); morceaux.append(out)
    if src.endswith('.mp4'): entree = ['-i', os.path.join(E, src)]
    else: entree = ['-framerate', '30', '-i', os.path.join(PLANS, src + ('' if FINAL else '_apercu'), '%04d.png')]
    run(entree + ['-t', str(d), '-vf', f'scale={W}:{H},fps=30,tpad=stop_mode=clone:stop_duration=1,setsar=1',
                  '-t', str(d), '-an', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', out])
liste = os.path.join(HERE, 'tmp', 'liste.txt')
open(liste, 'w').write(''.join(f"file '{m}'\n" for m in morceaux))

# --- son -------------------------------------------------------------------
vo = os.path.join(V, 'voix', 'VO_complete_SilkRoad.mp3'); son = os.path.join(HERE, 'tmp', 'son.wav')
run(['-i', vo,
     '-f', 'lavfi', '-i', f'anoisesrc=color=brown:amplitude=0.5:d={TOTAL}',                               # ambiance de salle
     '-f', 'lavfi', '-i', f'sine=f=55:d={COUPE_NAPPE}', '-f', 'lavfi', '-i', f'sine=f=82.4:d={COUPE_NAPPE}',  # nappe grave
     '-f', 'lavfi', '-i', 'sine=f=42:d=2.5',                                                                # impact du titre
     '-f', 'lavfi', '-i', 'sine=f=1320:d=0.12',                                                             # bip de connexion (0.6)
     '-filter_complex',
     f"[0]atrim=0:{TOTAL},asetpts=N/SR/TB,volume=1.0[vo];"
     "[1]lowpass=f=400,volume=0.05[amb];"
     f"[2][3]amix=2,volume='0.5*t/{COUPE_NAPPE}':eval=frame,tremolo=f=0.25:d=0.4[nappe];"
     "[4]afade=t=out:st=0.05:d=2.4,volume=1.6,adelay=23000|23000[impact];"
     "[5]volume=0.25,adelay=13600|13600[bip];"
     f"[vo][amb][nappe][impact][bip]amix=5:normalize=0,alimiter=limit=0.9,atrim=0:{TOTAL}[a]",
     '-map', '[a]', '-ar', '48000', son])

# --- image + son ------------------------------------------------------------
sortie = os.path.join(V, 'rendu', 'silk-road_minute' + ('' if FINAL else '_apercu') + '.mp4')
H169 = W * 9 // 16
run(['-f', 'concat', '-safe', '0', '-i', liste, '-i', son,
     '-vf', f"noise=alls=7:allf=t,vignette=PI/5,pad={W}:{H169}:0:({H169}-{H})/2:black,fade=in:d=1,fade=out:st={TOTAL - .6}:d=0.6",
     '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', sortie])
print('OK', sortie)
