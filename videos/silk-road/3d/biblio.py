# Décor commun « bibliothèque de Glen Park » pour les plans [3D] de Silk Road.
# Lit le kit d'objets de Mo en lecture seule (jamais modifié) et les persos allégés.
import bpy, math, os, mathutils
DL = r"C:\Users\HP\Downloads\TRU Stories"
KIT = os.environ.get('TRU_KIT', DL + r"\persos\Sans titre_kit_leger.blend")
PERSOS = DL + r"\persos\leger"
ANIMS = DL
FPS = 30

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.fps = FPS
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
    sc.render.engine = 'BLENDER_EEVEE'
    sc.render.resolution_x, sc.render.resolution_y = 1920, 804   # 2,39:1
    sc.render.film_transparent = False
    w = bpy.data.worlds.new('monde'); sc.world = w
    w.node_tree.nodes['Background'].inputs[0].default_value = (.012, .010, .009, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 1
    return sc

def mat(n, c, r=.6, em=0, emc=None):
    m = bpy.data.materials.new(n); b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*c, 1); b.inputs['Roughness'].default_value = r
    if em:
        b.inputs['Emission Color'].default_value = (*(emc or c), 1); b.inputs['Emission Strength'].default_value = em
    return m

def monde(o):
    """Matrice monde calculée à la main (les objets ajoutés hors scène ne sont pas encore évalués)."""
    m = o.matrix_basis
    while o.parent: m = o.parent.matrix_basis @ o.matrix_parent_inverse @ m if False else monde(o.parent) @ o.matrix_parent_inverse @ m; break
    return m

_kit = {}
def objet(nom, loc, rot=0, scale=1):
    """Instance d'une collection du kit (ajoutée une seule fois au fichier)."""
    if nom not in _kit:
        with bpy.data.libraries.load(KIT, link=False) as (src, dst): dst.collections = [nom]
        c = dst.collections[0]; _kit[nom] = c
        pts = [monde(o) @ mathutils.Vector(b) for o in c.all_objects if o.type == 'MESH' for b in o.bound_box]
        if pts:   # recentre : origine = centre au sol de la boîte englobante
            c.instance_offset = (sum(p.x for p in pts)/len(pts), sum(p.y for p in pts)/len(pts), min(p.z for p in pts))
    e = bpy.data.objects.new(nom + '_inst', None); e.instance_type = 'COLLECTION'
    e.instance_collection = _kit[nom]; e.location = loc; e.rotation_euler.z = math.radians(rot)
    e.scale = (scale,) * 3; bpy.context.scene.collection.objects.link(e); return e

def salle(L=28, P=18, H=5.5):
    """Grande salle de lecture aérée : parquet clair, plafond à panneaux lumineux, baie vitrée (côté +Y) sur l'extérieur."""
    bpy.ops.mesh.primitive_plane_add(size=1); s = bpy.context.object; s.scale = (L, P, 1); s.name = 'sol'
    s.data.materials.append(mat('parquet', (.26, .15, .08), .45))
    murs = mat('mur', (.42, .36, .3), .9)
    for x, y, sx, sy in [(0, -P/2, L, .3), (-L/2, 0, .3, P), (L/2, 0, .3, P)]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, H/2)); m = bpy.context.object; m.scale = (sx, sy, H); m.data.materials.append(murs)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, H)); pl = bpy.context.object; pl.scale = (L, P, 1); pl.name = 'plafond'
    pl.rotation_euler.x = math.pi; pl.data.materials.append(mat('plafond', (.35, .3, .26), .9)); pl.visible_shadow = False
    neon = mat('neon', (1, .95, .85), .5, em=6)
    for x in range(-10, 11, 5):
        for y in (-5, 0, 5):
            bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, H - .01)); n = bpy.context.object; n.name = 'neon'
            n.scale = (2.4, .6, 1); n.rotation_euler.x = math.pi; n.data.materials.append(neon); n.visible_shadow = False
    # baie vitrée du sol au plafond : montants fins + traverses, pas de vitre (rien ne bloque la vue)
    cadre = mat('cadre', (.04, .04, .045), .4)
    for i in range(13):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-L/2 + i*L/12, P/2, H/2)); m = bpy.context.object; m.name = 'montant'; m.scale = (.1, .14, H); m.data.materials.append(cadre)
    for z in (.15, H*.72, H - .1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, P/2, z)); m = bpy.context.object; m.name = 'traverse'; m.scale = (L, .14, .08); m.data.materials.append(cadre)
    exterieur(P/2)
    bpy.ops.object.light_add(type='SUN', location=(0, 8, 6)); so = bpy.context.object; so.name = 'soleil'
    so.data.energy = 4; so.data.color = (1, .82, .6); so.data.angle = math.radians(1.5)
    so.rotation_euler = (math.radians(-62), 0, math.radians(205))   # soleil d'après-midi qui entre par la baie
    bpy.ops.object.light_add(type='AREA', location=(0, 0, H - .2)); a = bpy.context.object; a.name = 'ambiance'
    a.data.energy = 1500; a.data.size = 20; a.data.color = (1, .9, .78)
    w = bpy.context.scene.world.node_tree.nodes['Background']
    w.inputs[0].default_value = (.5, .62, .78, 1); w.inputs[1].default_value = .9   # ciel de fin d'après-midi

