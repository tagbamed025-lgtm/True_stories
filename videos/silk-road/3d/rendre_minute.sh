#!/bin/sh
# Rend tous les plans 3D de la première minute (reprenable : relancer saute les images déjà faites).
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; cd "$(dirname "$0")"
for p in p03_visage p11_pousse p01_entree p02_assis p04_zenith p07_travelling p08_epaule p09_salle p10_poitrine; do
  echo "== $p $(date +%T)"; "$B" -b --python plans_minute.py -- $p "$@" 2>&1 | grep -E "^OK|Error" ; done
echo FIN $(date +%T)
