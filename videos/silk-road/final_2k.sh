#!/bin/sh
# Vidéo finale Silk Road en 2K (image 2560×1072 au format 2,39:1 dans un 2560×1440).
# Prérequis : plans Blender de la partie 4 rendus en final (partie4/rendre.sh final).
# 1) captures Three.js / HTML en 2560×1072, 30 i/s ; 2) montages finaux des parties 2, 3, fin ; 3) assemblage avec la minute v4.
set -e
cd "$(dirname "$0")"; R=../..; CAP="node $R/outils/capture/capture.js"; F=/c/ffmpeg/bin/ffmpeg
P2=videos/silk-road/partie2; P3=videos/silk-road/partie3; P4=videos/silk-road/partie4
mkdir -p partie2/final partie3/final partie4/final
( cd $R
  $CAP "$P2/scenes.html?s=silkroad&d=5.0" $P2/final/silkroad.mp4 5.0 30 2560 1072
  $CAP "$P2/scenes.html?s=tor&d=4.6" $P2/final/tor.mp4 4.6 30 2560 1072
  $CAP "$P2/scenes.html?s=dpr&d=8.1" $P2/final/dpr.mp4 8.1 30 2560 1072
  $CAP "$P2/scenes.html?s=compteur&d=4.2" $P2/final/compteur.mp4 4.2 30 2560 1072
  $CAP "$P3/decors.html?s=mur&v=1" $P3/final/mur1.mp4 7.55 30 2560 1072
  $CAP "$P3/decors.html?s=mur&v=2" $P3/final/mur2.mp4 13.4 30 2560 1072
  $CAP "$P3/decors.html?s=bureau" $P3/final/bureau.mp4 5.9 30 2560 1072
  $CAP "$P3/decors.html?s=couloir" $P3/final/couloir.mp4 6.7 30 2560 1072
  $CAP "$P3/forum.html" $P3/final/forum.mp4 22.7 30 2560 1072
  $CAP "$P3/decors.html?s=kiernan" $P4/final/kiernan.mp4 6.7 30 2560 1072
  $CAP "$P4/preuves.html" $P4/final/preuves.mp4 9.3 30 2560 1072 )
python -I partie2/montage_partie2.py final
python -I partie3/montage_partie3.py final
python -I partie4/montage_fin.py final
# minute 1 validée (v4, rendue en 1920) : recadrée et agrandie en 2K
V4="/c/Users/HP/Documents/Codex/2026-10-12/files-mentioned-by-the-user-silk/outputs/production_v4/silk-road_minute_v4.mp4"
$F -v error -y -i "$V4" -vf "crop=1920:804:0:138,scale=2560:1072:flags=lanczos,pad=2560:1440:0:184:black,fps=30,setsar=1" -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 rendu/_m1_2k.mp4
for p in partie2 partie3 fin; do
  $F -v error -y -i rendu/silk-road_$p.mp4 -vf "fps=30,setsar=1" -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 rendu/_${p}_2k.mp4
done
printf "file '_m1_2k.mp4'\nfile '_partie2_2k.mp4'\nfile '_partie3_2k.mp4'\nfile '_fin_2k.mp4'\n" > rendu/_liste.txt
$F -v error -y -f concat -safe 0 -i rendu/_liste.txt -c copy rendu/silk-road_final.mp4
echo "OK rendu/silk-road_final.mp4"
