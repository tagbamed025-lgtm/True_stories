# Planche « distribution » : chaque personnage Mixamo au style TRU Stories (principal rouge émissif, autres blanc lumineux)
import bpy, os, sys, math, addon_utils
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(HERE,'../../assets3d/silk-road/personnages')
CAST=[('Ch21.fbx','blanc'),('Ch22.fbx','blanc'),('Ch23.fbx','blanc'),('Ch31.fbx','blanc')]
import sys as _s
ROUGE=[a for a in _s.argv if a.startswith('Ch')]
bpy.ops.wm.read_factory_settings(use_empty=True); addon_utils.enable('cycles',default_set=True)
sc=bpy.context.scene; sc.view_settings.view_transform='Standard'
w=bpy.data.worlds.new('w'); sc.world=w; w.node_tree.nodes['Background'].inputs[0].default_value=(.002,.002,.004,1)
def m_rouge():
    m=bpy.data.materials.new('TRU_rouge'); b=m.node_tree.nodes['Principled BSDF']; c=(.75,.02,.02,1)
    b.inputs['Base Color'].default_value=c; b.inputs['Emission Color'].default_value=c; b.inputs['Emission Strength'].default_value=.45; b.inputs['Roughness'].default_value=.5; return m
def m_blanc():
    m=bpy.data.materials.new('TRU_blanc'); b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(.85,.85,.87,1); b.inputs['Emission Color'].default_value=(1,1,1,1); b.inputs['Emission Strength'].default_value=.12; b.inputs['Roughness'].default_value=.6; return m
for i,(f,coul) in enumerate(CAST):
    bpy.ops.import_scene.fbx(filepath=os.path.join(P,f)); objs=list(bpy.context.selected_objects); m=m_rouge() if (f[:-4] in ROUGE) else m_blanc()
    bpy.ops.object.empty_add(location=((i-1.5)*1.3,0,0)); sup=bpy.context.object
    for o in objs:
        if o.parent is None: o.parent=sup
        if o.type=='MESH': o.data.materials.clear(); o.data.materials.append(m)
bpy.ops.mesh.primitive_plane_add(size=40); fm=bpy.data.materials.new('sol'); fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.015,.015,.02,1); bpy.context.object.data.materials.append(fm)
bpy.ops.object.light_add(type='SPOT',location=(0,-3,5)); s=bpy.context.object; s.data.energy=2500; s.data.spot_size=math.radians(70); s.data.color=(1,.85,.7); s.rotation_euler=(math.radians(32),0,0)
bpy.ops.object.light_add(type='AREA',location=(0,3,3)); a=bpy.context.object; a.data.energy=400; a.data.color=(.4,.5,1); a.data.size=6; a.rotation_euler=(math.radians(-55),0,0)
bpy.ops.object.camera_add(location=(0,-7,1.3),rotation=(math.radians(86),0,0)); sc.camera=bpy.context.object; sc.camera.data.lens=35
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=32; sc.render.resolution_x=1920; sc.render.resolution_y=900; sc.render.resolution_percentage=55
sc.render.filepath=os.path.join(HERE,'distribution.png'); bpy.ops.render.render(write_still=True); print('OK')
