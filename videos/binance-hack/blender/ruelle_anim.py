import bpy, math, sys
ROT_SENS=float(sys.argv[-1]) if sys.argv[-1].replace('.','').replace('-','').isdigit() else 0.0
from mathutils import Vector as V
bpy.ops.wm.open_mainfile(filepath='/home/claude/true_stories/assets3d/decors/ruelle.blend')
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
OBJ='/home/claude/binance_assets/binance_objets.blend'
with bpy.data.libraries.load(OBJ) as (A,B): B.collections=['Volvo S90','Moon']
for c in B.collections: sc.collection.children.link(c)
volvo=bpy.data.collections['Volvo S90']; neufs=list(volvo.all_objects)
pivot=bpy.data.objects.new('voiture',None); sc.collection.objects.link(pivot)
for o in neufs:
    if o.parent is None: o.parent=pivot
bpy.context.view_layer.update()
pts=[o.matrix_world@V(c) for o in neufs if o.type=='MESH' and not o.hide_render for c in o.bound_box]
lx=max(p.x for p in pts)-min(p.x for p in pts); ly=max(p.y for p in pts)-min(p.y for p in pts); zmin=min(p.z for p in pts)
cx=(max(p.x for p in pts)+min(p.x for p in pts))/2; cy=(max(p.y for p in pts)+min(p.y for p in pts))/2
for o in neufs:
    if o.parent==pivot: o.location-=V((cx,cy,zmin))
k=1.0
pivot.rotation_euler.z=(math.radians(90) if lx>ly else 0)+ROT_SENS
pivot.location=(2.3,-30,0)
# animation : pivot.location.y de -30 (image 1) à 6 (image 240) — posée par plan pour les tests
for x in (-.6,.6):
    bpy.ops.object.light_add(type='SPOT'); ph=bpy.context.object; ph.data.energy=1800; ph.data.color=(1,.93,.75); ph.data.spot_size=math.radians(50); ph.data.spot_blend=.5
    ph.parent=pivot; ph.location=(x,2.4,.7); ph.rotation_euler=(math.radians(-80),0,0)
# la lune, haute et lointaine, au-dessus de la rue
moon=bpy.data.collections['Moon'].all_objects[0]
moon.location=(-30,-90,45); moon.scale=(9,9,9)
bpy.ops.object.light_add(type='AREA',location=(-20,-70,40)); _l=bpy.context.object; _l.data.energy=60000; _l.data.size=6; _l.rotation_euler=(0,0,0); _l.rotation_euler=(V((-30,-90,45))-V((-20,-70,40))).to_track_quat('-Z','Y').to_euler()
for m in moon.data.materials:
    if m and m.use_nodes:
        b=m.node_tree.nodes.get('Principled BSDF')
        if b: b.inputs['Emission Strength'].default_value=0.0; b.inputs['Emission Color'].default_value=(.85,.88,1,1)
# ciel : dégradé nuit + lueur de ville à l'horizon + étoiles
w=sc.world; w.use_nodes=True; nt=w.node_tree; nt.nodes.clear()
out=nt.nodes.new('ShaderNodeOutputWorld'); bg=nt.nodes.new('ShaderNodeBackground'); tc=nt.nodes.new('ShaderNodeTexCoord'); sep=nt.nodes.new('ShaderNodeSeparateXYZ')
ramp=nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=0.0; ramp.color_ramp.elements[0].color=(.09,.07,.09,1); ramp.color_ramp.elements[1].position=.35; ramp.color_ramp.elements[1].color=(.006,.009,.02,1)
vor=nt.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value=420; mr=nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value=0.0; mr.inputs['From Max'].default_value=0.018; mr.inputs['To Min'].default_value=1.2; mr.inputs['To Max'].default_value=0
add=nt.nodes.new('ShaderNodeMix'); add.data_type='RGBA'; add.blend_type='ADD'; add.inputs['Factor'].default_value=1
nt.links.new(tc.outputs['Generated'],sep.inputs[0]); nt.links.new(sep.outputs['Z'],ramp.inputs[0])
nt.links.new(tc.outputs['Generated'],vor.inputs[0]); nt.links.new(vor.outputs['Distance'],mr.inputs[0])
nt.links.new(ramp.outputs[0],add.inputs[6]); nt.links.new(mr.outputs[0],add.inputs[7]); nt.links.new(add.outputs[2],bg.inputs[0]); nt.links.new(bg.outputs[0],out.inputs[0]); bg.inputs[1].default_value=1
print('VOITURE',round(lx,2),round(ly,2))
# 5. rendu
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=32; sc.cycles.use_denoising=True
sc.render.resolution_x=1920; sc.render.resolution_y=804; sc.render.resolution_percentage=50
sc.render.image_settings.media_type='IMAGE'; sc.render.image_settings.file_format='PNG'
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
PHARE_M=bpy.data.materials.new('phare_glow'); PHARE_M.use_nodes=True; _b=PHARE_M.node_tree.nodes['Principled BSDF']; _b.inputs['Emission Color'].default_value=(1,.95,.8,1); _b.inputs['Emission Strength'].default_value=60
PHARES=[]
for sx in (-.62,.62):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.09,segments=12,ring_count=8); g=bpy.context.object; g.data.materials.append(PHARE_M); g.scale=(1.6,.4,.8)
    bpy.ops.object.light_add(type='SPOT'); l=bpy.context.object; l.data.energy=4000; l.data.color=(1,.93,.75); l.data.spot_size=math.radians(60); l.data.spot_blend=.6; l.data.shadow_soft_size=.1
    PHARES.append((sx,g,l))
