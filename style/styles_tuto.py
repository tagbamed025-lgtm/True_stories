# Les 5 styles du tutoriel « Easy Characters are META », appliqués automatiquement à un personnage Mixamo.
# Usage : python3 styles_tuto.py [perso.fbx]  → planche_styles.png
import bpy, os, sys, math, addon_utils
HERE=os.path.dirname(os.path.abspath(__file__)); args=[a for a in sys.argv if a.endswith('.fbx')]
SRC=args[0] if args else os.path.join(HERE,'../../experiences/swat/swat.fbx')
bpy.ops.wm.read_factory_settings(use_empty=True); addon_utils.enable('cycles',default_set=True)
sc=bpy.context.scene; sc.view_settings.view_transform='AgX'
w=bpy.data.worlds.new('w'); sc.world=w; w.node_tree.nodes['Background'].inputs[0].default_value=(.003,.003,.005,1)

def base_mat(name):
    m=bpy.data.materials.new(name); nt=m.node_tree; return m, nt, nt.nodes['Principled BSDF']
def s1_lowpoly(c=(.05,.15,.9)):   # 1. facettes + couleur unie (Spectacles, Neo)
    m,nt,b=base_mat('S1'); b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=.6; return m,True
def s2_blanc_lumineux():          # 2. blanc émissif (Nexpo)
    m,nt,b=base_mat('S2'); b.inputs['Base Color'].default_value=(1,1,1,1); b.inputs['Emission Color'].default_value=(1,1,1,1); b.inputs['Emission Strength'].default_value=.6; return m,False
def s3_fresnel(c=(.8,.05,.05)):   # 3. contour lumineux Fresnel (miniatures)
    m,nt,b=base_mat('S3'); b.inputs['Base Color'].default_value=(*c,1)
    fr=nt.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value=1.3
    cr=nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position=.35; cr.color_ramp.elements[1].position=.75
    nt.links.new(fr.outputs[0],cr.inputs[0]); nt.links.new(cr.outputs[0],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=2; return m,False
def s4_metal():                   # 4. métal gris (Imperial)
    m,nt,b=base_mat('S4'); b.inputs['Base Color'].default_value=(.45,.45,.47,1); b.inputs['Metallic'].default_value=1; b.inputs['Roughness'].default_value=.35; return m,False
def s5_rouge_emissif(c=(.9,.03,.03)):  # 5. rouge auto-éclairé (LEMMiNO)
    m,nt,b=base_mat('S5'); b.inputs['Base Color'].default_value=(*c,1); b.inputs['Emission Color'].default_value=(*c,1); b.inputs['Emission Strength'].default_value=3; return m,False

STYLES=[('1 · Facettes',s1_lowpoly),('2 · Blanc lumineux',s2_blanc_lumineux),('3 · Contour Fresnel',s3_fresnel),('4 · Métal',s4_metal),('5 · Rouge émissif',s5_rouge_emissif)]
for i,(nom,f) in enumerate(STYLES):
    bpy.ops.import_scene.fbx(filepath=SRC); objs=list(bpy.context.selected_objects); m,lowpoly=f()
    for o in objs:
        if o.type=='ARMATURE': o.location.x=(i-2)*1.6; pass
        if o.type=='MESH':
            o.data.materials.clear(); o.data.materials.append(m)
            if lowpoly:
                d=o.modifiers.new('lowpoly','DECIMATE'); d.ratio=.03; o.modifiers.move(len(o.modifiers)-1,0)
                for p in o.data.polygons: p.use_smooth=False
    bpy.ops.object.text_add(location=((i-2)*1.6,-.75,.02)); t=bpy.context.object; t.data.body=nom; t.data.size=.16; t.data.align_x='CENTER'
    tm=bpy.data.materials.new('t'); tm.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(1,1,1,1); tm.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=2; t.data.materials.append(tm)
bpy.ops.mesh.primitive_plane_add(size=40); fl=bpy.context.object; fm=bpy.data.materials.new('sol'); fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.02,.02,.025,1); fl.data.materials.append(fm)
bpy.ops.object.light_add(type='AREA',location=(0,-4,4)); a=bpy.context.object; a.data.energy=900; a.data.size=6; a.rotation_euler=(math.radians(45),0,0)
bpy.ops.object.light_add(type='AREA',location=(0,3,3)); a=bpy.context.object; a.data.energy=500; a.data.color=(.5,.6,1); a.data.size=6; a.rotation_euler=(math.radians(-50),0,0)
bpy.ops.object.camera_add(location=(0,-9,1.5),rotation=(math.radians(85),0,0)); sc.camera=bpy.context.object; sc.camera.data.lens=32
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=32; sc.render.resolution_x=1920; sc.render.resolution_y=820; sc.render.resolution_percentage=60
sc.render.filepath=os.path.join(HERE,'planche_styles.png'); bpy.ops.render.render(write_still=True); print('OK')
