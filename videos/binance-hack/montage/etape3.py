# Partie 2 · étape 2 (voix 105,3 → 129,67 s : « Vingt heures vingt-quatre » → « Binance. »).
# Chaque plan coupe sur le début de la phrase (calage_p2p5.json). Plans de 1 à 3 s, alternance 3D / écran / Three.js / footage.
import os, shutil, subprocess, wave
from urllib.parse import quote
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from playwright.sync_api import sync_playwright
ANIM = '/home/claude/anim'; R = '/home/claude/true_stories/videos/binance-hack/code/'
FOOT = '/mnt/user-data/attachments/320b0a0f-0a6b-5eaa-97cb-bc509def2206/'
VOIX = '/home/claude/voix/vo_complete.mp3'; TMP = ANIM + '/et3'; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1280, 536, 24
def ff(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
V0, S1, D1, VF = 129.67, 179.9, 0.0, 179.9
def g(v): return v - V0 + (D1 if v >= S1 else 0)
T = g(VF) + 2.6
PLEIN = (0, 138, 1920, 804); CIBLE = (16, 52, 620, 260); FLUX = (16, 700, 1100, 460)
PL = [
 (129.67, 131.6, ('three', 'tours', 0, 2.2)),
 (131.6, 134.75, ('code', 'forteresse', 0, 2.6, {'x': 360, 'y': 150, 'width': 1200, 'height': 502})),
 (134.75, 137.85, ('portrait', 'cz_reuters.png', 'Changpeng Zhao', 'fondateur de Binance')),
 (137.85, 140.56, ('portrait', 'cz_websummit.png', '', '')),
 (140.56, 143.16, ('3d', 'V_coffre', .4, 1, True)),
 (143.16, 145.6, ('code', 'frise', 0, 2.6, {'x': 360, 'y': 150, 'width': 1200, 'height': 502})),
 (145.6, 147.98, ('foot', '7f2770ef-weddingvideoeditornomi_pindown.io_1793468724.mp4', .2)),
 (147.98, 150.22, ('code', 'frise', 2.6, 4.6, {'x': 360, 'y': 150, 'width': 1200, 'height': 502})),
 (150.22, 152.3, ('portrait', 'cz_sourire.png', '', '')),
 (152.3, 153.75, ('code', 'rembobine', 0, 1.5)),
 (153.75, 155.6, ('foot', '520535af-themkpcaptain_pindown.io_1793468880.mp4', 6.0)),
 (155.6, 159.45, ('code', 'safu', 0, 2.6, {'x': 360, 'y': 150, 'width': 1200, 'height': 502})),
 (159.45, 163.2, ('art', 'binance_square_safu.png', '0,18,100,24')),
 (163.2, 165.6, ('portrait', 'cz_sourire.png', 'Changpeng Zhao', '« Funds are SAFU »')),
 (165.6, 168.43, ('code', 'fois', 0, 2.6, {'x': 360, 'y': 150, 'width': 1200, 'height': 502})),
 (168.43, 169.81, ('foot', '14a53b43-viatkinaviktoria_pindown.io_1793469151.mp4', 3.0)),
 (169.81, 172.0, ('code', 'alerte', 0, 2.0, {'x': 360, 'y': 150, 'width': 1200, 'height': 502})),
 (172.0, 174.19, ('three', 'telephone', .4, 2.6)),
 (174.19, 177.68, ('art', 'art_journaldugeek_trm.png', '3,43,94,7')),
 (177.68, 179.9, ('foot', 'e14f3f18-georgehowell2020_pindown.io_1793469250.mp4', 2.0)),
]
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
def seg_foot(out, n, f, ss):
    ff('-ss', str(ss), '-i', FOOT + f, '-vf', f'scale={W}:-2,crop={W}:{H},fps={FPS},eq=saturation=.75:brightness=-.03,format=yuv420p', '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '17', out)
def capture(pg, out, n, url_de):
    rep = out + '_c'; shutil.rmtree(rep, ignore_errors=True); os.makedirs(rep)
    for k in range(n):
        url, c = url_de(k / max(1, n - 1)); pg.goto(url); pg.wait_for_function('window.FRAME_PRET===true')
        pg.screenshot(path=f'{rep}/{k:04d}.jpg', type='jpeg', quality=92, **({'clip': c} if c else {}))
    ff('-framerate', str(FPS), '-i', f'{rep}/%04d.jpg', '-vf', f'scale={W}:{H}:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '17', out)
def E(u): return u * u * (3 - 2 * u)
def lerpc(a, b, e): x, y, w, h = [p + (q - p) * e for p, q in zip(a, b)]; return {'x': x, 'y': y, 'width': w, 'height': h}
evts = [(g(a), g(b), s) for a, b, s in PL] + [(g(VF), T, ('noir',))] 
morceaux = []
with sync_playwright() as p:
    br = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']); pg = br.new_page(viewport={'width': 1920, 'height': 804})
    for i, (a, b, s) in enumerate(sorted(evts)):
        n = round(b * FPS) - round(a * FPS); out = f'{TMP}/{i:03d}.mp4'; typ = s[0]
        if typ == 'noir': seg_noir(out, n)
        elif typ == '3d': seg_3d(out, n, *s[1:])
        elif typ == 'foot': seg_foot(out, n, *s[1:])
        elif typ == 'code': sc_, t0, t1, *cz = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}plans.html?s={sc_}&h=29.10.2026%20%E2%80%94%2020:24%20UTC&t={t0+(t1-t0)*u:.3f}', cz[0] if cz else None))
        elif typ == 'three': sc_, t0, t1, *cz = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}scenes3d.html?s={sc_}&t={t0+(t1-t0)*u:.3f}', cz[0] if cz else None))
        elif typ == 'envoi': t0, t1, z0, z1 = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}envoi.html?t={t0+(t1-t0)*u:.3f}&z={z0+(z1-z0)*E(u):.3f}', None))
        elif typ == 'logo': capture(pg, out, n, lambda u: (f'file://{R}logo.html?d={n/FPS:.2f}&t={u*n/FPS:.3f}', None))
        elif typ == 'art': img, hl = s[1:]; d = n / FPS; capture(pg, out, n, lambda u: (f'file://{R}archive.html?img={img}&mode=article&d={d:.2f}&t={u*d:.3f}&hl={hl}', None))
        elif typ == 'portrait': img, nom, role = s[1:]; d = n / FPS; capture(pg, out, n, lambda u: (f'file://{R}archive.html?img={img}&mode=portrait&d={d:.2f}&t={u*d:.3f}&nom={quote(nom)}&role={quote(role)}', None))
        elif typ == 'hack':
            t0, t1, c0, c1 = s[1:]; pg.set_viewport_size({'width': 1920, 'height': 1080})
            capture(pg, out, n, lambda u: (f'file://{R}ecran_hacker.html?t={t0+(t1-t0)*u:.3f}', lerpc(c0, c1, E(u))))
            pg.set_viewport_size({'width': 1920, 'height': 804})
        morceaux.append(out); print('SEG', i, typ, round(a, 2), flush=True)
    br.close()
