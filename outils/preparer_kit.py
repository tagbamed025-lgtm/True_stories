# PRÉPARER UN KIT D'OBJETS AVANT ENVOI (allège le fichier .blend)
# Dans Blender : onglet « Scripting » → Ouvrir ce fichier → ▶ (Run Script).
# 1) réduit toutes les textures à 1024 px maximum (largement suffisant pour la vidéo)
# 2) intègre (« empaquette ») les textures dans le fichier
# 3) enregistre une copie « _kit_leger.blend » à côté de ton fichier, compressée
import bpy, os
MAX = 1024
n = 0
for img in bpy.data.images:
    if img.source not in {'FILE', 'GENERATED'} or not img.has_data and not img.filepath: continue
    try:
        w, h = img.size
        if max(w, h) > MAX:
            k = MAX / max(w, h); img.scale(int(w * k), int(h * k)); n += 1
        img.pack()
    except Exception as e:
        print("ignoré :", img.name, e)
bpy.ops.outliner.orphans_purge(do_recursive=True) if hasattr(bpy.ops.outliner, "orphans_purge") else None
src = bpy.data.filepath or os.path.join(os.path.expanduser("~"), "Desktop", "scene.blend")
dest = os.path.splitext(src)[0] + "_kit_leger.blend"
bpy.ops.wm.save_as_mainfile(filepath=dest, compress=True, copy=True)
msg = f"{n} texture(s) réduite(s). Fichier : {dest} ({os.path.getsize(dest)/1e6:.1f} Mo)"
print(msg)
def dessin(self, ctx): self.layout.label(text=msg)
bpy.context.window_manager.popup_menu(dessin, title="Kit prêt", icon='INFO')
