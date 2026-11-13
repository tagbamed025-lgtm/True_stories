# Version anglaise : chaque phrase anglaise (voix de Mo, p1_en … p10_en) est posée au début de la phrase française correspondante,
# sur les mêmes images (images EN = images FR avec les textes traduits, rendues par LANGUE=en HD=1 <montage>.py).
# Usage : python3 montage_en.py <dossier des p*_en.mp3>
import json, os, re, subprocess, sys
import numpy as np
EN_DIR = sys.argv[1]; W = '/home/claude/en'; ANIM = '/home/claude/anim'
PH = json.load(open('/home/claude/true_stories/videos/binance-hack/voix/phrases_en.json'))
FR = json.load(open(f'{W}/phrases_fr_globales.json'))
# phrases anglaises fusionnées là où le calage français a fusionné deux phrases
FUSION = {'p3': [(10, 11)], 'p4': [(3, 4)], 'p5': [(15, 16)]}
def ff(*a): subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
def duree(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)


REMP = {'aave': 'ah vey', 'binance': 'by nance', "binance's": 'by nance', 'bitget': 'bit get', 'blockchains': 'block chains', 'bybit': 'by bit', 'cryptos': 'crypto',
        'cz': 'c z', 'defillama': 'defy llama', 'devops': 'dev ops', 'eth': 'e t h', "safe's": 'safe', 'safu': 'safe who', 'stablecoin': 'stable coin',
        'tradertraitor': 'trader traitor', 'trm': 't r m', 'usdc': 'u s d c', 'usdt': 'u s d t', 'utc': 'u t c', 'xrp': 'x r p', 'zachxbt': 'zach x b t',
        '10:15': 'ten fifteen', '14': 'fourteen', '2019': 'twenty nineteen', '2022': 'twenty twenty two', '2025': 'twenty twenty five', '2026': 'twenty twenty six',
        '29': 'twenty nine', '8:05': 'eight oh five', '8:20': 'eight twenty', '8:24': 'eight twenty four', '8:32': 'eight thirty two', '9:15': 'nine fifteen',
        'p.m.': 'p m', 'a.m.': 'a m'}
def mots(phrase):
    out = []
    for m in re.findall(r"[0-9]+:[0-9]+|[0-9]+|[a-zA-Z][a-zA-Z'\-\.]*", phrase.lower()):
        m = m.strip('.') if m not in ('p.m.', 'a.m.') else m
        if m.endswith('.') and m not in REMP: m = m.rstrip('.')
        r = REMP.get(m, m.replace('-', ' ')); out += r.split()
    return out
def aligne(mp3, phrases):
    """début/fin de chaque phrase par alignement forcé PocketSphinx (modèle anglais fourni avec le paquet)"""
    from pocketsphinx import Decoder
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    toks = [mots(p) for p in phrases]
    dec = Decoder(samprate=16000, bestpath=False, loglevel='FATAL'); dec.set_align_text(' '.join(w for t in toks for w in t))
    dec.start_utt(); dec.process_raw(raw, full_utt=True); dec.end_utt(); dec.set_alignment(); dec.start_utt(); dec.process_raw(raw, full_utt=True); dec.end_utt()
    segs = [(x.name, x.start / 100, (x.start + x.duration) / 100) for x in dec.get_alignment().words()]
    segs = [x for x in segs if x[0] not in ('<sil>', '<s>', '</s>', '[NOISE]')]
    assert len(segs) == sum(len(t) for t in toks), (len(segs), sum(len(t) for t in toks))
    res, k = [], 0
    for t in toks: res.append((segs[k][1], segs[k + len(t) - 1][2])); k += len(t)
    D = duree(mp3); return [(max(0, a - .06), min(D, b + .12)) for a, b in res]

