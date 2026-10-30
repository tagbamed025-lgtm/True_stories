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
def img_mat(n,path,force=1.4):
    m=bpy.data.materials.new(n); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    t=nt.nodes.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(path)
    nt.links.new(t.outputs[0],b.inputs['Base Color']); nt.links.new(t.outputs[0],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=force; return m
ECRAN=img_mat('ecran_hack','/home/claude/ecrans/ecran.png'); ECRAN2=img_mat('ecran_hex','/home/claude/ecrans/ecran2.png'); LED=mat('led',(0,.2,0),.5,(.1,1,.3),15); RIDEAU=mat('rideau',(.12,.12,.16))
NUIT=mat('nuit',(.02,.03,.06),.1,(.1,.18,.4),1.5)
def box(n,p,s,m,r=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=p,rotation=r); o=bpy.context.object; o.name=n; o.scale=[x/2 for x in s]; o.data.materials.append(m); return o
def cyl(n,p,r,h,m,v=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v,radius=r,depth=h,location=p); o=bpy.context.object; o.data.materials.append(m); return o
box('sol',(0,0,-.05),(6,6,.1),SOL); box('mur_f',(0,2.2,1.4),(6,.1,2.8),MUR); box('mur_g',(-2.6,0,1.4),(.1,6,2.8),MUR)
box('fenetre',(-2.54,.3,1.6),(.05,1.4,1.2),NUIT); box('rideau',(-2.5,-.55,1.5),(.08,.5,1.9),RIDEAU)
box('table',(0,1.5,.74),(1.8,.8,.05),BOIS)
for x in(-.8,.8): box('pied',(x,1.5,.37),(.05,.7,.72),NOIR)
def dalle(n,p,w,h,m,rz=0):
    bpy.ops.mesh.primitive_plane_add(location=p,rotation=(math.radians(90),0,math.radians(rz)))
    o=bpy.context.object; o.name=n; o.scale=(w/2,h/2,1); o.data.materials.append(m); return o
box('ecran_c',(0,1.75,1.12),(.84,.03,.5),NOIR); dalle('dalle_c',(0,1.73,1.12),.8,.45,ECRAN); box('pied_e',(0,1.8,.85),(.05,.05,.2),NOIR)
box('ecran_g',(-.85,1.68,1.1),(.66,.03,.41),NOIR,(0,0,math.radians(22))); dalle('dalle_g',(-.855,1.664,1.1),.62,.37,ECRAN2,22)
box('ecran_d',(.85,1.68,1.1),(.62,.03,.38),NOIR,(0,0,math.radians(-22)))
box('clavier',(0,1.32,.772),(.46,.155,.018),mat('clav',(.07,.07,.08),.35))
TOUCHE=mat('touche',(.16,.16,.18),.5); TL=mat('touche_led',(.02,.02,.03),.5,(.2,.45,1),.6)
for r in range(5):
    n=14 if r<4 else 7
    for k in range(n):
        x=-.205+k*.0315 + (r*.006 if r<4 else 0)
        if r==4: x=-.205+k*.0315
        w=.026 if not (r==4 and k==3) else .16
        if r==4 and k>3: x+=.135
        box('t',(x,1.268+r*.026,.785),(w,.022,.01),TOUCHE if (r+k)%9 else TL)
box('souris',(.32,1.3,.785),(.05,.08,.025),NOIR); box('tapis',(.32,1.3,.7705),(.2,.18,.003),mat('tapis_s',(.05,.05,.06)))
cyl('canette',(-.6,1.3,.83),.033,.12,mat('alu',(.6,.6,.62),.3),12); cyl('bol',(.62,1.35,.8),.08,.07,BLANC,16)
box('routeur',(-.75,1.72,.8),(.22,.13,.04),NOIR)
for k in range(4): box('led',(-.83+k*.05,1.65,.81),(.012,.005,.012),LED)
# lit + étagère pour lire une vraie chambre
DRAP=mat('drap',(.30,.32,.38),.8); COUV=mat('couverture',(.13,.15,.22),.9); OREILLER=mat('oreiller',(.75,.76,.8),.9)
box('sommier',(1.75,-1.85,.18),(1.5,2.1,.36),BOIS); box('matelas',(1.75,-1.85,.44),(1.42,2.0,.18),DRAP)
box('tete_lit',(2.52,-1.85,.75),(.06,1.5,1.1),BOIS)
box('couverture',(1.6,-1.85,.55),(1.15,2.02,.06),COUV,(0,math.radians(1.5),0))
box('oreiller1',(2.25,-2.3,.6),(.35,.55,.12),OREILLER); box('oreiller2',(2.25,-1.4,.6),(.35,.55,.12),OREILLER)
OBJ='/home/claude/binance_assets/binance_objets.blend'
with bpy.data.libraries.load(OBJ) as (A,B): B.collections=['Night Stand Modern','Duck Silicone Night Light']
def poser(col,pos,rotz,haut=None):
    sc.collection.children.link(col); objs=list(col.all_objects); bpy.context.view_layer.update()
    pts=[o.matrix_world@Vector(c) for o in objs if o.type=='MESH' and not o.hide_render for c in o.bound_box]
    mi=Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts))); ma=Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
    pv=bpy.data.objects.new('pv_'+col.name,None); sc.collection.objects.link(pv)
    for o in objs:
        if o.parent is None: o.parent=pv; o.location-=Vector(((mi.x+ma.x)/2,(mi.y+ma.y)/2,mi.z))
    if haut: k=haut/(ma.z-mi.z); pv.scale=(k,k,k)
    pv.location=pos; pv.rotation_euler.z=math.radians(rotz); return ma.z-mi.z
