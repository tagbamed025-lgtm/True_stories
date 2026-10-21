# Bon de production — L'empire à un milliard piégé dans une bibliothèque (`videos/silk-road/`)
État vérifié le 21 octobre 2026. **Vidéo terminée** : FR publiée sur YouTube (montage final CapCut de Mo), EN stockée pour la future chaîne anglaise.

## État
| Étape | État | Fichier |
|---|---|---|
| Script FR vérifié | ✅ | SCRIPT_V2.md |
| Script EN | ✅ | SCRIPT_EN.md |
| Voix off FR (Adrien) | ✅ | voix/VO_complete_SilkRoad.mp3 + p1…p6 ; transcription horodatée parties 4-6 : voix/transcription_192-305.md |
| Voix off EN (Nathan – Deep Podcast Narrator) | ✅ | voix/VO_EN_Nathan.mp3 (4:03) |
| Découpage | ✅ | DECOUPAGE.md (v1) ; découpage réel = scripts de montage ci-dessous |
| Minute 1 (0:00 → 0:51,5, Blender) | ✅ validée | rendu ChatGPT `silk-road_minute_v4.mp4` ; scène `3d/silk-road_v4_VALIDE.blend` (Drive) |
| Partie 2 – Qui est cet homme (Three.js/HTML + archives) | ✅ | partie2/scenes.html, partie2/montage_partie2.py |
| Partie 3 – La traque (décors Three.js maquette grise) | ✅ | partie3/decors.html, forum.html, montage_partie3.py |
| Parties 4-6 – Diversion, procès, clôture (Blender poses figées + HTML) | ✅ | partie4/plans_blender.py, preuves.html, montage_fin.py ; images rendues dans partie4/final/ (local, non versionnées) |
| Vidéo finale FR 2K (notre montage) | ✅ | rendu/silk-road_final.mp4 (4:58, 2560×1440) — Drive |
| Vidéo finale FR publiée (montage CapCut de Mo, 4K) | ✅ publiée | rendu/silk-road_final_CapCut_publiee.mp4 — Drive |
| Version EN complète (textes traduits) | ✅ | rendu/silk-road_FULL_EN.mp4 (4:26, 2K) — Drive ; `final_en.sh` + `montage_en.py` + `trad_en.json` |
| Miniatures (A/B) | ✅ | livrables/miniature_3d_1.png (cercle FBI), miniature_3d_2.png (fausse dispute) — Drive + GitHub |
| Reels 9:16 (×4, 35-40 s) | ✅ | livrables/reels/reel_1…4.mp4 — Drive ; script livrables/reels.py |
| Titres + descriptions FR/EN | ✅ | voir section « Publication » ci-dessous |
| Reels EN | ⬜ | à faire (relancer reels.py sur la vidéo EN avec accroches anglaises) |
| Sous-titres (.srt) FR/EN | ⬜ | à faire (transcription ElevenLabs disponible pour FR p4-p6) |

## Livrables sur Google Drive
Dossier : **Google Drive › Mon Drive › `TRU_Stories_Assets/videos/silk-road/`** (copiés le 21 oct. 2026 via Google Drive pour ordinateur, `G:\Mon Drive\…`). Liens de partage : à copier depuis drive.google.com (clic droit › Partager › Copier le lien) et à coller ici.
| Fichier | Chemin Drive | Lien |
|---|---|---|
| Vidéo finale FR publiée (CapCut, 4K) | rendu/silk-road_final_CapCut_publiee.mp4 | _à coller_ |
| Vidéo finale FR (2K, notre montage) | rendu/silk-road_final.mp4 | _à coller_ |
| Vidéo finale EN (2K) | rendu/silk-road_FULL_EN.mp4 | _à coller_ |
| Reels FR ×4 | livrables/reels/reel_1…4.mp4 | _à coller_ |
| Miniatures A/B + 1280 | livrables/miniature_3d_1.png, miniature_3d_2.png, miniature_finale_1280.jpg | _à coller_ |
| Scène Blender validée (chaises corrigées) | 3d/silk-road_v4_VALIDE.blend | _à coller_ |

Restent uniquement en local (PC de Mo, régénérables par les scripts) : morceaux `rendu/_*.mp4`, brouillons, images PNG de `partie4/final/`, `silk-road_EN.mp4` (EN calée sur le montage CapCut, textes FR).

## Publication
**FR** — Titre A : *Le FBI a simulé une dispute pour l'arrêter* · Titre B : *Comment le FBI a piégé le roi du dark web dans une bibliothèque*. A/B : miniature 1 (cercle FBI) + titre B ; miniature 2 (dispute) + titre A.
**EN** — Title A : *The FBI Faked a Fight to Arrest Him* · Title B : *How the FBI Trapped the Dark Web King in a Library*.
Description FR (chapitres 00:00 La bibliothèque · 00:18 L'homme à la table · 00:54 Qui est Dread Pirate Roberts ? · 01:34 La traque · 03:05 La diversion · 04:15 Le procès · 04:32 Libre) et description EN : texte complet dans l'historique de production, à reprendre depuis YouTube Studio.

## Distribution (utilisée)
| Rôle | Fichier | Couleur |
|---|---|---|
| Ross Ulbricht | Ch31 | Rouge émissif |
| Agent en veste (dispute) | Ch12 = DL\Typing (4).fbx | Blanc |
| Agente de la dispute | Ch26 = DL\Typing (2).fbx | Blanc |
| Agente | Ch02 = DL\Typing (1).fbx | Blanc |
| Gary Alford / Thomas Kiernan / lecteur | Ch18 = DL\Typing (3).fbx | Blanc |
| Agents, lecteurs, bibliothécaire | Ch21, Ch22, Ch23 | Blanc |

## Leçons (reportées dans la bible)
Brouillon basse qualité avant tout rendu HQ ; personnages secondaires figés ; vérifier chaises/mains de près ; scène v4 lourde (≈ 50 s/image en 1920) → rendre en 1280 ; un seul rendu à la fois ; bilingue dès le départ via trad_en.json.
