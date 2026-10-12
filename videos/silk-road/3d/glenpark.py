# Salle de lecture de la bibliothèque de Glen Park (2e étage), d'après les photos réelles :
# murs crème, piliers entre de hautes fenêtres à stores, sol vinyle ambré brillant, étagères en érable,
# panneaux « Romances » / « Science Fiction » / « Large Print », tables rondes à pied gris, poste du bibliothécaire.
# Dehors : la rue en contrebas, maisons de San Francisco en face, poteau et fils électriques, colline boisée.
import bpy, math, random, mathutils
import biblio as B
from biblio import mat

L, P, H = 14, 10, 3.6                       # salle : x ∈ [-7, 7], y ∈ [-5, 5] ; fenêtres côté +Y
PILIERS = [-6.4, -2.0, 2.4, 6.4]            # x des piliers du mur des fenêtres
FENETRES = [(-5.8, -2.6), (-1.4, 1.8), (3.0, 5.8)]
SOL_RUE = -4.6                              # on est au 2e étage
ERABLE = (.62, .44, .26)
LIVRES = [(.07, .07, .08), (.42, .07, .05), (.09, .13, .28), (.72, .67, .56), (.13, .22, .13), (.6, .43, .1), (.3, .3, .32), (.55, .2, .1)]

def cube(nom, loc, dim, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = nom; o.scale = dim
    o.data.materials.append(m); return o

def texte(corps, loc, rot, taille, m, police='C:/Windows/Fonts/corbel.ttf'):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object; t.data.body = corps
    t.data.font = bpy.data.fonts.load(police, check_existing=True); t.data.size = taille
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.materials.append(m); return t

def panneau(corps, x, y, z, rz=0):
    """Plaque crème au texte gris, posée sur un pilier."""
    pl = cube('panneau_' + corps, (x, y, z), (1.25, .03, .3), mat('plaque', (.86, .83, .68), .6))
    pl.rotation_euler.z = rz
    d = mathutils.Vector((0, -.02, 0)); d.rotate(mathutils.Euler((0, 0, rz)))
    texte(corps, (x + d.x, y + d.y, z), (math.pi / 2, 0, rz), .13, mat('texte_plaque', (.25, .26, .27), .5))

def ombre_seule(o): o.visible_shadow = False

def salle():
    creme = mat('creme', (.86, .72, .48), .85); creme_clair = mat('creme_clair', (.9, .8, .6), .85)
    sol = mat('vinyle', (.55, .36, .17), .22)                                  # sol brillant : reflets du soleil
    cube('sol', (0, 0, -.05), (L, P, .1), sol)
    cube('plafond', (0, 0, H + .05), (L, P, .1), mat('plafond', (.9, .86, .76), .9, em=.35, emc=(1, .92, .8))).visible_shadow = False
    cube('mur_fond', (0, -P/2 - .1, H/2), (L, .2, H), creme)
    cube('mur_gauche_a', (-L/2 - .1, -4.2, H/2), (.2, 1.6, H), creme)           # porte de l'escalier entre y = -3.4 et -1.4
    cube('mur_gauche_b', (-L/2 - .1, 1.6, H/2), (.2, 6.8, H), creme)
    cube('linteau_porte', (-L/2 - .1, -2.4, H - .4), (.2, 2, .8), creme)
    cube('couloir', (-L/2 - 1.6, -2.4, H/2), (2.8, 2.4, H), mat('couloir', (.12, .1, .08), .9)).visible_shadow = False
    cube('mur_droit', (L/2 + .1, 0, H/2), (.2, P, H), creme)
    cube('plinthe', (0, -P/2 + .01, .05), (L, .02, .1), mat('plinthe', (.25, .17, .1), .5))
    # mur des fenêtres : allège, imposte, piliers saillants
    cube('allege', (0, P/2 + .1, .3), (L, .3, .6), creme)
    cube('imposte', (0, P/2 + .1, H - .2), (L, .3, .4), creme)
    for x in PILIERS: cube('pilier', (x, P/2 - .1, H/2), (1.2, .6, H), creme_clair)
    cadre = mat('cadre_alu', (.42, .43, .45), .35)
    store = mat('store', (.92, .9, .85), .9)
    store.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = .55
    store.surface_render_method = 'BLENDED'
    for x0, x1 in FENETRES:
        cx, w = (x0 + x1) / 2, x1 - x0
        for x in (x0 + .03, cx, x1 - .03): cube('montant', (x, P/2 + .05, H/2), (.07, .1, H - .8), cadre)
        for z in (.62, 2.35, H - .42): cube('traverse', (cx, P/2 + .05, z), (w, .1, .07), cadre)
        s = cube('store', (cx, P/2, 2.6), (w - .1, .01, 1.3), store); ombre_seule(s)   # stores à moitié baissés
    # éclairage : plafonniers ronds + diffuseurs carrés
    disque = mat('plafonnier', (1, .97, .9), .5, em=4)
    for x in (-4.5, 0, 4.5):
        for y in (-2.5, 1.5):
            bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=.45, depth=.08, location=(x, y, H - .04))
            o = bpy.context.object; o.name = 'plafonnier'; o.data.materials.append(disque); ombre_seule(o)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, H - .15)); a = bpy.context.object; a.name = 'plafond_lumiere'
    a.data.shape = 'RECTANGLE'; a.data.size = 12; a.data.size_y = 8; a.data.energy = 380; a.data.color = (1, .88, .7)
    # soleil de 15 h en octobre : bas, chaud, entre par les fenêtres et dessine des bandes sur le sol
    bpy.ops.object.light_add(type='SUN'); so = bpy.context.object; so.name = 'soleil'
    so.data.energy = 5.5; so.data.color = (1, .8, .55); so.data.angle = math.radians(.8)
    so.rotation_euler = (math.radians(-64), 0, math.radians(24))   # vient de la rue (+Y), bas sur l'horizon
    w = bpy.context.scene.world.node_tree.nodes['Background']
    w.inputs[0].default_value = (.42, .58, .85, 1); w.inputs[1].default_value = .65   # ciel bleu
    details(creme_clair)

