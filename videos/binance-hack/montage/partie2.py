# Partie 2 (voix 63,6 → 265,4 s, parties p2 à p5) : montage + bande son, même charte que l'ouverture.
# Silences de tension insérés dans la voix : après « Une seule suffit… », avant « Trop tard. », avant « trois. ».
import os, sys, json, shutil, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from playwright.sync_api import sync_playwright
ANIM = '/home/claude/anim'; R = '/home/claude/true_stories/videos/binance-hack/code/'
VOIX = '/home/claude/voix/vo_complete.mp3'; TMP = ANIM + '/seg2'; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1280, 536, 24
def ff(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)

# ---------- carte voix → temps du montage ----------
V0 = 63.6; S1, D1 = 104.2, 1.0; S2, D2 = 205.45, 0.8; S3, D3 = 264.62, 1.5; VFIN = 265.4; QUEUE = 2.4
def g(v):
    x = v - V0
    if v >= S1: x += D1
    if v >= S2: x += D2
    if v >= S3: x += D3
    return x
T = g(VFIN) + QUEUE
SIL = [(g(S1) - D1, g(S1)), (g(S2) - D2, g(S2)), (g(S3) - D3, g(S3))]

# ---------- plans (en temps VOIX) ----------
# ('3d', plan, u0, u1, envers) · ('code', scène, t0, t1) · ('hack', t0, t1, crop0, crop1) · ('p12', t0, t1)
# ('art', image, surlignage) · ('portrait', image, nom, rôle) · ('noir',)
PLEIN = (0, 138, 1920, 804); CIBLE = (10, 40, 680, 285); CHAINES = (0, 352, 760, 318)
PL = [
 (63.6, 66.0, ('code', 'rembobine', 0, 2.4)),
 (66.0, 72.6, ('hack', 0, 2.6, PLEIN, CIBLE)),
 (72.6, 77.8, ('3d', 'S_serveurs', 0, 1, False)),
 (77.8, 83.0, ('3d', 'S_coffre', 0, .45, False)),
 (83.0, 88.3, ('code', 'nonce', 0, 5.3)),
 (88.3, 93.9, ('art', 'etherscan_accueil.png', '50,62,49,38')),
 (93.9, 103.1, ('p12', 1.0, 8.0)),
 (103.1, 104.2, ('hack', 4.9, 5.6, PLEIN, PLEIN)),
 (104.2, 105.3, ('3d', 'S_coffre', .45, 1, False)),
 (105.3, 115.9, ('code', 'transaction', 0, 5.2)),
 (115.9, 121.2, ('art', 'binance_square_50auth.png', '0,34,100,30')),
 (121.2, 127.7, ('hack', 6.0, 9.4, CHAINES, CHAINES)),
 (127.7, 129.7, ('art', 'art_france24.png', '11,22,76,22')),
 (129.7, 134.2, ('code', 'forteresse', 0, 3.0)),
 (134.2, 137.6, ('portrait', 'cz_reuters.png', 'Changpeng Zhao', 'fondateur de Binance')),
 (137.6, 140.2, ('portrait', 'cz_websummit.png', '', '')),
 (140.2, 142.8, ('3d', 'S_serveurs', 0, .6, True)),
 (142.8, 149.7, ('code', 'frise', 0, 5.0)),
 (149.7, 155.1, ('portrait', 'cz_sourire.png', '', '')),
 (155.1, 159.0, ('art', 'binance_square_safu.png', '0,18,100,24')),
 (159.0, 164.0, ('code', 'safu', 0, 3.0)),
 (164.0, 168.9, ('code', 'fois', 0, 3.0)),
 (168.9, 174.0, ('code', 'alerte', 0, 3.3)),
 (174.0, 180.3, ('art', 'art_journaldugeek_trm.png', '1,24,98,9')),
 (180.3, 185.0, ('code', 'postcz', 0, 2.0)),
 (185.0, 189.2, ('3d', 'X_crise', 0, .5, False)),
 (189.2, 194.5, ('3d', 'X_equipe', 0, 1, False)),
 (194.5, 199.4, ('3d', 'X_crise', .5, 1, False)),
 (199.4, 205.45, ('code', 'reprise', 0, 3.0)),
 (205.45, 207.0, ('hack', 9.0, 9.8, CIBLE, CIBLE)),
 (207.0, 214.2, ('code', 'jauges', 0, 1.6)),
 (214.2, 225.9, ('code', 'jauges', 1.6, 6.0)),
 (225.9, 235.6, ('code', 'aave', 0, 3.6)),
 (235.6, 241.4, ('code', 'suspendu', 0, 3.6)),
 (241.4, 248.0, ('portrait', 'yihe_rouge.png', 'Yi He', 'cofondatrice de Binance')),
 (248.0, 252.5, ('3d', 'X_equipe', 1, 0, True)),
 (252.5, 256.5, ('art', 'art_ft_yahoo_securite.png', '0,8,100,22')),
 (256.5, 259.5, ('portrait', 'cz_websummit.png', 'Changpeng Zhao', '« Ça fait mal, mais on survivra. »')),
 (259.5, 264.62, ('code', 'bilan', 0, 1.2)),
 (264.62, 265.4, ('code', 'bilan', 2.4, 3.0)),
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
def capture(pg, out, n, url_de, clip=None):
    rep = out + '_c'; shutil.rmtree(rep, ignore_errors=True); os.makedirs(rep)
    for k in range(n):
        u = k / max(1, n - 1); url, c = url_de(u)
        pg.goto(url); pg.wait_for_function('window.FRAME_PRET===true')
        pg.screenshot(path=f'{rep}/{k:04d}.jpg', type='jpeg', quality=92, **({'clip': c} if c else {}))
    ff('-framerate', str(FPS), '-i', f'{rep}/%04d.jpg', '-vf', f'scale={W}:{H}:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '17', out)
def lerpc(a, b, e): x, y, w, h = [p + (q - p) * e for p, q in zip(a, b)]; return {'x': x, 'y': y, 'width': w, 'height': h}
from urllib.parse import quote

morceaux = []; cur = 0.0
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 804})
    evts = []
    for a, b, spec in PL: evts.append((g(a), g(b) if b != S1 and b != S2 and b != S3 else g(b) - {S1: D1, S2: D2, S3: D3}[b], spec))
    for (s, e) in SIL: evts.append((s, e, ('noir',)))
    evts.append((g(VFIN), T, ('noir',)))
    evts.sort()
    for i, (a, b, spec) in enumerate(evts):
        n = round(b * FPS) - round(a * FPS)
        if n <= 0: continue
        out = f'{TMP}/{i:03d}.mp4'; typ = spec[0]; d = n / FPS
        if typ == 'noir': seg_noir(out, n)
        elif typ == '3d': seg_3d(out, n, *spec[1:])
        elif typ == 'code':
            sc_, t0, t1 = spec[1:]; capture(pg, out, n, lambda u: (f'file://{R}plans.html?s={sc_}&t={t0 + (t1 - t0) * u:.3f}', None))
        elif typ == 'p12':
            t0, t1 = spec[1:]; capture(pg, out, n, lambda u: (f'file:///home/claude/plan12/p12.html?frame={int((t0 + (t1 - t0) * u) * 30)}', None))
        elif typ == 'hack':
            t0, t1, c0, c1 = spec[1:]; pg.set_viewport_size({'width': 1920, 'height': 1080})
            capture(pg, out, n, lambda u: (f'file://{R}ecran_hacker.html?t={t0 + (t1 - t0) * u:.3f}', lerpc(c0, c1, u * u * (3 - 2 * u))))
            pg.set_viewport_size({'width': 1920, 'height': 804})
        elif typ == 'art':
            img, hl = spec[1:]; capture(pg, out, n, lambda u: (f'file://{R}archive.html?img={img}&mode=article&d={d:.2f}&t={u * d:.3f}&hl={hl}', None))
        elif typ == 'portrait':
            img, nom, role = spec[1:]; capture(pg, out, n, lambda u: (f'file://{R}archive.html?img={img}&mode=portrait&d={d:.2f}&t={u * d:.3f}&nom={quote(nom)}&role={quote(role)}', None))
        morceaux.append(out); print('SEG', i, typ, round(a, 2), round(d, 2), flush=True)
    br.close()
