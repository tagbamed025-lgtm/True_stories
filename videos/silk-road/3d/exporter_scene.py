# Exporte la scène de la 1re minute dans un .blend que Mo peut retoucher à la main :
# noms clairs (Ross, Agent_veste, Chaise_Ross, Table_Ross…), une caméra par plan, marqueurs sur la timeline.
# Usage : blender -b --python exporter_scene.py -- <chemin.blend>
import bpy, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import biblio as B, minute as M
sortie = sys.argv[sys.argv.index('--') + 1]
sc = M.construire()

ROLES = {(M.CHAISE_ROSS): 'Ross'}
noms = ['Agent_veste_Ch12', 'Agente_dispute_Ch26', 'Agente_Ch02', 'Agent_LargePrint_Ch23',
        'Lecteur_Ch18', 'Lectrice_Ch22', 'Lecteur_Ch31', 'Lectrice_Ch21']
for (f, pos, o, a, d), n in zip(M.AGENTS + M.LECTEURS, noms): ROLES[pos] = n
ROLES[M.BIBLIOTHECAIRE[1]] = 'Bibliothecaire'
persos = {}
for e in [o for o in bpy.data.objects if o.type == 'EMPTY' and o.name.startswith('E_')]:
    p = (round(e.location.x, 2), round(e.location.y, 2))
    if e.name.startswith('E_Ch31') and e.animation_data and e.animation_data.action: n = 'Ross'
    else: n = next((v for k, v in ROLES.items() if abs(k[0] - p[0]) < .05 and abs(k[1] - p[1]) < .05), e.name)
    e.name = n; persos[n] = e
    for c in e.children: c.name = n + '_squelette'
# chaises, ordinateurs, livres : nommés d'après la personne la plus proche
def proche(o):
    return min(persos.items(), key=lambda kv: (kv[1].location.xy - o.location.xy).length)[0]
for o in list(bpy.data.objects):
    if o.type != 'EMPTY' or not o.instance_collection: continue
    c = o.instance_collection.name
    pref = {'Simple wooden chair': 'Chaise', 'Samsung Galaxy Book 2': 'Ordi', 'Stacked set of books': 'Livres',
            'Mcbook Laptop': 'Ordi_Ross', 'Coffee Cup': 'Tasse_Ross', 'Backpack': 'SacADos_Ross'}.get(c)
    if pref: o.name = pref if pref.endswith('Ross') else f'{pref}_{proche(o)}'
# tables (maillages) : nommées d'après leur position
for t, x, y in M.TABLES:
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.startswith(('Cylinder', 'plateau')) and abs(o.location.x - x) < .05 and abs(o.location.y - y) < .05 and abs(o.location.z - .735) < .01:
            o.name = 'Table_Ross' if (x, y) == (3.9, 3.7) else f'Table_{t}_{x}_{y}'
# une caméra par plan + marqueurs (la caméra active change toute seule en lisant la timeline)
for nom in M.PLANS:
    M.camera(nom, garder=True); c = sc.camera; c.name = 'CAM_' + nom
    for o in [o for o in bpy.data.objects if o.name in ('cible', 'lueur_ecran')]: o.name = ('Visee_' if o.name == 'cible' else 'Lueur_') + nom
    m = sc.timeline_markers.new(nom, frame=M.PLANS[nom][0]); m.camera = c
sc.frame_start, sc.frame_end = 1, 1920
bpy.ops.wm.save_as_mainfile(filepath=sortie)
print('OK', sortie)
