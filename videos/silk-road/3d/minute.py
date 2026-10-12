# Première minute de Silk Road (cold open + section 1) dans la vraie salle de Glen Park.
# Une seule timeline (30 i/s, image 1 = 0:00) : chaque plan rend sa tranche → la marche de Ross est continue d'un angle à l'autre.
# Usage : blender -b --python minute.py -- <plan|tous> [test <image>] [apercu]
import bpy, sys, os, math, mathutils
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import biblio as B, glenpark as G
V = mathutils.Vector
DL = B.DL + os.sep
NOUVEAUX = {'Ch12': DL + 'Typing (4).fbx', 'Ch18': DL + 'Typing (3).fbx', 'Ch02': DL + 'Typing (1).fbx', 'Ch26': DL + 'Typing (2).fbx'}

# --- Ross : il entre par la porte de l'escalier, traverse lentement, s'assoit à la table ronde près de « Science Fiction »
PORTE, ARRIVEE = V((-6.6, -1.9)), V((2.9, 2.55))
F_MARCHE, F_ASSIS = 375, 376                 # marche 0:00 → 0:12,5 ; il s'assoit à 0:12,5
CHAISE_ROSS = (3.9, 4.35)                    # dos à la fenêtre, regarde -Y
TETE = V((3.9, 4.22, 1.08))
LAPTOP = (3.9, 3.82)

def ross_pos(f):
    t = min(max((f - 1) / (F_MARCHE - 1), 0), 1); p = PORTE.lerp(ARRIVEE, t); return V((p.x, p.y, 0))

# tables : (type, x, y) ; personnes : (fichier, chaise, orientation, anim, décalage) — orientation 0 = regarde -Y, 180 = regarde +Y
TABLES = [('ronde', 3.9, 3.7), ('ronde', .3, 3.5), ('rect', 1.2, .3), ('rect', -3.8, 1.8), ('rect', -.6, -2.8)]
AGENTS = [(NOUVEAUX['Ch12'], (.3, 2.85), 180, 'Typing', 300),       # l'homme en veste, à la table ronde voisine
          (NOUVEAUX['Ch26'], (1.2, .95), 0, 'Sitting', 0),          # la femme de la « dispute »
          (NOUVEAUX['Ch02'], (1.2, -.35), 180, 'Sitting Idle', 60),
          ('Ch23_nonPBR.fbx', (5.7, -1.6), -90, 'Sitting Idle', 120)]  # coin « Large Print »
LECTEURS = [(NOUVEAUX['Ch18'], (-3.8, 1.2), 180, 'Sitting Idle', 30), ('Ch22_nonPBR.fbx', (-3.8, 2.4), 0, 'Sitting', 90),
            ('Ch31_nonPBR.fbx', (-.6, -2.15), 0, 'Typing', 150), ('Ch21_nonPBR.fbx', (-1.3, -3.45), 180, 'Sitting Idle', 200)]
BIBLIOTHECAIRE = ('Ch23_nonPBR.fbx', (-5.3, -4.2), 180, 'Typing', 0)

