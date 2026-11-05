# Fin de la vidéo : voix 1 (vo_complete 179,9 → 265,4 : CZ sur X → « Il en manque… trois. ») + voix 2 (vo_suite, p6 → p10).
# Silences de tension : avant « Trop tard. » (0,8 s), avant « trois. » (1,5 s), puis 2,2 s de noir + impact avant la voix 2. Titre final + noir.
import os, shutil, subprocess, wave
from urllib.parse import quote
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from playwright.sync_api import sync_playwright
ANIM = '/home/claude/anim'; R = '/home/claude/true_stories/videos/binance-hack/code/'
FOOT = '/mnt/user-data/attachments/320b0a0f-0a6b-5eaa-97cb-bc509def2206/'
VA, VB = '/home/claude/voix/vo_complete.mp3', '/home/claude/voix/vo_suite.mp3'
TMP = ANIM + '/et4'; os.makedirs(TMP, exist_ok=True); W, H, FPS = 1280, 536, 24
def ff(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
A0, SA1, DA1, SA2, DA2, AF = 179.9, 205.45, .8, 264.62, 1.5, 265.4
def gA(v): return v - A0 + (DA1 if v >= SA1 else 0) + (DA2 if v >= SA2 else 0)
OB = gA(AF) + 2.2; BF = 169.48
def gB(v): return OB + v
FIN_TITRE = gB(BF) + 4.5; T = FIN_TITRE + 1.5
F = {k: FOOT + v for k, v in {'capuche': '14a53b43-viatkinaviktoria_pindown.io_1793469151.mp4', 'serveurs': '1aeebce7-BestAfterEffectsTutorials_pindown.io_1793469299.mp4',
     'vert': '26e3e112-bchaib729_pindown.io_1793469178.mp4', 'ville': '520535af-themkpcaptain_pindown.io_1793468880.mp4', 'pieces': '54f7ed59-dezinejunkieArt_pindown.io_1793468742.mp4',
     'code': 'e14f3f18-georgehowell2020_pindown.io_1793469250.mp4', 'pluie': 'f69de8de-maskedtran_pindown.io_1793468966.mp4', 'lampes': 'fa474c37-Movies404_pindown.io_1793468995.mp4'}.items()}
Zc = {'x': 360, 'y': 150, 'width': 1200, 'height': 502}; Gl = {'x': 420, 'y': 176, 'width': 1080, 'height': 452}
J = {'x': 150, 'y': 120, 'width': 1400, 'height': 586}; Sc = {'x': 420, 'y': 90, 'width': 1080, 'height': 452}
By = {'x': 160, 'y': 40, 'width': 1600, 'height': 670}; Su = {'x': 900, 'y': 40, 'width': 1020, 'height': 427}
Pz = {'x': 300, 'y': 200, 'width': 1320, 'height': 552}; Mz = {'x': 200, 'y': 40, 'width': 1500, 'height': 628}
CIBLE = (16, 52, 620, 260); FLUX = (16, 700, 1100, 460)
PA = [
 (179.9, 180.88, ('three', 'telephone', 2.6, 3.6, None)),
 (180.88, 184.4, ('portrait', 'cz_reuters.png', '', '')),
 (184.4, 189.02, ('code', 'postcz', 0, 2, Pz)),
 (189.02, 193.97, ('foot', 'capuche', 1.0)),
 (193.97, 196.5, ('3d', 'X_crise', 0, .5, False)),
 (196.5, 199.99, ('3d', 'X_equipe', 0, 1, False)),
 (199.99, 205.45, ('code', 'reprise', 0, 3, None)),
 (205.45, 207.21, ('hack', 9.0, 9.8, CIBLE, CIBLE)),
 (207.21, 209.74, ('three', 'globe', 2.0, 4.6, Gl)),
 (209.74, 212.42, ('foot', 'pluie', 2.0)),
 (212.42, 214.49, ('foot', 'pieces', 5.0)),
 (214.49, 219.65, ('code', 'jauges', 0, 3, J)),
 (219.65, 221.95, ('code', 'jauges', 3, 4.5, J)),
 (221.95, 224.0, ('3d', 'X_crise', .5, 1, False)),
 (224.0, 226.51, ('code', 'jauges', 4.5, 6, J)),
 (226.51, 231.0, ('hack', 6.5, 9.0, FLUX, (16, 720, 900, 377))),
 (231.0, 236.14, ('code', 'aave', 0, 3.6, Zc)),
 (236.14, 239.43, ('code', 'suspendu', 0, 1.5, None)),
 (239.43, 241.89, ('code', 'suspendu', 1.5, 3.6, None)),
 (241.89, 247.49, ('portrait', 'yihe_rouge.png', 'Yi He', 'cofondatrice de Binance')),
 (247.49, 252.0, ('3d', 'X_equipe', 1, 0, True)),
 (252.0, 256.14, ('3d', 'X_crise', .2, .8, False)),
 (256.14, 259.5, ('portrait', 'cz_websummit.png', 'Changpeng Zhao', '« Ça fait mal, mais on survivra. »')),
 (259.5, 264.62, ('code', 'bilan', 0, 1.2, None)),
 (264.62, 265.4, ('code', 'bilan', 2.4, 3.0, None)),
]
PB = [
 (0, 2.37, ('foot', 'ville', 3.0)),
 (2.37, 5.5, ('code', 'marche', 0, 2.5, Mz)),
 (5.5, 7.4, ('foot', 'pieces', 7.0)),
 (7.4, 13.08, ('code', 'marche', 2.5, 5, Mz)),
 (13.08, 18.24, ('three', 'graphe', 0, 4, None)),
 (18.24, 21.0, ('code', 'schema', 0, .4, Sc)),
 (21.0, 25.72, ('art', 'art_forkast_laptop.png', '')),
 (25.72, 28.39, ('foot', 'vert', 3.0)),
 (28.39, 31.5, ('foot', 'code', 6.0)),
 (31.5, 34.0, ('three', 'cles', 0, 1.5, None)),
 (34.0, 37.5, ('3d', 'D_dos', 0, .7, False)),
 (37.5, 41.43, ('code', 'schema', 0, 1.4, Sc)),
 (41.43, 43.0, ('3d', 'S_serveurs', 0, .5, False)),
 (43.0, 44.91, ('code', 'schema', 1.4, 2.6, Sc)),
 (44.91, 48.35, ('3d', 'V_coffre', 0, .4, False)),
 (48.35, 51.68, ('envoi', 2.0, 5.0, .2, .3)),
 (51.68, 54.76, ('logo',)),
 (54.76, 56.21, ('foot', 'lampes', 2.0)),
 (56.21, 61.41, ('3d', 'W_matin', 0, 1, False)),
 (61.41, 64.41, ('foot', 'capuche', 4.0)),
 (64.41, 67.29, ('code', 'bybit', 0, 1.2, By)),
 (67.29, 70.52, ('code', 'bybit', 1.2, 2.4, By)),
 (70.52, 74.33, ('foot', 'code', 10.0)),
 (74.33, 77.5, ('code', 'bybit', 2.4, 4.5, By)),
 (77.5, 81.34, ('foot', 'vert', 6.0)),
 (81.34, 84.28, ('portrait', 'cz_sourire.png', '', '')),
 (84.28, 87.86, ('3d', 'F_entree', 0, 1, False)),
 (87.86, 90.89, ('three', 'tours', 2.4, 4.6, None)),
 (90.89, 95.35, ('portrait', 'richard_teng.png', 'Richard Teng', 'co-PDG de Binance')),
 (95.35, 98.2, ('three', 'cles', 2.3, 4.6, None)),
 (98.2, 100.25, ('3d', 'C_montee', 0, 1, False)),
 (100.25, 102.58, ('3d', 'L_ecran', 0, .5, False)),
 (102.58, 107.82, ('code', 'suspects', 0, 2.5, Su)),
 (107.82, 111.09, ('code', 'suspects', 2.5, 4.5, Su)),
 (111.09, 113.15, ('code', 'bybit', 3.5, 4.5, By)),
 (113.15, 117.0, ('art', 'art_infocrypto_bitget.png', '')),
 (117.0, 120.41, ('art', 'art_infocrypto_bitget_2.png', '')),
 (120.41, 123.5, ('foot', 'ville', 8.0)),
 (123.5, 132.47, ('compare', 0, 5.2)),
 (132.47, 135.33, ('code', 'maj', 0, 1.2, None)),
 (135.33, 143.09, ('code', 'maj', 1.2, 3.0, None)),
 (143.09, 146.48, ('code', 'maj', 3.0, 4.6, None)),
 (146.48, 148.32, ('foot', 'code', 14.0)),
 (148.32, 151.68, ('3d', 'V_coffre', .5, 1, False)),
 (151.68, 153.15, ('foot', 'pieces', 9.0)),
 (153.15, 155.4, ('3d', 'S_serveurs', .3, 1, False)),
 (155.4, 158.45, ('three', 'tours', 0, 3, None)),
 (158.45, 161.03, ('3d', 'W_matin', .6, 1, False)),
 (161.03, 162.32, ('3d', 'A_entree', 0, .6, False)),
 (162.32, 163.83, ('3d', 'B_passe', 0, .6, False)),
 (163.83, 166.34, ('3d', 'C_montee', 0, 1, False)),
 (166.34, 169.48, ('3d', 'L_ecran', .4, 1, False)),
]
evts = [(gA(a), gA(b) - (DA1 if b == SA1 else DA2 if b == SA2 else 0), s) for a, b, s in PA]
evts += [(gA(SA1) - DA1, gA(SA1), ('noir',)), (gA(SA2) - DA2, gA(SA2), ('noir',)), (gA(AF), OB, ('noir',))]
evts += [(gB(a), gB(b), s) for a, b, s in PB] + [(gB(BF), FIN_TITRE, ('code', 'final', 0, 3.5, None)), (FIN_TITRE, T, ('noir',))]
AV = .4
evts = [(max(0, a - AV) if i else a, b - AV, s) for i, (a, b, s) in enumerate(sorted(evts, key=lambda e: e[0]))]
evts[-1] = (evts[-1][0], T, evts[-1][2])
def E(u): return u * u * (3 - 2 * u)
def seg_noir(out, n): ff('-f', 'lavfi', '-i', f'color=c=black:s={W}x{H}:r={FPS}', '-frames:v', str(n), '-pix_fmt', 'yuv420p', '-c:v', 'libx264', out)
def seg_3d(out, n, plan, u0, u1, envers):
    src = sorted(f for f in os.listdir(f'{ANIM}/{plan}') if f.endswith('.png')); k = len(src)
    a, b = sorted((int(round(u0 * (k - 1))), int(round(u1 * (k - 1)))))
    sel = src[a:max(b + 1, a + 2)]; sel = sel[::-1] if envers else sel
    lst = out + '_i'; shutil.rmtree(lst, ignore_errors=True); os.makedirs(lst)
    for i, f in enumerate(sel): os.symlink(f'{ANIM}/{plan}/{f}', f'{lst}/{i:04d}.png')
    d = n / FPS; v = (len(sel) / 8.0) / d
    ff('-framerate', '8', '-i', f'{lst}/%04d.png', '-vf', f'setpts={1/v:.4f}*PTS,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,scale={W}:{H}:flags=lanczos,tpad=stop_mode=clone:stop_duration={d:.3f},format=yuv420p',
       '-frames:v', str(n), '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', out)
def seg_foot(out, n, k, ss):
    crop = 'crop=iw*0.85:ih*0.85:0:ih*0.15,' if k == 'vert' else ''
    ff('-ss', str(ss), '-i', F[k], '-vf', f'{crop}scale={W}:-2,crop={W}:{H},fps={FPS},eq=saturation=.75:brightness=-.03,tpad=stop_mode=clone:stop_duration=5,format=yuv420p', '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '17', out)
def capture(pg, out, n, url_de):
    rep = out + '_c'; shutil.rmtree(rep, ignore_errors=True); os.makedirs(rep)
    for k in range(n):
        url, c = url_de(k / max(1, n - 1)); pg.goto(url); pg.wait_for_function('window.FRAME_PRET===true')
        pg.screenshot(path=f'{rep}/{k:04d}.jpg', type='jpeg', quality=92, **({'clip': c} if c else {}))
    ff('-framerate', str(FPS), '-i', f'{rep}/%04d.jpg', '-vf', f'scale={W}:{H}:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '17', out)
def lerpc(a, b, e): x, y, w, h = [p + (q - p) * e for p, q in zip(a, b)]; return {'x': x, 'y': y, 'width': w, 'height': h}
morceaux = []
with sync_playwright() as p:
    br = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']); pg = br.new_page(viewport={'width': 1920, 'height': 804})
    for i, (a, b, s) in enumerate(evts):
        n = round(b * FPS) - round(a * FPS); typ = s[0]; out = f'{TMP}/{i:03d}.mp4'
        if n <= 0: continue
        d = n / FPS
        if os.path.exists(out) and os.environ.get('REPRISE'): morceaux.append(out); continue
        if typ == 'noir': seg_noir(out, n)
        elif typ == '3d': seg_3d(out, n, *s[1:])
        elif typ == 'foot': seg_foot(out, n, *s[1:])
        elif typ == 'code': sc_, t0, t1, cz = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}plans.html?s={sc_}&t={t0+(t1-t0)*u:.3f}', cz))
        elif typ == 'three': sc_, t0, t1, cz = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}scenes3d.html?s={sc_}&t={t0+(t1-t0)*u:.3f}', cz))
        elif typ == 'compare': t0, t1 = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}compare.html?t={t0+(t1-t0)*u:.3f}', None))
        elif typ == 'envoi': t0, t1, z0, z1 = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}envoi.html?t={t0+(t1-t0)*u:.3f}&z={z0+(z1-z0)*E(u):.3f}', None))
        elif typ == 'logo': capture(pg, out, n, lambda u: (f'file://{R}logo.html?d={d:.2f}&t={u*d:.3f}', None))
        elif typ == 'art': img, hl = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}archive.html?img={img}&mode=article&d={d:.2f}&t={u*d:.3f}&hl={hl}', None))
        elif typ == 'portrait': img, nom, role = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}archive.html?img={img}&mode=portrait&d={d:.2f}&t={u*d:.3f}&nom={quote(nom)}&role={quote(role)}', None))
        elif typ == 'hack':
            t0, t1, c0, c1 = s[1:]; pg.set_viewport_size({'width': 1920, 'height': 1080})
            capture(pg, out, n, lambda u: (f'file://{R}ecran_hacker.html?t={t0+(t1-t0)*u:.3f}', lerpc(c0, c1, E(u))))
            pg.set_viewport_size({'width': 1920, 'height': 804})
        morceaux.append(out); print('SEG', i, typ, round(a, 2), flush=True)
    br.close()
