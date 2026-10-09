# BIBLE — TRU Stories
Document de référence unique. Toute discussion (projet Claude ou Claude Code) le lit **avant** de répondre. Mise à jour : 9 octobre 2026.

## 1. La chaîne
- **TRU Stories** : histoires vraies racontées comme des thrillers Netflix. 3D stylisée + footage + archives. Langue : français.
- Thèmes : environ 70 % histoire, psychologie, guerre et espionnage, environ 30 % hackers, crime et systèmes qui s'effondrent. L'actualité internationale forte passe aussi.
- Format : **5 à 6 min maximum** (≈ 600 à 750 mots de voix off). Un Short de 45 à 60 s par vidéo.
- Vidéos déjà faites (modèles de ton) : `references/scripts_precedents/`
  - Pablo Escobar : « Le jour où Pablo Escobar a compris que c'était fini »
  - El Chapo : « L'Évasion Impossible »
  - Gary McKinnon : « Le hacker qui a piraté les ordinateurs de l'armée américaine »
  - Ross Ulbricht / Silk Road : en production (`videos/silk-road/`)

## 2. ADN narratif (résumé de `references/prompts/`)
- **Ouverture in medias res.** On commence dans la tension (un danger, une décision, un compte à rebours), jamais par une date ou une biographie. Une heure précise et un lieu (« 2 décembre 1993. 15 h 17. »).
- Écriture **au présent**, phrases courtes, pauses (« … »), description visuelle et sonore : le spectateur voit le film.
- Le **« tu »** est réservé aux passages clés, pour projeter le spectateur.
- **Structure en remparts** : cold open → qui est cet homme → escalade → point de rupture → conséquence → fin philosophique. Toutes les 20 à 40 s : une révélation, un danger ou une question nouvelle. Des boucles ouvertes et des rappels du cold open.
- Petits dialogues réalistes (radio, agents, gardiens).
- Fin : une phrase forte, ironique ou philosophique, et une question laissée ouverte. Jamais de résumé.
- Interdits : ton scolaire, ton Wikipédia, remplissage, listes à puces dans la narration.
- **Vérité** : dates, noms et chiffres réels, chaque fait sourcé. Un fait incertain est retiré ou présenté comme « selon… ». Les dialogues reconstitués sont signalés comme tels dans les notes.

## 3. Format du script
- Code couleur : **[3D]** (jaune) Blender · **[STOCK]** (cyan) footage générique · **[ARCHIVE]** (vert) vraie image · **[CODE]** écrans, cartes, chronologies, titres animés.
- La voix off est en blocs `>`. « … » = respiration, **[PAUSE]** = 1 s de silence.
- En fin de script : section **Sources** (liens).

## 4. Voix off
- ElevenLabs, voix **Adrien** : `voice_id = TTtB1x9U8PF0Vgf20IAP` (français, grave, calme, narration).
- **Économie de crédits** : un essai fait 100 caractères maximum. Une seule génération par passage (generations_count = 1). On génère par parties (p1, p2…) pour pouvoir refaire un seul passage.
- Fichiers : `videos/<slug>/voix/p1.mp3…` + `VO_complete.mp3`.

## 5. Style visuel de marque
- Personnages **low poly stylisés** (décimation 0,03 + flat shading). Jamais réalistes.
- **Personnage principal en rouge émissif. Tous les autres en blanc lumineux.** Les femmes se reconnaissent à leur silhouette et à leurs cheveux.
- Décors sombres. Le rouge est réservé aux moments de rupture. Image en 2,39:1, grain léger, flou de profondeur, caméras lentes.
- Méthode hybride : **[CODE]** = HTML/Three.js capturé image par image. **[3D]** = Blender piloté par scripts Python. Une vidéo codée peut devenir l'écran d'un objet 3D (matériau émissif, texture MOVIE).
- Scripts de style : `style/` (`styles_tuto.py`, `distribution.py`).

## 6. Assets
- Inventaire de tout ce qu'on possède : **`ASSETS.md`**. On le consulte avant de demander un téléchargement, et on le met à jour après chaque ajout.
- Stockage : sur GitHub dans `assets3d/<catégorie>/` (fichier de moins de 50 Mo, à alléger avec `outils/`). Sur Google Drive « TRU_Stories_Assets/ » avec la même arborescence pour les fichiers plus lourds.
- Sources : Mixamo (personnages + animations : **Without Skin, 30 fps**), BlenderKit, Poly Haven (HDRI, textures), Sketchfab, MPFB.

## 7. Chaîne de production (qui fait quoi)
| Étape | Où | Résultat |
|---|---|---|
| 1. Idée (proposée par Mo ou veille hebdomadaire) | Projet Claude (chat) | 3 à 5 idées → Mo choisit |
| 2. Recherche + script vérifié | Projet Claude | `SCRIPT.md` + sources |
| 3. Voix off Adrien | Projet Claude (ElevenLabs) | p1…pN.mp3 |
| 4. Découpage + liste d'assets | Projet Claude | `DECOUPAGE.md` + `BON_DE_PRODUCTION.md` |
| 5. Téléchargements manquants | Mo (ou Claude Code via Blender) | assets dans `assets3d/` |
| 6. Montage 3D, rendu, assemblage | **Claude Code** sur le PC de Mo | `rendu/<slug>_final.mp4` |
| 7. Miniature, Short, sous-titres | Claude Code | fichiers dans `videos/<slug>/livrables/` |

Le **bon de production** (`videos/<slug>/BON_DE_PRODUCTION.md`) fait le lien entre le chat et Claude Code. Modèle : `videos/_MODELE/`.

## 8. Matériel et règles techniques
- PC de Mo : NVIDIA Quadro P2000 (OptiX), 32 Go de RAM, Windows, Blender 5.2 avec les extensions BlenderKit, MPFB et « MCP for Blender ». EEVEE ≈ 7 s par image en 1080p.
- Rendu : menu Rendu (Ctrl+F12 ne marche pas). Rendu reprenable, image par image.
- `outils/alleger_personnages.py` : à lancer **uniquement dans un fichier Blender vide**, sinon il efface la scène. `outils/preparer_kit.py` : pour alléger un kit d'objets.

## 9. Production en cours
Voir le tableau d'état dans `videos/<slug>/BON_DE_PRODUCTION.md`. Projet actif : **`videos/silk-road/`**.

## 10. Veille hebdomadaire (à activer)
Une fois par semaine : 3 à 5 affaires internationales marquantes ou histoires oubliées, avec pour chacune un titre, un hook d'une phrase, pourquoi on reste jusqu'au bout, et 2 sources. Jour, heure et fuseau horaire : à fixer par Mo.