h=poser(B.collections[0],(2.25,-.6,0),-90,.55)
poser(B.collections[1],(2.25,-.6,.55),200,.16)
cyl('lampe_chevet',(2.25,-.45,.66),.0,.0,mat('x',(0,0,0)),3)
bpy.ops.object.light_add(type='POINT',location=(2.25,-.6,.78)); lc=bpy.context.object; lc.data.energy=12; lc.data.color=(1,.6,.3); lc.data.shadow_soft_size=.3
box('tapis_sol',(.6,-1.2,.005),(2.2,1.6,.01),mat('tapis',(.22,.08,.06),.95))
box('poster1',(1.2,-3.0+.06,1.6),(.6,.02,.85),mat('poster1',(.05,.08,.12),.6,(.15,.3,.6),.4))
box('poster2',(2.0,-3.0+.06,1.7),(.45,.02,.6),mat('poster2',(.12,.05,.05),.6,(.5,.1,.08),.3))
box('mur_arriere',(0,-3.0,1.4),(6,.1,2.8),MUR); box('mur_droit',(2.6,0,1.4),(.1,6,2.8),MUR)
box('vetements',(-1.2,-2.5,.15),(.6,.4,.3),mat('linge',(.2,.2,.25)))
box('porte',(-1.9,-2.94,1.0),(.9,.04,2.0),BOIS); box('etagere',(-2.35,1.6,1.1),(.3,.9,2.2),BOIS)
for k in range(5): box('livre',(-2.3,1.3+k*.12,1.3),(.2,.08,.28),mat(f'l{k}',[(.5,.2,.15),(.2,.3,.5),(.6,.55,.4),(.2,.4,.3),(.4,.4,.45)][k]))
# pirate : Ch18 + animation Typing (Mixamo), stylisé low poly rouge, face au bureau (+y)
avant=set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath='/home/claude/true_stories/assets3d/personnages_animes/Typing_3_Ch18_homme.fbx')
neufs=[o for o in bpy.data.objects if o not in avant]
ARM=[o for o in neufs if o.type=='ARMATURE'][0]
for o in neufs:
    if o.type=='MESH':
        o.data.materials.clear(); o.data.materials.append(ROUGE)
        d=o.modifiers.new('lowpoly','DECIMATE'); d.decimate_type='COLLAPSE'; d.ratio=.035
        for p in o.data.polygons: p.use_smooth=False
        o.modifiers.move(len(o.modifiers)-1,0)
ARM.rotation_mode='XYZ'; ARM.rotation_euler.z+=math.pi
ARM.location=(0.0,0.92,0.0)
ACTION=ARM.animation_data.action
SEAT_Y=.86


KIT='/home/claude/true_stories/assets3d/objets/kit_meubles.blend'
with bpy.data.libraries.load(KIT) as (a,b): b.objects=list(a.objects)
garde=set()
def desc(o):
    garde.add(o); [desc(c) for c in o.children]
