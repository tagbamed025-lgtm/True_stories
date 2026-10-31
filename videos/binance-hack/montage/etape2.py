# Partie 2 · étape 2 (voix 105,3 → 129,67 s : « Vingt heures vingt-quatre » → « Binance. »).
# Chaque plan coupe sur le début de la phrase (calage_p2p5.json). Plans de 1 à 3 s, alternance 3D / écran / Three.js / footage.
import os, shutil, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from playwright.sync_api import sync_playwright
ANIM = '/home/claude/anim'; R = '/home/claude/true_stories/videos/binance-hack/code/'
FOOT = '/mnt/user-data/attachments/320b0a0f-0a6b-5eaa-97cb-bc509def2206/'
VOIX = '/home/claude/voix/vo_complete.mp3'; TMP = ANIM + '/et2'; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1280, 536, 24
def ff(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
V0, S1, D1, VF = 105.3, 129.67, 0.0, 129.67
def g(v): return v - V0 + (D1 if v >= S1 else 0)
T = g(VF)
PLEIN = (0, 138, 1920, 804); CIBLE = (16, 52, 620, 260); FLUX = (16, 700, 1100, 460)
PL = [
 (105.3, 107.04, ('code', 'horodatage', 1.6, 2.6)),
 (107.04, 109.0, ('code', 'transaction', 0, 1.2, {'x': 560, 'y': 100, 'width': 800, 'height': 335})),
 (109.0, 110.23, ('foot', '54f7ed59-dezinejunkieArt_pindown.io_1793468742.mp4', 3.0)),
 (110.23, 112.49, ('code', 'transaction', 1.2, 2.4, {'x': 560, 'y': 190, 'width': 800, 'height': 335})),
 (112.49, 114.6, ('code', 'transaction', 2.4, 4.0, {'x': 560, 'y': 340, 'width': 800, 'height': 335})),
 (114.6, 116.37, ('foot', '54f7ed59-dezinejunkieArt_pindown.io_1793468742.mp4', 9.0)),
 (116.37, 118.64, ('envoi', 7.8, 8.4, .6, .75)),
 (118.64, 121.42, ('3d', 'X_equipe', 0, .6, False)),
 (121.42, 123.75, ('three', 'globe', 0, 2.6, {'x': 420, 'y': 176, 'width': 1080, 'height': 452})),
 (123.75, 126.76, ('hack', 7.0, 8.4, (16, 380, 620, 259), (16, 380, 620, 259))),
 (126.76, 128.02, ('three', 'globe', 3.8, 5.2, {'x': 420, 'y': 176, 'width': 1080, 'height': 452})),
 (128.02, 129.67, ('three', 'tours', 2.4, 4.6)),
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
evts = [(g(a), g(b) if b != S1 else g(b) - D1, s) for a, b, s in PL] 
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
on = env([(0, 1), (sil0 - .01, 1), (sil0, 0), (T, 0)])
basse = np.zeros(N); tp = 0; k = 0; mot = [73.42, 73.42, 73.42, 87.31, 73.42, 73.42, 130.81, 110.0]
while tp < T:
    i0 = int(tp * SR); n = min(int(.24 * SR), N - i0); tt = np.arange(n) / SR; basse[i0:i0 + n] += np.sin(2 * np.pi * mot[k % 8] * tt) * np.exp(-tt * 9); tp += .25; k += 1
basse = lp(basse, 400) * .24 * on
fond = a_(lp(sum(np.sin(2 * np.pi * 73.42 * j * t + j) / j for j in range(1, 10)), 300)) * .12 * on
tic = sum(burst(s, .012, 2500, 9000, 1) for s in np.arange(.5, T, 1.0)) * .2 * on
fx = np.zeros(N)
for v in (107.04, 110.23, 112.49): fx += reverb(coup(g(v) + .05, 62, 36, .8, .45), 2, .35)        # montants
for j in range(30): fx += burst(g(109.0) + j * .04, .02, 2000, 9000, .1)                          # pièces
fx += reverb(coup(g(116.37), 55, 32, 1.2, .6), 2.4, .45)                                          # « une seule transaction »
for v in (123.75, 124.82, 125.66, 126.76, 128.02): fx += burst(g(v), .09, 400, 6000, .45) + coup(g(v), 90, 40, .25, .3)   # chaque chaîne
mw = env([(0, 0), (g(127.2), 0), (T - .02, 1), (T, 0)]); fx += bp(rng.standard_normal(N), 300, 7000) * mw ** 2 * .35   # montée vers la suite
mix = basse + fond + tic + fx; st = mix * (.85 / np.max(np.abs(mix)))
with wave.open(f'{TMP}/mus.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([st, st], 1) * 32767).astype('<i2').tobytes())
ff('-i', f'{TMP}/image.mp4', '-i', f'{TMP}/voix.wav', '-i', f'{TMP}/mus.wav', '-filter_complex',
   "[1]asplit[va][vb];[2]volume=0.55[m];[m][va]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[vb][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a];[0]noise=alls=2:allf=t,vignette=PI/6[v]",
   '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-t', f'{T:.3f}', f'{ANIM}/binance_p2_etape2_v1.mp4')
print('FINI', round(T, 2))
