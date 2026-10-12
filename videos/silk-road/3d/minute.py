# Première minute de Silk Road dans la salle de Glen Park — découpage « producteur » (v3).
# Ross est DÉJÀ assis (on ne voit jamais arriver l'ordinateur). Les personnages secondaires sont figés
# (comme dans les grandes chaînes : c'est la caméra et le montage qui bougent) ; seul Ross a de petits mouvements (Typing).
# Une seule timeline (30 i/s, image 1 = 0:00). Voix à 0:18.
# Usage : blender -b --python minute.py -- <plan|tous> [test [image]] [brouillon]
import bpy, sys, os, math, mathutils
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import biblio as B, glenpark as G
V = mathutils.Vector
DL = B.DL + os.sep
NOUVEAUX = {'Ch12': DL + 'Typing (4).fbx', 'Ch18': DL + 'Typing (3).fbx', 'Ch02': DL + 'Typing (1).fbx', 'Ch26': DL + 'Typing (2).fbx'}

CHAISE_ROSS = (3.9, 4.35)                    # table ronde près de « Science Fiction », dos à la fenêtre, regarde -Y
TETE = V((3.9, 4.2, 1.06))
LAPTOP = (3.9, 3.82)

# tables : (type, x, y) ; personnes : (fichier, chaise, orientation, pose, image de la pose)
# orientation 0 = regarde -Y, 180 = regarde +Y. Pose figée = une image précise de l'animation.
TABLES = [('ronde', 3.9, 3.7), ('ronde', .3, 3.5), ('rect', 1.2, .3), ('rect', -3.8, 1.8), ('rect', -.6, -2.8)]
AGENTS = [(NOUVEAUX['Ch12'], (.3, 2.85), 180, 'Typing', 300),       # l'homme en veste, à la table ronde voisine
          (NOUVEAUX['Ch26'], (1.2, .95), 0, 'Sitting Idle', 10),    # la femme de la « dispute »
          (NOUVEAUX['Ch02'], (1.2, -.35), 180, 'Sitting Idle', 60),
          ('Ch23_nonPBR.fbx', (-3.8, 2.4), 0, 'Sitting Idle', 120)]
LECTEURS = [(NOUVEAUX['Ch18'], (-3.8, 1.2), 180, 'Sitting Idle', 30), ('Ch22_nonPBR.fbx', (-.6, -2.15), 0, 'Sitting Idle', 90),
            ('Ch31_nonPBR.fbx', (-1.3, -3.45), 180, 'Typing', 150)]
BIBLIOTHECAIRE = ('Ch21_nonPBR.fbx', (-5.3, -4.2), 180, 'Typing', 0)

def construire():
    sc = B.reset(); G.salle(); G.rayonnages(); G.exterieur(); G.poste_bibliothecaire(); B.styles()
    for t, x, y in TABLES: (G.table_ronde if t == 'ronde' else G.table_rect)(x, y)
    for f, (x, y), o, a, img in AGENTS + LECTEURS + [BIBLIOTHECAIRE]:
        if (x, y) != BIBLIOTHECAIRE[1]:
            B.objet('Simple wooden chair', (x, y, 0), rot=o + 180)   # dossier derrière la personne
            if a == 'Typing': B.objet('Samsung Galaxy Book 2', (x, y + (.55 if o == 180 else -.55), .755), rot=o + 180)
            else: B.objet('Stacked set of books', (x, y + (.5 if o == 180 else -.5), .755), rot=o + 8)
        e, arm = B.perso(f, B.BLANC, (x, y, 0), o, [(a, 1, img, 0, 1)])   # pose figée
        B.figer(e)
    B.objet('Simple wooden chair', (*CHAISE_ROSS, 0), rot=180)
    B.objet('Mcbook Laptop', (*LAPTOP, .755), rot=180); B.ecran_portable(os.path.join(HERE, '..', 'ecran', 'ecran.mp4'))
    B.objet('Coffee Cup', (3.4, 3.95, .755)); B.objet('Backpack', (4.45, 4.3, 0), rot=200)
    B.perso('Ch31_nonPBR.fbx', B.ROUGE, (*CHAISE_ROSS, 0), 0, [('Typing', 1, 0)])   # seul Ross bouge un peu
    return sc

