# ⚠️⚠️ ATTENTION : À LANCER DANS UNE SCÈNE VIDE (Fichier → Nouveau → Général, puis supprimer le cube) ⚠️⚠️
# Ce script VIDE la scène ouverte. Ne jamais le lancer dans un fichier contenant ton décor ou tes objets.
# ALLÉGER LES PERSONNAGES MIXAMO (50 Mo → quelques Mo)
# Dans Blender : onglet « Scripting » → Ouvrir ce fichier → modifier DOSSIER ci-dessous → bouton ▶ (Run Script).
# Chaque fichier .fbx du dossier est réenregistré SANS ses textures dans le sous-dossier « leger ».
# Les personnages, leur squelette et leurs animations sont conservés (les couleurs TRU Stories sont ajoutées ensuite).
import bpy, os, glob

DOSSIER = r"C:\Users\HP\Downloads\persos"   # ← mets ici le dossier où sont tes .fbx

sortie = os.path.join(DOSSIER, "leger"); os.makedirs(sortie, exist_ok=True)
# cherche les .fbx (majuscules ou minuscules) dans le dossier ET ses sous-dossiers, sauf « leger »
fichiers = sorted(f for f in glob.glob(os.path.join(DOSSIER, "**", "*"), recursive=True)
                  if f.lower().endswith(".fbx") and os.sep + "leger" + os.sep not in f)
def message(txt):
    print(txt)
    def dessin(self, ctx): self.layout.label(text=txt)
    bpy.context.window_manager.popup_menu(dessin, title="Alléger les personnages", icon='INFO')
if not os.path.isdir(DOSSIER):
    message(f"Dossier introuvable : {DOSSIER}"); raise SystemExit
if not fichiers:
    message(f"Aucun fichier .fbx trouvé dans {DOSSIER}"); raise SystemExit
# sécurité : refuse de tourner si la scène contient autre chose que le cube, la caméra et la lumière par défaut
autres=[o for o in bpy.context.scene.objects if o.name not in {"Cube","Camera","Light","Caméra","Lumière"}]
if len(autres) > 0:
    message(f"STOP : la scène contient {len(autres)} objet(s). Ouvre une scène vide avant de lancer ce script."); raise SystemExit
print(f"{len(fichiers)} fichier(s) à alléger")
for f in fichiers:
    # scène vide
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    bpy.data.orphans_purge(do_recursive=True)
    bpy.ops.import_scene.fbx(filepath=f)
    # retirer toutes les textures (images) des matériaux
    for m in bpy.data.materials:
        if m.node_tree:
            for n in list(m.node_tree.nodes):
                if n.type == 'TEX_IMAGE': m.node_tree.nodes.remove(n)
    for img in list(bpy.data.images): bpy.data.images.remove(img)
    bpy.ops.object.select_all(action='SELECT')
    dest = os.path.join(sortie, os.path.basename(f))
    bpy.ops.export_scene.fbx(filepath=dest, use_selection=True, path_mode='STRIP', embed_textures=False,
                             add_leaf_bones=False, bake_anim=True)
    print(f"OK  {os.path.basename(f)} : {os.path.getsize(f)/1e6:.1f} Mo → {os.path.getsize(dest)/1e6:.1f} Mo")
message(f"Terminé : {len(fichiers)} fichier(s) allégé(s) dans le dossier « leger ».")
