# Charte d'étalonnage TRU Stories (filtres ffmpeg) — à appliquer aux footages selon le passage et le contexte.
# Usage dans un montage :  from etalonnage import ETALONNAGE ;  vf = f"{cadre},{ETALONNAGE['nuit_enquete']},{base}"
# Finition commune (sur la vidéo montée) : FINITION.
ETALONNAGE = {
    # ★ Référence validée par Mo (13 oct. 2026) : « homme devant ses écrans la nuit », Silk Road partie 2.
    #   Nuit, désaturé, ombres bleutées, peau qui reste lisible, coins sombres. Pour : enquêteurs, hackers, bureaux de nuit, tension.
    'nuit_enquete': "eq=saturation=.45:brightness=-.08,colorbalance=bs=.12:bm=.06",
    # Salle de serveurs / technologie froide : quasi monochrome, contrasté, bleu léger.
    'tech_froide': "eq=saturation=.35:brightness=-.1:contrast=1.1,colorbalance=bs=.08",
    # Extérieur de jour / rues : couleurs adoucies, réalistes.
    'jour_doux': "eq=saturation=.7",
    # Objets, colis, détails du quotidien : un peu ternes, légèrement sombres.
    'objet_terne': "eq=saturation=.6:brightness=-.05",
    # Souvenir / archive personnelle (photos de famille) : chaud, contraste doux.
    'souvenir': "eq=saturation=.85:contrast=1.05,colorbalance=rs=.04:bs=-.04",
}
# Finition de toute la vidéo : grain très léger + vignette (les côtés assombris aimés par Mo).
FINITION = "noise=alls=2:allf=t,vignette=PI/6"
