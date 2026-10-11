# Grande salle de lecture de Glen Park, commune à tous les plans « bibliothèque » de Silk Road.
# Ross (rouge) à la table centrale, dos à la baie vitrée. 4 agents en civil + 6 vrais lecteurs (blanc).
import bpy, os, math, mathutils
import biblio as B
ECRAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ecran', 'ecran.mp4')
TABLES = [(-6, 3.5), (0, 3.5), (6, 3.5), (-6, -3.5), (0, -3.5), (6, -3.5)]
ROSS = (0, 4.25)                                                     # dos à la baie, regarde vers -Y
# (fichier, chaise, orientation, décalage d'anim) — orientation 0 = regarde -Y, 180 = regarde +Y
AGENTS = [('Ch23_nonPBR.fbx', (.8, 2.75), 180, 40), ('Ch21_nonPBR.fbx', (-5.6, 4.25), 0, 90),
          ('Ch22_nonPBR.fbx', (5.5, 2.75), 180, 140), ('Ch23_nonPBR.fbx', (-6.4, 2.75), 180, 190)]
LECTEURS = [('Ch22_nonPBR.fbx', (-6, -4.25), 0, 20), ('Ch31_nonPBR.fbx', (-.6, -2.75), 180, 70),
            ('Ch21_nonPBR.fbx', (.7, -4.25), 0, 120), ('Ch23_nonPBR.fbx', (6.3, -2.75), 180, 170),
            ('Ch31_nonPBR.fbx', (5.6, -4.25), 0, 220), ('Ch22_nonPBR.fbx', (6.4, 4.25), 0, 60)]

def construire(ross='assis', actions_agents=None, lecteurs=True):
    sc = B.reset(); B.salle(); B.rayonnages(); B.styles()
    for x, y in TABLES: B.objet('GUBI Rectangular Table', (x, y, 0))
    gens = [(ROSS, 0)] + [(c, r) for _, c, r, _ in AGENTS + (LECTEURS if lecteurs else [])]
    for (x, y), r in gens:
        B.objet('Simple wooden chair', (x, y, 0), rot=r + 180)
        if (x, y) != ROSS: B.objet('Stacked set of books', (x, y + (.5 if r == 180 else -.5), .745), rot=r + 8)
    B.objet('Mcbook Laptop', (0, 3.72, .74), rot=180); B.ecran_portable(ECRAN)
    B.objet('Coffee Cup', (-.38, 3.75, .74)); B.objet('Backpack', (.5, 4.45, 0), rot=200)
    B.objet('Minimalist LED Desk Lamp black', (-.8, 3.95, .74), rot=160)
    if ross == 'assis':
        r = B.perso('Ch31_nonPBR.fbx', B.ROUGE, (*ROSS, 0), 0, [('Sitting Idle', 1, 0)])
    else:   # ross = (frame_debut, frame_fin, depart, arrivee) : il traverse la salle
        f0, f1, a, b = ross
        r = B.perso('Ch31_nonPBR.fbx', B.ROUGE, (*a, 0), 0, [('Walking*', 1, 0)])
        d = mathutils.Vector(b) - mathutils.Vector(a)
        r[0].rotation_euler.z = math.atan2(d.x, -d.y)
        dist = B.VITESSE['Walking'] * (f1 - f0) / B.FPS; b = mathutils.Vector(a) + d.normalized() * dist
        r[0].keyframe_insert('location', frame=f0); r[0].location = (*b, 0); r[0].keyframe_insert('location', frame=f1)
        for fc in B.courbes(r[0].animation_data.action):
            for k in fc.keyframe_points: k.interpolation = 'LINEAR'
    agents = [B.perso(f, B.BLANC, (x, y, 0), o, (actions_agents(i, dec) if actions_agents else [('Sitting Idle', 1, dec)]))
              for i, (f, (x, y), o, dec) in enumerate(AGENTS)]
    if lecteurs:
        for f, (x, y), o, dec in LECTEURS: B.perso(f, B.BLANC, (x, y, 0), o, [('Sitting Idle', 1, dec)])
    return sc, r, agents