def decoupe(mp3, phrases):
    """bornes (début, fin) de chaque phrase dans le mp3 : programmation dynamique sur les silences, guidée par la longueur du texte"""
    D = duree(mp3); err = subprocess.run(['ffmpeg', '-i', mp3, '-af', 'silencedetect=noise=-38dB:d=0.18', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s0 = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]; s1 = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    gaps = [(a, b) for a, b in zip(s0, s1) if a > .05 and b < D - .05]
    N = len(phrases); w = np.array([len(p) + 8 for p in phrases], float); attendu = w / w.sum()
    voix = D - sum(b - a for a, b in gaps)   # temps parlé
    G = len(gaps); INF = 1e18
    # cout[i][g] = meilleur coût pour terminer la phrase i au trou g
    cout = np.full((N, G + 1), INF); arr = np.zeros((N, G + 1), int)
    def c(i, a, b, g):  # phrase i de a à b, se terminant sur le trou g (bonus pour un long silence)
        d = b - a; e = attendu[i] * D
        return ((d - e) / max(e, .6)) ** 2 - (1.5 * (gaps[g][1] - gaps[g][0]) if g < G else 0)
    debut = lambda g: 0 if g < 0 else gaps[g][1]
    for g in range(G):
        cout[0][g] = c(0, 0, gaps[g][0], g)
    for i in range(1, N):
        for g in range(i, G + (1 if i == N - 1 else 0)):
            fin = gaps[g][0] if g < G else D
            for h in range(i - 1, g):
                if cout[i - 1][h] >= INF: continue
                v = cout[i - 1][h] + c(i, gaps[h][1], fin, g)
                if v < cout[i][g]: cout[i][g] = v; arr[i][g] = h
    if N == 1: return [(0, D)]
    g = G; res = []
    for i in range(N - 1, -1, -1):
        h = arr[i][g] if i > 0 else -1
        res.append((debut(h), gaps[g][0] if g < G else D)); g = h
    return res[::-1]

morceaux = []   # (fichier, début, fin, texte)
for k in [f'p{i}' for i in range(1, 11)]:
    mp3 = f'{EN_DIR}/{k}_en.mp3'; ph = PH[k]
    try: b = aligne(mp3, ph); meth = 'alignement'
    except Exception as e: print('alignement impossible', k, e); b = decoupe(mp3, ph); meth = 'silences'
    paires = list(zip(ph, b))
    for x, y in sorted(FUSION.get(k, []), reverse=True):
        (tx, (a, _)), (ty, (_, fin)) = paires[x], paires[y]; paires[x:y + 1] = [(tx + ' ' + ty, (a, fin))]
    morceaux += [(mp3, a, f, t) for t, (a, f) in paires]
    print(k, len(paires), 'phrases', round(duree(mp3), 1), 's', meth)
# regroupe les phrases françaises qui commencent au même instant
fr = []
for x in FR:
    if fr and abs(x['g'] - fr[-1]['g']) < .05: fr[-1]['txt'] += ' ' + x['txt']; fr[-1]['n'] += 1
    else: fr.append({**x, 'n': 1})
# chaque groupe français reçoit autant de phrases anglaises que de phrases françaises fusionnées
assert sum(x['n'] for x in fr) == len(morceaux), (sum(x['n'] for x in fr), len(morceaux))
TOT = duree(f'{W}/voix_fr_globale.wav'); SR = 48000; piste = np.zeros(int(TOT * SR) + SR, np.float32)
fin_prec = 0; j = 0; rapport = []
for gi, x in enumerate(fr):
    grp = morceaux[j:j + x['n']]; j += x['n']
    suivant = fr[gi + 1]['g'] if gi + 1 < len(fr) else TOT - .3
    for mp3, a, b, t in grp:
        aud = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', mp3, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
        d = len(aud) / SR; debut = max(x['g'], fin_prec + .12); place = suivant - .1 - debut
        if d > place and place > .3:
            tempo = min(1.15, d / place)
            aud = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', mp3, '-af', f'atempo={tempo:.3f}', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
            d = len(aud) / SR
        i0 = int(debut * SR); piste[i0:i0 + len(aud)] += aud[:len(piste) - i0]; fin_prec = debut + d
        rapport.append(f"{x['g']:7.2f} → {debut:7.2f} ({d:4.1f}s) {t[:60]}")
open(f'{W}/rapport_calage_en.txt', 'w').write('\n'.join(rapport))
import wave
st = np.clip(piste[:int(TOT * SR)], -1, 1)
with wave.open(f'{W}/voix_en_globale.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.repeat(st[:, None], 2, 1) * 32767).astype('<i2').tobytes())
# musique / bruitages (sans voix) de chaque partie, mis bout à bout
ff('-i', f'{ANIM}/musique.wav', '-i', f'{ANIM}/et1_hd/mus.wav', '-i', f'{ANIM}/et2_hd/mus.wav', '-i', f'{ANIM}/et3_hd/mus.wav', '-i', f'{ANIM}/et4_hd/mus.wav',
   '-filter_complex', 'concat=n=5:v=0:a=1', '-ar', '48000', '-ac', '2', f'{W}/musique_globale.wav')
open(f'{W}/images_en.txt', 'w').write(''.join(f"file '{ANIM}/{d}/image.mp4'\n" for d in ('seg_hd_en', 'et1_hd_en', 'et2_hd_en', 'et3_hd_en', 'et4_hd_en')))
ff('-f', 'concat', '-safe', '0', '-i', f'{W}/images_en.txt', '-i', f'{W}/voix_en_globale.wav', '-i', f'{W}/musique_globale.wav', '-filter_complex',
   "[1]asplit[va][vb];[2]volume=0.55[m];[m][va]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];[vb][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a];"
   "[0]fps=60,noise=alls=2:allf=t,vignette=PI/6,pad=1920:1080:0:138:black[v]",
   '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-t', f'{TOT:.3f}', f'{ANIM}/Binance_hack_EN_1080p60.mp4')
print('FINI_EN')
