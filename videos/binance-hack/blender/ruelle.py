import bpy, math
from mathutils import Vector as V
bpy.ops.wm.open_mainfile(filepath='assets3d/decors/ruelle.blend')
sc=bpy.context.scene
# 1. retirer le soldat (squelette + corps + tête) et l'ancienne voiture en blocs
for n in ('Coureur','Soldier_body','Soldier_head','voiture_bas','voiture_haut','feux','Cylinder','Cylinder.001','Cylinder.002','Cylinder.003'):
    o=bpy.data.objects.get(n)
    if o: bpy.data.objects.remove(o,do_unlink=True)
def nodes(m): m.use_nodes=True; return m.node_tree.nodes, m.node_tree.links, m.node_tree.nodes['Principled BSDF']
def coord(nt,ln,scale):
    tc=nt.new('ShaderNodeTexCoord'); mp=nt.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=scale
    ln.new(tc.outputs['Object'],mp.inputs[0]); return mp.outputs[0]
# 2. textures procédurales (aucune image)
def brique(m):
    nt,ln,b=nodes(m); br=nt.new('ShaderNodeTexBrick'); ln.new(coord(nt,ln,(1.6,1.6,1.6)),br.inputs[0])
    br.inputs['Color1'].default_value=(.20,.11,.08,1); br.inputs['Color2'].default_value=(.14,.08,.06,1); br.inputs['Mortar'].default_value=(.09,.09,.09,1)
    br.inputs['Scale'].default_value=4; br.inputs['Mortar Size'].default_value=.015
    no=nt.new('ShaderNodeTexNoise'); no.inputs['Scale'].default_value=6
    mx=nt.new('ShaderNodeMix'); mx.data_type='RGBA'; mx.blend_type='MULTIPLY'; mx.inputs['Factor'].default_value=.35
    ln.new(br.outputs['Color'],mx.inputs[6]); ln.new(no.outputs['Color'],mx.inputs[7]); ln.new(mx.outputs[2],b.inputs['Base Color'])
    bp=nt.new('ShaderNodeBump'); bp.inputs['Strength'].default_value=.4; ln.new(br.outputs['Fac'],bp.inputs['Height']); ln.new(bp.outputs[0],b.inputs['Normal'])
    b.inputs['Roughness'].default_value=.85
def asphalte(m):
    nt,ln,b=nodes(m); no=nt.new('ShaderNodeTexNoise'); no.inputs['Scale'].default_value=40; no.inputs['Detail'].default_value=8
    ln.new(coord(nt,ln,(1,1,1)),no.inputs[0])
    cr=nt.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color=(.025,.025,.03,1); cr.color_ramp.elements[1].color=(.07,.07,.075,1)
    ln.new(no.outputs['Fac'],cr.inputs[0]); ln.new(cr.outputs[0],b.inputs['Base Color'])
    fl=nt.new('ShaderNodeTexNoise'); fl.inputs['Scale'].default_value=.6        # flaques : zones brillantes
    ln.new(coord(nt,ln,(1,1,1)),fl.inputs[0])
    r=nt.new('ShaderNodeValToRGB'); r.color_ramp.elements[0].position=.48; r.color_ramp.elements[0].color=(.05,.05,.05,1); r.color_ramp.elements[1].position=.56; r.color_ramp.elements[1].color=(.55,.55,.55,1)
    ln.new(fl.outputs['Fac'],r.inputs[0]); ln.new(r.outputs[0],b.inputs['Roughness'])
    bp=nt.new('ShaderNodeBump'); bp.inputs['Strength'].default_value=.15; ln.new(no.outputs['Fac'],bp.inputs['Height']); ln.new(bp.outputs[0],b.inputs['Normal'])
def beton(m):
    nt,ln,b=nodes(m); br=nt.new('ShaderNodeTexBrick'); ln.new(coord(nt,ln,(1,1,1)),br.inputs[0])
    br.inputs['Scale'].default_value=1.2; br.inputs['Mortar Size'].default_value=.01; br.offset=0
    br.inputs['Color1'].default_value=(.16,.16,.17,1); br.inputs['Color2'].default_value=(.13,.13,.14,1); br.inputs['Mortar'].default_value=(.06,.06,.06,1)
    ln.new(br.outputs['Color'],b.inputs['Base Color']); b.inputs['Roughness'].default_value=.7
for n,f in (('brique',brique),('asphalte',asphalte),('beton',beton)):
    m=bpy.data.materials.get(n)
    if m: f(m)
for o in bpy.data.objects:
    if o.name=='mur': o.data.materials.clear(); o.data.materials.append(bpy.data.materials['brique'])
    if o.name=='Plane': o.data.materials.clear(); o.data.materials.append(bpy.data.materials['asphalte'])
    if o.name=='trottoir': o.data.materials.clear(); o.data.materials.append(bpy.data.materials['beton'])
for o in bpy.data.objects:
    if o.type=='MESH' and o.name in('mur','Plane','trottoir'):
        bpy.context.view_layer.objects.active=o