def details(creme_clair):
    panneau('Romances', -2.0, P/2 - .42, 2.75); panneau('Science Fiction', 2.4, P/2 - .42, 2.75)
    panneau('Large Print', L/2 - .05, -1.0, 2.75, rz=math.pi / 2)
    # horloge ronde sur le pilier de droite, extincteur
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=.17, depth=.04, location=(6.4, P/2 - .42, 2.9), rotation=(math.pi/2, 0, 0))
    bpy.context.object.data.materials.append(mat('horloge', (.95, .95, .93), .4))
    cube('extincteur', (6.0, P/2 - .42, 1.4), (.32, .05, .6), mat('vitrine', (.92, .92, .9), .3))
    cube('extincteur_r', (6.0, P/2 - .45, 1.35), (.12, .05, .4), mat('rouge_ext', (.6, .04, .03), .4))
    for x, c in ((-6.3, (.05, .2, .65)), (-6.75, (.05, .05, .05))):   # poubelles bleue / noire
        cube('poubelle', (x, -.5, .3), (.35, .3, .6), mat('poub%.1f' % x, c, .5))

def rayonnages():
    """Étagères en érable pleines de livres : devant les piliers, le long du mur droit et du mur du fond."""
    me = B.rayon_maillage(L=1.0, P=.38, H=1.95, n=6, graine=21, bois=ERABLE, livres=LIVRES)
    def r(loc, rz):
        o = bpy.data.objects.new('etagere', me); o.location = loc; o.rotation_euler.z = math.radians(rz)
        bpy.context.scene.collection.objects.link(o)
    for x in (-2.0, 2.4): r((x, P/2 - .62, 0), 0)                    # « Romances », « Science Fiction »
    for i in range(7): r((L/2 - .22, -4.0 + i * 1.02, 0), -90)         # mur droit (photo 1)
    for i in range(6): r((-1.5 + i * 1.02, -P/2 + .22, 0), 180)        # mur du fond
    for i in range(3): r((-L/2 + .22, 2.3 + i * 1.02, 0), 90)          # mur gauche, côté fenêtres

def table_ronde(x, y, r=.55):
    bois = mat('erable_table', ERABLE, .35); gris = mat('gris_pied', (.45, .46, .48), .3)
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=r, depth=.035, location=(x, y, .735)); bpy.context.object.data.materials.append(bois)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.045, depth=.7, location=(x, y, .37)); bpy.context.object.data.materials.append(gris)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=.28, depth=.03, location=(x, y, .015)); bpy.context.object.data.materials.append(gris)

def table_rect(x, y, lx=1.8, ly=.9):
    bois = mat('erable_table', ERABLE, .35); gris = mat('gris_pied', (.45, .46, .48), .3)
    cube('plateau', (x, y, .735), (lx, ly, .035), bois)
    for sx in (-1, 1):
        for sy in (-1, 1): cube('pied', (x + sx * (lx/2 - .08), y + sy * (ly/2 - .08), .36), (.06, .06, .72), gris)