def exterieur(y0, graine=3):
    """Glen Park : pelouse, eucalyptus et arbres low poly, colline, maisons en bois pastel sur la pente."""
    import random; rnd = random.Random(graine)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y0 + 60, -.02)); g = bpy.context.object; g.name = 'pelouse'
    g.scale = (220, 120, 1); g.data.materials.append(mat('pelouse', (.09, .17, .05), .9))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y0 + 2.5, .05)); t = bpy.context.object; t.scale = (40, 3, .1)
    t.data.materials.append(mat('terrasse', (.35, .33, .3), .8))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1, location=(10, y0 + 120, -40)); c = bpy.context.object; c.name = 'colline'
    c.scale = (140, 60, 62); c.data.materials.append(mat('colline', (.16, .2, .08), .9))
    for p in c.data.polygons: p.use_smooth = False
    verts = [mat('feuillage%d' % k, col, .8) for k, col in enumerate([(.06, .14, .04), (.1, .18, .06), (.13, .17, .07), (.08, .12, .05)])]
    tronc = mat('tronc', (.18, .12, .08), .9)
    for k in range(70):
        x = rnd.uniform(-60, 60); y = y0 + rnd.uniform(5, 55)
        if abs(x) < 16 and y < y0 + 9: continue
        h = rnd.uniform(5, 14); r = rnd.uniform(1.6, 3.5)
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=.2, depth=h*.6, location=(x, y, h*.3)); bpy.context.object.data.materials.append(tronc)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=(x, y, h*.6 + r*.6)); f = bpy.context.object
        f.scale = (1, 1, rnd.uniform(1.1, 1.8)); f.rotation_euler.z = rnd.uniform(0, 6); f.data.materials.append(rnd.choice(verts))
    murs = [mat('maison%d' % k, col, .8) for k, col in enumerate([(.75, .7, .6), (.6, .66, .7), (.8, .62, .5), (.7, .72, .62)])]
    toit = mat('toit', (.2, .17, .16), .8)
    for k in range(26):
        x = rnd.uniform(-70, 70); y = y0 + rnd.uniform(60, 95); z = (y - y0 - 55) * .55
        w_, d, h = rnd.uniform(5, 8), rnd.uniform(6, 9), rnd.uniform(5, 8)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z + h/2)); m = bpy.context.object; m.scale = (w_, d, h); m.data.materials.append(rnd.choice(murs))
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=w_*.75, depth=2.2, location=(x, y, z + h + 1.1)); r_ = bpy.context.object
        r_.rotation_euler.z = math.pi/4; r_.scale.y = d / w_; r_.data.materials.append(toit)

