# Musique de tension + effets, synthétisés et calés sur la première minute (64 s). Sortie : elements/musique.wav
# 0–24 s : nappe grave + battement de cœur qui accélère + cordes dissonantes + montée → impact du titre à 24 s.
# 30,5–60 s : sous la voix, pulsation de basse + tic-tac d'horloge (15 h 15). 60,7 s : montée → coupure sèche à 63,5 s.
import numpy as np, os, wave
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; T = 64.0; N = int(SR * T); t = np.arange(N) / SR
rng = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'elements', 'musique.wav')

def env(points):
    """Enveloppe linéaire à partir de [(temps, valeur), ...]."""
    xs, ys = zip(*points); return np.interp(t, xs, ys)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def scie(f, n=12):   # onde « cordes » douce : quelques harmoniques
    return sum(np.sin(2 * np.pi * f * k * t + k) / k for k in range(1, n + 1))
def a(x): return x / (np.max(np.abs(x)) + 1e-9)
def hz(note):   # notes utilisées (ré mineur)
    return {'D1': 36.71, 'A1': 55.0, 'D2': 73.42, 'F2': 87.31, 'A2': 110.0, 'C3': 130.81, 'D3': 146.83,
            'Eb3': 155.56, 'F3': 174.61, 'A3': 220.0, 'D4': 293.66, 'Eb4': 311.13}[note]
def coup(t0, f0=58, f1=38, dur=.35, gain=1.0):   # grosse caisse sourde (battement, impact)
    out = np.zeros(N); i0 = int(t0 * SR); n = min(int(dur * SR), N - i0)
    if n <= 0: return out
    tt = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-tt * 18)
    out[i0:i0 + n] = gain * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (4.5 / dur)); return out
def reverb(x, dur=2.8, mix=.35):
    n = int(dur * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.2); ir = lp(ir, 5000)
    w = fftconvolve(x, ir)[:N]; return x + mix * a(w) * np.max(np.abs(x))

COUPE = 24.0
# 1. nappe grave (0 → 24 s), monte lentement, coupée net
nappe = lp(scie(hz('D1')) + .7 * scie(hz('A1')) + .5 * scie(hz('D2')), 260)
nappe = a(nappe) * env([(0, 0), (3, .25), (20, .55), (23.9, .7), (COUPE, 0)])
# 2. cordes dissonantes : ré-fa-la, puis le mi bémol qui grince à partir de 10 s
lent = 1 + .25 * np.sin(2 * np.pi * .18 * t)
cordes = lp(scie(hz('D3') * 1.002) + scie(hz('D3') * .998) + .7 * scie(hz('F3')) + .6 * scie(hz('A3')), 1800)
cordes = a(cordes) * env([(0, 0), (6, 0), (12, .18), (23.9, .32), (COUPE, 0)]) * lent
grince = a(lp(scie(hz('Eb4') * 1.003) + scie(hz('Eb4')), 2500)) * env([(0, 0), (10, 0), (16, .08), (23.9, .2), (COUPE, 0)])
# 3. battement de cœur « lub-dub » qui accélère (64 → 92 bpm)
coeur = np.zeros(N); tb = 2.0
while tb < 23.6:
    bpm = 64 + 28 * (tb / 23.6) ** 2; g = .55 + .45 * tb / 23.6
    coeur += coup(tb, gain=g) + coup(tb + .22, gain=.6 * g); tb += 60 / bpm
# 4. montée : souffle filtré + glissando, 19 → 24 s
souffle = rng.standard_normal(N); m = env([(0, 0), (19, 0), (23.95, 1), (COUPE, 0)])
montee = bp(souffle, 300, 6000) * m ** 2 * .5 + np.sin(2 * np.pi * np.cumsum(80 + 600 * m ** 2) / SR) * m ** 3 * .25
# 5. impact du titre (24 s) + longue traîne
impact = reverb(coup(COUPE, 70, 30, 2.5, 1.0) + lp(rng.standard_normal(N), 900) * env([(0, 0), (COUPE, 0), (COUPE + .01, .6), (COUPE + .6, 0)]), 3.5, .6)
# 6. bip de connexion quand l'écran s'allume (16 s)
bip = np.sin(2 * np.pi * 1320 * t) * env([(0, 0), (16.0, 0), (16.01, .12), (16.12, .12), (16.13, 0)])
# 7. sous la voix (30,5 → 63,5 s) : pulsation de basse en croches + tic-tac
basse = np.zeros(N); tp = 30.5; k = 0
motif = ['D2', 'D2', 'D2', 'F2', 'D2', 'D2', 'C3', 'A2']
while tp < 63.4:
    i0 = int(tp * SR); n = min(int(.24 * SR), N - i0); tt = np.arange(n) / SR
    basse[i0:i0 + n] += np.sin(2 * np.pi * hz(motif[k % 8]) * tt) * np.exp(-tt * 9); tp += .25; k += 1
basse = lp(basse, 400) * env([(0, 0), (30.5, 0), (33, .22), (55, .3), (63.4, .45), (63.5, 0)])
tic = np.zeros(N)
for s in np.arange(31.0, 63.4, 1.0):
    i0 = int(s * SR); n = int(.012 * SR); tic[i0:i0 + n] += hp(rng.standard_normal(n), 2500) * np.exp(-np.arange(n) / SR * 400)
tic *= env([(0, 0), (31, .18), (63.4, .3), (63.5, 0)])
fond = lp(scie(hz('D2')) + .6 * scie(hz('A2')), 300)
fond = a(fond) * env([(0, 0), (30.5, 0), (34, .12), (58, .18), (63.4, .3), (63.5, 0)])
m2 = env([(0, 0), (60.6, 0), (63.45, 1), (63.5, 0)])
montee2 = bp(souffle, 300, 7000) * m2 ** 2 * .45 + a(lp(scie(hz('Eb3')) + scie(hz('D3')), 2000)) * m2 ** 2 * .25
fin = reverb(coup(63.5, 65, 32, 1.6, .9), 2.5, .5)

mix = (.9 * nappe + cordes + grince + .9 * coeur + montee + 1.0 * impact + bip
       + basse + tic + fond + montee2 + fin)
mix = reverb(mix, 2.2, .18)
g = .89 / np.max(np.abs(mix)); g_ = mix * g
# stéréo : léger décalage pour élargir
d = int(.012 * SR); L_ = g_; R_ = np.concatenate([np.zeros(d), g_[:-d]])
st = np.stack([L_, .92 * R_ + .08 * L_], 1)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
print('OK', OUT)
