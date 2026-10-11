# Salle de lecture commune aux plans 0.7, 4.1, 4.7, 4.8 : tables, chaises, Ross (rouge) et 4 agents en civil (blanc).
import bpy, math
import biblio as B
# (fichier, position de la chaise, orientation, décalage dans l'anim pour désynchroniser)
AGENTS = [('Ch23_nonPBR.fbx', (-3.6, .2), 180, 40), ('Ch22_nonPBR.fbx', (-3.0, 1.7), 0, 90),
          ('Ch21_nonPBR.fbx', (3.3, -.45), 0, 140), ('Ch23_nonPBR.fbx', (.7, .75), 0, 190)]

def construire(actions_agents=None, actions_ross=None):
    sc = B.reset(); B.salle(); B.rayonnages(); B.styles()
    B.objet('GUBI Rectangular Table', (0, 0, 0))
    B.objet('GUBI Rectangular Table', (-3.3, .95, 0))
    B.objet('GUBI Rectangular Table', (3.3, -1.2, 0))
    for (x, y), r in [((0, -.75), 0), ((-3.6, .2), 0), ((-3.0, 1.7), 180), ((3.3, -.45), 180), ((.7, .75), 180)]:
        B.objet('Simple wooden chair', (x, y, 0), rot=r)
    B.objet('Mcbook Laptop', (0, -.22, .74))
    B.objet('Coffee Cup', (.35, -.3, .74)); B.objet('Backpack', (-.45, -.9, 0), rot=20)
    for x, y, r in [(-3.6, .7, 10), (-3.0, 1.3, 170), (3.3, -.95, 190), (.7, .3, 175)]:
        B.objet('Stacked set of books', (x, y, .745), rot=r)
    B.objet('Minimalist LED Desk Lamp black', (-.85, .3, .74), rot=200)
    ross = B.perso('Ch31_nonPBR.fbx', B.ROUGE, (0, -.75, 0), 180, actions_ross or [('Sitting Idle', 1, 0)])
    agents = [B.perso(f, B.BLANC, (x, y, 0), r, (actions_agents(i, d) if actions_agents else [('Sitting Idle', 1, d)]))
              for i, (f, (x, y), r, d) in enumerate(AGENTS)]
    return sc, ross, agents