open(f'{TMP}/liste.txt', 'w').write(''.join(f"file '{m}'\n" for m in morceaux))
ff('-f', 'concat', '-safe', '0', '-i', f'{TMP}/liste.txt', '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', f'{TMP}/image.mp4')

# ---------- voix découpée ----------
parts = [(V0, S1, g(V0)), (S1, S2, g(S1)), (S2, S3, g(S2)), (S3, VFIN, g(S3))]
fc = ''.join(f"[0]atrim={a}:{b},asetpts=PTS-STARTPTS,adelay={int(o*1000)}|{int(o*1000)}[v{i}];" for i, (a, b, o) in enumerate(parts))
fc += ''.join(f'[v{i}]' for i in range(4)) + f"amix=inputs=4:normalize=0,apad=whole_dur={T}[voix]"
ff('-i', VOIX, '-filter_complex', fc, '-map', '[voix]', '-ar', '48000', '-ac', '2', f'{TMP}/voix.wav')

# ---------- bande son ----------
SR = 48000; N = int(SR * T); t = np.arange(N) / SR; rng = np.random.default_rng(31)
def env(pts): xs, ys = zip(*pts); return np.interp(t, xs, ys)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def scie(f, n=12): return sum(np.sin(2 * np.pi * f * k * t + k) / k for k in range(1, n + 1))
def a_(x): return x / (np.max(np.abs(x)) + 1e-9)
def coup(t0, f0=58, f1=38, dur=.35, gain=1.0):
    out = np.zeros(N); i0 = int(t0 * SR); n = min(int(dur * SR), N - i0)
    if n <= 0: return out
    tt = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-tt * 18)
    out[i0:i0 + n] = gain * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (4.5 / dur)); return out
