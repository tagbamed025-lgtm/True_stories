# Style d'identité TRU Stories : un personnage Mixamo réaliste devient un mannequin « low poly » à facettes, d'une seule couleur.
# Usage : python3 style_lowpoly.py perso.fbx [anim.fbx]  → apercu_style.png (+ style_demo.blend)
import bpy, sys, os, math, addon_utils
HERE=os.path.dirname(os.path.abspath(__file__)); args=[a for a in sys.argv if a.endswith('.fbx')]
bpy.ops.wm.read_factory_settings(use_empty=True); addon_utils.enable('cycles',default_set=True)
sc=bpy.context.scene; sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - High Contrast'
w=bpy.data.worlds.new('w'); sc.world=w; w.node_tree.nodes['Background'].inputs[0].default_value=(.004,.005,.008,1)
def mat(n,c,r=.55):
    m=bpy.data.materials.new(n); b=m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=r; return m
ROUGE=mat('TRU_rouge',(.75,.04,.05),.45); BLANC=mat('TRU_blanc',(.78,.78,.8),.6)
def stylise(objs, m, ratio=.035):
    for o in objs:
        if o.type!='MESH': continue
        o.data.materials.clear(); o.data.materials.append(m)
        d=o.modifiers.new('lowpoly','DECIMATE'); d.decimate_type='COLLAPSE'; d.ratio=ratio   # facettes
        for p in o.data.polygons: p.use_smooth=False                                          # ombrage plat
        o.modifiers.move(len(o.modifiers)-1,0)   # décimer AVANT le squelette pour que l'animation reste propre
def importe(path,x,m):
    bpy.ops.import_scene.fbx(filepath=path); objs=list(bpy.context.selected_objects)
    for o in objs:
        if o.type=='ARMATURE': o.location.x=x
    stylise(objs,m); return objs
src=args[0] if args else os.path.join(HERE,'../../experiences/swat/swat.fbx')
importe(src,-.7,ROUGE); importe(src,.7,BLANC)
bpy.ops.mesh.primitive_plane_add(size=30); bpy.context.object.data.materials.append(mat('sol',(.03,.03,.035),.8))
bpy.ops.object.light_add(type='SPOT',location=(-2,3,5)); s=bpy.context.object; s.data.energy=2500; s.data.spot_size=math.radians(45); s.data.color=(1,.85,.7); s.rotation_euler=(math.radians(35),0,math.radians(-145))
bpy.ops.object.light_add(type='AREA',location=(3,-1,2.5)); a=bpy.context.object; a.data.energy=400; a.data.color=(.4,.55,1); a.data.size=2; a.rotation_euler=(math.radians(70),0,math.radians(75))
bpy.ops.object.camera_add(location=(0,-5.2,1.3),rotation=(math.radians(86),0,0)); sc.camera=bpy.context.object; sc.camera.data.lens=42
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=32; sc.render.resolution_x=1600; sc.render.resolution_y=900; sc.render.resolution_percentage=60
sc.render.filepath=os.path.join(HERE,'apercu_style.png'); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE,'style_demo.blend')); print('OK')
