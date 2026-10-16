# Partie 4 (la diversion) + plan final de la partie 6, dans la salle de Glen Park VALIDÉE (silk-road_v4_VALIDE.blend, ouvert en lecture :
# on ne l'enregistre jamais). Personnages figés dans une pose par plan, c'est la caméra qui bouge (style validé).
# Usage : blender -b "…/silk-road_v4_VALIDE.blend" --python plans_blender.py -- <plan|tous> [test] [final]
#   brouillon par défaut : 960×402, 16 échantillons, 15 i/s. Écrit aussi etiquettes.json (positions écran des étiquettes).
import bpy, sys, os, math, json, mathutils
from bpy_extras.object_utils import world_to_camera_view
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '3d'))
import biblio as B
V = mathutils.Vector
args = sys.argv[sys.argv.index('--') + 1:]; FINAL = 'final' in args
sc = bpy.context.scene; FPS = 30 if FINAL else 15
sc.timeline_markers.clear()   # les repères du .blend imposeraient leurs caméras (le fichier n'est jamais enregistré)
sc.render.fps = FPS; sc.render.resolution_x, sc.render.resolution_y = (1280, 536) if FINAL else (1920, 804)   # fichier v4 lourd (≈ 47 s/image en 1920) : final rendu en 1280, agrandi en 2K au montage
sc.render.resolution_percentage = 100 if FINAL else 50; sc.eevee.taa_render_samples = 20 if FINAL else 16
DL = B.DL + os.sep
ROSS = V((3.9, 4.35, 0)); TETE = V((3.9, 4.2, 1.1)); LAPTOP = bpy.data.objects['Ordi_Ross']
B.ROUGE = bpy.data.materials.get('TRU_rouge'); B.BLANC = bpy.data.materials.get('TRU_blanc')
if not B.BLANC: B.styles()

def yaw_vers(a, b): d = V(b) - V(a); return math.degrees(math.atan2(d.x, -d.y))
def cacher(*noms):
    for n in noms:
        o = bpy.data.objects.get(n)
        if not o: continue
        for x in [o] + list(o.children_recursive): x.hide_render = x.hide_viewport = True
def debout(fichier, anim, img, pos, regarde, gilet=False):
    """Personnage figé debout (pose = une image de l'animation), orienté vers un point."""
    e, arm = B.perso(fichier, B.BLANC, (*pos, 0), yaw_vers(pos, regarde), [(anim, 1, img, 0, 1)])
    sc.frame_set(sc.frame_current); B.figer(e)
    if gilet:   # gilet FBI bleu nuit, lettres jaunes dans le dos
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=1, depth=1, location=(pos[0], pos[1], 1.27))
        g = bpy.context.object; g.scale = (.21, .15, .38); g.rotation_euler.z = math.radians(yaw_vers(pos, regarde))
        g.data.materials.append(B.mat('gilet_FBI', (.015, .025, .06), .7))
        bpy.ops.object.text_add(location=(0, 0, 0)); t = bpy.context.object; t.data.body = 'FBI'; t.data.align_x = t.data.align_y = 'CENTER'
        t.data.size = .12; t.data.extrude = .004; t.data.materials.append(B.mat('FBI_jaune', (1, .78, .05), .4, em=1.2))
        t.parent = g; t.location = (0, 1.02, .15); t.rotation_euler = (math.radians(90), 0, math.pi); t.scale = (1 / .21, 1 / .15, 1 / .38)
    return e
def ross_regarde(point):
    """Ross tourne la tête (contrainte sur les os du cou et de la tête)."""
    arm = bpy.data.objects['Ross_squelette']; cible = bpy.data.objects.new('regard_ross', None); cible.location = point
    sc.collection.objects.link(cible)
    for os_, inf in (('mixamorig:Neck', .5), ('mixamorig:Head', .85)):
        pb = arm.pose.bones.get(os_)
        if pb: c = pb.constraints.new('DAMPED_TRACK'); c.target = cible; c.track_axis = 'TRACK_Z'; c.influence = inf