_rayon = None
def rayon_maillage(L=1.2, P=.34, H=2.1, n=5, graine=7):
    """Un rayonnage bois sombre rempli de livres (un seul maillage, 6 matériaux)."""
    import bmesh, random
    rnd = random.Random(graine); bm = bmesh.new()
    def boite(x0, y0, z0, x1, y1, z1, mi):
        r = bmesh.ops.create_cube(bm, size=1)['verts']
        for v in r:
            v.co.x = x0 if v.co.x < 0 else x1; v.co.y = y0 if v.co.y < 0 else y1; v.co.z = z0 if v.co.z < 0 else z1
        for f in {f for v in r for f in v.link_faces}: f.material_index = mi
    e = .03
    for x in (-L/2, L/2 - e): boite(x, -P/2, 0, x + e, P/2, H, 0)          # montants
    boite(-L/2, P/2 - .01, 0, L/2, P/2, H, 0)                              # fond
    for k in range(n + 1):
        z = .08 + k * (H - .1) / n
        if k == n: break                                                   # pas de plateau : livres visibles d'en haut
        boite(-L/2, -P/2, z - e, L/2, P/2, z, 0)
        x = -L/2 + e; hmax = (H - .1) / n - .05
        while x < L/2 - e - .05:
            w = rnd.uniform(.025, .055); h = rnd.uniform(.6, .95) * hmax
            if rnd.random() < .08: x += w; continue                        # trou
            boite(x, -P/2 + .03 + rnd.uniform(0, .04), z, min(x + w, L/2 - e), P/2 - .02, z + h, 1 + rnd.randrange(5))
            x += w + .002
    me = bpy.data.meshes.new('rayon'); bm.to_mesh(me); bm.free()
    for c in [(.16, .09, .05), (.25, .05, .04), (.06, .1, .16), (.32, .27, .18), (.08, .13, .08), (.5, .45, .38)]:
        me.materials.append(mat('livre%d' % len(me.materials), c, .7))
    return me

def rayon(loc, rot=0):
    global _rayon
    if _rayon is None: _rayon = rayon_maillage()
    o = bpy.data.objects.new('rayon', _rayon); o.location = loc; o.rotation_euler.z = math.radians(rot)
    bpy.context.scene.collection.objects.link(o); return o

_rayon_bas = None
def rayon_bas(loc, rot=0):
    global _rayon_bas
    if _rayon_bas is None: _rayon_bas = rayon_maillage(H=1.35, n=3, graine=11)
    o = bpy.data.objects.new('rayon_bas', _rayon_bas); o.location = loc; o.rotation_euler.z = math.radians(rot)
    bpy.context.scene.collection.objects.link(o); return o

def rayonnages(L=28, P=18):
    """Livres au mur du fond seulement + îlots bas sur les côtés : la salle reste ouverte vers la baie."""
    for i in range(-10, 11):
        if abs(i) in (0, 1): continue                     # passage central vers l'entrée
        rayon((i * 1.2, -P/2 + .35, 0), 180)
    for x in (-11.5, 11.5):
        for j in range(4):
            rayon_bas((x - .18, -6 + j * 1.2, 0), 90); rayon_bas((x + .18, -6 + j * 1.2, 0), -90)

# --- personnages ----------------------------------------------------------
ROUGE = None; BLANC = None
def styles():
    global ROUGE, BLANC
    ROUGE = mat('TRU_rouge', (.75, .03, .04), .45, em=2.5, emc=(1, .05, .05))
    BLANC = mat('TRU_blanc', (.8, .8, .82), .6, em=.35, emc=(1, 1, 1))

_anims = {}; VITESSE = {}
def courbes(act):
    try: return list(act.fcurves)
    except AttributeError:   # Blender 5 : actions en couches
        return [fc for L in act.layers for st in L.strips for cb in st.channelbags for fc in cb.fcurves]

def anim(nom, sur_place=False):
    """Action Mixamo. sur_place=True : on fige l'avancée des hanches (l'Empty fera le déplacement) et on note la vitesse (m/s)."""
    cle = (nom, sur_place)
    if cle not in _anims:
        avant = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=os.path.join(ANIMS, nom + '.fbx'))
        nv = set(bpy.data.objects) - avant
        arm = [o for o in nv if o.type == 'ARMATURE'][0]; act = arm.animation_data.action
        act.name = 'anim_' + nom + ('_place' if sur_place else ''); act.use_fake_user = True
        if sur_place:
            fcs = [fc for fc in courbes(act) if fc.data_path.endswith('Hips"].location')]
            net = lambda fc: abs(fc.keyframe_points[-1].co[1] - fc.keyframe_points[0].co[1])
            fc = max(fcs, key=net); d = net(fc)
            for k in fc.keyframe_points: k.co[1] = fc.keyframe_points[0].co[1]; k.handle_left[1] = k.handle_right[1] = k.co[1]
            duree = (act.frame_range[1] - act.frame_range[0]) / 60
            VITESSE[nom] = d * .01 / duree
        for o in nv: bpy.data.objects.remove(o, do_unlink=True)
        _anims[cle] = act
    return _anims[cle]

