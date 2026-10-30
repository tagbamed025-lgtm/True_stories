# Inventaire des assets TRU Stories
Consulter avant de demander un téléchargement. Mettre à jour après chaque ajout.
Règle : tout est sur GitHub (fichiers < 50 Mo). Les fichiers trop lourds sont **allégés** (textures retirées : notre style est une maquette grise sans textures) avant d'être versionnés.
Dernier inventaire : 30 octobre 2026 (versement des assets du PC de Mo sur GitHub).

## Style visuel de référence → `references/style_visuel/`
| Fichier | Contenu |
|---|---|
| Charte_documentaire_3D_V1.pdf | Charte graphique 3D documentaire |
| ref_maquette_grise_perso_rouge.png | Maquette grise claire, perso principal rouge, étiquettes de nom noires |
| ref_interieur_lowpoly_rouge_bleu.png | Intérieur low poly, persos à facettes, lumière de fenêtres |
| ref_video_1011.mp4 | Vidéo de référence |
| Planche validée Silk Road | videos/silk-road/3d/tests/planche_v3.png |

## Personnages
| Fichier | Description | Emplacement |
|---|---|---|
| Ch31.fbx | Homme jeune, pull (Ross, rouge) | assets3d/silk-road/personnages/ |
| Ch23.fbx | Homme en veste | assets3d/silk-road/personnages/ |
| Ch21.fbx, Ch22.fbx | Femmes | assets3d/silk-road/personnages/ |
| Ch18.fbx | Homme (Mixamo, 13 Mo) | assets3d/personnages/ |
| X_Bot.fbx / Y_Bot.fbx | Mannequins Mixamo homme / femme | assets3d/personnages/ |
| guy_lowpoly_cloaking.glb | Homme low poly (Sketchfab) | assets3d/personnages/ |
| fbi_soldier.zip | Agent FBI tactique texturé (squelette Biped, échelle ×100 ; licence à vérifier) | assets3d/personnages/ |
| GLB figés (Three.js / Blender) | ross_assis_tape, ross_debout, alford_assis_tape, agent_debout_veste, agent_debout_2, agente_debout | assets3d/silk-road/glb/ |
Les versions lourdes `Ch21/22/23/31_nonPBR.fbx` (50 Mo) ne sont pas versionnées : les Ch*.fbx du dépôt suffisent.

## Personnages déjà animés (perso + animation Typing, textures retirées)
| Fichier | Personnage | Emplacement |
|---|---|---|
| Typing_1_Ch02_femme.fbx | Ch02, femme | assets3d/personnages_animes/ |
| Typing_2_Ch26_femme_talons.fbx | Ch26, femme en talons | assets3d/personnages_animes/ |
| Typing_3_Ch18_homme.fbx | Ch18, homme | assets3d/personnages_animes/ |
| Typing_4_Ch12_homme_veste.fbx | Ch12, homme en veste | assets3d/personnages_animes/ |

## Animations Mixamo → `assets3d/animations/`
⚠️ Exportées **With Skin, 60 i/s** (pas « Without Skin, 30 fps »). Elles marchent : les scripts gardent l'action et la ralentissent ×0,5. Os `mixamorig:` ; les persos (`mixamorig9:`) sont renommés à l'import.
| Fichier | Mouvement |
|---|---|
| Typing.fbx | Taper au clavier, assis |
| Sitting_Idle.fbx | Assis, au repos |
| Sitting.fbx | Assis (se relève en boucle : pose figée seulement) |
| Stand_To_Sit.fbx | S'asseoir |
| Stand_Up.fbx | Se lever |
| Idle.fbx / Standing_Idle.fbx | Debout, au repos |
| Standing_Arguing.fbx | Debout, dispute |
| Yelling.fbx | Crier |
| Picking_Up.fbx / Picking_Up_Object.fbx | Ramasser / saisir un objet |
| Walking.fbx / Walking_1.fbx | Marche |
| Walking_Left_Turn.fbx | Marche + virage à gauche |
| Female_Start_Walking.fbx | Départ de marche (image 1 = pose debout) |
| Texting_And_Walking.fbx / Walking_While_Texting.fbx | Marche en tapant sur un téléphone |
| Talking_On_Phone.fbx | Debout, au téléphone |
| Driving.fbx | Conduite |
**Manquent encore** : Looking Around, Surprised, Reading, Slow Walk, Looking Behind (remplacements : Standing_Idle, Stand_Up).

## Objets
| Fichier | Contenu | Emplacement |
|---|---|---|
| **kit_meubles.blend** (7 Mo, textures retirées) | Kit BlenderKit complet : tables (GUBI, Reading Table, Wooden table ×3, Mid Century, Wooden table office-01, Coffee Table), chaises (Simple wooden chair, Wooden Chair, Wooden Dining Chair), étagères (Ash wood, Wooden, Hazel, Pyrite, Bookcase, Ikea Billy, Wall Book Shelf, Display Shelves), livres (Books, Stacked set, Encyclopedia set, Julius Caesar), **portables** (Mcbook, Samsung Galaxy Book 2, Laptop Notebook), **lampes** (Vintage, LED noire/blanche), Coffee Cup, Coffee and cookies, **Backpack** | assets3d/objets/ |
| kit_bibliotheque.blend | tasse, lampe, table (partiel, ancien) | assets3d/silk-road/objets/ |
| silk-road_v4_VALIDE.blend | Salle de Glen Park validée | assets3d/silk-road/scenes/ |
| Écran de portable animé | ecran.html → ecran.mp4 (texture MOVIE sur l'écran 3D) | videos/silk-road/ecran/ |

## Décors
| Fichier | Contenu | Emplacement |
|---|---|---|
| **ruelle.blend** | Ruelle de nuit : murs, fenêtres, lampadaires, conteneur, voiture, soldat/coureur animé | assets3d/decors/ |
| Salle de Glen Park (code) | glenpark.py | videos/silk-road/3d/ |

## Véhicules → `assets3d/vehicules/`
| Fichier | Contenu |
|---|---|
| car_quaternius.glb | Voiture low poly (Quaternius) |
| nissan_gtr.glb | Voiture de sport low poly (David Sirera) |
| kenney_car-kit.zip | Kit Kenney : voitures, camions, police, taxi (low poly) |
| kenney_watercraft-pack.zip | Kit Kenney : bateaux |

## Objets réalistes (BlenderKit, choisis par Mo) → `assets3d/binance/`
| Fichier | Contenu |
|---|---|
| binance_objets.blend (26 Mo, textures réduites à 512 px) | Collections : **Volvo S90** (berline noire), **Moon** (lune texturée), **Night Stand Modern**, **Night stand ESMEE**, **Duck Silicone Night Light** |
| planche_assets_binance.png | Photo de tous les objets du fichier complet de Mo |
Fichier complet (135 Mo, PC de Mo) : `Downloads\tru stories\Binance pirate other asset\Sans titre.blend` — contient aussi : bus Neoplan, Generic Sport Sedan (rouge), Toyota GR GT, 2× Volvo P1800, Vespa, scooter, moto, homme barbu réaliste, immeuble low poly, pâté d'immeubles. Trop lourd pour être ouvert en entier dans le cloud : importer **par collection** (`bpy.data.libraries.load(..., B.collections=[nom])`).

## HDRI
Aucun pour l'instant (Poly Haven si besoin).

## Non versionné (volontairement)
Tutoriel vidéo « Easy Characters are META » (.zip/.tar/.7z, ~30 Mo chacun), extension BlenderKit (.zip, réinstallable depuis blenderkit.com), sauvegardes .blend1 et bibliotheque_recup.7z (doublons du kit).
