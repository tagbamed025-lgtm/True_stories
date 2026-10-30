import sys; sys.path.insert(0,'videos/binance-hack/blender')
from commun import *
sc=reset(); D='videos/binance-hack/blender'
MUR=mat('mur',(.62,.64,.68)); SOL=mat('sol',(.22,.23,.25),.7); NOIR=mat('noir',(.04,.04,.05),.4); BL=BLANC(); ROUGE_FIL=mat('fil',(.8,.02,.02),.4,(1,.05,.03),8)
box('sol',(0,0,-.05),(16,12,.1),SOL); box('plafond',(0,0,3.2),(16,12,.1),MUR); box('mur_g',(-8,0,1.6),(.1,12,3.2),MUR)
# baie vitrée au fond : matin bleuté
VITRE=mat('vitre',(.5,.6,.75),.1,(.55,.7,1),2.2)
for k in range(7): box('vitre%d'%k,(-6+k*2,6,1.7),(1.9,.05,2.6),VITRE); box('montant%d'%k,(-7+k*2,5.97,1.6),(.08,.08,3.2),NOIR)
box('allege',(0,5.95,.2),(16,.1,.4),MUR)
DESK=mat('desk',(.72,.70,.66),.5); CH=mat('ch',(.08,.08,.09),.5)
# rangées de bureaux
TERM=img_mat('term',REPO+'videos/binance-hack/code/apercus/ecran.png',1.0) if False else img_mat('term','videos/binance-hack/code/ecrans/ecran2.png',1.0)
for r,y in enumerate((-1.5,1.2,3.6)):
    for c,x in enumerate((-4.5,-1.5,1.5,4.5)):
        kit('Wooden table office-01',(x,y,0),0,.75,DESK)
        kit('Wooden Chair',(x,y-.75,0),180,.95,CH)
        box('ecran_%d_%d'%(r,c),(x,y+.25,1.05),(.56,.03,.34),NOIR); dalle('dalle_%d_%d'%(r,c),(x,y+.233,1.05),.52,.3,TERM if (r+c)%3==0 else NOIR)
        if (r,c)!=(1,1): kit('Minimalist LED Desk Lamp black',(x+.55,y+.2,.75),0,.4,CH)
# le bureau de l'ingénieur (rangée 1, colonne 1) : portable ouvert, café, sac
kit('Mcbook Laptop',(-1.5,1.05,.75),0,.18,mat('alu',(.55,.56,.58),.3))
kit('Coffee Cup',(-1.1,.95,.75),0,.1,BL)
kit('Backpack',(-.8,.55,0),20,.5,mat('sac',(.08,.09,.12),.8))
for k in range(4): box('postit%d'%k,(-1.85+k*.07,1.47,1.27),(.055,.005,.055),mat('pi%d'%k,[(.9,.85,.3),(.95,.6,.4),(.6,.85,.95),(.9,.85,.3)][k]))
perso('agent_debout_veste.glb',(-1.5,.15,0),0,BL)   # l'ingénieur arrive à son bureau
perso('agente_debout.glb',(3.6,2.4,0),160,BL)       # collègue au loin
# le fil rouge : du portable au sol, puis vers la baie vitrée
bpy.ops.curve.primitive_bezier_curve_add(); f=bpy.context.object; sp=f.data.splines[0]; sp.bezier_points.add(3)
for p,co in zip(sp.bezier_points,[(-1.5,1.12,.86),(-1.6,1.4,.02),(.8,4.0,.02),(2.6,5.9,1.2)]): p.co=co; p.handle_left_type=p.handle_right_type='AUTO'
f.data.bevel_depth=.008; f.data.materials.append(ROUGE_FIL)
lum('AREA',(0,0,3.1),700,(.9,.93,1),(0,0,0),12)
lum('AREA',(0,7,1.8),500,(.6,.75,1),(math.radians(90),0,0),14)
rendu(sc,'bureau_large',(-6.3,-4.2,1.9),(-.6,1.6,.9),24,D)
rendu(sc,'bureau_fil',(-3.2,-.6,1.45),(.4,3.4,.6),28,D)
