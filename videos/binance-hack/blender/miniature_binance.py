# Miniatures YouTube Binance (charte TRU Stories) : diorama 3D dans un puits de lumière sur fond noir,
# le pirate en rouge, les autres en blanc, la situation lisible en 1 s. Étiquettes ajoutées ensuite (etiquettes_miniature.py).
# Usage : blender -b -P miniature_binance.py -- A|B [test]
import bpy, bmesh, math, os, sys, json, random
from bpy_extras.object_utils import world_to_camera_view
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir('/home/claude/true_stories')
from commun import *
from mathutils import Vector as V
args = sys.argv[sys.argv.index('--') + 1:]; VAR = args[0]; TEST = 'test' in args
OUT = '/home/claude/true_stories/videos/binance-hack/livrables/miniatures/3d'; os.makedirs(OUT, exist_ok=True)
sc = reset(); K4 = '4k' in args; sc.render.resolution_x, sc.render.resolution_y = (3840, 2160) if K4 else (1920, 1080); sc.render.resolution_percentage = 50 if TEST else 100
sc.cycles.samples = 24 if TEST else (64 if K4 else 96); sc.view_settings.look = 'AgX - Punchy'
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0, 0, 0, 1)
random.seed(4)
SOL = mat('sol', (.62, .63, .66), .7); BL = mat('perso_blanc', (.85, .86, .88), .55)
COUL = os.environ.get('COUL', 'rouge')
RG = {'rouge': mat('pirate', (.7, .02, .02), .45, (1, .03, .02), .25), 'bleu': mat('pirate', (0, .1, .85), .45, (0, .35, 1), .9),
      'blanc': mat('pirate', (.95, .96, 1), .45, (.9, .95, 1), .15)}[COUL]
OR = mat('or', (1, .68, .08), .3); OR.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1
OR_E = mat('or_logo', (1, .7, .05), .3, (1, .6, .02), 2.2)
ACIER = mat('acier', (.6, .62, .66), .3); ACIER.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1
MUR = mat('mur', (.55, .56, .6), .7); NOIR = mat('noir', (.03, .03, .035), .4)
ECRAN = img_mat('ecran', '/home/claude/true_stories/videos/binance-hack/livrables/miniatures/3d/ecran_mini.png', 2.5) if VAR in 'CD' else mat('ecran', (.1, .3, 1), .3, (.3, .55, 1), 6); ROUGE_E = mat('rouge_e', (.3, 0, 0), .4, (1, .06, .03), 2.5)
box('sol', (0, 0, -.05), (60, 60, .1), SOL)

def logo(pos, taille, rot=(math.radians(90), 0, 0), m=OR_E, epaisseur=.12, coupe=False):
    P = [[(38.5,53),(24.2,38.7),(63,0),(101.8,38.7),(87.5,53),(63,28.5)], [(38.5,73),(63,97.5),(87.5,73),(101.8,87.2),(63,126),(24.2,87.3)],
         [(0,63),(14.3,77.3),(28.6,63),(14.3,48.7)], [(97.4,63),(111.7,77.3),(126,63),(111.7,48.7)], [(48.5,63),(63,77.5),(77.5,63),(63,48.5)]]
    objs = []
    for k, poly in enumerate(P):
        me = bpy.data.meshes.new('logo'); bm = bmesh.new()
        vs = [bm.verts.new(((x - 63) / 126 * taille, (63 - y) / 126 * taille, 0)) for x, y in poly]
        bm.faces.new(vs); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(f'logo{k}', me); sc.collection.objects.link(o); o.data.materials.append(m)
        s = o.modifiers.new('s', 'SOLIDIFY'); s.thickness = epaisseur; s.offset = 0
        b = o.modifiers.new('b', 'BEVEL'); b.width = epaisseur * .15; b.segments = 2
        o.location = pos; o.rotation_euler = rot; objs.append(o)
    return objs

