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
| Typing (1) à (4).fbx | Persos + Typing : (1) Ch02 femme · (2) Ch26 femme en talons · (3) Ch18 homme · (4) Ch12 homme en veste | 50 Mo chacun | DL\ |

**Manquent pour Silk Road** : Typing, Sitting Down, Standing Up, Looking Around, Surprised, Arguing, Reading, Slow Walk. Plan 4.7 : le lever est simulé (fondu Sitting Idle → pose debout) en attendant Standing Up.

## Objets
| Fichier | Contenu | Emplacement |
|---|---|---|
| Sans titre_kit_leger.blend (74 Mo) | **Kit bibliothèque complet** (BlenderKit) : tables (GUBI, Reading Table, Wooden table ×3, Mid Century, office), chaises (Simple wooden chair, Wooden Chair ×2, Wooden Dining Chair), étagères vides (Ash wood, Wooden, Hazel, Pyrite, Bookcase, Ikea Billy, Wall Book Shelf, Display Shelves), livres (Books ×5, Stacked set, Encyclopedia set, Julius Caesar), portables (Mcbook, Samsung Galaxy Book 2, Laptop Notebook), lampes (Vintage, LED noire/blanche), tasse, café et biscuits, sac à dos, table basse | DL\persos\ (trop lourd pour GitHub → Drive) |
| Sans titre.blend (72 Mo) | Même kit, non allégé (+ .blend1, bibliotheque_recup.7z/.blend1 = sauvegardes) | DL\persos\ |
| kit_bibliotheque.blend | tasse, lampe de bureau, table (partiel, ancien) | assets3d/silk-road/objets/ |
| Rayonnage rempli de livres | généré par script (`rayon_maillage()` dans videos/silk-road/3d/biblio.py) | code |
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

## Éléments codés réutilisables
| Fichier | Contenu |
|---|---|
| videos/silk-road/ecran/ecran.html → ecran.mp4 | écran de portable : interview + tableau de bord (modifiable) |
| videos/silk-road/3d/biblio.py + salle_lecture.py | salle de lecture de Glen Park (tables, persos stylisés, rayonnages) pour tous les plans bibliothèque |
