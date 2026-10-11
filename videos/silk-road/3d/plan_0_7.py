# Plan 0.7 (repris en 4.1 et 4.8) : plongée zénithale, Ross au centre, 4 « lecteurs » autour. 4 s, lente rotation.
# Usage : blender -b --python plan_0_7.py [-- test]   → plan_0_7.blend (+ test_0_7.png)
import bpy, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import biblio as B, salle_lecture as S
N = 120
sc, ross, agents = S.construire()
bpy.data.objects.remove(bpy.data.objects['plafond'])   # caméra au-dessus du plafond
bpy.ops.object.camera_add(location=(0, .1, 8.6)); c = bpy.context.object; sc.camera = c; c.data.lens = 20
c.rotation_euler = (0, 0, math.radians(-7)); c.keyframe_insert('rotation_euler', frame=1)
c.rotation_euler = (0, 0, math.radians(7)); c.keyframe_insert('rotation_euler', frame=N)
B.sortie(sc, os.path.join(HERE, '..', 'rendu', 'plans', '0_7'), N)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'plan_0_7.blend'))
if 'test' in sys.argv:
    sc.frame_set(60); sc.render.filepath = os.path.join(HERE, 'test_0_7.png'); bpy.ops.render.render(write_still=True)
print('OK')
