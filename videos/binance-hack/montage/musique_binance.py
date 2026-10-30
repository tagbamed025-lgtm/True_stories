# Bande son de l'ouverture Binance (0 → 85 s), d'après videos/silk-road/montage/musique.py (même recette = charte sonore TRU Stories).
# 0–13 s : cold open muet — nappe grave + cordes dissonantes + cœur qui accélère + pluie + moteur qui passe + clavier + montée → clic « Entrée » + IMPACT à 13 s.
# 13–18 s : titre puis date, silence + traîne.  18 s → : voix + pulsation de basse + TIC-TAC 1 coup / seconde (signature de la chaîne).
# « Pas de musique » (53,1 s) : la musique se coupe, il ne reste que le tic-tac et les touches. « Binance. » (62,6 s) : montée → coupure sèche à 66,3 s
# → silence → « Entrée. » à 67,95 s : clic + impact → la pulsation repart jusqu'à la fin.
import numpy as np, os, sys, wave
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; T = 85.0; N = int(SR * T); t = np.arange(N) / SR
rng = np.random.default_rng(29)
OUT = sys.argv[1] if len(sys.argv) > 1 else 'musique_binance.wav'

def env(points): xs, ys = zip(*points); return np.interp(t, xs, ys)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def scie(f, n=12): return sum(np.sin(2 * np.pi * f * k * t + k) / k for k in range(1, n + 1))
def a(x): return x / (np.max(np.abs(x)) + 1e-9)
HZ = {'D1': 36.71, 'A1': 55.0, 'D2': 73.42, 'F2': 87.31, 'A2': 110.0, 'C3': 130.81, 'D3': 146.83, 'Eb3': 155.56, 'F3': 174.61, 'A3': 220.0, 'Eb4': 311.13}
def coup(t0, f0=58, f1=38, dur=.35, gain=1.0):
    out = np.zeros(N); i0 = int(t0 * SR); n = min(int(dur * SR), N - i0)
    if n <= 0: return out
    tt = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-tt * 18)
    out[i0:i0 + n] = gain * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (4.5 / dur)); return out
def reverb(x, dur=2.8, mix=.35):
    n = int(dur * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.2); ir = lp(ir, 5000)
    w = fftconvolve(x, ir)[:N]; return x + mix * a(w) * np.max(np.abs(x))
def clics(debut, fin, cadence=9.0, gain=.12, seed=1):          # touches de clavier mécanique
    r = np.random.default_rng(seed); out = np.zeros(N); s = debut
    while s < fin:
        i0 = int(s * SR); n = int(.018 * SR)
        if i0 + n < N: out[i0:i0 + n] += bp(r.standard_normal(n), 1800, 7000) * np.exp(-np.arange(n) / SR * 260) * gain * (.6 + .4 * r.random())
        s += r.exponential(1 / cadence) + .03
    return out
def clic_entree(t0, gain=.5):
    out = np.zeros(N); i0 = int(t0 * SR); n = int(.05 * SR)
    out[i0:i0 + n] = (bp(rng.standard_normal(n), 900, 5000) * np.exp(-np.arange(n) / SR * 120)) * gain; return out

COUPE = 13.0; SILENCE = (66.3, 67.95); ENTREE = 67.95; VOIX = 18.0; FIN_VOIX = 83.2; PAS_MUSIQUE = 53.14; BINANCE = 62.6
# 1. cold open : nappe + cordes + mi bémol qui grince + cœur qui accélère + montée → impact
nappe = a(lp(scie(HZ['D1']) + .7 * scie(HZ['A1']) + .5 * scie(HZ['D2']), 260)) * env([(0, 0), (1.5, .3), (11, .55), (12.9, .7), (COUPE, 0)])
cordes = a(lp(scie(HZ['D3'] * 1.002) + scie(HZ['D3'] * .998) + .7 * scie(HZ['F3']) + .6 * scie(HZ['A3']), 1800)) * env([(0, 0), (2, 0), (6, .18), (12.9, .32), (COUPE, 0)]) * (1 + .25 * np.sin(2 * np.pi * .18 * t))
grince = a(lp(scie(HZ['Eb4'] * 1.003) + scie(HZ['Eb4']), 2500)) * env([(0, 0), (5, 0), (8.5, .08), (12.9, .2), (COUPE, 0)])
coeur = np.zeros(N); tb = 5.6
while tb < 12.6:
    u = (tb - 5.6) / 7; coeur += coup(tb, gain=.5 + .5 * u) + coup(tb + .22, gain=.3 + .3 * u); tb += 60 / (66 + 34 * u * u)
