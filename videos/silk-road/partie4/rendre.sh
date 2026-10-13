#!/bin/sh
# Rend les plans Blender de la partie 4 (+ table vide de la partie 6) en brouillon. Reprenable.
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; V4="C:/Users/HP/Documents/TRU Stories Blender/silk-road_v4_VALIDE.blend"
cd "$(dirname "$0")"
for p in agents dispute retourne saisie debout cercle table_vide; do "$B" -b "$V4" --python plans_blender.py -- $p "$@" 2>&1 | grep -E "^OK|Traceback"; done
echo FIN
