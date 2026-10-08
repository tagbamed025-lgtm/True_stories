# BIBLE — TRU Stories (à lire en premier par toute nouvelle discussion Claude)

Mise à jour : 8 octobre 2026.

## 1. La chaîne
- **TRU Stories** : true crime immersif façon Fern / Netflix. Reconstitutions en 3D stylisée, mêlées à du footage générique et à de vraies archives.
- Vidéos **courtes, 5 à 6 min maximum**, pour économiser les crédits.
- Langue : français. Voix off **ElevenLabs, voix « Adrien »**, débit posé. Les tests de voix font **100 caractères maximum, une seule génération** (generations_count = 1).
- Règle des faits : rien n'est affirmé sans source. Chaque script se termine par une section « Sources ».

## 2. Style de marque (à respecter sur chaque vidéo)
- Personnages stylisés, pas réalistes : low poly (décimation 0,03 + flat shading).
- **Personnage principal en rouge émissif. Tous les autres en blanc lumineux.** Les femmes se reconnaissent à leur silhouette et à leurs cheveux.
- Décors sombres. Rouge réservé aux moments de rupture. Format 2,39:1, grain léger, flou de profondeur, caméras lentes.
- Script en code couleur : **jaune = 3D Blender**, **cyan = footage stock**, **vert = archives réelles**.
- Méthode hybride : **code** (HTML/Three.js capturé en vidéo) pour les écrans, cartes, chronologies, titres et murs d'enquête. **Blender** pour les décors et les personnages. Une vidéo codée peut servir de texture d'écran dans Blender (matériau émissif, ImageTexture en mode MOVIE).

## 3. Répartition du travail
- **Mo** télécharge les personnages (Mixamo, MPFB) et les objets (BlenderKit, Poly Haven, Sketchfab), puis rend sur son PC.
- **Claude** écrit le script, le vérifie, génère la voix, stylise les personnages, construit les scènes Blender en Python (lumières, caméras, animation) et prépare le montage.
- PC de Mo : NVIDIA Quadro P2000 (OptiX), 32 Go de RAM, Blender 5.2. EEVEE ≈ 7 s par image en 1080p.

## 4. Règles techniques
- Mixamo : personnages en « With Skin », animations en « **Without Skin, 30 fps** ».
- Fichiers de plus de 25 Mo : lancer `outils/alleger_personnages.py` (dans un fichier Blender VIDE, sinon il efface la scène) pour les personnages, ou `outils/preparer_kit.py` pour un kit d'objets. Sinon, compresser en .7z.
- Les scripts Blender sont lancés dans l'onglet Scripting → Texte → Ouvrir → ▶ Run Script. Le rendu se lance par le menu Rendu (Ctrl+F12 ne marche pas sur le PC de Mo).

## 5. Projet en cours : Silk Road (arrestation de Ross Ulbricht)
| Élément | Fichier | État |
|---|---|---|
| Script vérifié (5 min 30) | `silk-road/SCRIPT_V2.md` | ✅ |
| Script d'origine en couleurs | `silk-road/Script_Silk_Road_Code_Couleur.docx` | ✅ |
| Découpage plan par plan | `silk-road/DECOUPAGE.md` | ✅ |
| Voix off Adrien | `silk-road/voix/VO_complete_SilkRoad.mp3` (5:05, dont 30 s de silence au début) + p1 à p6 | ✅ |
| Écran du portable (vidéo codée) | `silk-road/ecran/ecran.html` → `ecran.mp4`, test Blender `portable_demo.blend` | ✅ |
| Distribution des personnages | `assets3d/silk-road/personnages/` (Ch31 = Ross en rouge, Ch23 = agent FBI en veste, Ch21 et Ch22 = femmes) | ✅ |
| Styles de personnages | `style/` (planche_styles.png, distribution.py) | ✅ |
| Kit d'objets de la bibliothèque | `assets3d/silk-road/objets/kit_bibliotheque.blend` | ⚠️ partiel : il manque étagères, livres, portable et chaises |

### Prochaines étapes, dans l'ordre
1. Mo envoie le kit d'objets complet (`Sans titre_kit_leger.blend`).
2. Mo télécharge les animations Mixamo pour Ch31 : marche, assis, tape au clavier, assis en attente, regarde autour, dispute, se lève, lecture, surpris, marche lente.
3. Personnages en plus : 1 ou 2 hommes (veste, blouson) et une femme aux cheveux longs.
4. Claude construit la scène de la bibliothèque : d'abord le plan 0.7 (plongée zénithale) et le plan 4.7 (twist des gilets FBI).
5. Éléments codés : titre, dates, mur d'enquête, chronologie des erreurs. Caler sur la voix off.
6. Montage : couches de son, étalonnage 2,39:1, sous-titres, miniature, un Short.

## 6. Routine hebdomadaire (à configurer)
Chaque semaine : trouver les grosses affaires de la semaine (ex. le casse du Louvre) et produire un brouillon de script vérifié. Mo doit encore donner le jour, l'heure, le fuseau horaire et les thèmes.
