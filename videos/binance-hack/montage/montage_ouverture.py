# Montage de l'ouverture Binance (0 → 85 s) : cold open muet 13 s → impact + titre → date → voix (partie 1) avec silence de tension avant « Entrée. »
# Plans 3D : séquences PNG rendues à 8 i/s (anim/<plan>/0000.png…), interpolées à 24 i/s et étirées à la durée voulue.
# Plans [CODE] : code/plans.html capturé image par image. Son : musique_binance.py + voix (vo_complete.mp3, partie 1).
import os, subprocess, shutil
from playwright.sync_api import sync_playwright
ANIM = '/home/claude/anim'; CODE = '/home/claude/true_stories/videos/binance-hack/code/plans.html'
HACK = '/home/claude/true_stories/videos/binance-hack/code/ecran_hacker.html'
VOIX = '/home/claude/voix/vo_complete.mp3'; MUS = ANIM + '/musique.wav'
W, H, FPS = 1280, 536, 24; TMP = ANIM + '/seg'; os.makedirs(TMP, exist_ok=True)
def ff(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)

# (début, fin, type, paramètres)
#  '3d'   : (plan, u0, u1, à_l'envers)  portion u0→u1 de la séquence
#  'code' : (scène, t0, t1)             temps de l'animation HTML (secondes) à étirer sur la durée
#  'noir' : ()
TL = [
 (0.0, 0.8, 'noir', ()),
 (0.8, 3.5, '3d', ('A_entree', 0, 1, False)),
 (3.5, 5.5, '3d', ('B_passe', 0, .45, False)),
 (5.5, 8.0, '3d', ('C_montee', 0, 1, False)),
 (8.0, 10.5, '3d', ('D_dos', 0, 1, False)),
 (10.5, 12.0, 'hack', (1.5, 3.6, (0, 138, 1920, 804), (0, 138, 1920, 804))),
 (12.0, 13.0, '3d', ('F_entree', 0, 1, False)),
 (13.0, 16.2, 'code', ('titre', 0, 3.2)),
 (16.2, 22.4, 'code', ('date', 0, 6.2)),
 (22.4, 26.4, '3d', ('I_dessus', 0, .5, False)),
 (26.4, 30.4, '3d', ('J_face', 0, 1, False)),
 (30.4, 33.22, '3d', ('K_facades', 0, 1, False)),
 (33.22, 37.44, '3d', ('C_montee', 0, 1, False)),
 (37.44, 40.57, '3d', ('G_large', 0, .5, False)),
 (40.57, 46.88, '3d', ('L_ecran', 0, 1, False)),
 (46.88, 49.4, 'hack', (0, 2.6, (0, 138, 1920, 804), (300, 160, 1500, 628))),
 (49.4, 54.6, '3d', ('D_dos', 0, 1, False)),
 (54.6, 57.13, '3d', ('F_entree', 0, .5, False)),
 (57.13, 63.37, 'hack', (2.4, 8.8, (0, 138, 1920, 804), (10, 46, 640, 268))),
 (63.37, 66.3, '3d', ('D_dos', .3, 1, True)),
 (66.3, 67.5, 'noir', ()),
 (67.5, 69.0, '3d', ('F_entree', .3, 1, False)),
 (69.0, 79.1, 'code', ('montant', 0, 10.1)),
 (79.1, 83.2, '3d', ('C_montee', 0, 1, True)),
 (83.2, 85.0, 'noir', ()),
]

def seg_noir(i, d):
    out = f'{TMP}/{i:02d}.mp4'; ff('-f', 'lavfi', '-i', f'color=c=black:s={W}x{H}:r={FPS}', '-frames:v', str(round(d * FPS)), '-pix_fmt', 'yuv420p', '-c:v', 'libx264', out); return out

def seg_3d(i, d, plan, u0, u1, envers):
    src = sorted(f for f in os.listdir(f'{ANIM}/{plan}') if f.endswith('.png')); n = len(src)
    a, b = int(round(u0 * (n - 1))), max(int(round(u0 * (n - 1))) + 2, int(round(u1 * (n - 1))) + 1)
    sel = src[a:b][::-1] if envers else src[a:b]
    lst = f'{TMP}/{i:02d}_imgs'; shutil.rmtree(lst, ignore_errors=True); os.makedirs(lst)
    for k, f in enumerate(sel): os.symlink(f'{ANIM}/{plan}/{f}', f'{lst}/{k:04d}.png')
    src_d = len(sel) / 8.0; vitesse = src_d / d                # < 1 = ralenti
    out = f'{TMP}/{i:02d}.mp4'
    vf = (f"setpts={1/vitesse:.4f}*PTS,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
          f"scale={W}:{H}:flags=lanczos,tpad=stop_mode=clone:stop_duration={d:.3f},format=yuv420p")
    ff('-framerate', '8', '-i', f'{lst}/%04d.png', '-vf', vf, '-frames:v', str(round(d * FPS)), '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', out)
    return out