open(f'{TMP}/l.txt', 'w').write(''.join(f"file '{m}'\n" for m in morceaux))
ff('-f', 'concat', '-safe', '0', '-i', f'{TMP}/l.txt', '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', f'{TMP}/image.mp4')
ff('-ss', str(V0), '-to', str(VF), '-i', VOIX, '-af', f'apad=whole_dur={T}', '-ar', '48000', '-ac', '2', f'{TMP}/voix.wav')
# ---- bande son : basse + tic-tac (charte), rewind, clavier, clic, montée + impact au silence ----
SR = 48000; N = int(SR * T); t = np.arange(N) / SR; rng = np.random.default_rng(7)
env = lambda pts: np.interp(t, *zip(*pts))
lp = lambda x, f: sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x); hp = lambda x, f: sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
bp = lambda x, a, b: sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
a_ = lambda x: x / (np.max(np.abs(x)) + 1e-9)
def burst(t0, dur, f1, f2, gain):
    o = np.zeros(N); i0 = int(t0 * SR); n = min(int(dur * SR), N - i0)
    if n > 0: o[i0:i0 + n] = bp(rng.standard_normal(n), f1, f2) * np.exp(-np.arange(n) / SR * (5 / dur)) * gain
    return o
def coup(t0, f0, f1, dur, gain):
    o = np.zeros(N); i0 = int(t0 * SR); n = min(int(dur * SR), N - i0); tt = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-tt * 18)
    o[i0:i0 + n] = gain * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (4.5 / dur)); return o