open(f'{TMP}/l.txt', 'w').write(''.join(f"file '{m}'\n" for m in morceaux))
ff('-f', 'concat', '-safe', '0', '-i', f'{TMP}/l.txt', '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', f'{TMP}/image.mp4')
ms = lambda x: int(x * 1000)
ff('-i', VA, '-i', VB, '-filter_complex',
   f"[0]atrim={A0}:{SA1},asetpts=PTS-STARTPTS[a];[0]atrim={SA1}:{SA2},asetpts=PTS-STARTPTS,adelay={ms(gA(SA1))}|{ms(gA(SA1))}[b];"
   f"[0]atrim={SA2}:{AF},asetpts=PTS-STARTPTS,adelay={ms(gA(SA2))}|{ms(gA(SA2))}[c];[1]adelay={ms(OB)}|{ms(OB)}[d];"
   f"[a][b][c][d]amix=inputs=4:normalize=0,apad=whole_dur={T}[v]", '-map', '[v]', '-ar', '48000', '-ac', '2', '-t', f'{T:.3f}', f'{TMP}/voix.wav')
# ---- bande son ----
SR = 48000; N = int(SR * T); t = np.arange(N) / SR; rng = np.random.default_rng(11)
env = lambda pts: np.interp(t, *zip(*pts))
lp = lambda x, f: sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x); bp = lambda x, a, b: sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
a_ = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def burst(t0, dur, f1, f2, gain):
    o = np.zeros(N); i0 = int(t0 * SR); n = min(int(dur * SR), N - i0)
    if n > 0: o[i0:i0 + n] = bp(rng.standard_normal(n), f1, f2) * np.exp(-np.arange(n) / SR * (5 / dur)) * gain
    return o
