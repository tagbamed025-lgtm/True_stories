# Exporte des personnages TRU Stories en pose figée (low poly, rouge/blanc) au format GLB pour les décors Three.js.
# Usage : blender -b --python exporter_glb.py
import bpy, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import biblio as B
OUT = os.path.join(HERE, '..', '..', '..', 'assets3d', 'silk-road', 'glb'); os.makedirs(OUT, exist_ok=True)
DL = B.DL + os.sep
# nom : (fichier perso, couleur, animation, image de la pose)
POSES = {
    'alford_assis_tape': (DL + 'Typing (3).fbx', 'blanc', 'Typing', 300),         # Gary Alford (IRS) à son bureau
    'agent_debout_veste': (DL + 'Typing (4).fbx', 'blanc', 'Standing Idle', 40),  # agent en veste
    'agent_debout_2':     ('Ch23_nonPBR.fbx', 'blanc', 'Standing Idle', 120),
    'agente_debout':      (DL + 'Typing (1).fbx', 'blanc', 'Standing Idle', 80),
    'ross_assis_tape':    ('Ch31_nonPBR.fbx', 'rouge', 'Typing', 200),
    'ross_debout':        ('Ch31_nonPBR.fbx', 'rouge', 'Standing Idle', 60),
}
for nom, (f, coul, anim, img) in POSES.items():
    B._anims.clear(); B._kit.clear(); sc = B.reset(); B.styles()   # caches vidés : reset() efface les actions
    e, arm = B.perso(f, B.ROUGE if coul == 'rouge' else B.BLANC, (0, 0, 0), 0, [(anim, 1, img, 0, 1)])
    bpy.context.scene.frame_set(1); B.figer(e)
    for o in bpy.data.objects: o.select_set(o.type == 'MESH')
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, nom + '.glb'), export_format='GLB', use_selection=True,
                              export_apply=True, export_yup=True, export_normals=True, export_materials='EXPORT')
    print('OK', nom, flush=True)
