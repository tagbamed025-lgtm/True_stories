# BIBLE — TRU Stories
Document de référence unique. Toute discussion (projet Claude ou Claude Code) le lit **avant** de répondre. Mise à jour : 21 octobre 2026 (leçons de Silk Road).

## 1. La chaîne
- **TRU Stories** : histoires vraies racontées comme des thrillers Netflix. 3D stylisée + footage + archives. Langue : **français**, et chaque vidéo a aussi sa **version anglaise** (stockée pour la future chaîne anglaise, lancée à partir de 10 vidéos).
- Thèmes : environ 70 % histoire, psychologie, guerre et espionnage, environ 30 % hackers, crime et systèmes qui s'effondrent. L'actualité internationale forte passe aussi.
- Format : **5 à 6 min maximum** (≈ 600 à 750 mots de voix off). Un Short de 45 à 60 s par vidéo.
- Vidéos déjà faites (modèles de ton) : `references/scripts_precedents/`
  - Pablo Escobar : « Le jour où Pablo Escobar a compris que c'était fini »
  - El Chapo : « L'Évasion Impossible »
  - Gary McKinnon : « Le hacker qui a piraté les ordinateurs de l'armée américaine »
  - Ross Ulbricht / Silk Road : **terminée** (oct. 2026) — vidéo de référence pour la méthode (`videos/silk-road/`)

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
- **Anglais** : voix **Nathan — Deep Podcast Narrator** (ElevenLabs), script `SCRIPT_EN.md` adapté (pas une traduction mot à mot), mêmes parties p1…p6. Fichier : `voix/VO_EN_<voix>.mp3`.
- **Cold open sans voix** : la voix démarre vers **0:18** (après titre + date).
- **Calage au mot** : transcription horodatée ElevenLabs (Scribe) de la voix → `voix/transcription_*.md`. Chaque plan est calé sur sa phrase.

## 5. Style visuel de marque
- Personnages **low poly stylisés** (décimation 0,03 + flat shading). Jamais réalistes.
- **Personnage principal en rouge émissif. Tous les autres en blanc lumineux.** Les femmes se reconnaissent à leur silhouette et à leurs cheveux.
- Décors sombres. Le rouge est réservé aux moments de rupture. Image en 2,39:1, grain léger, flou de profondeur, caméras lentes.
- Méthode hybride : **[CODE]** = HTML/Three.js capturé image par image. **[3D]** = Blender piloté par scripts Python. Une vidéo codée peut devenir l'écran d'un objet 3D (matériau émissif, texture MOVIE).
- Scripts de style : `style/` (`styles_tuto.py`, `distribution.py`).
- **Style validé (13 oct. 2026, Silk Road)** : ouverture « trailer » ≈ 1 min en Blender, puis alternance de décors **Three.js style maquette grise** (seul le rouge ressort, ombres douces, flou de profondeur) avec nos personnages **figés** (GLB exportés par `videos/silk-road/3d/exporter_glb.py`), footage sombre et désaturé, archives réelles, cartes sobres. Étiquettes de noms noires à bord blanc déchiré. Son : voix + pulsation basse + tic-tac. Blender seulement quand les personnages doivent bouger. Modèles : `outils/capture/capture.js`, `videos/silk-road/partie3/decors.html`.
- **Étalonnage (charte)** : presets ffmpeg dans `outils/etalonnage.py`. Référence validée : `nuit_enquete` (homme devant ses écrans la nuit : désaturé, ombres bleutées, coins sombres). Autres : `tech_froide`, `jour_doux`, `objet_terne`, `souvenir`. Ajouter un preset nommé à chaque nouveau look validé.

