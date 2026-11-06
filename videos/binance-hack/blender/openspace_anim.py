# Open space Binance, la nuit de la crise : 8 employés en blanc (dont 3 femmes) tapent au clavier, mur d'écrans rouges « BINANCE 14 ».
# Plans : O_large (travelling le long de la rangée) · O_femme (profil d'une employée, gros plan).  Usage : SEUL=O_large python3 openspace_anim.py [--test]
import bpy, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir('/home/claude/true_stories')
from commun import *
from mathutils import Vector as V, Matrix
sc = reset(); sc.cycles.samples = 10; sc.render.resolution_x = 1280; sc.render.resolution_y = 536; sc.render.resolution_percentage = 100
sc.view_settings.look = 'AgX - Punchy'
MUR = mat('mur', (.16, .17, .2), .8); SOL = mat('sol', (.05, .055, .065), .35); NOIR = mat('noir', (.03, .03, .035), .4)
CLAVIER = mat('clavier', (.16, .17, .19), .45); TOUCHE = mat('touche', (.62, .64, .67), .4)
BUREAU = mat('bureau', (.55, .56, .58), .35); BL = mat('perso_blanc', (.85, .86, .88), .55)
ROUGE_E = mat('e_rouge', (.15, 0, 0), .4, (.9, .05, .03), 3.0)
HACK = img_mat('e_hack', '/home/claude/ecrans/ecran_hacker_tex.png', 2.2)
APS = [img_mat(f'e{k}', f'/home/claude/true_stories/videos/binance-hack/code/apercus/{k}.png', 1.8) for k in ('chaines', 'jauges', 'alerte')]
box('sol', (0, 0, -.05), (16, 14, .1), SOL); box('mur_fond', (0, 4.2, 2), (16, .1, 4), MUR); box('mur_g', (-7, 0, 2), (.1, 14, 4), MUR)
box('plafond', (0, 0, 3.6), (16, 14, .1), MUR)
for i in range(4): box(f'neon{i}', (-4.5 + i * 3, 0, 3.52), (2.2, .12, .04), mat(f'neon{i}', (1, 1, 1), .5, (.8, .87, 1), 2.5))
for k, m in enumerate([ROUGE_E, APS[0], HACK, APS[1], ROUGE_E]):           # mur d'écrans
    x = -5 + k * 2.5; box(f'cadre{k}', (x, 4.12, 2.2), (2.3, .06, 1.36), NOIR); dalle(f'ecran{k}', (x, 4.08, 2.2), 2.2, 1.26, m)
bpy.ops.object.text_add(location=(0, 4.04, 2.2), rotation=(math.radians(90), 0, 0)); t = bpy.context.object
t.data.body = 'BINANCE 14'; t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = .34; t.data.materials.append(mat('txt', (1, 1, 1), .5, (1, 1, 1), 4))
PERSOS = ['Typing_1_Ch02_femme.fbx', 'Typing_3_Ch18_homme.fbx', 'Typing_2_Ch26_femme_talons.fbx']
ARMS = []
def poste(x, y, fbx, k):
    dz = -.08 if k == 2 else 0   # bureau un peu plus bas pour l'employée enceinte : mains posées dessus
    box(f'bur{k}', (x, y + .62, .73 + dz), (1.3, .7, .04), BUREAU)
    for dx in (-.6, .6): box(f'pied{k}{dx}', (x + dx, y + .62, .36), (.04, .6, .72), NOIR)
    box(f'mon{k}', (x, y + .9, 1.08), (.62, .03, .38), NOIR); dalle(f'ecr{k}', (x, y + .88, 1.08), .58, .34, [HACK, APS[0], APS[1], APS[2], ROUGE_E][k % 5])
    zc = .755 + dz; box(f'clav{k}', (x, y + .42, zc), (.46, .16, .022), CLAVIER)       # clavier visible : socle gris + touches claires
    for r_ in range(4):
        for c_ in range(12): box(f't{k}_{r_}_{c_}', (x - .2 + c_ * .0365, y + .363 + r_ * .038, zc + .014), (.03, .03, .008), TOUCHE)
    box(f'souris{k}', (x + .32, y + .42, zc), (.06, .1, .03), CLAVIER)
    kit('Wooden Chair', (x, y - .06, 0), 180, .9, NOIR)
    av = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=f'/home/claude/true_stories/assets3d/personnages_animes/{fbx}')
    neufs = [o for o in bpy.data.objects if o not in av]; arm = [o for o in neufs if o.type == 'ARMATURE'][0]
    for o in neufs:
        if o.type == 'MESH':
            o.data.materials.clear(); o.data.materials.append(BL)
            d = o.modifiers.new('lp', 'DECIMATE'); d.decimate_type = 'COLLAPSE'; d.ratio = .05
            o.modifiers.move(len(o.modifiers) - 1, 0)
    emp = bpy.data.objects.new(f'empty{k}', None); sc.collection.objects.link(emp); emp.location = (x, y, 0); emp.rotation_euler.z = math.pi
    arm.parent = emp; ARMS.append((arm, k))
    if k == 2:   # l'employée enceinte : ventre arrondi accroché à l'os du dos
        bpy.context.view_layer.update(); sc.frame_set(30)
        bn = [b.name for b in arm.pose.bones if b.name.endswith('Spine')][0]
        pb = arm.pose.bones[bn]; w = arm.matrix_world @ pb.head
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=w); v = bpy.context.object; v.name = 'ventre'
        v.data.materials.append(BL); bpy.ops.object.shade_smooth()
        v.parent = arm; v.parent_type = 'BONE'; v.parent_bone = bn
        bpy.context.view_layer.update(); v.matrix_world = Matrix.Translation(w + V((0, .2, 0.0))) @ Matrix.Diagonal((.14, .17, .15, 1)); print('VENTRE', tuple(round(c,2) for c in w), bn, flush=True)