def place_phares():
    p=pivot.location
    for sx,g,l in PHARES:
        g.location=(p.x+sx,p.y+2.42,.72); l.location=(p.x+sx,p.y+2.5,.72); l.rotation_euler=(math.radians(-90+8),0,0)
for o in list(pivot.children):
    if o.type=='LIGHT': o.data.energy=0
cam=bpy.data.objects['Camera']
def vise(loc,tgt,lens):
    cam.location=loc; cam.rotation_mode='XYZ'; cam.rotation_euler=(V(tgt)-V(loc)).to_track_quat('-Z','Y').to_euler(); cam.data.lens=lens

import os
FPS=8
sc.cycles.samples=6; sc.cycles.use_denoising=True; sc.cycles.max_bounces=3; sc.cycles.diffuse_bounces=1; sc.cycles.glossy_bounces=2; sc.cycles.transmission_bounces=2; sc.cycles.transparent_max_bounces=4; sc.cycles.caustics_reflective=False; sc.cycles.caustics_refractive=False; sc.render.resolution_x=1280; sc.render.resolution_y=536; sc.render.resolution_percentage=75
sc.render.use_motion_blur=True; sc.render.motion_blur_shutter=.5
def lerp(a,b,u): return tuple(x+(y-x)*u for x,y in zip(a,b))
def ease(u): return u*u*(3-2*u)
PLANS={
 # nom : durée(s), voiture (y début, y fin), caméra (pos début, pos fin), cible (début, fin), focale
 'A_entree':(2.7,(-34,-22),((5.8,-6,0.45),(5.6,-6.6,0.5)),((0,-26,0.8),(1,-21,0.9)),30),
 'B_passe':(2.0,(-20,-9),((5.2,-8.0,0.75),(5.0,-8.2,0.75)),('VOITURE',),24),
 'I_dessus':(8.0,(-14,14),((0,0,0),(0,0,0)),('DESSUS',),30),
 'C_montee':(2.5,(10,10),((3.2,-12.5,1.4),(3.0,-11.2,3.4)),((-6.9,-10.6,2.0),(-6.9,-10.0,8.4)),24),
}
PHARE_M=bpy.data.materials.new('phare_glow'); PHARE_M.use_nodes=True; _b=PHARE_M.node_tree.nodes['Principled BSDF']; _b.inputs['Emission Color'].default_value=(1,.95,.8,1); _b.inputs['Emission Strength'].default_value=60
PHARES=[]
for sx in (-.62,.62):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.09,segments=12,ring_count=8); g=bpy.context.object; g.data.materials.append(PHARE_M); g.scale=(1.6,.4,.8)
    bpy.ops.object.light_add(type='SPOT'); l=bpy.context.object; l.data.energy=4000; l.data.color=(1,.93,.75); l.data.spot_size=math.radians(60); l.data.spot_blend=.6; l.data.shadow_soft_size=.1
    PHARES.append((sx,g,l))
def place_phares():
    p=pivot.location
    for sx,g,l in PHARES:
        g.location=(p.x+sx,p.y+2.42,.72); l.location=(p.x+sx,p.y+2.5,.72); l.rotation_euler=(math.radians(-90+8),0,0)
for o in list(pivot.children):
    if o.type=='LIGHT': o.data.energy=0
if os.environ.get('SEUL','').find('I_dessus')>=0:
    for o in [o for o in bpy.data.objects if o.type=='MESH' and o.location.x<-4.2 and o.parent is None]:
        c=o.copy(); c.data=o.data; sc.collection.objects.link(c); c.location.x=-o.location.x+0.3; c.rotation_euler.z=-o.rotation_euler.z
        if c.name.startswith('bras'): c.location.x=-o.location.x
cam=bpy.data.objects['Camera']
cam.animation_data_clear(); cam.data.dof.focus_object=None; cam.data.dof.aperture_fstop=4.0
for c in cam.constraints: cam.constraints.remove(c)
for nom,(d,(y0,y1),(p0,p1),cible,lens) in PLANS.items():
    t0,t1=(cible[0],cible[0]) if len(cible)==1 else cible
    if os.environ.get('SEUL') and nom not in os.environ['SEUL'].split(','): continue
    os.makedirs(f'/home/claude/anim/{nom}',exist_ok=True); n=int(round(d*FPS))
    cam.data.lens=lens
    for f in range(n):
        out=f'/home/claude/anim/{nom}/{f:04d}.png'
        if os.path.exists(out): continue
        u=f/max(1,n-1); e=ease(u)
        pivot.location=(2.3,y0+(y1-y0)*u,0); place_phares()
        if t0=='DESSUS':
            px,py=pivot.location.x,pivot.location.y; p=(px+2.5-1.5*u,py-9+2*u,15-2*u); t=(px-.5,py+4,0)
        else:
            p=lerp(p0,p1,e); t=(pivot.location.x,pivot.location.y,0.8) if t0=='VOITURE' else lerp(t0,t1,e)
        cam.location=p; cam.rotation_mode='XYZ'
        cam.rotation_euler=(V(t)-V(p)).to_track_quat('-Z','Y').to_euler(); cam.data.dof.focus_distance=(V((pivot.location.x,pivot.location.y,.8))-V(p)).length if t0 in ('VOITURE','DESSUS') else (V(t)-V(p)).length
        bpy.context.view_layer.update()
        sc.render.filepath=out; bpy.ops.render.render(write_still=True); print('IMG',nom,f,flush=True)
print('FINI_RUELLE')