souffle = rng.standard_normal(N)
m = env([(0, 0), (9.5, 0), (12.95, 1), (COUPE, 0)])
montee = bp(souffle, 300, 6000) * m ** 2 * .5 + np.sin(2 * np.pi * np.cumsum(80 + 600 * m ** 2) / SR) * m ** 3 * .25
impact = reverb(coup(COUPE, 70, 30, 2.5, 1.0) + lp(rng.standard_normal(N), 900) * env([(0, 0), (COUPE, 0), (COUPE + .01, .6), (COUPE + .6, 0)]), 3.5, .6)
bip = np.sin(2 * np.pi * 1320 * t) * env([(0, 0), (10.5, 0), (10.51, .1), (10.62, .1), (10.63, 0)])
# 2. ambiance de la rue : pluie fine + moteur qui passe (effet Doppler, au plus près vers 4,4 s)
pluie = hp(rng.standard_normal(N), 3500) * .035 * env([(0, 0), (.8, 1), (12.9, 1), (COUPE, 0), (VOIX, 0), (VOIX + 1, .5), (T, .5)])
moteur_env = env([(0, 0), (.8, 0), (2.5, .25), (4.4, 1), (5.6, .3), (7.5, 0)])
f_mot = 48 + 14 * np.clip(1 - (t - 4.4) / 1.2, -1, 1)          # le ton descend quand la voiture passe
moteur = (lp(np.sin(2 * np.pi * np.cumsum(f_mot) / SR) + .5 * np.sin(4 * np.pi * np.cumsum(f_mot) / SR), 300) + .4 * lp(rng.standard_normal(N), 500)) * moteur_env * .35
moteur += (lp(rng.standard_normal(N), 1500) * env([(0, 0), (3.9, 0), (4.4, .25), (5.0, 0)]))   # souffle du passage
# 3. clavier : dans la chambre (8 → 12,9) et sous « le claquement des touches » (52,1 → 57,1)
clavier = clics(8.0, 12.8, 9, .12, 2) + clics(50.3, 57.1, 8, .10, 3) + clics(47.0, 50.3, 6, .06, 4) + clic_entree(12.9, .55) + clic_entree(ENTREE, .6)
# 4. sous la voix : pulsation de basse en croches + nappe de fond (coupées sur « Pas de musique », reprises après l'impact d'« Entrée »)
basse = np.zeros(N); tp = VOIX; k = 0; motif = ['D2', 'D2', 'D2', 'F2', 'D2', 'D2', 'C3', 'A2']
while tp < FIN_VOIX:
    i0 = int(tp * SR); n = min(int(.24 * SR), N - i0); tt = np.arange(n) / SR
    basse[i0:i0 + n] += np.sin(2 * np.pi * HZ[motif[k % 8]] * tt) * np.exp(-tt * 9); tp += .25; k += 1
musique_on = env([(0, 0), (VOIX, 0), (VOIX + 2.5, 1), (PAS_MUSIQUE - .05, 1), (PAS_MUSIQUE, 0), (ENTREE + .4, 0), (ENTREE + 2.5, 1), (FIN_VOIX, 1), (T, 0)])
basse = lp(basse, 400) * .25 * musique_on
fond = a(lp(scie(HZ['D2']) + .6 * scie(HZ['A2']), 300)) * .14 * musique_on
# 5. TIC-TAC : 1 coup par seconde, du début de la voix à la fin (seulement coupé pendant le silence de tension)
tic = np.zeros(N)
for s in np.arange(VOIX + .5, T - .5, 1.0):
    i0 = int(s * SR); n = int(.012 * SR); tic[i0:i0 + n] += hp(rng.standard_normal(n), 2500) * np.exp(-np.arange(n) / SR * 400)
tic *= env([(0, 0), (VOIX, .18), (SILENCE[0] - .01, .26), (SILENCE[0], 0), (SILENCE[1], 0), (SILENCE[1] + .01, .2), (T, .2)])
# 6. montée sur « Binance. » → coupure sèche → silence → impact sur « Entrée. »
m2 = env([(0, 0), (BINANCE, 0), (SILENCE[0] - .02, 1), (SILENCE[0], 0)])
montee2 = bp(souffle, 300, 7000) * m2 ** 2 * .45 + a(lp(scie(HZ['Eb3']) + scie(HZ['D3']), 2000)) * m2 ** 2 * .25
impact2 = reverb(coup(ENTREE + .02, 70, 30, 2.2, .95), 3.0, .55)
fin = reverb(coup(FIN_VOIX, 60, 30, 1.8, .7), 3.0, .5)

mix = (.9 * nappe + cordes + grince + .9 * coeur + montee + impact + bip + pluie + moteur + clavier
       + basse + fond + tic + montee2 + impact2 + fin)
mix = reverb(mix, 2.2, .15)
st = mix * (.89 / np.max(np.abs(mix)))
d = int(.012 * SR); R = np.concatenate([np.zeros(d), st[:-d]]); st2 = np.stack([st, .92 * R + .08 * st], 1)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st2 * 32767).astype('<i2').tobytes())
print('OK', OUT)