def camera(nom, cles, lens=35, fstop=2.8, bruit=0):
    c, cible = B.camera(cles[0][1], cles[0][2], lens, fstop); c.name = 'CAM4_' + nom
    for f, pos, tgt in cles:
        c.location = pos; c.keyframe_insert('location', frame=f); cible.location = tgt; cible.keyframe_insert('location', frame=f)
    if bruit:
        for fc in B.courbes(c.animation_data.action): m = fc.modifiers.new('NOISE'); m.scale = 12; m.strength = bruit
    return c

# plan : (durée s, fonction de mise en scène, étiquettes [(texte, point 3D)])
def p_agents():   # « Autour de lui, des agents du FBI, en civil. Ils attendent le bon moment. »
    camera('agents', [(1, (6.4, .2, 2.1), (2.2, 2.4, .9)), (N, (5.6, -.4, 1.9), (1.8, 2.0, .9))], 28, 5.6)
    return [('Agent du FBI', (.3, 2.85, 1.45)), ('Agente du FBI', (1.2, .95, 1.4)), ('Agente du FBI', (1.2, -.35, 1.4))]
def p_dispute():  # « Alors, derrière lui, un homme et une femme se mettent à se disputer. Ce sont deux agents du FBI. »
    cacher('Agente_dispute_Ch26', 'Agent_veste_Ch12')
    debout(DL + 'Typing (2).fbx', 'Yelling', 60, (5.55, 3.15), (5.0, 2.55))
    debout(DL + 'Typing (4).fbx', 'Standing Arguing', 200, (5.0, 2.55), (5.55, 3.15))
    camera('dispute', [(1, (6.15, .9, 1.6), (5.25, 2.9, 1.35)), (N, (6.05, 1.25, 1.55), (5.25, 2.9, 1.35))], 30, 2.8, bruit=.02)
    return [('Agents du FBI', (5.3, 2.85, 1.95))]
def p_retourne():  # « Ross se retourne. Une seconde. Une seule. »
    cacher('Agente_dispute_Ch26', 'Agent_veste_Ch12'); ross_regarde((5.3, 2.9, 1.5))
    camera('retourne', [(1, (4.75, 3.2, 1.3), (3.9, 4.2, 1.22)), (N, (4.6, 3.4, 1.27), (3.9, 4.2, 1.22))], 55, 1.8)
    return []
def p_saisie():   # « Et pendant cette seconde, les agents le saisissent. L'ordinateur reste ouvert, déverrouillé. » (ralenti)
    cacher('Agente_dispute_Ch26', 'Agent_veste_Ch12'); ross_regarde((5.3, 2.9, 1.5))
    debout(DL + 'Typing (1).fbx', 'Picking Up', 70, (4.6, 3.35), (3.95, 3.8))
    LAPTOP.keyframe_insert('location', frame=1); LAPTOP.location.x += .32; LAPTOP.location.y -= .12; LAPTOP.keyframe_insert('location', frame=N)
    camera('saisie', [(1, (3.3, 3.05, .98), (4.05, 3.75, .86)), (N, (3.42, 3.2, .95), (4.2, 3.7, .86))], 45, 2.0)
    return []
def p_debout():   # « Les lecteurs autour de lui se lèvent. Ce n'était pas des lecteurs. » — gilets FBI, contre-plongée
    cacher('Agente_dispute_Ch26', 'Agent_veste_Ch12', 'Agente_Ch02', 'Agent_Ch23'); ross_regarde((4.6, 3.0, 1.6))
    for f, a, img, pos in [(DL + 'Typing (2).fbx', 'Standing Idle', 20, (5.2, 3.6)), (DL + 'Typing (4).fbx', 'Standing Idle', 90, (4.7, 2.85)),
                           (DL + 'Typing (1).fbx', 'Standing Idle', 150, (3.3, 2.95)), ('Ch23_nonPBR.fbx', 'Standing Idle', 60, (2.75, 3.75))]:
        debout(f, a, img, pos, ROSS.xy, gilet=True)
    camera('debout', [(1, (3.0, 1.6, .35), (4.0, 3.6, 1.55)), (N, (3.25, 1.95, .4), (4.0, 3.7, 1.6))], 24, 4)
    return []
