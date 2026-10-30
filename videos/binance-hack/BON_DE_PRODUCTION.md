# Bon de production — Binance : 20 minutes (`videos/binance-hack/`)

## État
| Étape | État | Fichier |
|---|---|---|
| Script vérifié | ✅ v3 validé | SCRIPT.md (= SCRIPT_v3.md) |
| Voix off | ⏳ Mo génère p1…p10 | voix/ (texte : VOIX_OFF_BRUT.txt) |
| Découpage | ✅ 42 plans | DECOUPAGE.md |
| Assets réunis | ⏳ voir plus bas | assets3d/binance-hack/ |
| Plans [CODE] | 🟡 plan 12 fait, 23 à faire | code/ |
| Plans [3D] | 🟡 chambre du pirate en test (méthode Silk Road) | blender/chambre_pirate.py |
| Montage final | ⬜ | rendu/binance-hack_final.mp4 |
| Miniature + Short | ⬜ | livrables/ |

## Infos clés
- Durée : ≈ 7 min 45 (8 min max) · 2,39:1 · 30 fps · EEVEE 1080p.
- Personnage principal (rouge émissif) : **le pirate** (silhouette anonyme). Tous les autres en blanc lumineux.
- Ambiance : nuit, bleu froid, écrans. Rouge réservé aux ruptures (fenêtre, Binance 14, fil du laptop).
- Voix : Adrien, p1…p10. Recaler les timecodes du découpage sur les vraies durées des mp3.

## Distribution
| Rôle | Personnage (fichier) | Couleur | Animations nécessaires |
|---|---|---|---|
| Pirate (de dos, capuche) | **Ch31.fbx** (déjà là, homme jeune pull) | rouge émissif | Typing, Sitting Idle |
| Ingénieur DevOps | **Ch23.fbx** (déjà là, homme en veste) | blanc | Walking, Sitting Down, Typing |
| Équipe Binance (salle de crise) | Ch23 + Ch21 dupliqués | blanc | Looking Around, Standing Idle, Arguing |
| Salariée enceinte | **Ch22.fbx** (déjà là) + ventre ajouté par sculpt/primitive | blanc | Sitting Idle, Surprised (lève la tête) |
| Développeur Bybit 2025 | Ch31 recoloré | blanc | Typing |

## Assets (presque tout est déjà dans assets3d/ — voir ASSETS.md)
- Animations : déjà dans `assets3d/animations/` (Typing, Sitting_Idle, Walking, Stand_To_Sit, Stand_Up, Standing_Idle, Standing_Arguing, Yelling). Manquent seulement Looking Around → Standing_Idle, Surprised → Stand_Up.
- Meubles : `assets3d/objets/kit_meubles.blend` (tables, chaises, portables, lampes, tasse, sac à dos).
- Rue de nuit : `assets3d/decors/ruelle.blend`. Voiture : `assets3d/vehicules/` (Quaternius, kit Kenney).
- Pirate assis : `assets3d/silk-road/glb/ross_assis_tape.glb` recoloré en rouge. Agents / équipe : GLB figés + Ch21/22/23 en blanc.
- Style de référence : `references/style_visuel/` + planche Silk Road. Méthode : brouillon 480 px → validation Mo → HQ la nuit ; secondaires figés, la caméra bouge.
- À télécharger éventuellement : 1 HDRI de nuit (Poly Haven), facultatif.

## Archives et stock
| Plan | Description | Lien | Droits |
|---|---|---|---|
| 16 | Logo Binance | https://www.binance.com/en/press (kit presse officiel) | usage éditorial, à vérifier |
| 16 | Photo de CZ | Wikimedia Commons, recherche `Changpeng Zhao` | vérifier la licence (CC-BY ou CC-BY-SA) |
| 31 | Écrans de trading rouges | Pexels, `stock market crash screen` / Pixabay, `trading screen red` | libre |
| 19, 22 | Posts de CZ | **recréer** en [CODE] (pas de capture réelle) | — |
| 38 | Bybit / Safe | aucun visuel réel : tout en [CODE] | — |

## Notes pour le montage
- Plans prioritaires : 2-7 (cold open), 12 (les 50 autorisations), 34 (le fil rouge), 42 (fin). Si le temps manque, ces plans d'abord, le reste en [CODE].
- Musique et ambiances : drone grave continu, pas de mélodie avant P5. Bruitages : ventilateur de PC, touches de clavier mécanique, ville de nuit, notifications, glace qui craque (gels).
- Texte obligatoire à l'écran, P1 : « Scène illustrée — l'identité et le lieu des pirates sont inconnus. »
- Avant d'exporter : re-vérifier le post-mortem de Binance (cause, montant gelé, reprise des retraits).