def pieces(cx, cy, n, r, h=.0):
    for i in range(n):
        a = random.uniform(0, 2 * math.pi); d = abs(random.gauss(0, r))
        bpy.ops.mesh.primitive_cylinder_add(radius=.11, depth=.025, vertices=24, location=(cx + math.cos(a) * d, cy + math.sin(a) * d, .013 + h + random.random() * .05),
                                            rotation=(random.uniform(-.4, .4), random.uniform(-.4, .4), 0))
        bpy.context.object.data.materials.append(OR)
    for i in range(n // 8):   # piles
        x, y = cx + random.gauss(0, r * .6), cy + random.gauss(0, r * .6)
        for k in range(random.randint(3, 9)):
            bpy.ops.mesh.primitive_cylinder_add(radius=.11, depth=.025, vertices=24, location=(x + random.gauss(0, .01), y + random.gauss(0, .01), .013 + k * .027))
            bpy.context.object.data.materials.append(OR)

def poste_pirate(x, y, rz):
    """pirate rouge assis devant un ordinateur portable allumé (bleu), sur une petite table ronde"""
    tab = bpy.data.objects.new('poste', None); sc.collection.objects.link(tab)
    bpy.ops.mesh.primitive_cylinder_add(radius=.55, depth=.04, location=(0, .55, .74), vertices=64); t = bpy.context.object; t.data.materials.append(BL); t.parent = tab
    bpy.ops.mesh.primitive_cylinder_add(radius=.04, depth=.72, location=(0, .55, .37)); p = bpy.context.object; p.data.materials.append(BL); p.parent = tab
    b = box('clav', (0, .45, .77), (.42, .3, .02), NOIR); b.parent = tab
    e = dalle('ecr', (0, .615, .93), .42, .28, ECRAN, 0); e.rotation_euler.x = math.radians(90 - 12); e.parent = tab
    box('dos_ecr', (0, .635, .93), (.45, .02, .31), NOIR, (math.radians(-12), 0, 0)).parent = tab
    pr = perso('ross_assis_tape.glb', (0, .0, 0), 180, RG); pr.parent = tab
    tab.location = (x, y, 0); tab.rotation_euler.z = math.radians(rz)
    lum('AREA', (x, y + .2, 1.1), 40, (.4, .6, 1), (math.radians(-70), 0, math.radians(rz)), .4)
    return V((x, y, 2.05))

ETIQ = []
if VAR in 'ACD':   # le coffre de Binance grand ouvert, l'or qui en sort, le pirate devant son PC
    box('mur', (0, 3.2, 2.2), (8, .8, 4.4), MUR)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.45, depth=2, location=(0, 3.2, 1.6), rotation=(math.pi / 2, 0, 0), vertices=96)
    tr = bpy.context.object; bo = sc.objects['mur'].modifiers.new('t', 'BOOLEAN'); bo.object = tr; bo.operation = 'DIFFERENCE'; tr.hide_render = True
    bpy.ops.mesh.primitive_torus_add(major_radius=1.52, minor_radius=.12, location=(0, 2.78, 1.6), rotation=(math.pi / 2, 0, 0), major_segments=96)
    bpy.context.object.data.materials.append(ACIER)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.45, depth=.45, location=(-1.25, 1.6, 1.6), rotation=(math.pi / 2, 0, math.radians(-75)), vertices=96)
    bpy.context.object.data.materials.append(ACIER)            # porte ouverte
    for i in range(8):
        a = i / 8 * 2 * math.pi
        bpy.ops.mesh.primitive_cylinder_add(radius=.07, depth=.5, location=(-1.25 + math.cos(a) * 1.25 * math.cos(math.radians(15)), 1.6 + math.cos(a) * 1.25 * math.sin(math.radians(-15)) * -1, 1.6 + math.sin(a) * 1.25),
                                            rotation=(math.pi / 2, 0, math.radians(-75))); bpy.context.object.data.materials.append(NOIR)
    box('fond_coffre', (0, 4.5, 1.6), (3, .1, 3), ROUGE_E)
    lum('POINT', (0, 3.8, 1.6), 120, (1, .12, .05)); logo((0, 4.38, 1.65), 1.7); lum('POINT', (0, 2.4, .5), 150, (1, .3, .1))
    logo((0, 2.75, 3.6), 1.05)
    pieces(0, 2.3, 260, .9); pieces(.4, 1.2, 90, .5)
    tete = poste_pirate(.9, -.4, 200)
    for f, p, rz in (('agent_debout_veste.glb', (-2.4, .4, 0), 60), ('agente_debout.glb', (2.9, 1.3, 0), 230), ('agent_debout_2.glb', (-1.9, -1.6, 0), 30)):
        perso(f, p, rz, BL)
    ETIQ = [('6,3 MILLIARDS $', 'rouge', tete), ('BINANCE', 'noir', V((0, 2.75, 4.35)))]
    lum('SPOT', (0, .3, 9), 4500 if VAR in 'CD' else 9000, (.92, .95, 1), (0, 0, 0)).data.spot_size = math.radians(58)
    cam = ((3.6, -6.2, 4.6), (.1, 1.2, 1.3), 30)
    if VAR == 'C': cam = ((1.45, -2.3, 1.28), (.93, -.42, 1.15), 45)        # face au pirate, le coffre ouvert derrière lui
    if VAR == 'D': cam = ((.42, .5, 1.9), (1.1, -.95, .95), 32)          # par-dessus l'épaule : l'écran du retrait
    if VAR in 'CD': lum('AREA', (1.5, -1.6, 1.4), 25, (1, .25, .15) if COUL == 'rouge' else (.6, .75, 1), (math.radians(80), 0, math.radians(30)), .6)