racines=[o for o in b.objects if o and o.name=='Wooden Chair']
for r in racines: desc(r)
for o in b.objects:
    if o and o not in garde: bpy.data.objects.remove(o)
for o in garde: sc.collection.objects.link(o)
ch=racines[0]; ch.rotation_mode='XYZ'; ch.rotation_euler.z+=math.pi
bpy.context.view_layer.update()
def bb(objs):
    mi=Vector((1e9,)*3); ma=Vector((-1e9,)*3)
    for o in objs:
        if o.type=='MESH':
            for c in o.bound_box:
                v=o.matrix_world@Vector(c); mi=Vector(map(min,mi,v)); ma=Vector(map(max,ma,v))
    return mi,ma
mi,ma=bb(garde); print('CHAISE',mi,ma)
k=0.9/(ma.z-mi.z); ch.scale=[x*k for x in ch.scale]
bpy.context.view_layer.update(); mi,ma=bb(garde)
ch.location+=Vector((0-(mi.x+ma.x)/2, SEAT_Y-(mi.y+ma.y)/2, -mi.z))
for o in garde:
    if o.type=='MESH': o.data.materials.clear(); o.data.materials.append(NOIR if False else BOIS)

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

import os
FPS=8
sc.cycles.samples=8; sc.cycles.use_denoising=True; sc.cycles.max_bounces=3; sc.cycles.diffuse_bounces=1; sc.cycles.glossy_bounces=2; sc.render.resolution_x=1280; sc.render.resolution_y=536; sc.render.resolution_percentage=75
sc.render.image_settings.media_type='IMAGE'; sc.render.image_settings.file_format='PNG'
def lerp(a,b,u): return Vector(a)+(Vector(b)-Vector(a))*u
def ease(u): return u*u*(3-2*u)
bpy.ops.object.camera_add(); CAM=bpy.context.object; sc.camera=CAM
CAM.data.dof.use_dof=True; CAM.data.dof.aperture_fstop=2.4
# touche Entrée : on la retrouve parmi les touches (rangée du milieu, à droite)
touches=[o for o in bpy.data.objects if o.name.startswith('t') and o.type=='MESH' and abs(o.location.z-.785)<.002]
ENTREE=max(touches,key=lambda o:(o.location.x if abs(o.location.y-1.32)<.02 else -9)) if touches else None
PLANS={
 'D_dos':(2.5,((.6,-.15,1.5),(.35,.25,1.35)),((0,1.75,1.1),(0,1.75,1.1)),38,0),
 'F_entree':(1.2,((.42,1.05,.93),(.40,1.08,.91)),((.19,1.32,.79),(.19,1.32,.79)),60,1),
 'G_large':(3.0,((-2.1,-2.6,1.75),(-1.7,-2.3,1.6)),((.3,.8,.95),(.2,1.0,.95)),24,0),
 'H_contre':(3.0,((-1.25,1.85,1.32),(-1.1,1.75,1.25)),((.35,-.7,1.0),(.3,-.7,1.0)),32,0),
}
for nom,(d,(p0,p1),(t0,t1),lens,entree) in PLANS.items():
    os.makedirs(f'/home/claude/anim/{nom}',exist_ok=True); n=int(round(d*FPS)); CAM.data.lens=lens
    for f in range(n):
        out=f'/home/claude/anim/{nom}/{f:04d}.png'
        if os.path.exists(out): continue
        u=f/max(1,n-1); e=ease(u)
        sc.frame_set(int(40+ (hash(nom)%300) + f*2.5))   # animation Mixamo 60 i/s ralentie ×0,5
        p=lerp(p0,p1,e); t=lerp(t0,t1,e); CAM.location=p; CAM.rotation_euler=(t-p).to_track_quat('-Z','Y').to_euler(); CAM.data.dof.focus_distance=(t-p).length
        if entree and ENTREE: ENTREE.location.z=.785-(.006 if u>.55 else 0)
        bpy.context.view_layer.update()
        sc.render.filepath=out; bpy.ops.render.render(write_still=True); print('IMG',nom,f,flush=True)
print('FINI_CHAMBRE')