def seg_hack(i, d, pg, t0, t1, c0, c1):
    rep = f'{TMP}/{i:02d}_hack'; shutil.rmtree(rep, ignore_errors=True); os.makedirs(rep)
    n = max(1, round(d * FPS)); pg.set_viewport_size({'width': 1920, 'height': 1080})
    for k in range(n):
        u = k / max(1, n - 1); e = u * u * (3 - 2 * u); t = t0 + (t1 - t0) * u
        x, y, w, h = [a + (b - a) * e for a, b in zip(c0, c1)]
        pg.goto(f'file://{HACK}?t={t:.3f}'); pg.wait_for_function('window.FRAME_PRET===true')
        pg.screenshot(path=f'{rep}/{k:04d}.jpg', type='jpeg', quality=92, clip={'x': x, 'y': y, 'width': w, 'height': h})
    pg.set_viewport_size({'width': 1920, 'height': 804})
    out = f'{TMP}/{i:02d}.mp4'
    ff('-framerate', str(FPS), '-i', f'{rep}/%04d.jpg', '-vf', f'scale={W}:{H}:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '17', out); return out

def seg_code(i, d, pg, scene, t0, t1):
    rep = f'{TMP}/{i:02d}_code'; shutil.rmtree(rep, ignore_errors=True); os.makedirs(rep)
    n = max(1, round(d * FPS))
    for k in range(n):
        t = t0 + (t1 - t0) * k / max(1, n - 1)
        pg.goto(f'file://{CODE}?s={scene}&t={t:.3f}'); pg.wait_for_function('window.FRAME_PRET===true')
        pg.screenshot(path=f'{rep}/{k:04d}.jpg', type='jpeg', quality=90)
    out = f'{TMP}/{i:02d}.mp4'
    ff('-framerate', str(FPS), '-i', f'{rep}/%04d.jpg', '-vf', f'scale={W}:{H},format=yuv420p', '-c:v', 'libx264', '-crf', '17', out); return out

morceaux = []
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 804})
    for i, (a, b, typ, par) in enumerate(TL):
        d = (round(b * FPS) - round(a * FPS)) / FPS
        if typ == 'noir': morceaux.append(seg_noir(i, d))
        elif typ == '3d': morceaux.append(seg_3d(i, d, *par))
        elif typ == 'hack': morceaux.append(seg_hack(i, d, pg, *par))
        else: morceaux.append(seg_code(i, d, pg, *par))
        print('SEG', i, typ, par[0] if par else '', round(d, 2), flush=True)
    br.close()
open(f'{TMP}/liste.txt', 'w').write(''.join(f"file '{m}'\n" for m in morceaux))
ff('-f', 'concat', '-safe', '0', '-i', f'{TMP}/liste.txt', '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', f'{TMP}/image.mp4')

# voix : partie 1 (0 → 64 s) découpée au silence avant « Entrée. » (48,30 s) et décalée : 18 s puis 67,5 s
ff('-i', VOIX, '-filter_complex',
   "[0]atrim=0:48.30,asetpts=PTS-STARTPTS,adelay=18000|18000[v1];"
   "[0]atrim=48.30:64.0,asetpts=PTS-STARTPTS,adelay=67500|67500[v2];"
   "[v1][v2]amix=inputs=2:normalize=0,apad=whole_dur=85[voix]", '-map', '[voix]', '-ar', '48000', '-ac', '2', f'{TMP}/voix.wav')
# mixage voix + musique (la musique baisse légèrement sous la voix) + finition image (grain + vignette, charte)
ff('-i', f'{TMP}/image.mp4', '-i', f'{TMP}/voix.wav', '-i', MUS, '-filter_complex',
   "[1]asplit[va][vb];[2]volume=0.55[m];[m][va]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[vb][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a];"
   "[0]noise=alls=2:allf=t,vignette=PI/6[v]",
   '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-t', '85',
   '/home/claude/anim/binance_ouverture_v4.mp4')
print('FINI')
