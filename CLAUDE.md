# TRU Stories — dépôt de production (instructions pour Claude Code)

Ce dépôt sert uniquement à la chaîne TRU Stories. **Lis d'abord `BIBLE_TRU_STORIES.md`**, puis `ASSETS.md` et le `BON_DE_PRODUCTION.md` de la vidéo demandée.

## Organisation
- `videos/<slug>/` : une vidéo (SCRIPT.md, DECOUPAGE.md, BON_DE_PRODUCTION.md, voix/, ecran/, rendu/, livrables/). Modèle : `videos/_MODELE/`.
- `assets3d/` : personnages, animations, objets, décors, véhicules. L'inventaire est dans `ASSETS.md`.
- `style/` : stylisation des personnages (principal en rouge émissif, autres en blanc).
- `outils/` : allègement des fichiers. `references/` : scripts précédents et prompts d'écriture.

## Quand Mo dit « réalise la vidéo <slug> »
1. Lis le bon de production. Vérifie que chaque asset listé existe (dans `assets3d/` ou dans le dossier indiqué). S'il manque quelque chose : télécharge-le via Blender (Poly Haven, Sketchfab ou BlenderKit, quand l'outil MCP Blender le permet), sinon donne à Mo la liste précise et attends.
2. Pour les personnages : applique `style/` (low poly, rouge pour le principal, blanc pour les autres). Chaque personnage est parenté à un Empty. Les animations Mixamo sont mises sur place, puis déplacées par l'Empty.
3. Pour les plans [CODE] : une page HTML + capture image par image (Playwright), puis un MP4. Pour les plans [3D] : une scène Blender construite par script Python et rendue en EEVEE. Les rendus doivent pouvoir reprendre là où ils se sont arrêtés.
4. Cale chaque plan sur la voix off (`voix/`), d'après les timecodes du découpage.
5. Assemble avec ffmpeg : format 2,39:1, voix, ambiances et musique, sous-titres. Le résultat va dans `videos/<slug>/rendu/<slug>_final.mp4`.
6. Prépare la miniature et un Short de 45 à 60 s dans `livrables/`.
7. Mets à jour le tableau d'état du bon de production et `ASSETS.md`. Commit et push.

## Règles
- Ne lance jamais `outils/alleger_personnages.py` dans une scène qui contient des objets.
- Avant tout rendu long, fais une image de test et montre-la à Mo.
- N'efface jamais un .blend de Mo. Travaille sur une copie.
- Économise les crédits ElevenLabs : ne régénère jamais une voix sans demander.