for r, y in enumerate((0, -2.3)):
    for c, x in enumerate((-3.6, -1.8, 0, 1.8, 3.6)):
        if r == 1 and c in (0, 4): continue
        poste(x, y, PERSOS[(r * 5 + c) % 3], r * 5 + c)
lum('AREA', (0, 3.4, 2.2), 700, (.6, .7, 1), (math.radians(-90), 0, 0), 9)
lum('AREA', (0, 3.6, 1.6), 250, (1, .1, .06), (math.radians(-90), 0, 0), 8)
lum('AREA', (0, -1, 3.4), 120, (.8, .85, 1), (0, 0, 0), 8)
lum('AREA', (-5, -5, 2.6), 90, (1, .75, .5), (math.radians(65), 0, math.radians(-40)), 3)
cd = bpy.data.cameras.new('c'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam; cd.dof.use_dof = True
E = lambda u: u * u * (3 - 2 * u)
PLANS = {  # durée, (cam0, cam1), (cible0, cible1), focale, f-stop
 'O_large': (5.0, ((-5.6, -4.6, 1.9), (-3.0, -4.2, 1.75)), ((-1.0, .6, 1.0), (.6, .6, 1.0)), 28, 3.5),
 'O_dessus': (4.0, ((-1.5, -1.6, 3.35), (1.0, -1.3, 3.35)), ((-1.2, -.5, .6), (1.0, -.4, .6)), 28, 5.6),
 'O_face': (4.0, ((-1.6, 2.4, 2.25), (.4, 2.4, 2.2)), ((-.8, -.1, 1.0), (.6, -.1, 1.0)), 30, 3.2),
 'O_femme': (4.0, ((1.15, -.15, 1.05), (1.0, .0, 1.0)), ((0, .18, .92), (0, .18, .92)), 30, 2.8),
}
seul = os.environ.get('SEUL'); test = '--test' in sys.argv
for nom, (D, (c0, c1), (t0, t1), lens, fs) in PLANS.items():
    if seul and nom not in seul.split(','): continue
    out = f'/home/claude/anim/{nom}'; os.makedirs(out, exist_ok=True); cd.lens = lens; cd.dof.aperture_fstop = fs
    for f in ([int(D * 8 * .6)] if test else range(int(D * 8))):
        u = E(f / (D * 8)); c = V(c0).lerp(V(c1), u); tg = V(t0).lerp(V(t1), u)
        cam.location = c; cam.rotation_euler = (tg - c).to_track_quat('-Z', 'Y').to_euler(); cd.dof.focus_distance = (tg - c).length
        sc.frame_set(int(30 + f * 2.5))
        if not test and os.path.exists(f'{out}/{f:04d}.png'): continue
        sc.render.filepath = f'/home/claude/anim/{nom}_test.png' if test else f'{out}/{f:04d}.png'
        bpy.ops.render.render(write_still=True); print('IMG', nom, f, flush=True)
