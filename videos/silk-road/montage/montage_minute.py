# Assemble la première minute (v3 : entrée de 9 s, voix à 0:18) dans la salle de Glen Park. Usage : python -I montage_minute.py
# Image : plans 3D (rendu/plans/<plan>/, numérotés sur la timeline de 3d/minute.py) + titres/écran (elements/),
#         grain très léger, vignette, image 2,39:1 dans un 1920×1080.
# Son : VO_complete (0 → 64 s) + musique de tension (musique.py) + ambiance de salle.
# Sortie : rendu/silk-road_minute.mp4 (non versionné : seule la vidéo finale ira sur GitHub).
import subprocess, os, sys
F = r"C:\ffmpeg\bin\ffmpeg.exe"; HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..')
W, H = 1920, 804
PLANS = os.path.join(V, 'rendu', 'plans'); E = os.path.join(HERE, 'elements')
# (source, image de début sur la timeline 3D ou None, durée en s) — les plans 3D se suivent sans trou sur la timeline
SEQ = [('c1_salle', 1, 3), ('c2_panneau', 91, 2), ('c3_visage', 151, 4), ('c4_zenith', 271, 4),
       ('titre.mp4', None, 3), ('date.mp4', None, 2),
       ('p07_travelling', 541, 5.5), ('p08_epaule', 706, 6), ('ecran_zoom.mp4', None, 7),
       ('p09_salle', 1096, 5.4), ('p10_poitrine', 1258, 6.1), ('p11_pousse', 1441, 3.5)]
DECALAGE_VO = 12.0   # on retire 12 s du silence de tête de la voix : elle démarre à 0:18
TOTAL = sum(d for _, _, d in SEQ)

def run(a): subprocess.run([F, '-v', 'error', '-y'] + a, check=True)
os.makedirs(os.path.join(HERE, 'tmp'), exist_ok=True); morceaux = []
for i, (src, f0, d) in enumerate(SEQ):
    out = os.path.join(HERE, 'tmp', f'{i:02d}.mp4'); morceaux.append(out)
    if f0 is None: entree = ['-i', os.path.join(E, src)]
    else: entree = ['-framerate', '30', '-start_number', str(f0), '-i', os.path.join(PLANS, src, '%04d.png')]
    run(entree + ['-vf', f'scale={W}:{H}:flags=lanczos,fps=30,tpad=stop_mode=clone:stop_duration=1,setsar=1',
                  '-t', str(d), '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p', out])
liste = os.path.join(HERE, 'tmp', 'liste.txt')
open(liste, 'w').write(''.join(f"file '{m}'\n" for m in morceaux))

vo = os.path.join(V, 'voix', 'VO_complete_SilkRoad.mp3'); musique = os.path.join(E, 'musique.wav')
son = os.path.join(HERE, 'tmp', 'son.wav')
run(['-i', vo, '-i', musique, '-f', 'lavfi', '-i', f'anoisesrc=color=brown:amplitude=0.5:d={TOTAL}',
     '-filter_complex',
     f"[0]atrim={DECALAGE_VO}:{DECALAGE_VO + TOTAL},asetpts=N/SR/TB,aformat=channel_layouts=stereo,volume=1.15,asplit[vo][vosc];"
     "[1]volume=0.55[mus];"
     "[2]lowpass=f=350,volume=0.035,aformat=channel_layouts=stereo[amb];"
     "[mus][vosc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[musd];"   # la musique s'efface sous la voix
     f"[vo][musd][amb]amix=3:normalize=0,alimiter=limit=0.9,atrim=0:{TOTAL}[a]",
     '-map', '[a]', '-ar', '48000', son])

sortie = os.path.join(V, 'rendu', 'silk-road_minute.mp4')
run(['-f', 'concat', '-safe', '0', '-i', liste, '-i', son,
     '-vf', f"noise=alls=2:allf=t,vignette=PI/6,pad={W}:1080:0:(1080-{H})/2:black,fade=in:d=0.8,fade=out:st={TOTAL - .4}:d=0.4",
     '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-shortest', sortie])
print('OK', sortie)
