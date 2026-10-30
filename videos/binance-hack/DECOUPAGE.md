# DÉCOUPAGE — Binance (`videos/binance-hack/`)
Format 2,39:1 · 30 fps · ≈ 7 min 45 · 42 plans. Timecodes indicatifs : à recaler sur p1…p10.mp3.
**Stratégie pour sortir vite** : 60 % des plans en **[CODE] Three.js/HTML** (rapides, pas de rendu lourd), 40 % en **[3D] Blender** limités à **5 décors**, réutilisés plusieurs fois. EEVEE ≈ 7 s/image → on garde les plans Blender courts (2 à 5 s) et les caméras lentes.

## Les 5 décors Blender (tout le reste = code)
| ID | Décor | Réutilisé dans | Base |
|---|---|---|---|
| D1 | Rue de nuit + façade (3e étage) | P1, P9, P10 | façade simple low poly + réverbère + voiture |
| D2 | Chambre du pirate | P1, P9 | kit bibliothèque (table, lampe, tasse) + écrans + clavier |
| D3 | Couloir de serveurs + coffre « BINANCE 14 » | P2 | baies dupliquées en array |
| D4 | Salle de crise | P4, P5 | table + écrans muraux + chaises |
| D5 | Open space / bureau | P7, P8 | même table, autre habillage |

## Plans
| # | Partie | Durée | Type | Image | Caméra | Son |
|---|---|---|---|---|---|---|
| 1 | P1 | 3 s | CODE | Noir, horodatage « 29.10.2026 — 20:05 UTC » qui s'écrit | fixe | grave serveurs |
| 2 | P1 | 6 s | 3D D1 | Rue vide, réverbère qui grésille | fixe, léger push-in | ville lointaine |
| 3 | P1 | 5 s | 3D D1 | Voiture qui passe, phares sur façades | pan qui suit | moteur doux |
| 4 | P1 | 6 s | 3D D1 | Tilt up le long de l'immeuble jusqu'à la fenêtre bleue | tilt up lent | la ville s'éteint |
| 5 | P1 | 7 s | 3D D2 | Homme rouge de dos, écran, canette, nouilles | dolly lent vers lui | ventilateur + touches |
| 6 | P1 | 5 s | CODE | Écran : code qui défile, « BINANCE » apparaît | fixe | touches |
| 7 | P1 | 4 s | 3D D2 | Gros plan doigt au-dessus d'Entrée → appuie | macro | silence puis clic |
| 8 | P1 | 6 s | CODE | « 6 300 000 000 $ » + « Le plus gros vol de l'histoire de la crypto » | fixe | impact grave |
| 9 | P2 | 3 s | CODE | Rembobinage (glitch VHS) 20:24 → 20:20 | — | rewind |
| 10 | P2 | 6 s | 3D D3 | Couloir de serveurs, coffre ouvert « BINANCE 14 » au fond | travelling avant | ronron |
| 11 | P2 | 8 s | CODE | Compteur de numéros qui défile (nonce), « ? » | fixe | tic-tac |
| 12 | P2 | 8 s | CODE Three.js | 50 cartes lumineuses → 49 s'éteignent, 1 rouge reste | orbite lente | cœur |
| 13 | P2 | 4 s | 3D D3 | Le coffre pivote et s'éclaire en rouge | fixe | clac métal |
| 14 | P2 | 6 s | CODE | Transaction : 167 464 ETH · 63 tokens · 1,6 Md$ USDT | fixe | chiffres |
| 15 | P2 | 6 s | CODE Three.js | Globe / carte : 10 blockchains qui s'ouvrent une à une | rotation | portes |
| 16 | P3 | 6 s | ARCHIVE | Logo Binance, photo CZ (droits à vérifier) | Ken Burns | marché |
| 17 | P3 | 6 s | CODE | Compteur 144 Md$ + forteresse en wireframe | fixe | — |
| 18 | P3 | 8 s | CODE | Frise 2018 SAFU → 2019 7 000 BTC → 2026 | slide | — |
| 19 | P3 | 5 s | CODE | Tweet recréé « Funds are SAFU » | fixe | — |
| 20 | P3 | 5 s | CODE | « × 150 » qui grossit | zoom | impact |
| 21 | P4 | 6 s | CODE | Chronologie verticale 20:32 · 21:15 | scroll | notifs |
| 22 | P4 | 5 s | CODE | Faux post X de CZ (recréé, pas de capture) | fixe | vibreur |
| 23 | P4 | 8 s | 3D D4 | Salle de crise, silhouettes blanches, horloge 1 h 52 | dolly latéral | voix étouffées |
| 24 | P4 | 4 s | CODE | « BINANCE 14 » rouge → blanc | fixe | souffle |
| 25 | P5 | 8 s | CODE | Jauges VOLÉ 6,3 Md$ / GELÉ qui monte (Tether, Circle) | fixe | glace qui craque |
| 26 | P5 | 7 s | CODE Three.js | Routes lumineuses, barrières qui tombent | survol | glace |
| 27 | P5 | 6 s | CODE | Aave : 60 M USDT → 44 M$ ETH (schéma) | fixe | — |
| 28 | P5 | 5 s | CODE | « 22:15 — DÉPÔTS / RETRAITS SUSPENDUS » | fixe | coupure |
| 29 | P5 | 5 s | 3D D4 | Silhouette femme enceinte à la table, lève la tête | fixe | silence |
| 30 | P5 | 5 s | CODE | « ≈ 3 Md$ gelés / ≈ 3 Md$ manquants » | fixe | note grave |
| 31 | P6 | 10 s | STOCK | Écrans de trading rouges, bougies qui chutent | — | alarme |
| 32 | P6 | 8 s | CODE | Courbe BTC → 76 000 $, compteur liquidations 628 M$ | fixe | — |
| 33 | P7 | 7 s | 3D D5 | Open space matin, ingénieur blanc ouvre son portable | dolly lent | open space |
| 34 | P7 | 6 s | 3D D5 | Fil rouge sort de l'écran, traverse le sol, sort par la fenêtre | suit le fil | silence net |
| 35 | P7 | 8 s | CODE | Schéma Laptop → Conteneur → Retraits + « ? » | fixe | — |
| 36 | P7 | 6 s | 3D D5 | « Imagine » : café posé, mains, clic d'ouverture | macro | tasse, clic |
| 37 | P8 | 6 s | 3D D5 | Bureau 2025, écran « InvestSim » | fixe | tension |
| 38 | P8 | 8 s | CODE | Frise Bybit 4 → 19 → 21 fév. 2025, « 1,5 Md$ » | slide | — |
| 39 | P9 | 6 s | 3D D1 | Retour rue, la fenêtre ; recul : 10 fenêtres s'allument | recul lent | touches × 10 |
| 40 | P9 | 10 s | CODE Three.js | Carte Pyongyang → Binance / Bybit / Bitget, compteurs 1,1 Md$ vs 6,3 Md$ | rotation globe | — |
| 41 | P10 | 6 s | CODE | « Retraits sous 48 h · post-mortem promis » | fixe | — |
| 42 | P10 | 12 s | 3D D1 | Rue, voiture qui repasse, fenêtre allumée → noir. Texte « Qui tient la porte de ton argent ? » | fixe | ventilateur s'arrête |

**Bilan** : 15 plans Blender (≈ 85 s de rendu → ≈ 2 550 images → ≈ 5 h EEVEE), 24 plans code, 1 archive, 1 stock. Les plans code couvrent les trous si un rendu Blender tombe.