def construire():
    sc = B.reset(); G.salle(); G.rayonnages(); G.exterieur(); G.poste_bibliothecaire(); B.styles()
    for t, x, y in TABLES: (G.table_ronde if t == 'ronde' else G.table_rect)(x, y)
    for f, (x, y), o, a, d in AGENTS + LECTEURS + [BIBLIOTHECAIRE]:
        if f != BIBLIOTHECAIRE[0] or (x, y) != BIBLIOTHECAIRE[1]: B.objet('Simple wooden chair', (x, y, 0), rot=o + 180)   # dossier derrière la personne
        if a == 'Typing': B.objet('Samsung Galaxy Book 2', (x + .0, y + (.55 if o == 180 else -.55), .755), rot=o + 180)
        else: B.objet('Stacked set of books', (x, y + (.5 if o == 180 else -.5), .755), rot=o + 8)
        B.perso(f, B.BLANC, (x, y, 0), o, [(a, 1, d)])
    B.objet('Simple wooden chair', (*CHAISE_ROSS, 0), rot=180); B.objet('Simple wooden chair', (3.9, 3.0, 0), rot=0)
    B.objet('Mcbook Laptop', (*LAPTOP, .755), rot=180); B.ecran_portable(os.path.join(HERE, '..', 'ecran', 'ecran.mp4'))
    B.objet('Coffee Cup', (3.35, 3.95, .755)); B.objet('Backpack', (4.45, 4.3, 0), rot=200)
    # Ross : marche lente (Walking ralentie) → Stand To Sit → Typing
    e, arm = B.perso('Ch31_nonPBR.fbx', B.ROUGE, ross_pos(1), 0, [])
    act = B.anim('Walking', True); d = ARRIVEE - PORTE
    vitesse = d.length / ((F_MARCHE - 1) / B.FPS)
    tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new('marche', 1, act)
    st.scale = .5 * B.VITESSE['Walking'] / vitesse                    # pas calés sur la vitesse réelle : pas de glissement
    st.repeat = math.ceil(F_MARCHE / ((act.frame_range[1] - act.frame_range[0]) * st.scale)) + 1
    tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new('assoit', F_ASSIS, B.anim('Stand To Sit')); st.scale = .5; st.extrapolation = 'HOLD_FORWARD'
    tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new('tape', F_ASSIS + 62, B.anim('Typing')); st.scale = .5
    st.blend_in = 14; st.repeat = 8; st.extrapolation = 'HOLD_FORWARD'
    e.rotation_euler.z = math.atan2(d.x, -d.y); e.keyframe_insert('rotation_euler', frame=F_MARCHE)
    e.location = ross_pos(1); e.keyframe_insert('location', frame=1)
    e.location = ross_pos(F_MARCHE); e.keyframe_insert('location', frame=F_MARCHE)
    e.location = (*CHAISE_ROSS, 0); e.keyframe_insert('location', frame=F_ASSIS)
    e.rotation_euler.z = 0; e.keyframe_insert('rotation_euler', frame=F_ASSIS)
    for fc in B.courbes(e.animation_data.action):
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'
    fc_c = [fc for fc in B.courbes(e.animation_data.action)]
    for fc in fc_c:
        for k in fc.keyframe_points:
            if int(k.co[0]) == F_ASSIS: k.interpolation = 'CONSTANT'
    for fc in fc_c:   # saut instantané entre la marche et la chaise (caché par la coupe entre deux plans)
        for k in fc.keyframe_points:
            if int(k.co[0]) == F_MARCHE: k.interpolation = 'CONSTANT'
    return sc

def suivi(f, recul, cote, z, zc=1.0, avance=0.0):
    """Caméra qui accompagne Ross : derrière (recul) et à côté (cote) de sa trajectoire."""
    d = (ARRIVEE - PORTE).normalized(); n = V((-d.y, d.x))
    p = ross_pos(f); base = V((p.x, p.y)) - d * recul + n * cote
    cible = V((p.x, p.y)) + d * avance
    return (base.x, base.y, z), (cible.x, cible.y, zc)

# plan : (image début, image fin, [(image, caméra, cible)], focale, ouverture f/, options)
PLANS = {
    'e1_pieds':     (1, 90, [(f, *suivi(f, -.2, 1.3, .22, .18, .3)) for f in (1, 90)], 50, 2.0, ''),
    'e2_dos':       (91, 180, [(f, *suivi(f, 2.6, .35, 1.55, 1.25, 1.5)) for f in (91, 180)], 32, 2.8, 'epaule'),
    'e3_salle':     (181, 300, [(181, (6.2, 4.3, 2.7), (-2.5, -1.2, .9)), (300, (6.2, 3.6, 2.5), (-1.0, -.6, .9))], 22, 8, ''),
    'e4_panneau':   (301, 375, [(301, (1.9, 2.0, 2.0), (2.4, 4.58, 2.75)), (375, (1.95, 2.15, 1.75), (2.4, 4.4, 1.45))], 50, 2.8, ''),
    'e5_assoit':    (376, 480, [(376, (6.0, 2.4, 1.35), (3.9, 4.15, .95)), (480, (5.8, 2.55, 1.3), (3.9, 4.15, .95))], 40, 2.8, ''),
    'e6_visage':    (481, 570, [(481, (3.98, 3.3, 1.13), tuple(TETE)), (570, (3.97, 3.45, 1.12), tuple(TETE))], 65, 2.0, 'lueur'),
    'e7_zenith':    (571, 720, [], 20, None, 'zenith'),
    'p07_travelling': (916, 1080, [(916, (-1.2, -3.2, 1.6), tuple(TETE)), (1080, (2.2, 1.4, 1.3), tuple(TETE))], 35, 4, 'lueur'),
    'p08_epaule':   (1081, 1260, [(1081, (4.3, 4.85, 1.42), (3.9, 3.6, .85)), (1260, (4.12, 4.62, 1.22), (3.9, 3.62, .85))], 35, 2.8, 'lueur'),
    'p09_salle':    (1471, 1632, [(1471, (6.2, -3.8, 1.5), (-3, 2, 1.0)), (1632, (5.8, -1.8, 1.45), (-3, 2.5, 1.0))], 26, 5.6, ''),
    'p10_poitrine': (1633, 1815, [(1633, (2.45, 3.05, 1.24), tuple(TETE)), (1815, (2.6, 3.2, 1.23), tuple(TETE))], 50, 2.0, 'lueur epaule'),
    'p11_pousse':   (1816, 1920, [(1816, (3.9, 3.28, 1.1), tuple(TETE)), (1920, (3.9, 3.6, 1.09), tuple(TETE))], 50, 1.8, 'lueur'),
}

