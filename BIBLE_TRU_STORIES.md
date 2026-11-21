# BIBLE — TRU Stories
Document de référence unique. Toute discussion (projet Claude ou Claude Code) le lit **avant** de répondre, puis **`ASSETS.md`** (où sont les assets et comment s'en servir). Mise à jour : 19 novembre 2026 (méthode Fern + bibliothèque LIBRARY).

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

### 2 bis. Hook style Fern (30 à 40 s)
Hook style Fern : on entre par un témoin ordinaire (heure + lieu), une image anormale en 2 détails concrets, le témoin qui fige, un vrai son/document sur noir (911, écoute, rapport), puis l'expert qui « sait déjà » — coupe. Marqueurs dossier en machine à écrire (CAM 4 · REC, FBI WIRETAP, « 3 jours après… »).

### 2 ter. Montage style Fern
Montage style Fern : plans de 2 à 4 s, alternance large / subjectif intérieur / surveillance N&B / noir / changement d'échelle / personnage ; caméra toujours en mouvement lent ; une seule source de lumière par plan ; 2 écrans noirs avec texte machine à écrire ; titres : heure en italique, archives en machine à écrire, source en italique fin ; chaque plan pose une question sans y répondre.

### 2 quater. Scène de référence (mini-doc « camping-car », ~26 s, à imiter pour chaque hook)
| t | Plan | Rôle |
|---|---|---|
| 0 s | Noir + petit texte | respiration avant le film |
| 2 s | Plan large de dos : voiture sur route de campagne à l'aube, danger petit au loin, titre « 5:30 AM » | heure précise, in medias res |
| 4 s | Subjectif depuis la banquette arrière, intérieur sombre éclairé en bleu, danger à travers le pare-brise | on est dans la voiture avec le témoin (voiture **avec intérieur**) |
| 6 s | Caméra de surveillance N&B, « REC », « 3 days after abduction » en machine à écrire | bascule « dossier réel » |
| 10 s | Travelling avant lent dans les phares, on découvre le corps sous le véhicule | la lumière révèle l'info |
| 13 s | Plan bas, lignes de route en diagonale | malaise |
| 15 s | Retour intérieur, fixe 4 s, silence | le témoin fige |
| 19 s | Noir : « Operator: "911, what's your emergency?" » | vrai son sur noir |
| 21 s | Avion militaire au-dessus de montagnes, « FBI WIRETAP » | changement d'échelle |
| 24 s | Agent en chemise, fond noir, lumière latérale, puis cible de tir | l'expert qui sait — indice non expliqué — coupe |

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

### Méthode de production « Fern » (scènes cinématographiques plongeantes)
1. **Vrais modèles 3D d'abord** : pour chaque scène, on prend les objets dans LIBRARY (route, voiture avec intérieur, véhicule suspect, personnage, décor). Ce qui manque se télécharge gratuitement (CGTrader « Free », Poly Haven), jamais généré.
2. **Dossier de références de la scène** : on copie les modèles utiles dans `videos/<slug>/references_3d/`.
3. **Blender piloté par Claude via MCP for Blender** : un prompt par scène qui donne (a) la description, (b) l'ambiance et la lumière (ex. aube, phares seuls), (c) résolution et FPS, (d) le budget de rendu.
4. **Vérification avant rendu** : scène et caméra montées, Mo regarde et corrige **avant** le rendu.
5. **Voix off** puis **montage** : l'agent reçoit l'emplacement des clips, de la bibliothèque musique et de la bibliothèque d'effets sonores ; il fait un premier montage que Mo retouche.

## 6. Assets
- Inventaire de tout ce qu'on possède : **`ASSETS.md`**. On le consulte avant de demander un téléchargement, et on le met à jour après chaque ajout.
- **Bibliothèque locale (PC de Mo)** : `C:\Users\HP\Documents\TRU Stories Blender\LIBRARY\` (01_PERSONNAGES, 02_ANIMATIONS, 03_VEHICULES, 04_DECORS, 05_SCENES_BLEND, 06_MEDIAS, 07_REFERENCES, 08_OUTILS, 99_CORBEILLE), catalogue `_INDEX.csv`, guide `LISEZ_MOI_LIBRARY.md`. Tout asset 3D vient d'abord de LIBRARY ; on ne télécharge que ce qui manque (Poly Haven puis CGTrader / Sketchfab, licence libre de droits, jamais « Editorial »), avec source et licence dans `_INDEX.csv`. Jamais de personnage de marque (Spider-Man, Marvel, Star Wars…). Un téléchargement n'est « fait » que s'il est **vérifié sur le disque**.
- Outil annexe : skill Claude Code **Faceless Videos v2** (5 styles dont « Red Ghost » true crime) dans `LIBRARY\07_REFERENCES\faceless-videos\` (procédure : `INSTALL_PROMPT.txt`).
- Stockage : sur GitHub dans `assets3d/<catégorie>/` (fichier de moins de 50 Mo, à alléger avec `outils/`). Sur Google Drive « TRU_Stories_Assets/ » avec la même arborescence pour les fichiers plus lourds.
- **Vidéos sur GitHub = copies de référence légères** (pas de Drive : espace insuffisant). Chaque fichier < 50 Mo (limite dure GitHub : 100 Mo). Vidéo finale FR et EN ré-encodées en **1080p, CRF 24, AAC 128k** (≈ 40-45 Mo pour 5 min) + reels, dans `videos/<slug>/archive_video/` ; scène .blend validée dans `assets3d/<slug>/scenes/`. Si une vidéo dépasse 50 Mo : monter le CRF (26-28) ou la découper par temps (`ffmpeg -f segment -segment_time 120 -reset_timestamps 1`), jamais un découpage binaire. Les masters 2K/4K et les rendus intermédiaires restent sur le PC de Mo (le `.gitignore` exclut `rendu/*.mp4`, `partie*/final*/`, `partie*/brouillon*/`) — ajouter les archives avec `git add -f`.
- Git : pousser avec le compte **tagbamed025-lgtm** (propriétaire). Le dépôt local force ce compte (`credential.https://github.com.username`).
- Sources : Mixamo (personnages + animations : **Without Skin, 30 fps**), BlenderKit, Poly Haven (HDRI, textures), Sketchfab, MPFB. Footage gratuit : Pexels, Pixabay.
- Personnages figés pour Three.js : `videos/silk-road/3d/exporter_glb.py` → `assets3d/<slug>/glb/`. Archives (photos) : `assets3d/<slug>/archives/`.

### 6 bis. Utiliser LIBRARY pour une nouvelle vidéo (procédure obligatoire)
1. **Chercher d'abord dans LIBRARY** : lire `ASSETS.md` §0 puis `LIBRARY\_INDEX_CGTRADER_3.csv` (un dossier par modèle : 03_VEHICULES\police_urgence | voitures | motos | autres | avions | bateaux ; 01_PERSONNAGES\humains ; 04_DECORS\ville | batiments | interieurs | objets). Chaque dossier contient le modèle **et ses textures**, déjà extraites.
2. **Choisir le plus propre, c'est à Claude de décider** : préférer `.blend` > `.fbx` > `.glb` > `.obj` ; préférer un modèle avec intérieur pour les plans POV voiture ; vérifier le nombre de polygones (alléger au-delà de ~500 k pour un objet de fond) ; faire **une image test EEVEE** du modèle choisi et la montrer à Mo avant de construire la scène. Si deux modèles conviennent, prendre le plus léger qui tient le plan.
3. **Copier, ne jamais déplacer** : copier le dossier choisi dans `videos/<slug>/references_3d/`. LIBRARY reste intacte.
4. **Textures** : après import, `Fichier > Données externes > Rechercher les fichiers manquants` sur le dossier du modèle ; puis `Empaqueter les ressources` dans la copie de travail.
5. **Style de marque** : personnages restylés (principal rouge émissif, autres blancs) ; véhicules, décors et objets gardent leurs textures mais en lumière sombre et contrastée (nuit, néons, éclairage latéral).
6. **Ce qui manque** : seulement après l'étape 1, chercher dans cet ordre : Poly Haven (CC0 : HDRI, textures, petits props, via API ou MCP Blender) → BlenderKit gratuit (MCP Blender) → Sketchfab « Downloadable » CC-BY (créditer l'auteur en description) → CGTrader gratuit **téléchargé par Mo à la main** (jamais d'automatisation : le compte a déjà été suspendu ; Claude dit seulement quel fichier prendre). Toujours « Royalty Free », jamais « Editorial ». Après tout ajout : ranger dans LIBRARY, mettre à jour `_INDEX` et `ASSETS.md`, et vérifier sur le disque.
7. **À ne pas utiliser** : `00_A_TRIER` (modèles non identifiés, à vérifier d'abord) et `99_CORBEILLE`.

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
Voir le tableau d'état dans `videos/<slug>/BON_DE_PRODUCTION.md`. **En cours : NVIDIA** (novembre 2026). Silk Road : terminée (FR publiée sur YouTube, EN stockée).
Idées proposées le 16 oct. 2026 (à choisir par Mo) : Malone Lam (casse bitcoin de 245 M$), Corée du Nord / Bitget (351 M$), Toni Musulin (convoyeur, 11 M€), fraude foncière à Dakar (5,5 M$).

## 10. Veille hebdomadaire (à activer)
Une fois par semaine : 3 à 5 affaires internationales marquantes ou histoires oubliées, avec pour chacune un titre, un hook d'une phrase, pourquoi on reste jusqu'au bout, et 2 sources. Jour, heure et fuseau horaire : à fixer par Mo.