# plan : (image début, image fin, [(image, caméra, cible)], focale, ouverture f/, options)
PLANS = {
    'c1_salle':     (1, 90, [(1, (6.2, 4.3, 2.7), (-2.5, -1.2, .9)), (90, (6.1, 3.9, 2.6), (-1.6, -.9, .9))], 22, 8, ''),
    'c2_panneau':   (91, 150, [(91, (2.55, 1.5, 1.8), (2.4, 4.58, 2.75)), (150, (2.75, 1.7, 1.55), (3.75, 4.1, 1.0))], 40, 4, ''),
    'c3_visage':    (151, 270, [(151, (4.0, 2.95, 1.16), tuple(TETE + V((0, 0, .06)))), (270, (3.99, 3.08, 1.15), tuple(TETE + V((0, 0, .06))))], 60, 2.0, 'lueur allume'),
    'c4_zenith':    (271, 390, [], 20, None, 'zenith'),
    # — titre 13–16 s, date 16–18 s (montage) —
    'p07_travelling': (541, 705, [(541, (-1.2, -3.2, 1.6), tuple(TETE)), (705, (2.2, 1.4, 1.3), tuple(TETE))], 35, 4, 'lueur'),
    'p08_epaule':   (706, 885, [(706, (4.3, 4.85, 1.42), (3.9, 3.6, .85)), (885, (4.12, 4.62, 1.22), (3.9, 3.62, .85))], 35, 2.8, 'lueur'),
    # — zoom dans l'écran 29,5–36,5 s (montage) —
    'p09_salle':    (1096, 1257, [(1096, (6.2, -3.8, 1.5), (-3, 2, 1.0)), (1257, (5.8, -1.8, 1.45), (-3, 2.5, 1.0))], 26, 5.6, ''),
    'p10_poitrine': (1258, 1440, [(1258, (2.45, 3.05, 1.22), tuple(TETE)), (1440, (2.6, 3.2, 1.21), tuple(TETE))], 50, 2.0, 'lueur epaule'),
    'p11_pousse':   (1441, 1545, [(1441, (3.9, 3.0, 1.14), tuple(TETE + V((0, 0, .06)))), (1545, (3.9, 3.3, 1.13), tuple(TETE + V((0, 0, .06))))], 50, 1.8, 'lueur'),
}

def camera(nom, garder=False):
    sc = bpy.context.scene; f0, f1, cles, lens, fstop, opt = PLANS[nom]
    for o in [] if garder else [o for o in bpy.data.objects if o.type == 'CAMERA' or o.name.startswith(('cible', 'lueur'))]: bpy.data.objects.remove(o)
    if not garder:   # plafond visible partout sauf en plongée (ne touche plus aux tables rondes)
        for o in bpy.data.objects:
            if o.name.startswith(('plafond', 'plafonnier')): o.hide_render = 'zenith' in opt
    if 'zenith' in opt:
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
    if 'lueur' in opt:   # lumière bleue de l'écran sur le visage ; au plan c3 elle s'allume avec le bip
        bpy.ops.object.light_add(type='AREA', location=(LAPTOP[0], LAPTOP[1] - .08, 1.0)); l = bpy.context.object; l.name = 'lueur_ecran'
        l.data.color = (.45, .65, 1); l.data.size = .3; l.rotation_euler = (math.radians(-80), 0, 0)
        l.data.energy = 4 if 'allume' in opt else 40; l.data.keyframe_insert('energy', frame=f0)
        if 'allume' in opt: l.data.energy = 45; l.data.keyframe_insert('energy', frame=f0 + 12)
    sc.frame_start, sc.frame_end = f0, f1

if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]
    sc = construire()
    sc.render.resolution_percentage = 50 if 'brouillon' in args else 100
    sc.eevee.taa_render_samples = 16 if 'brouillon' in args else 48
    noms = list(PLANS) if args[0] == 'tous' else args[0].split(',')
    for nom in noms:
        camera(nom)
        dossier = os.path.join(HERE, '..', 'rendu', 'plans' + ('_brouillon' if 'brouillon' in args else ''), nom)
        sc.render.filepath = os.path.join(dossier, '')
        sc.render.image_settings.file_format = 'PNG'; sc.render.use_overwrite = False; sc.render.use_placeholder = True
        if 'test' in args:
            i = args.index('test'); f = int(args[i + 1]) if len(args) > i + 1 and args[i + 1].isdigit() else (PLANS[nom][0] + PLANS[nom][1]) // 2
            sc.frame_set(f); sc.render.filepath = os.path.join(HERE, 'tests', f'{nom}.png'); bpy.ops.render.render(write_still=True)
        else:
            bpy.ops.render.render(animation=True)
        print('OK', nom, flush=True)
