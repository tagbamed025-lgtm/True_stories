# Plan 4.7 : le twist. Les « lecteurs » se lèvent, les gilets FBI apparaissent. Contre-plongée lente, 4 s.
# « Standing Up » Mixamo manque : lever simulé par fondu Sitting Idle → pose debout (Female Start Walking, image 1).
import bpy, sys, os, math, mathutils
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import biblio as B, salle_lecture as S
N = 120
LEVER = [18, 30, 8, 24]          # image où chaque agent commence à se lever (désynchronisés)
debout = lambda i, d: [('Sitting Idle', 1, d), ('Female Start Walking', LEVER[i], 0, 22, 1)]
sc, ross, agents = S.construire(debout)
GILET = B.mat('gilet_FBI', (.015, .025, .06), .7)
JAUNE = B.mat('FBI_jaune', (1, .78, .05), .4, em=1.5)

def lettres(parent, y, rz):
    bpy.ops.object.text_add(); t = bpy.context.object; t.data.body = 'FBI'; t.data.extrude = .002
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = .11; t.data.materials.append(JAUNE)
    t.parent = parent; t.location = (0, .07, y); t.rotation_euler = (math.radians(90), 0, rz)

def gilet(e, arm, i):
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=1, depth=2); g = bpy.context.object; g.name = f'gilet{i}'
    g.data.transform(mathutils.Matrix.Diagonal((.2, .14, .19, 1)))
    for p in g.data.polygons: p.use_smooth = False
    g.data.materials.append(GILET)
    cl = g.constraints.new('COPY_LOCATION'); cl.target = arm; cl.subtarget = 'mixamorig:Spine1'; cl.head_tail = .6
    cr = g.constraints.new('COPY_ROTATION'); cr.target = arm; cr.subtarget = 'mixamorig:Spine1'
    # dans l'espace de l'os : Y = le long du dos, Z = vers l'avant → on remet l'axe du cylindre sur Y
    g.data.transform(mathutils.Matrix.Rotation(math.radians(-90), 4, 'X'))
    for sgn, nom in ((1, 'avant'), (-1, 'dos')):
        bpy.ops.object.text_add(); t = bpy.context.object; t.data.body = 'FBI'; t.data.extrude = .004
        t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = .1 if sgn < 0 else .055
        t.data.materials.append(JAUNE); t.parent = g
        t.location = (0 if sgn < 0 else .08, .02, sgn * .145); t.rotation_euler = (0, 0 if sgn > 0 else math.pi, 0)
    # le gilet « sort » du torse quand la veste s'ouvre
    f0 = LEVER[i] + 26
    for o in [g] + list(g.children):   # invisible tant que la veste est fermée
        o.hide_render = True; o.keyframe_insert('hide_render', frame=f0 - 1)
        o.hide_render = False; o.keyframe_insert('hide_render', frame=f0)
    g.scale = (.75,) * 3; g.keyframe_insert('scale', frame=f0)
    g.scale = (1.07,) * 3; g.keyframe_insert('scale', frame=f0 + 14)
    # en se levant, l'agent recule de la table (l'Empty porte le déplacement)
    e.keyframe_insert('location', frame=LEVER[i])
    e.location += mathutils.Vector((0, -.3, 0)) @ mathutils.Matrix.Rotation(-e.rotation_euler.z, 3, 'Z').transposed()
    e.keyframe_insert('location', frame=LEVER[i] + 22)

for i, (e, arm) in enumerate(agents): gilet(e, arm, i)
c, cible = B.camera((1.9, -1.7, .35), (.4, .7, 1.35), lens=22, fstop=2.8)
c.keyframe_insert('location', frame=1); c.location = (1.6, -1.35, .3); c.keyframe_insert('location', frame=N)
B.sortie(sc, os.path.join(HERE, '..', 'rendu', 'plans', '4_7'), N)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'plan_4_7.blend'))
if 'test' in sys.argv:
    for f in [int(a) for a in sys.argv if a.isdigit()] or [100]:
        sc.frame_set(f); sc.render.filepath = os.path.join(HERE, f'test_4_7_{f}.png'); bpy.ops.render.render(write_still=True)
print('OK')
