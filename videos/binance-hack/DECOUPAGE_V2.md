# Découpage v2 — Binance (d'après l'analyse de Silk Road publiée)

## Ce que fait Silk Road (mesuré sur silk-road_FR_publiee_1080p.mp4)
| Moment | Image | Son |
|---|---|---|
| 0 → 0,8 s | noir | nappe grave qui entre |
| 0,8 → 13 s | **cold open sans voix** : 6 plans 3D (large, gros plan du perso rouge, plongée zénithale) | nappe + cordes dissonantes + **battement de cœur qui accélère** + montée (souffle) de 9,5 à 13 s |
| 13 s | **coupe au noir** + titre « l'empire à un milliard » (Georgia gras italique) | **impact** + longue traîne |
| 13 → 17 s | titre puis fondu au noir | silence, traîne |
| 17 → 18 s | date « 1er octobre 2013 » | silence |
| 18 s → | la voix commence | pulsation de basse en croches + **tic-tac d'horloge, 1 coup / seconde, tout le long** |
| révélations | coupe sèche au noir, 0,5 à 1,5 s de silence, puis impact | montée → coupure sèche |

Rythme : un plan toutes les 3 à 6 s dans les parties d'enquête, plus long dans la scène pivot. Chaque phrase forte a son image. Grain + vignettage, footage désaturé (preset `nuit_enquete`).
**Charte typographique** : grands titres en **Georgia Gras Italique** (`georgiaz.ttf`), ex. « Dread Pirate Roberts » ; petites légendes en Segoe UI Light espacé ; chiffres en Segoe UI Light. Étiquettes de noms : noires à bord blanc déchiré.

## Mes erreurs sur le brouillon v1
1. La voix démarre à 0 s : pas de cold open muet, pas de tension.
2. Aucun son : ni nappe, ni cœur, ni impact, ni tic-tac.
3. Images fixes zoomées au lieu d'animations (voiture immobile, personne qui ne tape pas).
4. Calage estimé, donc décalé.
5. Titres en Georgia italique fin au lieu de Georgia gras italique.

## Nouvelle méthode
- **Calage exact** : transcription mot à mot de la voix (ElevenLabs Speech-to-Text), pas d'estimation.
- **Son** : `musique.py` de Silk Road adapté à Binance (nappe, cœur, montées, impacts, basse, **tic-tac 1/s sur toute la vidéo**), plus des bruitages (moteur, pluie fine, clavier, notifications).
- **Silences de tension** insérés dans la voix (coupe au noir + impact) aux révélations : « Entrée. » · « Une seule suffit… » · « Trop tard. » · « Il en manque… trois. » · « Mais comment ? » · « quelqu'un attendait ce geste » · question finale.
- **Animation** : les décors où seule la caméra bouge passent en **Three.js maquette grise** (modèle `silk-road/partie3/decors.html`, capture < 0,5 s/image, donc faisable ici) avec nos persos figés (GLB). Blender uniquement pour ce qui bouge vraiment : la voiture qui roule et le pirate qui tape (rendu de nuit sur le PC de Mo).

## Ouverture Binance (0 → ~20 s), plan par plan
| Temps | Image (animée) | Son |
|---|---|---|
| 0 → 0,8 | noir | nappe grave |
| 0,8 → 3,5 | [3D] ruelle de nuit, sol mouillé, caméra au ras du sol ; la Volvo entre dans le champ, phares qui balaient les façades | nappe + moteur lointain + pluie |
| 3,5 → 5,5 | [3D] la Volvo passe tout près, reflets sur l'asphalte | moteur qui passe (Doppler) |
| 5,5 → 8 | [3D] la caméra monte le long de l'immeuble jusqu'à la seule fenêtre bleue | cordes, cœur qui démarre |
| 8 → 10,5 | [3D] chambre : le pirate rouge de dos, il tape (Typing) | cœur qui accélère + clavier |
| 10,5 → 12 | [3D] gros plan écran : « BINANCE » apparaît dans le code | montée |
| 12 → 13 | [3D] macro sur la touche Entrée, le doigt appuie | montée → **clic** |
| 13 | **coupe au noir** + titre « 20 minutes » en Georgia gras italique | **impact** |
| 13 → 16 | titre puis fondu | traîne |
| 16 → 18 | date « 29 octobre 2026 · 20:05 UTC » | silence |
| 18 → | la voix commence (« Vingt-neuf octobre… ») sur la ruelle, et la suite du cold open se rejoue avec la voix | basse + tic-tac |
