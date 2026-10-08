# Démonstration : la vidéo codée (ecran.mp4) devient l'écran lumineux d'un portable dans Blender.
import bpy, math, os, sys, addon_utils
HERE=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True); addon_utils.enable('cycles',default_set=True)
sc=bpy.context.scene; sc.render.fps=30; sc.frame_start=1; sc.frame_end=180
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Punchy'
def mat(n,c,r=.5):
    m=bpy.data.materials.new(n); b=m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=r; return m
w=bpy.data.worlds.new('w'); sc.world=w; w.node_tree.nodes['Background'].inputs[0].default_value=(.01,.012,.02,1)
# table en bois
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,.74)); t=bpy.context.object; t.scale=(2.4,1.2,.05); t.data.materials.append(mat('bois',(.18,.09,.04),.45))
# portable : base + écran incliné
alu=mat('alu',(.35,.35,.37),.3); alu.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=1
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,.775)); base=bpy.context.object; base.scale=(.34,.23,.018); base.data.materials.append(alu)
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,.112,.78)); lid=bpy.context.object; lid.scale=(.34,.012,.22); lid.data.materials.append(alu)
lid.data.transform(__import__('mathutils').Matrix.Translation((0,0,.5))); lid.rotation_euler=(math.radians(-14),0,0)
# dalle d'écran : texture vidéo en émission
bpy.ops.mesh.primitive_plane_add(size=1); scr=bpy.context.object; scr.scale=(.32,.2,1); scr.rotation_euler=(math.radians(90-14),0,0)
scr.parent=lid; scr.matrix_parent_inverse=lid.matrix_world.inverted(); scr.location=(0,.1045,.78+.11*0+.0)
scr.location=(0,.112-.0065,.78); scr.rotation_euler=(math.radians(90),0,0)
scr.parent=lid; scr.location=(0,-.51,.5); scr.rotation_euler=(math.radians(90),0,0); scr.scale=(.94/1,.9/1,1)
m=bpy.data.materials.new('ecran'); nt=m.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF'])
tex=nt.nodes.new('ShaderNodeTexImage'); img=bpy.data.images.load(os.path.join(HERE,'ecran.mp4')); img.source='MOVIE'; tex.image=img
tex.image_user.frame_duration=180; tex.image_user.use_auto_refresh=True; tex.image_user.use_cyclic=True
em=nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value=2.4
nt.links.new(tex.outputs['Color'],em.inputs['Color']); nt.links.new(em.outputs[0],nt.nodes['Material Output'].inputs['Surface'])
scr.data.materials.append(m)
# rayonnages flous au fond + lampe chaude
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(-2+i*1,2.6,1.2)); s=bpy.context.object; s.scale=(.9,.35,2.4); s.data.materials.append(mat(f'r{i}',(.08,.05,.03),.8))
bpy.ops.object.light_add(type='AREA',location=(1.6,1.4,2.2)); a=bpy.context.object; a.data.energy=120; a.data.color=(1,.7,.45); a.data.size=1; a.rotation_euler=(math.radians(-50),math.radians(35),0)
# caméra : par-dessus l'épaule, mise au point sur l'écran
bpy.ops.object.camera_add(location=(-.35,-.75,1.12)); c=bpy.context.object; sc.camera=c; c.data.lens=45
tc=c.constraints.new('TRACK_TO'); bpy.ops.object.empty_add(location=(0,.1,.92)); tgt=bpy.context.object; tc.target=tgt; tc.track_axis='TRACK_NEGATIVE_Z'; tc.up_axis='UP_Y'
c.data.dof.use_dof=True; c.data.dof.focus_object=tgt; c.data.dof.aperture_fstop=2
c.location=(-.35,-.75,1.12); c.keyframe_insert('location',frame=1); c.location=(-.12,-.45,1.02); c.keyframe_insert('location',frame=180)
sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=1920; sc.render.resolution_y=1080
if 'apercu' in sys.argv:
    sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=24; sc.render.resolution_percentage=40
    sc.frame_set(90); sc.render.filepath=os.path.join(HERE,'apercu_portable.png'); bpy.ops.render.render(write_still=True)
    sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_percentage=100
bpy.ops.file.pack_all() if False else None
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE,'portable_demo.blend'))
print('OK')
