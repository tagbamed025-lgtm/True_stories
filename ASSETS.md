# Inventaire des assets TRU Stories
Consulter avant de demander un téléchargement. Mettre à jour après chaque ajout.
Emplacement : GitHub `assets3d/…` (fichiers de moins de 50 Mo). Sinon Google Drive `TRU_Stories_Assets/…` (même arborescence) : indiquer « Drive » dans la colonne.
**PC de Mo** = `C:\Users\HP\Downloads\TRU Stories\` (abrégé `DL\`), pas encore sur GitHub ni Drive.
Dernier inventaire : 11 octobre 2026 (Claude Code).

## Personnages (Mixamo, sans textures, à styliser)
| Fichier | Description | Utilisé dans | Emplacement |
|---|---|---|---|
| Ch31.fbx | Homme jeune, pull | Silk Road (Ross, rouge) | assets3d/silk-road/personnages/ · version allégée 2,6 Mo : DL\persos\leger\ |
| Ch23.fbx | Homme en veste | Silk Road (agents FBI ×2) | assets3d/silk-road/personnages/ · allégée : DL\persos\leger\ |
| Ch21.fbx | Femme | Silk Road (agente) | assets3d/silk-road/personnages/ · allégée : DL\persos\leger\ |
| Ch22.fbx | Femme | Silk Road (lectrice / agente) | assets3d/silk-road/personnages/ · allégée : DL\persos\leger\ |
| Ch18_nonPBR.fbx | Personnage Mixamo (13 Mo, 21 600 faces) | — | DL\ |
| X Bot.fbx / Y Bot.fbx | Mannequins Mixamo | — | DL\ |
| guy by CLOAKING .US (.glb) | Homme low poly (Sketchfab) | — | DL\ |

Versions lourdes (50 Mo chacune) : DL\persos\Ch21/22/23/31_nonPBR.fbx. Les scripts utilisent les versions `leger\`.
Manque souvent : homme en blouson, femme aux cheveux longs, policier ou soldat, homme âgé.

## Animations Mixamo
⚠️ Les fichiers de DL\ sont exportés **With Skin, 60 i/s** (pas « Without Skin, 30 fps » comme le veut la bible). Ils marchent : les scripts gardent seulement l'action et la ralentissent ×0,5. Os en `mixamorig:` ; les persos (`mixamorig9:`) sont renommés à l'import.
| Fichier | Mouvement | Durée | Emplacement |
|---|---|---|---|
| Sitting Idle.fbx | Assis, au repos | 258 img | DL\ |
| Walking.fbx / Walking (1).fbx | Marche | 62 img | DL\ |
| Walking Left Turn.fbx | Marche + virage à gauche | 72 img | DL\ |
| Female Start Walking.fbx | Départ de marche (image 1 = pose debout) | 113 img | DL\ |
| Texting And Walking.fbx / Walking While Texting.fbx | Marche en tapant sur un téléphone | 199 / 241 img | DL\ |
| Talking On Phone.fbx | Debout, au téléphone | 1166 img (30 i/s) | DL\ |
| Driving.fbx | Conduite | 301 img | DL\ |
| Sitting.fbx | Assis — se relève en boucle : n'utiliser qu'une pose figée | 267 img | DL\ |
| Stand To Sit.fbx | S'asseoir | 135 img | DL\ |
| Typing.fbx | Taper au clavier, assis | 988 img | DL\ |
| Idle, Standing Idle, Standing Arguing, Yelling, Stand Up, Picking Up (Object).fbx | Poses debout, dispute, saisie (os `mixamorig4:`, renommés à l'import) | 45 Mo chacun | DL\ |
| Typing (1) à (4).fbx | Persos + Typing : (1) Ch02 femme · (2) Ch26 femme en talons · (3) Ch18 homme · (4) Ch12 homme en veste | 50 Mo chacun | DL\ |

**Manquent pour Silk Road** : Typing, Sitting Down, Standing Up, Looking Around, Surprised, Arguing, Reading, Slow Walk. Plan 4.7 : le lever est simulé (fondu Sitting Idle → pose debout) en attendant Standing Up.

## Objets
| Fichier | Contenu | Emplacement |
|---|---|---|
| Sans titre_kit_leger.blend (74 Mo) | **Kit bibliothèque complet** (BlenderKit) : tables (GUBI, Reading Table, Wooden table ×3, Mid Century, office), chaises (Simple wooden chair, Wooden Chair ×2, Wooden Dining Chair), étagères vides (Ash wood, Wooden, Hazel, Pyrite, Bookcase, Ikea Billy, Wall Book Shelf, Display Shelves), livres (Books ×5, Stacked set, Encyclopedia set, Julius Caesar), portables (Mcbook, Samsung Galaxy Book 2, Laptop Notebook), lampes (Vintage, LED noire/blanche), tasse, café et biscuits, sac à dos, table basse | DL\persos\ (trop lourd pour GitHub → Drive) |
| Sans titre.blend (72 Mo) | Même kit, non allégé (+ .blend1, bibliotheque_recup.7z/.blend1 = sauvegardes) | DL\persos\ |
| kit_bibliotheque.blend | tasse, lampe de bureau, table (partiel, ancien) | assets3d/silk-road/objets/ |
| Rayonnage rempli de livres | généré par script (`rayon_maillage()` dans videos/silk-road/3d/biblio.py) | code |
| silk-road_v4_VALIDE.blend (34 Mo) | Scène finale salle de Glen Park, chaises corrigées, persos figés, caméras par plan | Drive : TRU_Stories_Assets/videos/silk-road/3d/ (+ local Documents\TRU Stories Blender\) |
| Salle de Glen Park (code) | murs crème, piliers, fenêtres à stores, panneau « Science Fiction », rue de SF | videos/silk-road/3d/glenpark.py |
| FBI.fbx (+ FBI_D2.png) | Agent FBI tactique texturé, squelette Biped (pas Mixamo), échelle ×100 à l'import ; licence à vérifier | assets3d/silk-road/fbi_soldier_src/ (non utilisé) |
| GLB figés pour Three.js | alford_assis_tape, agent_debout_veste, agent_debout_2, agente_debout, ross_assis_tape, ross_debout | assets3d/silk-road/glb/ (générés par videos/silk-road/3d/exporter_glb.py) |
| kenney_car-kit.zip / kenney_watercraft-pack.zip | Kits Kenney voitures et bateaux (low poly) | DL\ |

## Décors, véhicules, bâtiments, HDRI
| Fichier | Contenu | Emplacement |
|---|---|---|
| ruelle.blend | Ruelle de nuit : murs, fenêtres, lampadaires, conteneur, voiture, soldat/coureur animé | DL\ |
| Car by Quaternius (.glb) | Voiture low poly | DL\ |
| Nissan GTR by David Sirera (.glb) | Voiture de sport low poly | DL\ |
| (HDRI) | aucun | — |

Manque pour Silk Road (cold open) : rue en pente, façades, berline sombre, porte vitrée, HDRI intérieur et rue brumeuse.

## Divers (DL\)
blenderkit-v3.21.3.zip (extension), Scene_ThreeJS.zip, Charte_documentaire_3D_V1.pdf, Apercu_Blender.mp4, Le_dernier_message.mp4, « True Story _ test d'ouverture.html », tutoriel « Easy Characters are META » (.zip/.7z/.tar, 3 copies).

## Archives (photos réelles) et footage
| Fichier | Contenu | Emplacement |
|---|---|---|
| portrait_ross.jpg, ross_carreaux.png, ross_prison(2,3).png, ross_codetenus.png, ross_libre.png | Photos de Ross Ulbricht (presse, FreeRoss) — usage éditorial, créditer | assets3d/silk-road/archives/ |
| Screenshot 2026-10-12 2232…2237 | article « Finally Ross is free », faux papiers (GX 402), bannières « Seized » | DL\ |
| Footage Pexels (9 clips) | colis, rue de SF, homme devant écrans la nuit, serveurs, barreaux, bitcoin, campus, marteau, balance | DL\ (noms numériques, ex. 10472351-hd…mp4) |

## Livrables Silk Road (Drive)
Vidéos finales FR/EN, reels, miniatures, .blend validé : Drive `TRU_Stories_Assets/videos/silk-road/` — détail et liens dans videos/silk-road/BON_DE_PRODUCTION.md.

## Éléments codés réutilisables
| outils/capture/capture.js | capture image par image d'une page HTML/Three.js → MP4 (Edge ; `?lang=en` = traduction) |
| outils/etalonnage.py | presets d'étalonnage ffmpeg (nuit_enquete validé) |
| videos/silk-road/partie3/decors.html | décors Three.js « maquette grise », étiquettes, miniatures diorama (`?s=mini`) — modèle à copier |
| videos/silk-road/livrables/reels.py | découpe de reels 9:16 avec accroche |
| videos/silk-road/trad_en.json + final_en.sh + montage_en.py | fabrication de la version anglaise |
| Fichier | Contenu |
|---|---|
| videos/silk-road/ecran/ecran.html → ecran.mp4 | écran de portable : interview + tableau de bord (modifiable) |
| videos/silk-road/3d/biblio.py + salle_lecture.py | salle de lecture de Glen Park (tables, persos stylisés, rayonnages) pour tous les plans bibliothèque |
