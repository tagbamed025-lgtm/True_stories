# « Un matin ordinaire. Un café. Tu ouvres ton ordinateur. » — bureau à l'aube, portable qui s'ouvre, tasse fumante, écran qui s'allume.
import bpy, math, os, sys
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
def M(n, c, metal=0, rug=.5, em=None, f=0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*c, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rug
    if em: b.inputs['Emission Color'].default_value = (*em, 1); b.inputs['Emission Strength'].default_value = f
    return m
BOIS = M('bois', (.09, .055, .035), 0, .45); ALU = M('alu', (.6, .62, .65), 1, .3); NOIR = M('noir', (.01, .01, .012), .2, .3)
CERAM = M('ceram', (.85, .86, .88), 0, .25); CAFE = M('cafe', (.05, .025, .01), 0, .1); MUR = M('mur', (.05, .055, .065), 0, .9)
ECRAN = M('ecran', (0, 0, 0), 0, .2, (.55, .7, 1), 0)
def add(o, m): o.data.materials.append(m); return o
def box(s, p, m, r=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=p, rotation=r); o = bpy.context.object; o.scale = [x / 2 for x in s]
    b = o.modifiers.new('b', 'BEVEL'); b.width = min(s) * .25; b.segments = 3; return add(o, m)
box((3, 1.6, .06), (0, 0, .73), BOIS)
box((6, .1, 4), (0, 1.2, 2), MUR)
box((.36, .25, .012), (0, 0, .767), ALU)                               # base du portable
box((.32, .12, .002), (0, -.03, .774), NOIR)                           # clavier
piv = bpy.data.objects.new('ch', None); sc.collection.objects.link(piv); piv.location = (0, .125, .773)
lid = box((.36, .012, .25), (0, .125, .773 + .125), ALU); lid.parent = piv; lid.matrix_parent_inverse = piv.matrix_world.inverted()
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, .118, .773 + .125), rotation=(math.pi / 2, 0, 0)); e = bpy.context.object; e.scale = (.33, .23, 1)
add(e, ECRAN); e.parent = piv; e.matrix_parent_inverse = piv.matrix_world.inverted()
bpy.ops.mesh.primitive_cylinder_add(radius=.045, depth=.1, location=(.32, -.05, .81), vertices=48); add(bpy.context.object, CERAM)
bpy.ops.mesh.primitive_cylinder_add(radius=.04, depth=.002, location=(.32, -.05, .85), vertices=48); add(bpy.context.object, CAFE)
bpy.ops.mesh.primitive_torus_add(major_radius=.028, minor_radius=.008, location=(.37, -.05, .81), rotation=(math.pi / 2, 0, 0)); add(bpy.context.object, CERAM)
# vapeur : volume léger
bpy.ops.mesh.primitive_cylinder_add(radius=.03, depth=.22, location=(.32, -.05, .97)); v = bpy.context.object
vm = bpy.data.materials.new('vap'); vm.use_nodes = True; nt = vm.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF'])
pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = .25
nt.links.new(pv.outputs[0], nt.nodes['Material Output'].inputs['Volume']); v.data.materials.append(vm)
box((.02, .9, .02), (-1.0, 1.1, 1.6), M('cadre', (.02, .02, .02)))
s = bpy.data.lights.new('aube', 'AREA'); s.energy = 120; s.color = (1, .72, .45); s.size = 1.2
o = bpy.data.objects.new('aube', s); sc.collection.objects.link(o); o.location = (-1.6, .6, 1.5); o.rotation_euler = (Vector((0, 0, .8)) - o.location).to_track_quat('-Z', 'Y').to_euler()
f = bpy.data.lights.new('fill', 'AREA'); f.energy = 25; f.color = (.6, .7, 1); f.size = 2
o = bpy.data.objects.new('fill', f); sc.collection.objects.link(o); o.location = (1.5, -1.5, 1.6); o.rotation_euler = (Vector((0, 0, .8)) - o.location).to_track_quat('-Z', 'Y').to_euler()
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (.004, .004, .006, 1)
cd = bpy.data.cameras.new('c'); cd.lens = 50; cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 12; sc.cycles.use_denoising = True
sc.render.resolution_x = 1280; sc.render.resolution_y = 536
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'
E = lambda u: u * u * (3 - 2 * u)
D, FPS = 5.0, 8; OUT = '/home/claude/anim/W_matin'; os.makedirs(OUT, exist_ok=True); test = '--test' in sys.argv
for fr in ([30] if test else range(int(D * FPS))):
    t = fr / FPS; u = E(min(1, t / D))
    piv.rotation_euler = (-math.pi / 2 * (1 - E(min(1, max(0, (t - .6) / 2.2)))) * 0.98 + math.radians(-12) * E(min(1, max(0, (t - .6) / 2.2))), 0, 0)
    ECRAN.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 2.5 * E(min(1, max(0, (t - 2.6) / .8)))
    c = Vector((.8, -1.35, 1.15)).lerp(Vector((.55, -.95, 1.03)), u); cam.location = c
    tg = Vector((.12, .02, .9)); cam.rotation_euler = (tg - c).to_track_quat('-Z', 'Y').to_euler(); cd.dof.focus_distance = (tg - c).length
    sc.render.filepath = '/home/claude/anim/W_matin_test.png' if test else f'{OUT}/{fr:04d}.png'
    bpy.ops.render.render(write_still=True); print('IMG', fr, flush=True)
