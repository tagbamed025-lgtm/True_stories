import bpy, math
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; w.node_tree.nodes['Background'].inputs[0].default_value=(.02,.025,.04,1)
def mat(n,c,r=.6,e=None,es=0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=r
    if e: b.inputs['Emission Color'].default_value=(*e,1); b.inputs['Emission Strength'].default_value=es
    return m
MUR=mat('mur',(.32,.33,.38)); SOL=mat('sol',(.18,.14,.11)); BOIS=mat('bois',(.35,.24,.15)); NOIR=mat('noir',(.04,.04,.05),.4)
ROUGE=mat('TRU_rouge',(.75,.04,.05),.45); BLANC=mat('blanc',(.8,.8,.82))
ECRAN=mat('ecran',(.02,.04,.08),.2,(.25,.55,1),1.6); LED=mat('led',(0,.2,0),.5,(.1,1,.3),15); RIDEAU=mat('rideau',(.12,.12,.16))
NUIT=mat('nuit',(.02,.03,.06),.1,(.1,.18,.4),1.5)
def box(n,p,s,m,r=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=p,rotation=r); o=bpy.context.object; o.name=n; o.scale=[x/2 for x in s]; o.data.materials.append(m); return o
def cyl(n,p,r,h,m,v=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v,radius=r,depth=h,location=p); o=bpy.context.object; o.data.materials.append(m); return o
box('sol',(0,0,-.05),(6,6,.1),SOL); box('mur_f',(0,2.2,1.4),(6,.1,2.8),MUR); box('mur_g',(-2.6,0,1.4),(.1,6,2.8),MUR)
box('fenetre',(-2.54,.3,1.6),(.05,1.4,1.2),NUIT); box('rideau',(-2.5,-.55,1.5),(.08,.5,1.9),RIDEAU)
box('table',(0,1.5,.74),(1.8,.8,.05),BOIS)
for x in(-.8,.8): box('pied',(x,1.5,.37),(.05,.7,.72),NOIR)
box('ecran_c',(0,1.75,1.12),(.8,.03,.46),ECRAN); box('pied_e',(0,1.8,.85),(.05,.05,.2),NOIR)
box('ecran_g',(-.85,1.68,1.1),(.62,.03,.38),ECRAN,(0,0,math.radians(22)))
box('ecran_d',(.85,1.68,1.1),(.62,.03,.38),NOIR,(0,0,math.radians(-22)))
box('clavier',(0,1.32,.78),(.46,.15,.025),NOIR)
cyl('canette',(-.6,1.3,.83),.033,.12,mat('alu',(.6,.6,.62),.3),12); cyl('bol',(.62,1.35,.8),.08,.07,BLANC,16)
box('routeur',(-.75,1.72,.8),(.22,.13,.04),NOIR)
for k in range(4): box('led',(-.83+k*.05,1.65,.81),(.012,.005,.012),LED)
# lit + étagère pour lire une vraie chambre
box('lit',(1.9,-.6,.25),(1.2,2.2,.5),mat('drap',(.25,.27,.32))); box('etagere',(-2.35,1.6,1.1),(.3,.9,2.2),BOIS)
for k in range(5): box('livre',(-2.3,1.3+k*.12,1.3),(.2,.08,.28),mat(f'l{k}',[(.5,.2,.15),(.2,.3,.5),(.6,.55,.4),(.2,.4,.3),(.4,.4,.45)][k]))
# pirate : GLB figé de Silk Road (assis, tape), recoloré en rouge TRU
bpy.ops.import_scene.gltf(filepath='/home/claude/repo/assets3d/silk-road/glb/ross_assis_tape.glb')
objs=[o for o in bpy.context.selected_objects]
racine=[o for o in objs if o.parent is None]
for o in objs:
    if o.type=='MESH': o.data.materials.clear(); o.data.materials.append(ROUGE)
mins=Vector((1e9,)*3); maxs=Vector((-1e9,)*3)
bpy.context.view_layer.update()
for o in objs:
    if o.type=='MESH':
        for c in o.bound_box:
            v=o.matrix_world@Vector(c); mins=Vector(map(min,mins,v)); maxs=Vector(map(max,maxs,v))
print('BBOX',mins,maxs)
for r in racine:
    r.rotation_mode='XYZ'; r.rotation_euler.z+=math.radians(180)
bpy.context.view_layer.update()
mins=Vector((1e9,)*3); maxs=Vector((-1e9,)*3)
for o in objs:
    if o.type=='MESH':
        for c in o.bound_box:
            v=o.matrix_world@Vector(c); mins=Vector(map(min,mins,v)); maxs=Vector(map(max,maxs,v))
ctr=(mins+maxs)/2
for r in racine: r.location+=Vector((0-ctr.x,.85-ctr.y,-mins.z))
box('chaise',(0,.85,.45),(.5,.5,.05),NOIR)
# lumière : écran (clé bleue) + contre-jour chaud de la rue + ambiance lisible
bpy.ops.object.light_add(type='AREA',location=(0,1.6,1.15)); a=bpy.context.object; a.data.energy=60; a.data.size=.8; a.data.color=(.35,.6,1); a.rotation_euler=(math.radians(-90),0,0)
bpy.ops.object.light_add(type='SPOT',location=(-3.5,.3,2.2)); s=bpy.context.object; s.data.energy=900; s.data.color=(1,.6,.3); s.data.spot_size=math.radians(50); s.rotation_euler=(0,math.radians(-70),0)
bpy.ops.object.light_add(type='AREA',location=(1,-2,2.6)); f=bpy.context.object; f.data.energy=120; f.data.size=3; f.data.color=(.55,.65,1); f.rotation_euler=(math.radians(40),0,math.radians(20))
def cam(n,loc,tgt,lens):
    bpy.ops.object.camera_add(location=loc); c=bpy.context.object; c.data.lens=lens
    d=tgt-Vector(loc); c.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    c.data.dof.use_dof=True; c.data.dof.focus_distance=d.length; c.data.dof.aperture_fstop=2.8; return c
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=32; sc.cycles.use_denoising=True
sc.render.resolution_x=1920; sc.render.resolution_y=804; sc.render.resolution_percentage=50
for n,loc,tgt,lens in [('large',(1.6,-1.8,1.6),Vector((-.1,1.2,1.0)),30),('dos',(.55,-.35,1.45),Vector((0,1.7,1.05)),40),('epaule',(-.9,1.1,1.3),Vector((.1,1.0,1.15)),50)]:
    sc.camera=cam(n,loc,tgt,lens); sc.render.filepath=f'/home/claude/rendu/chambre_v4_{n}.png'; bpy.ops.render.render(write_still=True); print('RENDU',n)