def poste_bibliothecaire(x=-5.3, y=-3.5):
    """Comptoir en L avec écran d'ordinateur, dans le coin du fond à gauche."""
    bois = mat('comptoir', (.55, .38, .22), .45)
    cube('comptoir', (x, y, .5), (2.2, .6, 1.0), bois); cube('comptoir_cote', (x + 1.1, y - .6, .5), (.6, 1.2, 1.0), bois)
    cube('comptoir_dessus', (x, y, 1.02), (2.3, .7, .04), mat('dessus', (.75, .7, .6), .4))
    cube('ecran_pc', (x - .3, y - .25, 1.3), (.5, .04, .32), mat('ecran_pc', (.05, .08, .12), .3, em=.6, emc=(.5, .65, .9)))

def exterieur(graine=5):
    """La rue vue du 2e étage : chaussée, trottoirs, maisons de SF en face, poteau et fils, colline boisée."""
    rnd = random.Random(graine)
    cube('facade_bas', (0, P/2 + .5, SOL_RUE / 2), (40, .6, -SOL_RUE), mat('facade', (.78, .76, .72), .8))
    cube('trottoir', (0, P/2 + 2.2, SOL_RUE + .08), (60, 3, .16), mat('trottoir', (.6, .59, .57), .8))
    cube('rue', (0, P/2 + 8, SOL_RUE), (80, 9, .1), mat('asphalte', (.16, .16, .17), .7))
    cube('trottoir2', (0, P/2 + 13.5, SOL_RUE + .08), (80, 2.5, .16), mat('trottoir', (.6, .59, .57), .8))
    cube('ligne', (0, P/2 + 8, SOL_RUE + .06), (80, .15, .01), mat('ligne_jaune', (.8, .6, .1), .6))
    pastels = [(.82, .8, .74), (.7, .76, .78), (.86, .78, .62), (.74, .72, .8), (.9, .88, .84), (.62, .7, .66)]
    x = -32
    while x < 32:   # rangée de maisons victoriennes/Marina : façade, oriel, corniche, fenêtres
        w = rnd.uniform(6, 8.5); h = rnd.uniform(7.5, 10.5); y0 = P/2 + 15
        c = mat('maison%d' % int(x), rnd.choice(pastels), .8)
        cube('maison', (x + w/2, y0 + 5, SOL_RUE + h/2), (w - .2, 10, h), c)
        cube('corniche', (x + w/2, y0 - .15, SOL_RUE + h + .15), (w, .5, .3), mat('corniche', (.92, .9, .86), .7))
        cube('oriel', (x + w/2, y0 - .5, SOL_RUE + h * .55), (w * .45, 1, h * .35), c)
        vitre = mat('vitre_maison', (.08, .1, .13), .1)
        for k in range(2):
            for fx in (-.28, .28): cube('fenetre', (x + w/2 + fx * w, y0 - .02, SOL_RUE + 2.5 + k * 3), (1.1, .05, 1.6), vitre)
        cube('toit', (x + w/2, y0 + 5, SOL_RUE + h + .3), (w, 10, .5), mat('toit_maison', (.55, .32, .22), .8))
        x += w
    # poteau électrique en bois + fils qui barrent les fenêtres (photos)
    bois = mat('poteau', (.3, .22, .15), .9); fil = mat('fil', (.03, .03, .03), .6)
    cube('poteau', (3.5, P/2 + 3.4, SOL_RUE + 6), (.28, .28, 12), bois)
    cube('traverse_poteau', (3.5, P/2 + 3.4, SOL_RUE + 11), (2.4, .15, .15), bois)
    for k, (z0, z1) in enumerate([(6.4, 6.0), (6.6, 6.3), (5.6, 5.1), (5.9, 5.6)]):
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=.015, depth=80, location=(0, P/2 + 3.4 + k * .3, (z0 + z1) / 2 - .3), rotation=(0, math.pi/2, 0))
        bpy.context.object.data.materials.append(fil)
    # colline boisée au loin (Glen Canyon)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=1, location=(0, 120, -30)); c = bpy.context.object
    c.scale = (160, 50, 52); c.data.materials.append(mat('colline', (.22, .28, .14), .9))
    verts = [mat('arbre%d' % k, col, .8) for k, col in enumerate([(.1, .2, .07), (.14, .23, .09), (.18, .22, .1)])]
    for k in range(45):
        x = rnd.uniform(-70, 70); y = rnd.uniform(85, 110); z = rnd.uniform(5, 16)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rnd.uniform(3, 6), location=(x, y, z))
        o = bpy.context.object; o.scale.z = 1.4; o.data.materials.append(rnd.choice(verts))