def reverb(x, dur=2.8, mix=.35):
    n = int(dur * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.2); ir = lp(ir, 5000)
    return x + mix * a_(fftconvolve(x, ir)[:N]) * np.max(np.abs(x))
def impact(t0, g_=1.0): return reverb(coup(t0, 70, 30, 2.3, g_) + lp(rng.standard_normal(N), 900) * env([(0, 0), (t0, 0), (t0 + .01, .5 * g_), (t0 + .5, 0), (T, 0)]), 3.2, .55)
def sting(t0, g_=.5): return reverb(coup(t0, 62, 36, .9, g_), 2.0, .4)
def montee(t1, d=3.0):
    m = env([(0, 0), (max(0, t1 - d), 0), (t1 - .02, 1), (t1, 0), (T, 0)])
    return bp(rng.standard_normal(N), 300, 7000) * m ** 2 * .45 + a_(lp(scie(155.56) + scie(146.83), 2000)) * m ** 2 * .22
def bips(t0, k=3):
    out = np.zeros(N)
    for j in range(k): out += np.sin(2 * np.pi * 1760 * t) * env([(0, 0), (t0 + j * .16, 0), (t0 + j * .16 + .005, .09), (t0 + j * .16 + .08, .09), (t0 + j * .16 + .085, 0), (T, 0)])
    return out
def glace(t0, g_=.25):
    out = np.zeros(N); i0 = int(t0 * SR); n = int(.35 * SR)
    if i0 + n < N: out[i0:i0 + n] = hp(rng.standard_normal(n), 2500) * np.exp(-np.arange(n) / SR * 14) * (rng.random(n) > .7) * g_
    return out
def rewind(t0, d=1.6):
    m = env([(0, 0), (t0, 0), (t0 + d * .8, 1), (t0 + d, 0), (T, 0)])
    return bp(rng.standard_normal(N), 500, 4000) * m * .25 + np.sin(2 * np.pi * np.cumsum(900 - 700 * m) / SR) * m * .08
on = np.ones(N)
for s, e in SIL: on *= env([(0, 1), (s - .01, 1), (s, 0), (e, 0), (e + .01, 1), (T, 1)])
on *= env([(0, 1), (g(VFIN) - .01, 1), (g(VFIN), 0), (T, 0)])
basse = np.zeros(N); tp = 0.0; k = 0; motif = [73.42, 73.42, 73.42, 87.31, 73.42, 73.42, 130.81, 110.0]
while tp < T:
    i0 = int(tp * SR); n = min(int(.24 * SR), N - i0); tt = np.arange(n) / SR
    basse[i0:i0 + n] += np.sin(2 * np.pi * motif[k % 8] * tt) * np.exp(-tt * 9); tp += .25; k += 1
basse = lp(basse, 400) * .24 * on
fond = a_(lp(scie(73.42) + .6 * scie(110.0), 300)) * .13 * on
tic = np.zeros(N)
for s in np.arange(.5, T, 1.0):
    i0 = int(s * SR); n = int(.012 * SR)
    if i0 + n < N: tic[i0:i0 + n] += hp(rng.standard_normal(n), 2500) * np.exp(-np.arange(n) / SR * 400)
tic *= .2 * on
fx = rewind(0.1) + sting(g(66.0), .4) + sting(g(105.3), .55) + sting(g(127.7), .45) + bips(g(168.9)) + bips(g(180.3), 2)
fx += sum(glace(g(x)) for x in (214.6, 219.8, 222.1)) + sting(g(235.6), .5)
for s, e in SIL: fx += montee(s) + impact(e + .02, .95)
fx += impact(g(VFIN) - .7, 1.0)
mix = basse + fond + tic + fx
mix = reverb(mix, 2.0, .12); st = mix * (.85 / np.max(np.abs(mix)))
with wave.open(f'{TMP}/musique.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([st, st], 1) * 32767).astype('<i2').tobytes())

ff('-i', f'{TMP}/image.mp4', '-i', f'{TMP}/voix.wav', '-i', f'{TMP}/musique.wav', '-filter_complex',
   "[1]asplit[va][vb];[2]volume=0.55[m];[m][va]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[vb][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a];"
   "[0]noise=alls=2:allf=t,vignette=PI/6[v]", '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-c:a', 'aac', '-b:a', '192k',
   '-t', f'{T:.3f}', f'{ANIM}/binance_partie2_v1.mp4')
print('FINI', round(T, 2))
