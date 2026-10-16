#!/bin/sh
# Vidéo finale Silk Road en 2K (image 2560×1072 au format 2,39:1 dans un 2560×1440).
# Prérequis : plans Blender de la partie 4 rendus en final (partie4/rendre.sh final).
# 1) captures Three.js / HTML en 2560×1072, 30 i/s ; 2) montages finaux des parties 2, 3, fin ; 3) assemblage avec la minute v4.
set -e
cd "$(dirname "$0")"; R=../..; F=/c/ffmpeg/bin/ffmpeg
CAP="node outils/capture/capture.js"   # chemin relatif à la racine du dépôt (on y fait cd $R)
P2=videos/silk-road/partie2; P3=videos/silk-road/partie3; P4=videos/silk-road/partie4
mkdir -p partie2/final_en partie3/final_en partie4/final_en
( cd $R
  $CAP "$P2/scenes.html?lang=en&s=silkroad&d=5.0" $P2/final_en/silkroad.mp4 5.0 30 2560 1072
  $CAP "$P2/scenes.html?lang=en&s=tor&d=4.6" $P2/final_en/tor.mp4 4.6 30 2560 1072
  $CAP "$P2/scenes.html?lang=en&s=dpr&d=8.1" $P2/final_en/dpr.mp4 8.1 30 2560 1072
  $CAP "$P2/scenes.html?lang=en&s=compteur&d=4.2" $P2/final_en/compteur.mp4 4.2 30 2560 1072
  $CAP "$P3/decors.html?lang=en&s=mur&v=1" $P3/final_en/mur1.mp4 7.55 30 2560 1072
  $CAP "$P3/decors.html?lang=en&s=mur&v=2" $P3/final_en/mur2.mp4 13.4 30 2560 1072
  $CAP "$P3/decors.html?lang=en&s=bureau" $P3/final_en/bureau.mp4 5.9 30 2560 1072
  $CAP "$P3/decors.html?lang=en&s=couloir" $P3/final_en/couloir.mp4 6.7 30 2560 1072
  $CAP "$P3/forum.html?lang=en" $P3/final_en/forum.mp4 22.7 30 2560 1072
  $CAP "$P3/decors.html?lang=en&s=kiernan" $P4/final_en/kiernan.mp4 6.7 30 2560 1072
  $CAP "$P4/preuves.html?lang=en" $P4/final_en/preuves.mp4 9.3 30 2560 1072 )
export TRU_LANG=en
python -I partie2/montage_partie2.py final
python -I partie3/montage_partie3.py final
python -I partie4/montage_fin.py final
python -I montage/titres.py
# minute 1 (v4) : titre et date anglais incrustés par-dessus les cartons français (13–16 s et 16–18 s)
V4="/c/Users/HP/Documents/Codex/2026-10-12/files-mentioned-by-the-user-silk/outputs/production_v4/silk-road_minute_v4.mp4"
$F -v error -y -i "$V4" -i montage/elements/titre_en.mp4 -i montage/elements/date_en.mp4 -filter_complex \
 "[0]crop=1920:804:0:138[b];[1]setpts=PTS+13/TB[t];[2]setpts=PTS+16/TB[d];[b][t]overlay=enable='between(t,13,16)'[x];[x][d]overlay=enable='between(t,16,18)',scale=2560:1072:flags=lanczos,pad=2560:1440:0:184:black,fps=30,setsar=1" \
 -an -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p rendu/_m1_EN.mp4
for p in partie2 partie3 fin; do $F -v error -y -i rendu/silk-road_${p}_EN.mp4 -an -vf "fps=30,setsar=1" -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p rendu/_${p}_EN.mp4; done
printf "file '_m1_EN.mp4'\nfile '_partie2_EN.mp4'\nfile '_partie3_EN.mp4'\nfile '_fin_EN.mp4'\n" > rendu/_liste_en.txt
$F -v error -y -f concat -safe 0 -i rendu/_liste_en.txt -c copy rendu/_video_EN.mp4
python -I montage_en.py rendu/_video_EN.mp4
echo "OK EN"
