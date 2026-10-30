import json, subprocess, os
from playwright.sync_api import sync_playwright
C=json.load(open('/home/claude/voix/calage.json'))
D=265.40; W,H,FPS=1280,536,24
R='/home/claude/'
S={'rue':R+'ruelle/v5_rue_large.png','lune':R+'ruelle/v5_ciel_lune.png','fenetre':R+'ruelle/v5_montee_fenetre.png',
   'ch_large':R+'rendu/chambre_v8_large.png','ch_dos':R+'rendu/chambre_v8_dos.png','ch_contre':R+'rendu/chambre_v8_contrechamp.png','ch_chevet':R+'rendu/chambre_v8_chevet.png',
   'serveurs':R+'rendu/D3_f090.png','crise':R+'decors/crise_large.png','crise_eq':R+'decors/crise_equipe.png','bureau':R+'decors/bureau_large.png','bureau_fil':R+'decors/bureau_fil.png'}
# (phrase de départ, visuel)  visuel = 'code:<scene>' | 'p12' | clé d'image fixe (+ ':in' zoom avant / ':out' zoom arrière)
PL=[(0,'code:horodatage'),(3,'rue:in'),(5,'lune:in'),(7,'fenetre:in'),(11,'ch_large:in'),(14,'ch_dos:in'),(19,'code:ecran'),(20,'ch_dos:out'),(22,'code:montant'),(25,'lune:out'),
 (27,'code:rembobine'),(29,'serveurs:in'),(33,'code:nonce'),(37,'p12'),(41,'code:transaction'),(47,'code:chaines'),
 (52,'code:forteresse'),(56,'code:frise'),(61,'code:safu'),(64,'code:fois'),
 (65,'code:alerte'),(68,'code:postcz'),(70,'crise:in'),(73,'code:reprise'),(74,'crise_eq:in'),
 (75,'code:jauges'),(82,'code:aave'),(83,'code:suspendu'),(86,'crise:out'),(87,'crise_eq:out'),(90,'code:bilan'),
 (93,'code:marche'),
 (97,'code:schema'),(98,'bureau:in'),(105,'code:schema'),(109,'bureau_fil:in'),(111,'bureau:out'),(115,'bureau_fil:out'),
 (116,'code:bybit'),(124,'bureau_fil:in'),
 (127,'fenetre:out'),(128,'ch_contre:in'),(129,'code:suspects'),
 (135,'code:maj'),(138,'crise:in'),(142,'ch_chevet:in'),(143,'rue:out'),(145,'fenetre:in'),(146,'code:final')]
deb=[C[i]['deb'] for i,_ in PL]; fin=deb[1:]+[D]
plans=[(v,a,b-a) for (i,v),a,b in zip(PL,deb,fin) if b-a>0.05]
liste=[]
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':804})
    for k,(v,a,d) in enumerate(plans):
        out=f'clips/{k:03d}.mp4'; liste.append(out); n=max(1,round(d*FPS))
        if os.path.exists(out): continue
        if v.startswith('code:') or v=='p12':
            os.makedirs('fr',exist_ok=True); [os.remove('fr/'+f) for f in os.listdir('fr')]
            if v=='p12': url='file://'+R+'plan12/p12.html?frame=%d'
            else: url='file://'+R+'true_stories/videos/binance-hack/code/plans.html?s='+v[5:]+'&t=%s'
            for f in range(n):
                t=f/FPS
                pg.goto(url%(int(t*30) if v=='p12' else f'{t:.3f}')); pg.wait_for_function('window.FRAME_PRET===true')
                pg.screenshot(path=f'fr/{f:05d}.jpg',type='jpeg',quality=88)
            subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i','fr/%05d.jpg','-vf',f'scale={W}:{H}','-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p',out],check=True)
        else:
            cle,sens=v.split(':'); z0,z1=(1.0,1.12) if sens=='in' else (1.12,1.0)
            zp=f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}"
            subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',S[cle],'-vf',f'scale=3840:-2,{zp},format=yuv420p','-frames:v',str(n),'-c:v','libx264','-preset','veryfast',out],check=True)
        print('PLAN',k,v,round(d,2),flush=True)
    br.close()
open('liste.txt','w').write(''.join(f"file '{x}'\n" for x in liste))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','liste.txt','-c','copy','video_muette.mp4'],check=True)
# voix + texte obligatoire « scène illustrée » pendant le cold open + bandes 2,39:1
dt="drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='Scène illustrée — l’identité et le lieu des pirates sont inconnus':fontcolor=white@0.8:fontsize=16:x=(w-text_w)/2:y=h-38:enable='between(t,3,10)'"
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','video_muette.mp4','-i','/home/claude/voix/vo_complete.mp3','-vf',dt,'-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','160k','-shortest','binance_brouillon_v1.mp4'],check=True)
print('FINI')
