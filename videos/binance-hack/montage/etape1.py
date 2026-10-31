# Partie 2 · étape 1 (voix 63,6 → 104,2 s : « Rembobine » → « Une seule suffit… ») + silence de tension + impact.
# Chaque plan coupe sur le début de la phrase (calage_p2p5.json). Plans de 1 à 3 s, alternance 3D / écran / Three.js / footage.
import os, shutil, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from playwright.sync_api import sync_playwright
ANIM = '/home/claude/anim'; R = '/home/claude/true_stories/videos/binance-hack/code/'
FOOT = '/mnt/user-data/attachments/320b0a0f-0a6b-5eaa-97cb-bc509def2206/'
VOIX = '/home/claude/voix/vo_complete.mp3'; TMP = ANIM + '/et1'; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1280, 536, 24
def ff(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
V0, S1, D1, VF = 63.6, 104.2, 1.0, 105.3
def g(v): return v - V0 + (D1 if v >= S1 else 0)
T = g(VF) + .2
PLEIN = (0, 138, 1920, 804); CIBLE = (16, 52, 620, 260); FLUX = (16, 700, 1100, 460)
PL = [  # (début voix, fin voix, plan)
 (63.6, 66.04, ('code', 'rembobine', 0, 2.4)),
 (66.04, 67.62, ('code', 'horodatage', 0, 1.6)),
 (67.62, 69.4, ('foot', 'f69de8de-maskedtran_pindown.io_1793468966.mp4', 2.0)),
 (69.4, 71.86, ('3d', 'D_dos', 0, 1, False)),
 (71.86, 73.08, ('hack', 7.0, 7.6, CIBLE, (16, 60, 560, 234))),
 (73.08, 74.9, ('foot', '1aeebce7-BestAfterEffectsTutorials_pindown.io_1793469299.mp4', 4.0)),
 (74.9, 80.2, ('3d', 'V_coffre', 0, 1, False)),
 (80.2, 83.58, ('three', 'pieces', 0, 4.5)),
 (83.58, 85.6, ('3d', 'N_epaule', 0, 1, False)),
 (85.6, 88.67, ('code', 'nonce', 0, 3.0)),
 (88.67, 90.58, ('hack', 3.0, 4.6, FLUX, (16, 720, 900, 377))),
 (90.58, 94.16, ('three', 'cles', 0, 2.3)),
 (94.16, 96.27, ('3d', 'M_mains', 0, 1, False)),
 (96.27, 100.56, ('envoi', 0, 4.6, 0, .15)),
 (100.56, 103.05, ('three', 'cles', 2.3, 4.6)),
 (103.05, 104.2, ('envoi', 6.6, 7.8, .2, .6)),
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
evts = [(g(a), g(b) if b != S1 else g(b) - D1, s) for a, b, s in PL] + [(g(S1) - D1, g(S1), ('noir',)), (g(S1), T, ('noir',))]
morceaux = []
with sync_playwright() as p:
    br = p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']); pg = br.new_page(viewport={'width': 1920, 'height': 804})
    for i, (a, b, s) in enumerate(sorted(evts)):
        n = round(b * FPS) - round(a * FPS); out = f'{TMP}/{i:03d}.mp4'; typ = s[0]
        if typ == 'noir': seg_noir(out, n)
        elif typ == '3d': seg_3d(out, n, *s[1:])
        elif typ == 'foot': seg_foot(out, n, *s[1:])
        elif typ == 'code': sc_, t0, t1 = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}plans.html?s={sc_}&h=29.10.2026%20%E2%80%94%2020:20%20UTC&t={t0+(t1-t0)*u:.3f}', None))
        elif typ == 'three': sc_, t0, t1 = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}scenes3d.html?s={sc_}&t={t0+(t1-t0)*u:.3f}', None))
        elif typ == 'envoi': t0, t1, z0, z1 = s[1:]; capture(pg, out, n, lambda u: (f'file://{R}envoi.html?t={t0+(t1-t0)*u:.3f}&z={z0+(z1-z0)*E(u):.3f}', None))
        elif typ == 'hack':
            t0, t1, c0, c1 = s[1:]; pg.set_viewport_size({'width': 1920, 'height': 1080})
            capture(pg, out, n, lambda u: (f'file://{R}ecran_hacker.html?t={t0+(t1-t0)*u:.3f}', lerpc(c0, c1, E(u))))
            pg.set_viewport_size({'width': 1920, 'height': 804})
        morceaux.append(out); print('SEG', i, typ, round(a, 2), flush=True)
    br.close()
open(f'{TMP}/l.txt', 'w').write(''.join(f"file '{m}'\n" for m in morceaux))
ff('-f', 'concat', '-safe', '0', '-i', f'{TMP}/l.txt', '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', f'{TMP}/image.mp4')
ff('-i', VOIX, '-filter_complex', f"[0]atrim={V0}:{S1},asetpts=PTS-STARTPTS[a];[0]atrim={S1}:{VF},asetpts=PTS-STARTPTS,adelay={int(g(S1)*1000)}|{int(g(S1)*1000)}[b];[a][b]amix=inputs=2:normalize=0,apad=whole_dur={T}[v]",
   '-map', '[v]', '-ar', '48000', '-ac', '2', f'{TMP}/voix.wav')
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
m = env([(0, 0), (.1, 0), (1.4, 1), (1.6, 0), (T, 0)])
fx = bp(rng.standard_normal(N), 500, 4000) * m * .25 + np.sin(2 * np.pi * np.cumsum(900 - 700 * m) / SR) * m * .08          # rembobine
for s in np.cumsum(rng.uniform(.07, .16, 40)) + g(94.16):
    if s < g(96.27): fx += burst(s, .03, 1500, 7000, .35)                                                          # clavier (mains)
for s in np.cumsum(rng.uniform(.08, .2, 30)) + g(83.58):
    if s < g(85.6): fx += burst(s, .03, 1500, 7000, .22)
fx += burst(g(96.27) + 1.5 * (100.56 - 96.27) / 4.6, .06, 800, 6000, .7)                                           # clic « ENVOYER »
for j in range(50): fx += burst(g(96.27) + (2 + j * 3.5 / 50) * (100.56 - 96.27) / 4.6, .015, 3000, 9000, .12)       # 50 envois
fx += reverb(coup(g(74.9) + 1.6 * 5.3 / 5, 50, 30, 1.6, .5), 2.2, .4)                                              # porte du coffre
fx += reverb(coup(g(103.05) + .2, 62, 36, .9, .5), 2, .4)                                                          # « acceptée »
mt = env([(0, 0), (sil0 - 3, 0), (sil0 - .02, 1), (sil0, 0), (T, 0)])
fx += bp(rng.standard_normal(N), 300, 7000) * mt ** 2 * .4
fx += reverb(coup(sil1 + .02, 70, 30, 2.3, 1) + burst(sil1 + .02, .5, 60, 900, .5), 3.2, .55)                       # impact
mix = basse + fond + tic + fx; st = mix * (.85 / np.max(np.abs(mix)))
with wave.open(f'{TMP}/mus.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([st, st], 1) * 32767).astype('<i2').tobytes())
ff('-i', f'{TMP}/image.mp4', '-i', f'{TMP}/voix.wav', '-i', f'{TMP}/mus.wav', '-filter_complex',
   "[1]asplit[va][vb];[2]volume=0.55[m];[m][va]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[vb][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a];[0]noise=alls=2:allf=t,vignette=PI/6[v]",
   '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-t', f'{T:.3f}', f'{ANIM}/binance_p2_etape1_v1.mp4')
print('FINI', round(T, 2))