def coup(t0, f0, f1, dur, gain):
    o = np.zeros(N); i0 = int(t0 * SR); n = min(int(dur * SR), N - i0)
    if n <= 0: return o
    tt = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-tt * 18); o[i0:i0 + n] = gain * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (4.5 / dur)); return o
def reverb(x, d=2.6, mix=.4):
    n = int(d * SR); ir = lp(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.2), 5000); return x + mix * a_(fftconvolve(x, ir)[:N]) * np.max(np.abs(x))
def impact(x0, g=1.0): return reverb(coup(x0, 70, 30, 2.3, g) + burst(x0, .5, 60, 900, .5 * g), 3.2, .55)
def montee(x1, d=3.0): m = env([(0, 0), (max(0, x1 - d), 0), (x1 - .02, 1), (x1, 0), (T, 0)]); return bp(rng.standard_normal(N), 300, 7000) * m ** 2 * .4
SIL = [(gA(SA1) - DA1, gA(SA1)), (gA(SA2) - DA2, gA(SA2)), (gA(AF), OB)]
on = np.ones(N)
for s0, s1 in SIL: on *= env([(0, 1), (s0 - .01, 1), (s0, 0), (s1, 0), (s1 + .01, 1), (T, 1)])
on *= env([(0, 1), (gB(BF) + 1.0, 1), (FIN_TITRE, 0), (T, 0)])
basse = np.zeros(N); tp = 0; k = 0; mot = [73.42, 73.42, 73.42, 87.31, 73.42, 73.42, 130.81, 110.0]
while tp < T:
    i0 = int(tp * SR); n = min(int(.24 * SR), N - i0); tt = np.arange(n) / SR; basse[i0:i0 + n] += np.sin(2 * np.pi * mot[k % 8] * tt) * np.exp(-tt * 9); tp += .25; k += 1