def p_cercle():   # « L'homme le plus recherché du dark web vient d'être arrêté… » — plongée, le cercle se referme
    p_debout(); [bpy.data.objects.remove(o) for o in bpy.data.objects if o.name.startswith(('CAM4_', 'cible'))]
    for o in bpy.data.objects:
        if o.name.startswith(('plafond', 'plafonnier')): o.hide_render = True
    bpy.ops.object.camera_add(location=(3.9, 3.7, 6.5)); c = bpy.context.object; sc.camera = c; c.data.lens = 26
    c.rotation_euler = (0, 0, math.radians(-4)); c.keyframe_insert('rotation_euler', frame=1); c.keyframe_insert('location', frame=1)
    c.rotation_euler = (0, 0, math.radians(4)); c.location.z = 5.6; c.keyframe_insert('rotation_euler', frame=N); c.keyframe_insert('location', frame=N)
    return []
def p_table_vide():  # partie 6 : « Mais une question reste… » — la table vide, la chaise reculée, plus d'ordinateur
    cacher('Ross', 'Ordi_Ross', 'Tasse_Ross', 'SacADos_Ross')
    ch = bpy.data.objects['Chaise_Ross']; ch.location.y += .35; ch.location.x += .2; ch.rotation_euler.z += math.radians(25)
    camera('table_vide', [(1, (2.4, 1.9, 1.5), (3.9, 3.8, .8)), (N, (2.9, 2.6, 1.35), (3.9, 3.85, .8))], 35, 2.8)
    return []

def p_miniature():   # miniature YouTube 16:9 : Ross (rouge) cerné par les agents FBI debout, contre-plongée, écran allumé
    p_debout(); [bpy.data.objects.remove(o) for o in bpy.data.objects if o.name.startswith(('CAM4_', 'cible'))]
    camera('miniature', [(1, (4.0, 1.9, 1.42), (3.92, 4.2, 1.12)), (N, (4.0, 1.9, 1.42), (3.92, 4.2, 1.12))], 30, 5.6)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 2560, 1440, 100
    sc.eevee.taa_render_samples = 96
    bpy.ops.object.light_add(type='AREA', location=(3.9, 3.55, 1.0)); l = bpy.context.object; l.data.color = (.45, .65, 1)
    l.data.energy = 60; l.data.size = .35; l.rotation_euler = (math.radians(-80), 0, 0)   # lueur bleue de l'écran sur Ross
    return []

PLANS = {'miniature': (0.1, p_miniature), 'agents': (7.1, p_agents), 'dispute': (7.7, p_dispute), 'retourne': (5.0, p_retourne), 'saisie': (6.1, p_saisie),
         'debout': (5.8, p_debout), 'cercle': (3.4, p_cercle), 'table_vide': (7.5, p_table_vide)}
nom = args[0]; duree, fonc = PLANS[nom]; N = round(duree * FPS) + 2
sc.frame_start, sc.frame_end = 1, N
etiq = fonc()
# positions écran des étiquettes (au milieu du plan) pour le montage
sc.frame_set(N // 2); res = {}
for texte, p in etiq:
    v = world_to_camera_view(sc, sc.camera, V(p)); res.setdefault(nom, []).append([texte, round(v.x, 4), round(1 - v.y, 4)])
fj = os.path.join(HERE, 'etiquettes.json'); tout = json.load(open(fj)) if os.path.exists(fj) else {}
tout.update(res if res else {nom: []}); json.dump(tout, open(fj, 'w'), ensure_ascii=False, indent=1)
dossier = os.path.join(HERE, 'final' if FINAL else 'brouillon', nom)
sc.render.image_settings.file_format = 'PNG'; sc.render.use_overwrite = False; sc.render.use_placeholder = True
if 'test' in args:
    sc.render.filepath = os.path.join(HERE, 'tests', nom + '.png'); bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(dossier, ''); bpy.ops.render.render(animation=True)
print('OK', nom, flush=True)