else:            # le logo géant de Binance fendu en deux, le pirate seul devant son PC, les employés figés qui regardent
    g = logo((-.32, 2.6, 2.3), 3.6, (math.radians(90), 0, math.radians(-4)), OR_E, .35)
    d = logo((.32, 2.6, 2.3), 3.6, (math.radians(90), 0, math.radians(5)), OR_E, .35)
    for o in g + d:   # chaque moitié ne garde que son côté (fissure verticale)
        bo = o.modifiers.new('c', 'BOOLEAN'); bo.operation = 'DIFFERENCE'
        bpy.ops.mesh.primitive_cube_add(location=(o.location.x + (1.5 if o in g else -1.5) - .02 * (1 if o in g else -1), 2.6, 2.3)); c = bpy.context.object
        c.scale = (1.5, 1, 3); c.rotation_euler.y = math.radians(8); c.hide_render = True; c.hide_viewport = True; bo.object = c
    lum('POINT', (0, 2.0, 2.3), 500, (1, .1, .04))            # lueur rouge dans la fissure
    pieces(0, 1.4, 320, 1.1)
    tete = poste_pirate(.3, -1.0, 180)
    for f, p, rz in (('agent_debout_veste.glb', (-2.2, -.2, 0), 25), ('agente_debout.glb', (2.4, .1, 0), 335), ('agent_debout_2.glb', (-1.2, 1.0, 0), 10)):
        perso(f, p, rz, BL)
    ETIQ = [('CORÉE DU NORD ?', 'noir', tete), ('20 MINUTES', 'rouge', V((0, 2.6, 4.5)))]
    lum('SPOT', (0, .2, 9), 9000, (.92, .95, 1), (0, 0, 0)).data.spot_size = math.radians(60)
    cam = ((2.6, -6.6, 3.2), (0, 1.0, 1.7), 30)
lum('AREA', (-4, -5, 4), 120, (.7, .8, 1), (math.radians(55), 0, math.radians(-40)), 4)
loc, tgt, lens = cam
bpy.ops.object.camera_add(location=loc); c = bpy.context.object; c.data.lens = lens
c.rotation_euler = (V(tgt) - V(loc)).to_track_quat('-Z', 'Y').to_euler(); c.data.dof.use_dof = True
c.data.dof.focus_distance = (V(tgt) - V(loc)).length; c.data.dof.aperture_fstop = 2.2 if VAR in 'CD' else 6; sc.camera = c
bpy.context.view_layer.update()
pos = [[t, coul, round(world_to_camera_view(sc, c, p).x, 4), round(1 - world_to_camera_view(sc, c, p).y, 4)] for t, coul, p in ETIQ]
json.dump(pos, open(f'{OUT}/etiquettes_{VAR}.json', 'w'), ensure_ascii=False)
sc.render.filepath = f'{OUT}/mini_{VAR}{"_" + COUL if COUL != "rouge" else ""}{"_4k" if K4 else ""}{"_test" if TEST else ""}.png'; bpy.ops.render.render(write_still=True); print('OK', VAR, flush=True)
