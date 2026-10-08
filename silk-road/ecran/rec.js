// node rec.js → ecran.mp4 (1280×800, 30 i/s, 6 s)
const {chromium}=require(process.env.PW);const {spawn}=require('child_process');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});
await p.goto('http://127.0.0.1:8765/truestory/silk-road/ecran/ecran.html');await p.waitForFunction('window.ready');
const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',__dirname+'/ecran.mp4']);
for(let i=0;i<180;i++){await p.evaluate(t=>renderAt(t),i/30);ff.stdin.write(await p.screenshot({type:'jpeg',quality:95}));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();})();