### Rythme et mise en scène (validé)
- **Cold open ≤ 10 s d'images** puis titre (3 s) et date (2 s). Le personnage principal est **déjà en place** : ne jamais révéler trop tôt l'objet clé (ex. l'ordinateur).
- Personnages secondaires **toujours figés**, assis ou debout dans une pose ; c'est la caméra qui bouge (travellings lents, contre-plongées, plongée zénithale) et les coupes qui rythment.
- Chaque phrase importante de la voix a **son image** (motion design qui suit la parole : liste ✓/✗, compteur, fenêtres qui s'ouvrent, fils rouges qui se tendent).
- Utiliser les **vraies photos** de la personne (archives) aux moments clés : portrait, prison, libération.
- Mise en garde : vérifier de près **chaises, mains/clavier, orientation** sur une planche rapprochée avant tout rendu.

### Miniatures (validé)
- **Diorama 3D** : puits de lumière sur fond noir ou monde gris, le personnage principal en rouge, la situation lisible en 1 s (ex. agents FBI autour de lui, fausse dispute derrière lui).
- 1 à 3 **étiquettes** maximum (noire à bord blanc, ou rouge pour l'enjeu : « 1 MILLIARD $ », « DARK WEB »). **Pas de gros titre** sur l'image : c'est le titre YouTube qui parle.
- Toujours **2 miniatures + 2 titres** pour l'A/B testing (un titre affirmation choc « Le FBI a simulé une dispute pour l'arrêter », un titre « Comment / Pourquoi… »), en FR et en EN. Outil : `decors.html?s=mini&v=1|2`.

### Livrables par vidéo
Vidéo FR 2K · vidéo EN 2K · 2 miniatures · 2 titres FR + 2 EN · description FR + EN (avec chapitres et sources) · **3 à 4 reels 9:16 de 30 à 40 s** (accroche en haut, extraits de tension) via `livrables/reels.py`.

## 6. Assets
- Inventaire de tout ce qu'on possède : **`ASSETS.md`**. On le consulte avant de demander un téléchargement, et on le met à jour après chaque ajout.
- Stockage : sur GitHub dans `assets3d/<catégorie>/` (fichier de moins de 50 Mo, à alléger avec `outils/`). Sur Google Drive « TRU_Stories_Assets/ » avec la même arborescence pour les fichiers plus lourds.
- Sources : Mixamo (personnages + animations : **Without Skin, 30 fps**), BlenderKit, Poly Haven (HDRI, textures), Sketchfab, MPFB. Footage gratuit : Pexels, Pixabay.
- Personnages figés pour Three.js : `videos/silk-road/3d/exporter_glb.py` → `assets3d/<slug>/glb/`. Archives (photos) : `assets3d/<slug>/archives/`.

## 7. Chaîne de production (qui fait quoi)
| Étape | Où | Résultat |
|---|---|---|
| 1. Idée (proposée par Mo ou veille hebdomadaire) | Projet Claude (chat) | 3 à 5 idées → Mo choisit |
| 2. Recherche + script vérifié | Projet Claude | `SCRIPT.md` + sources |
| 3. Voix off Adrien | Projet Claude (ElevenLabs) | p1…pN.mp3 |
| 4. Découpage + liste d'assets | Projet Claude | `DECOUPAGE.md` + `BON_DE_PRODUCTION.md` |
| 5. Téléchargements manquants | Mo (ou Claude Code via Blender) | assets dans `assets3d/` |
| 6. Montage 3D, rendu, assemblage | **Claude Code** sur le PC de Mo | `rendu/<slug>_final.mp4` |
| 7. Miniatures, reels, titres, descriptions | Claude Code | fichiers dans `videos/<slug>/livrables/` |
| 8. Version anglaise | Claude Code (voix EN par Mo) | `rendu/<slug>_FULL_EN.mp4` |

**Méthode de travail (obligatoire)**
1. **Brouillon d'abord** : 960 px, 15 i/s, 16 échantillons → Mo valide le déroulé (≈ 20 min). **Haute qualité seulement après « validé »**, lancée le soir, et on ne refait que les plans modifiés.
2. Donner des durées **mesurées** (chronométrer 10 images), jamais estimées.
3. Blender seulement pour les plans où des personnages bougent ; le reste en **Three.js / HTML** (capture ≈ 50× plus rapide).
4. **Bilingue dès le départ** : tous les textes à l'écran passent par le dictionnaire `trad_en.json` (fonction `T()` dans les scripts, `?lang=en` pour les pages capturées) ; la version EN se fabrique ensuite avec `final_en.sh` + `montage_en.py` (recalage sur la voix EN).
5. Mo peut finir le montage dans **CapCut** : on lui laisse aussi les morceaux séparés.

Le **bon de production** (`videos/<slug>/BON_DE_PRODUCTION.md`) fait le lien entre le chat et Claude Code. Modèle : `videos/_MODELE/`.

## 8. Matériel et règles techniques
- PC de Mo : NVIDIA Quadro P2000 (4 Go), 32 Go de RAM, Windows, Blender 5.2 avec les extensions BlenderKit, MPFB et « MCP for Blender ».
- Temps mesurés : EEVEE ≈ 6 à 9 s/image en 1920 sur une scène simple ; **≈ 50 s/image dans une scène lourde (kit BlenderKit + 11 personnages)** → rendre en 1280 et agrandir en 2K. 2560 sature la carte. Captures Three.js : < 0,5 s/image.
- Capture HTML/Three.js : `outils/capture/capture.js` (Edge + playwright-core ; mettre à jour playwright si Edge se met à jour). Étalonnage : `outils/etalonnage.py`.
- Pendant un rendu, le PC est lent : lancer les rendus longs le soir. Un seul rendu à la fois (vérifier qu'aucune ancienne boucle ne tourne).
- Rendu : menu Rendu (Ctrl+F12 ne marche pas). Rendu reprenable, image par image.
- `outils/alleger_personnages.py` : à lancer **uniquement dans un fichier Blender vide**, sinon il efface la scène. `outils/preparer_kit.py` : pour alléger un kit d'objets.

## 9. Production en cours
Voir le tableau d'état dans `videos/<slug>/BON_DE_PRODUCTION.md`. Silk Road : terminée (FR publiée sur YouTube, EN stockée).
Idées proposées le 16 oct. 2026 (à choisir par Mo) : Malone Lam (casse bitcoin de 245 M$), Corée du Nord / Bitget (351 M$), Toni Musulin (convoyeur, 11 M€), fraude foncière à Dakar (5,5 M$).

## 10. Veille hebdomadaire (à activer)
Une fois par semaine : 3 à 5 affaires internationales marquantes ou histoires oubliées, avec pour chacune un titre, un hook d'une phrase, pourquoi on reste jusqu'au bout, et 2 sources. Jour, heure et fuseau horaire : à fixer par Mo.