# 3. immeuble de 3 étages, fenêtres avec cadre, une seule allumée au 3e
mur=bpy.data.objects['mur']; mur.scale.z*=12/8; mur.location.z=6
CADRE=bpy.data.materials.new('cadre'); nodes(CADRE)[2].inputs['Base Color'].default_value=(.05,.05,.055,1)
NOIRE=bpy.data.materials.get('fenetre')
BLEUE=bpy.data.materials.new('fen_bleue'); _,_,b=nodes(BLEUE); b.inputs['Base Color'].default_value=(.03,.05,.1,1); b.inputs['Emission Color'].default_value=(.3,.55,1,1); b.inputs['Emission Strength'].default_value=7
def cube(p,s,m):
    bpy.ops.mesh.primitive_cube_add(location=p); o=bpy.context.object; o.scale=s; o.data.materials.append(m); return o
for y in range(-30,31,5):
    cube((-6.97,y,8.5),(.06,.85,.7),CADRE); cube((-6.93,y,8.5),(.04,.75,.6),BLEUE if y==-10 else NOIRE)
    cube((-6.9,y,7.75),(.12,.95,.05),CADRE)   # appui de fenêtre
bpy.ops.object.light_add(type='AREA',location=(-6.5,-10,8.5)); l=bpy.context.object; l.data.energy=180; l.data.color=(.35,.55,1); l.data.size=1.3; l.rotation_euler=(0,math.radians(-90),0)
cube((-6.95,-2.5,1.1),(.08,.6,1.1),CADRE)       # porte d'immeuble
for y in (-14,-20,4):                             # climatiseurs
    cube((-6.75,y+1.6,6.4),(.3,.35,.25),bpy.data.materials['beton'])
# marquage au sol
LIGNE=bpy.data.materials.new('ligne'); _,_,b=nodes(LIGNE); b.inputs['Base Color'].default_value=(.6,.58,.5,1); b.inputs['Roughness'].default_value=.6
for y in range(-34,35,6): cube((0,y,.003),(.08,1.4,.003),LIGNE)
# 4. voiture : tout le modèle (carrosserie + roues) bouge ensemble, plus grande, matériaux d'origine
avant=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath='assets3d/vehicules/car_quaternius.glb')
neufs=[o for o in bpy.data.objects if o not in avant]
pivot=bpy.data.objects.new('voiture',None); sc.collection.objects.link(pivot)
for o in neufs:
    if o.parent is None: o.parent=pivot
bpy.context.view_layer.update()
pts=[o.matrix_world@V(c) for o in neufs if o.type=='MESH' for c in o.bound_box]
lx=max(p.x for p in pts)-min(p.x for p in pts); ly=max(p.y for p in pts)-min(p.y for p in pts); zmin=min(p.z for p in pts)
k=4.8/max(lx,ly); pivot.scale=(k,k,k)
pivot.rotation_euler.z = (math.radians(90) if lx>ly else 0)+math.pi
pivot.location=(2.3,-30,-zmin*k)
pivot.keyframe_insert('location',frame=1); pivot.location.y=6; pivot.keyframe_insert('location',frame=240)
for fc in pivot.animation_data.action.fcurves if pivot.animation_data and hasattr(pivot.animation_data.action,'fcurves') else []:
    for kp in fc.keyframe_points: kp.interpolation='LINEAR'
for x in (-.55,.55):
    bpy.ops.object.light_add(type='SPOT'); ph=bpy.context.object; ph.data.energy=1800; ph.data.color=(1,.93,.7); ph.data.spot_size=math.radians(50); ph.data.spot_blend=.5
    ph.parent=pivot; ph.location=(x/k,-2.5/k,.75/k); ph.rotation_euler=(math.radians(80),0,0)
print('VOITURE',round(lx,2),round(ly,2),'k',round(k,2))
# 5. rendu
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=32; sc.cycles.use_denoising=True
sc.render.resolution_x=1920; sc.render.resolution_y=804; sc.render.resolution_percentage=50
sc.render.image_settings.media_type='IMAGE'; sc.render.image_settings.file_format='PNG'
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
cam=bpy.data.objects['Camera']
def vise(loc,tgt,lens):
    cam.location=loc; cam.rotation_mode='XYZ'; cam.rotation_euler=(V(tgt)-V(loc)).to_track_quat('-Z','Y').to_euler(); cam.data.lens=lens
for nom,f,loc,tgt,lens in [('voiture_passe',95,(6.2,-22.5,1.0),(2.3,-15.5,0.8),30),('montee_fenetre',140,(3.0,-10.5,1.5),(-6.9,-10.0,8.4),24)]:
    vise(loc,tgt,lens); sc.frame_set(f); sc.render.filepath=f'videos/binance-hack/blender/v4_{nom}.png'; bpy.ops.render.render(write_still=True); print('RENDU',nom,flush=True)
bpy.ops.wm.save_as_mainfile(filepath='videos/binance-hack/blender/ruelle_binance.blend')
