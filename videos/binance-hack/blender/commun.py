import bpy, math
from mathutils import Vector as V
REPO=''
KIT=REPO+'assets3d/objets/kit_meubles.blend'; GLB=REPO+'assets3d/silk-road/glb/'
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
    sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
    w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; w.node_tree.nodes['Background'].inputs[0].default_value=(.02,.025,.04,1)
    sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=32; sc.cycles.use_denoising=True
    sc.render.resolution_x=1920; sc.render.resolution_y=804; sc.render.resolution_percentage=50
    return sc
def mat(n,c,r=.6,e=None,es=0):
    m=bpy.data.materials.new(n); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*c,1); b.inputs['Roughness'].default_value=r
    if e: b.inputs['Emission Color'].default_value=(*e,1); b.inputs['Emission Strength'].default_value=es
    return m
def img_mat(n,path,force=1.4):
    m=bpy.data.materials.new(n); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    t=nt.nodes.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(path)
    nt.links.new(t.outputs[0],b.inputs['Base Color']); nt.links.new(t.outputs[0],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=force; return m
def box(n,p,s,m,r=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=p,rotation=r); o=bpy.context.object; o.name=n; o.scale=[x/2 for x in s]; o.data.materials.append(m); return o
def dalle(n,p,w,h,m,rz=0):
    bpy.ops.mesh.primitive_plane_add(location=p,rotation=(math.radians(90),0,math.radians(rz))); o=bpy.context.object; o.name=n; o.scale=(w/2,h/2,1); o.data.materials.append(m); return o
def bb(objs):
    pts=[o.matrix_world@V(c) for o in objs if o.type=='MESH' for c in o.bound_box]
    return V((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts))),V((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
_cache={}
BOIS_DEF=None
def _charger():
    if _cache: return
    with bpy.data.libraries.load(KIT) as (a,b): b.objects=list(a.objects)
    for o in b.objects:
        if o: _cache[o.name]=o
def _copie(o,parent,garde,materiau):
    c=o.copy(); bpy.context.scene.collection.objects.link(c); c.parent=parent
    if parent is not None: c.matrix_parent_inverse=o.matrix_parent_inverse.copy()
    if c.type=='MESH':
        c.data=c.data.copy(); c.data.materials.clear(); c.data.materials.append(materiau)
    garde.add(c)
    for e in o.children: _copie(e,c,garde,materiau)
    return c
def kit(nom, pos, rotz=0, hauteur=None, materiau=None):
    """copie un meuble du kit (chargé une seule fois), posé au sol en pos, tourné de rotz degrés.
    Les textures du kit ont été retirées : on applique une matière unie (bois par défaut)."""
    global BOIS_DEF
    _charger()
    if BOIS_DEF is None: BOIS_DEF=mat('kit_bois',(.30,.21,.14),.6)
    src=_cache.get(nom) or [o for k,o in _cache.items() if k.startswith(nom)][0]
    garde=set(); r=_copie(src,None,garde,materiau or BOIS_DEF)
    pivot=bpy.data.objects.new('kit_'+nom,None); bpy.context.scene.collection.objects.link(pivot); r.parent=pivot
    bpy.context.view_layer.update(); mi,ma=bb(garde)
    if hauteur: k=hauteur/(ma.z-mi.z); pivot.scale=(k,k,k); bpy.context.view_layer.update(); mi,ma=bb(garde)
    r.location-=V(((mi.x+ma.x)/2,(mi.y+ma.y)/2,mi.z))/ (pivot.scale.x or 1)
    p2=bpy.data.objects.new('pose_'+nom,None); bpy.context.scene.collection.objects.link(p2); pivot.parent=p2
    p2.location=pos; p2.rotation_euler.z=math.radians(rotz); return p2, garde
def perso(fichier, pos, rotz, materiau):
    avant=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=GLB+fichier)
    neufs=[o for o in bpy.data.objects if o not in avant]
    for o in neufs:
        if o.type=='MESH': o.data.materials.clear(); o.data.materials.append(materiau)
    pivot=bpy.data.objects.new('perso',None); bpy.context.scene.collection.objects.link(pivot)
    for o in neufs:
        if o.parent is None: o.parent=pivot
    bpy.context.view_layer.update(); mi,ma=bb(neufs)
    for o in neufs:
        if o.parent==pivot: o.location-=V(((mi.x+ma.x)/2,(mi.y+ma.y)/2,mi.z))
    pivot.location=pos; pivot.rotation_euler.z=math.radians(rotz); return pivot
def lum(t,loc,e,c=(1,1,1),rot=(0,0,0),taille=1):
    bpy.ops.object.light_add(type=t,location=loc); l=bpy.context.object; l.data.energy=e; l.data.color=c; l.rotation_euler=rot
    if t=='AREA': l.data.size=taille
    return l
def rendu(sc,nom,loc,tgt,lens,dossier,fstop=2.8):
    bpy.ops.object.camera_add(location=loc); c=bpy.context.object; c.data.lens=lens
    d=V(tgt)-V(loc); c.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    c.data.dof.use_dof=True; c.data.dof.focus_distance=d.length; c.data.dof.aperture_fstop=fstop
    sc.camera=c; sc.render.filepath=f'{dossier}/{nom}.png'; bpy.ops.render.render(write_still=True); print('RENDU',nom,flush=True)
ROUGE=lambda: mat('TRU_rouge',(.75,.04,.05),.45)
BLANC=lambda: mat('TRU_blanc',(.82,.83,.86),.55)