basse = lp(basse, 400) * .24 * on
fond = a_(lp(sum(np.sin(2 * np.pi * 73.42 * j * t + j) / j for j in range(1, 10)), 300)) * .12 * on
tic = sum(burst(s, .012, 2500, 9000, 1) for s in np.arange(.5, T, 1.0)) * .2 * on
fx = np.zeros(N)
for s0, s1 in SIL: fx += montee(s0) + impact(s1 + .02, .9)
for v in (184.4, 199.99, 241.89, 256.14): fx += reverb(coup(gA(v), 62, 36, .8, .4), 2, .35)
for v in (214.49, 219.65, 224.0): fx += burst(gA(v) + .3, .35, 2500, 9000, .3)                          # gel
for k in range(3): fx += np.sin(2 * np.pi * 1760 * t) * env([(0, 0), (gA(236.14) + k * .16, 0), (gA(236.14) + k * .16 + .005, .09), (gA(236.14) + k * .16 + .08, .09), (gA(236.14) + k * .16 + .085, 0), (T, 0)])

for s in np.cumsum(rng.uniform(.07, .16, 40)) + gB(84.28):
    if s < gB(87.86): fx += burst(s, .03, 1500, 7000, .3)                                                   # clavier
fx += burst(gB(58.77) + 1.0, .5, 200, 1200, .25)                                                              # le capot s'ouvre
fx += montee(gB(98.2), 2.5) + reverb(coup(gB(98.2), 55, 32, 1.4, .6), 2.4, .45)                            # « Reviens à la fenêtre allumée »

fx += montee(gB(BF), 3.0) + impact(gB(BF) + .05, 1.0)                                                         # titre final
mix = tic * 1.6 + fx; st = mix * (.85 / np.max(np.abs(mix)))
with wave.open(f'{TMP}/mus.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([st, st], 1) * 32767).astype('<i2').tobytes())
ff('-i', f'{TMP}/image.mp4', '-i', f'{TMP}/voix.wav', '-i', f'{TMP}/mus.wav', '-filter_complex',
   "[1]asplit[va][vb];[2]volume=0.55[m];[m][va]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[vb][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a];[0]noise=alls=2:allf=t,vignette=PI/6[v]",
   '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-t', f'{T:.3f}', f'{ANIM}/binance_partie3_v1.mp4')
print('FINI', round(T, 2))