def reverb(x, d=2.6, mix=.4):
    n = int(d * SR); ir = lp(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.2), 5000); return x + mix * a_(fftconvolve(x, ir)[:N]) * np.max(np.abs(x))
sil0, sil1 = g(S1) - D1, g(S1)
on = env([(0, 1), (g(VF) - .01, 1), (g(VF), 0), (T, 0)])
basse = np.zeros(N); tp = 0; k = 0; mot = [73.42, 73.42, 73.42, 87.31, 73.42, 73.42, 130.81, 110.0]
while tp < T:
    i0 = int(tp * SR); n = min(int(.24 * SR), N - i0); tt = np.arange(n) / SR; basse[i0:i0 + n] += np.sin(2 * np.pi * mot[k % 8] * tt) * np.exp(-tt * 9); tp += .25; k += 1
basse = lp(basse, 400) * .24 * on
fond = a_(lp(sum(np.sin(2 * np.pi * 73.42 * j * t + j) / j for j in range(1, 10)), 300)) * .12 * on
tic = sum(burst(s, .012, 2500, 9000, 1) for s in np.arange(.5, T, 1.0)) * .2 * on
fx = np.zeros(N)
fx += reverb(coup(g(131.6), 62, 36, .8, .4), 2, .35) + reverb(coup(g(140.56), 50, 30, 1.4, .5), 2.4, .4)
m = env([(0, 0), (g(152.3), 0), (g(153.2), 1), (g(153.75), 0), (T, 0)])
fx += bp(rng.standard_normal(N), 500, 4000) * m * .25 + np.sin(2 * np.pi * np.cumsum(900 - 700 * m) / SR) * m * .08
fx += reverb(coup(g(165.6) + .1, 62, 36, .9, .45), 2, .35)
for k in range(3): fx += np.sin(2 * np.pi * 1760 * t) * env([(0, 0), (g(169.81) + k * .16, 0), (g(169.81) + k * .16 + .005, .09), (g(169.81) + k * .16 + .08, .09), (g(169.81) + k * .16 + .085, 0), (T, 0)])
for k in range(4): fx += burst(g(172.4) + k * .5, .25, 80, 300, .5)
fx += reverb(coup(g(174.19), 55, 32, 1.0, .5), 2.2, .4)
mt = env([(0, 0), (g(VF) - 2.5, 0), (g(VF) - .02, 1), (g(VF), 0), (T, 0)]); fx += bp(rng.standard_normal(N), 300, 7000) * mt ** 2 * .4
fx += reverb(coup(g(VF) + 1.2, 70, 30, 2.3, 1) + burst(g(VF) + 1.2, .5, 60, 900, .5), 3.2, .55)
mix = basse + fond + tic + fx; st = mix * (.85 / np.max(np.abs(mix)))
with wave.open(f'{TMP}/mus.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([st, st], 1) * 32767).astype('<i2').tobytes())
ff('-i', f'{TMP}/image.mp4', '-i', f'{TMP}/voix.wav', '-i', f'{TMP}/mus.wav', '-filter_complex',
   "[1]asplit[va][vb];[2]volume=0.55[m];[m][va]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[vb][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a];[0]noise=alls=2:allf=t,vignette=PI/6[v]",
   '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-t', f'{T:.3f}', f'{ANIM}/binance_p2_etape3_v1.mp4')
print('FINI', round(T, 2))