def ecran_portable(chemin):
    """Remplace le fond d'écran du MacBook du kit par la vidéo codée (émissive, en boucle)."""
    m = bpy.data.materials.get('MB_desktop')
    if not m: return
    nt = m.node_tree; tex = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
    img = bpy.data.images.load(chemin); img.source = 'MOVIE'; tex.image = img
    tex.image_user.frame_duration = 180; tex.image_user.use_cyclic = True; tex.image_user.use_auto_refresh = True
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1.6
    nt.links.new(tex.outputs['Color'], em.inputs['Color'])
    nt.links.new(em.outputs[0], [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0].inputs['Surface'])

def perso(fichier, couleur, loc, yaw=0, actions=(), ratio=.03):
    """actions : liste de (nom_anim, frame_debut, frame_offset_dans_anim). Persos parentés à un Empty."""
    avant = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=os.path.join(PERSOS, fichier))
    nv = set(bpy.data.objects) - avant
    arm = [o for o in nv if o.type == 'ARMATURE'][0]
    for b in arm.data.bones:           # mixamorig9:Hips → mixamorig:Hips (groupes de sommets suivent)
        if ':' in b.name: b.name = 'mixamorig:' + b.name.split(':', 1)[1]
    for o in nv:
        if o.type != 'MESH': continue
        if 'Eyelash' in o.name: bpy.data.objects.remove(o, do_unlink=True); continue
        o.data.materials.clear(); o.data.materials.append(couleur)
        d = o.modifiers.new('lowpoly', 'DECIMATE'); d.decimate_type = 'COLLAPSE'; d.ratio = ratio
        o.modifiers.move(len(o.modifiers) - 1, 0)
        for p in o.data.polygons: p.use_smooth = False
    e = bpy.data.objects.new('E_' + fichier[:4], None); bpy.context.scene.collection.objects.link(e)
    e.location = loc; e.rotation_euler.z = math.radians(yaw); arm.parent = e
    arm.animation_data_create(); arm.animation_data.action = None
    for k, (nom, debut, off, *opt) in enumerate(actions):   # une piste NLA par action : la suivante se fond par-dessus
        place = nom.endswith('*'); nom = nom.rstrip('*')            # « Walking* » = marche sur place
        a = anim(nom, place); tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new(nom, int(debut), a)
        st.action_frame_start = a.frame_range[0] + off
        if len(opt) > 1: st.action_frame_end = st.action_frame_start + opt[1]   # pose figée (ex. image 1)
        st.scale = .5; st.extrapolation = 'HOLD' if k == 0 else 'HOLD_FORWARD'  # Mixamo 60 i/s → 30 i/s
        st.blend_in = opt[0] if opt else 0
        if place: st.repeat = 30
    return e, arm

def camera(loc, cible, lens=35, fstop=None):
    bpy.ops.object.camera_add(location=loc); c = bpy.context.object; bpy.context.scene.camera = c; c.data.lens = lens
    bpy.ops.object.empty_add(location=cible); t = bpy.context.object; t.name = 'cible'
    k = c.constraints.new('TRACK_TO'); k.target = t; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    if fstop: c.data.dof.use_dof = True; c.data.dof.focus_object = t; c.data.dof.aperture_fstop = fstop
    return c, t

def apercu(sc, oui=True):
    """Version de validation : 1280×536, moins d'échantillons (≈ 2× plus rapide)."""
    sc.render.resolution_percentage = 67 if oui else 100
    sc.eevee.taa_render_samples = 24 if oui else 64

def sortie(sc, dossier, n_frames):
    sc.frame_start, sc.frame_end = 1, n_frames
    sc.render.filepath = os.path.join(dossier, '')
    sc.render.image_settings.file_format = 'PNG'
    sc.render.use_overwrite = False; sc.render.use_placeholder = True   # rendu reprenable
