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

def salle(L=14, P=10, H=4.2):
    """Sol en parquet sombre, murs, baie vitrée côté +Y, soleil d'après-midi."""
    bpy.ops.mesh.primitive_plane_add(size=1); s = bpy.context.object; s.scale = (L, P, 1); s.name = 'sol'
    s.data.materials.append(mat('parquet', (.10, .055, .03), .5))
    murs = mat('mur', (.16, .13, .11), .9)
    for x, y, sx, sy in [(0, -P/2, L, .2), (-L/2, 0, .2, P), (L/2, 0, .2, P)]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, H/2)); m = bpy.context.object; m.scale = (sx, sy, H); m.data.materials.append(murs)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, H)); pl = bpy.context.object; pl.scale = (L, P, 1); pl.name = 'plafond'
    pl.rotation_euler.x = math.pi; pl.data.materials.append(mat('plafond', (.05, .04, .035), .9))
    pl.visible_shadow = False   # le soleil et la lumière zénithale passent toujours
    # baie vitrée : montants sombres + soleil qui entre
    for i in range(8):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-L/2 + i*L/7, P/2, H/2)); m = bpy.context.object; m.scale = (.12, .12, H); m.data.materials.append(mat('montant', (.02, .02, .02)))
    bpy.ops.object.light_add(type='SUN', location=(0, 8, 6)); so = bpy.context.object; so.name = 'soleil'
    so.data.energy = 4.5; so.data.color = (1, .78, .55); so.data.angle = math.radians(2)
    so.rotation_euler = (math.radians(-58), 0, math.radians(200))
    bpy.ops.object.light_add(type='AREA', location=(0, 0, H - .1)); a = bpy.context.object; a.name = 'plafond'
    a.data.energy = 700; a.data.size = 9; a.data.color = (1, .85, .7)

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

def rayonnages():
    """Deux murs de livres (haut/bas) et deux épis sur les côtés."""
    for i in range(-6, 7):
        rayon((i * 1.2, -2.3, 0), 180)
        rayon((i * 1.2, 2.45, 0), 0)
    for j in range(-1, 2):
        rayon((-5.3, j * 1.2, 0), 90); rayon((5.3, j * 1.2, 0), -90)

# --- personnages ----------------------------------------------------------
ROUGE = None; BLANC = None
def styles():
    global ROUGE, BLANC
    ROUGE = mat('TRU_rouge', (.75, .03, .04), .45, em=2.5, emc=(1, .05, .05))
    BLANC = mat('TRU_blanc', (.8, .8, .82), .6, em=.35, emc=(1, 1, 1))

_anims = {}
def anim(nom):
    if nom not in _anims:
        avant = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=os.path.join(ANIMS, nom + '.fbx'))
        nv = set(bpy.data.objects) - avant
        arm = [o for o in nv if o.type == 'ARMATURE'][0]; act = arm.animation_data.action
        act.name = 'anim_' + nom; act.use_fake_user = True
        for o in nv: bpy.data.objects.remove(o, do_unlink=True)
        _anims[nom] = act
    return _anims[nom]

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
        a = anim(nom); tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new(nom, int(debut), a)
        st.action_frame_start = a.frame_range[0] + off
        if len(opt) > 1: st.action_frame_end = st.action_frame_start + opt[1]   # pose figée (ex. image 1)
        st.scale = .5; st.extrapolation = 'HOLD' if k == 0 else 'HOLD_FORWARD'  # Mixamo 60 i/s → 30 i/s
        st.blend_in = opt[0] if opt else 0
    return e, arm

def camera(loc, cible, lens=35, fstop=None):
    bpy.ops.object.camera_add(location=loc); c = bpy.context.object; bpy.context.scene.camera = c; c.data.lens = lens
    bpy.ops.object.empty_add(location=cible); t = bpy.context.object; t.name = 'cible'
    k = c.constraints.new('TRACK_TO'); k.target = t; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    if fstop: c.data.dof.use_dof = True; c.data.dof.focus_object = t; c.data.dof.aperture_fstop = fstop
    return c, t

def sortie(sc, dossier, n_frames):
    sc.frame_start, sc.frame_end = 1, n_frames
    sc.render.filepath = os.path.join(dossier, '')
    sc.render.image_settings.file_format = 'PNG'
    sc.render.use_overwrite = False; sc.render.use_placeholder = True   # rendu reprenable
