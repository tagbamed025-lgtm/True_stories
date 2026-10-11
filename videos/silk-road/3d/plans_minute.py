# Plans [3D] de la première minute (cold open + section 1), calés sur VO_complete_SilkRoad.mp3.
# Usage : blender -b --python plans_minute.py -- <plan> [test <image>] [final]
#   sans « test » : rendu complet, reprenable (rendu/plans/<plan>/0001.png…). « final » = 1920×804, sinon aperçu 1280×536.
import bpy, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import biblio as B, salle_lecture as S
TETE = (0, 4.12, 1.08)    # tête de Ross assis
# plan : (nb d'images, ross, [(image, position caméra, cible)], focale, ouverture f/, extra)
PLANS = {
    'p01_entree':     (240, (1, 240, (-12.5, 6.3), (-1.2, 5.3)), [(1, (11, -7.5, 1.7), (-8, 5, 1.2)), (240, (10, -7, 1.7), (-3, 4.5, 1.2))], 24, None, ''),
    'p02_assis':      (150, 'assis', [(1, (2.9, 1.9, 1.35), (0, 3.9, 1.0)), (150, (2.6, 2.2, 1.3), (0, 3.9, 1.0))], 40, 2.8, ''),
    'p03_visage':     (120, 'assis', [(1, (.12, 2.8, 1.12), TETE), (120, (.1, 2.95, 1.11), TETE)], 65, 2.0, 'lueur'),
    'p04_zenith':     (180, 'assis', [(1, None, None), (180, None, None)], 20, None, 'zenith'),
    'p07_travelling': (165, 'assis', [(1, (0, -6.5, 1.6), (0, 4, 1.0)), (165, (0, -1.5, 1.35), (0, 4, 1.0))], 35, 4, ''),
    'p08_epaule':     (180, 'assis', [(1, (.45, 5.05, 1.4), (0, 3.6, .85)), (180, (.22, 4.7, 1.22), (0, 3.62, .85))], 35, 2.8, 'lueur'),
    'p09_salle':      (162, 'assis', [(1, (-10, -.8, 1.4), (1, 3, 1.0)), (162, (-7, -1.4, 1.4), (2, 3, 1.0))], 28, 5.6, ''),
    'p10_poitrine':   (183, 'assis', [(1, (-1.5, 2.3, 1.25), TETE), (183, (-1.35, 2.45, 1.24), TETE)], 50, 2.0, 'lueur epaule'),
    'p11_pousse':     (105, 'assis', [(1, (0, 2.95, 1.1), TETE), (105, (0, 3.3, 1.09), TETE)], 50, 1.8, 'lueur'),
}
nom = sys.argv[sys.argv.index('--') + 1]; N, ross, cles, lens, fstop, extra = PLANS[nom]
sc, r, agents = S.construire(ross)
if 'zenith' in extra:   # plongée verticale (plans 0.7 / 4.1 / 4.8) : sans plafond
    for o in [o for o in bpy.data.objects if o.name.startswith(('plafond', 'neon'))]: bpy.data.objects.remove(o)
    bpy.ops.object.camera_add(location=(0, 3.6, 7.6)); c = bpy.context.object; sc.camera = c; c.data.lens = lens
    c.rotation_euler = (0, 0, math.radians(-7)); c.keyframe_insert('rotation_euler', frame=1)
    c.rotation_euler = (0, 0, math.radians(7)); c.keyframe_insert('rotation_euler', frame=N)
else:
    c, cible = B.camera(cles[0][1], cles[0][2], lens, fstop)
    for f, pos, tgt in cles:
        c.location = pos; c.keyframe_insert('location', frame=f); cible.location = tgt; cible.keyframe_insert('location', frame=f)
    if 'epaule' in extra:   # caméra épaule légère
        for fc in B.courbes(c.animation_data.action):
            m = fc.modifiers.new('NOISE'); m.scale = 40; m.strength = .015
if 'lueur' in extra:   # lumière bleue de l'écran sur le visage
    bpy.ops.object.light_add(type='AREA', location=(0, 3.62, 1.0)); l = bpy.context.object; l.name = 'lueur_ecran'
    l.data.color = (.45, .65, 1); l.data.size = .3; l.rotation_euler = (math.radians(-80), 0, 0)
    l.data.energy = 0 if nom == 'p03_visage' else 25; l.data.keyframe_insert('energy', frame=1)
    if nom == 'p03_visage': l.data.energy = 25; l.data.keyframe_insert('energy', frame=30)
B.apercu(sc, 'final' not in sys.argv)
B.sortie(sc, os.path.join(HERE, '..', 'rendu', 'plans', nom + ('' if 'final' in sys.argv else '_apercu')), N)
if 'test' in sys.argv:
    f = int(sys.argv[sys.argv.index('test') + 1]); sc.frame_set(f)
    sc.render.filepath = os.path.join(HERE, 'tests', f'{nom}_{f}.png'); bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print('OK', nom)
