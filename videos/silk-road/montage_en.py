# Version anglaise : recale chaque partie d'une vidéo FR sur la voix anglaise (Nathan).
# Usage : python -I montage_en.py                 → depuis le montage CapCut de Mo (textes FR)       → rendu/silk-road_EN.mp4
#         python -I montage_en.py rendu/_video_EN.mp4 → depuis notre vidéo aux textes traduits (sans son) → rendu/silk-road_FULL_EN.mp4
# Cold open intact (0–18 s), puis chaque partie est accélérée/ralentie pour tomber sur la voix EN.
import subprocess, os, sys
F = r"C:\ffmpeg\bin\ffmpeg.exe"; HERE = os.path.dirname(os.path.abspath(__file__))
NOTRE = len(sys.argv) > 1
SRC = os.path.join(HERE, sys.argv[1]) if NOTRE else r"C:\Users\HP\Downloads\TRU Stories\Modifier et finale\Ross ulbrich.mp4"
VO = os.path.join(HERE, 'voix', 'VO_EN_Nathan.mp3'); MUS = os.path.join(HERE, 'montage', 'elements', 'musique.wav')
# débuts des parties p1…p6 + fin de voix : dans la vidéo FR source et dans la voix EN
FR = [18.0, 54.0, 93.2, 181.1, 252.0, 269.8, 292.3] if NOTRE else [18.0, 54.8, 94.0, 184.9, 254.6, 272.4, 294.8]
EN = [0.0, 33.3, 69.3, 146.7, 207.9, 223.1, 242.7]
CARTON = (297.7 if NOTRE else 300.07) - FR[-1]          # carton final, vitesse normale
TMP = os.path.join(HERE, 'rendu', '_en'); os.makedirs(TMP, exist_ok=True)
def run(a): subprocess.run([F, '-v', 'error', '-y'] + a, check=True)
seg = []
def morceau(a, b, duree):
    out = os.path.join(TMP, f'{len(seg):02d}.mp4'); k = duree / (b - a)
    run(['-ss', str(a), '-t', str(b - a), '-i', SRC, '-an', '-vf', f'setpts={k:.5f}*PTS,fps=30', '-t', str(duree),
         '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', out]); seg.append(out)
morceau(0, FR[0], FR[0])
for i in range(6): morceau(FR[i], FR[i + 1], EN[i + 1] - EN[i])
morceau(FR[-1], FR[-1] + CARTON, CARTON)
liste = os.path.join(TMP, 'liste.txt'); open(liste, 'w').write(''.join(f"file '{s}'\n" for s in seg))
TOTAL = FR[0] + EN[-1] + CARTON
D = int(FR[0] * 1000)
# son du cold open : celui du montage CapCut, ou (notre vidéo) la nappe/battement de la musique validée
intro = (f"[1:a]atrim=0:{FR[0]},afade=t=out:st={FR[0] - 1.5}:d=1.5[intro];" if not NOTRE
         else f"[3:a]atrim=0:{FR[0]},asetpts=N/SR/TB,volume=0.55,afade=t=out:st={FR[0] - 1.5}:d=1.5[intro];")
run(['-f', 'concat', '-safe', '0', '-i', liste, '-t', str(FR[0]), '-i', SRC if not NOTRE else MUS, '-i', VO, '-i', MUS, '-filter_complex',
     intro +
     f"[2:a]adelay={D}|{D},volume=1.1,asplit[vo][sc];"
     f"[3:a]atrim=18:48,asetpts=N/SR/TB,aloop=loop=9:size=1440000,atrim=0:{TOTAL - FR[0]},volume=0.4,"
     f"adelay={D}|{D},afade=t=out:st={TOTAL - 4}:d=4[m];"
     f"[m][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[md];"
     f"[intro][vo][md]amix=3:normalize=0,alimiter=limit=0.9,atrim=0:{TOTAL}[a]",
     '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(TOTAL),
     os.path.join(HERE, 'rendu', 'silk-road_FULL_EN.mp4' if NOTRE else 'silk-road_EN.mp4')])
print('OK', round(TOTAL, 1), 's')
