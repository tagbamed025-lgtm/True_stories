import sys; sys.path.insert(0,'videos/binance-hack/blender')
from commun import *
sc=reset(); D='videos/binance-hack/blender'
MUR=mat('mur',(.30,.32,.37)); SOL=mat('moquette',(.10,.11,.13),.95); NOIR=mat('noir',(.04,.04,.05),.4); BL=BLANC()
box('sol',(0,0,-.05),(14,10,.1),SOL); box('mur_ecrans',(0,4.6,1.8),(14,.1,3.6),MUR); box('mur_g',(-7,0,1.8),(.1,10,3.6),MUR); box('plafond',(0,0,3.6),(14,10,.1),MUR)
# mur d'écrans : tableaux de bord (on réutilise le terminal du pirate et le plan "chaînes")
E1=img_mat('e_term',REPO+'videos/binance-hack/code/apercus/chaines.png',1.2)
E2=img_mat('e_jauges',REPO+'videos/binance-hack/code/apercus/jauges.png',1.2)
E3=img_mat('e_alerte',REPO+'videos/binance-hack/code/apercus/alerte.png',1.2)
ROUGE_E=mat('e_rouge',(.15,0,0),.4,(.8,.04,.03),1.1)
for k,(m) in enumerate([E3,E1,ROUGE_E,E2,E1]):
    x=-5.0+k*2.5; box('cadre%d'%k,(x,4.52,2.2),(2.3,.06,1.36),NOIR); dalle('ecran%d'%k,(x,4.48,2.2),2.2,1.26,m)
bpy.ops.object.text_add(location=(0,4.45,2.2),rotation=(math.radians(90),0,0)); t=bpy.context.object; t.data.body='BINANCE 14'; t.data.align_x='CENTER'; t.data.align_y='CENTER'; t.data.size=.32; t.data.materials.append(mat('txt',(1,1,1),.5,(1,1,1),3))
# horloge 1 h 52
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.32,depth=.04,location=(5.8,4.5,3.05),rotation=(math.radians(90),0,0)); bpy.context.object.data.materials.append(mat('cadran',(.85,.85,.85)))
box('aig_h',(5.8,4.46,3.05),(.025,.01,.18),NOIR,(0,math.radians(-56),0)); box('aig_m',(5.8,4.45,3.05),(.018,.01,.27),NOIR,(0,math.radians(48),0))
# grande table de réunion (2 tables du kit côte à côte) + chaises
TABLE=mat('table_blanche',(.75,.75,.76),.4); CHAISE=mat('chaise_noire',(.06,.06,.07),.5)
for x in (-1.3,1.3): kit('GUBI Rectangular Table',(x,1.5,0),0,.75,TABLE)
for i,x in enumerate((-2.4,-.8,.8,2.4)):
    kit('Wooden Chair',(x,.55,0),180,.95,CHAISE); kit('Wooden Chair',(x,2.5,0),0,.95,CHAISE)
for i,x in enumerate((-2.2,0,1.6)): kit('Mcbook Laptop',(x,1.25,.75),180,.17,mat('alu',(.55,.56,.58),.3))
for x in (-1.2,.9,2.6): kit('Coffee Cup',(x,1.75,.75),0,.1,BL)
# l'équipe Binance, en blanc : debout devant les écrans, une assise
perso('agent_debout_veste.glb',(-1.6,3.4,0),180,BL)
perso('agente_debout.glb',(.6,3.6,0),200,BL)
perso('agent_debout_2.glb',(2.8,3.3,0),150,BL)
perso('alford_assis_tape.glb',(-.8,.75,.05),0,BL)
# lumière : le mur d'écrans éclaire la pièce, néons faibles
lum('AREA',(0,3.9,2.2),900,(.45,.6,1),(math.radians(-90),0,0),9)
lum('AREA',(0,0,3.5),250,(.75,.82,1),(0,0,0),6)
lum('AREA',(-4,-3,2.8),120,(1,.75,.5),(math.radians(60),0,math.radians(-40)),2)
rendu(sc,'crise_large',(-5.6,-3.6,2.3),(.6,2.6,1.3),24,D)
rendu(sc,'crise_equipe',(1.4,-.9,1.55),(.2,3.6,1.5),35,D)