def camera(nom):
    sc = bpy.context.scene; f0, f1, cles, lens, fstop, opt = PLANS[nom]
    for o in [o for o in bpy.data.objects if o.type == 'CAMERA' or o.name.startswith(('cible', 'lueur'))]: bpy.data.objects.remove(o)
    if 'zenith' in opt:
        for o in [o for o in bpy.data.objects if o.name.startswith(('plafond', 'Cylinder'))]: o.hide_render = True
        bpy.ops.object.camera_add(location=(2.3, 2.4, 8.2)); c = bpy.context.object; sc.camera = c; c.data.lens = lens
        c.rotation_euler = (0, 0, math.radians(-6)); c.keyframe_insert('rotation_euler', frame=f0)
        c.rotation_euler = (0, 0, math.radians(6)); c.keyframe_insert('rotation_euler', frame=f1)
    else:
        c, cible = B.camera(cles[0][1], cles[0][2], lens, fstop)
        for f, pos, tgt in cles:
            c.location = pos; c.keyframe_insert('location', frame=f); cible.location = tgt; cible.keyframe_insert('location', frame=f)
        if 'epaule' in opt:   # caméra épaule légère
            for fc in B.courbes(c.animation_data.action):
                m = fc.modifiers.new('NOISE'); m.scale = 40; m.strength = .012
    if 'lueur' in opt:   # lumière bleue de l'écran sur le visage, qui s'allume au plan e6
        bpy.ops.object.light_add(type='AREA', location=(LAPTOP[0], LAPTOP[1] - .08, 1.0)); l = bpy.context.object; l.name = 'lueur_ecran'
        l.data.color = (.45, .65, 1); l.data.size = .3; l.rotation_euler = (math.radians(-80), 0, 0)
        l.data.energy = 0 if nom == 'e6_visage' else 40; l.data.keyframe_insert('energy', frame=f0)
        if nom == 'e6_visage': l.data.energy = 40; l.data.keyframe_insert('energy', frame=f0 + 25)
    sc.frame_start, sc.frame_end = f0, f1

if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]
    sc = construire(); B.apercu(sc, 'apercu' in args)
    if not ('apercu' in args): sc.eevee.taa_render_samples = 64
    noms = list(PLANS) if args[0] == 'tous' else args[0].split(',')
    for nom in noms:
        camera(nom)
        dossier = os.path.join(HERE, '..', 'rendu', 'plans', nom); sc.render.filepath = os.path.join(dossier, '')
        sc.render.image_settings.file_format = 'PNG'; sc.render.use_overwrite = False; sc.render.use_placeholder = True
        if 'test' in args:
            f = int(args[args.index('test') + 1]) if args[args.index('test') + 1].isdigit() else (PLANS[nom][0] + PLANS[nom][1]) // 2
            sc.frame_set(f); sc.render.filepath = os.path.join(HERE, 'tests', f'{nom}.png'); bpy.ops.render.render(write_still=True)
        else:
            bpy.ops.render.render(animation=True)
        print('OK', nom, flush=True)
