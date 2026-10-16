// Capture image par image d'une page [CODE] (HTML / Three.js) → MP4.
// La page doit définir window.renderAt(t) (t en secondes) et window.ready = true.
// Usage : node capture.js <page.html relative au dépôt> <sortie.mp4> <durée s> [fps=30] [largeur=1920] [hauteur=804]
// Navigateur : Edge installé sur Windows (pas de téléchargement). Petit serveur local pour les modules ES.
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { chromium } = require('playwright-core');
const RACINE = path.resolve(__dirname, '..', '..');
const [page_, sortie, duree, fps = 30, W = 1920, H = 804] = process.argv.slice(2);
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.mp4': 'video/mp4', '.json': 'application/json', '.glb': 'model/gltf-binary', '.ttf': 'font/ttf' };
const serveur = http.createServer((req, res) => {
  const f = path.join(RACINE, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(RACINE) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(0, '127.0.0.1', async () => {
  const port = serveur.address().port;
  const b = await chromium.launch({ channel: 'msedge', ignoreDefaultArgs: ['--headless=old'], args: ['--headless=new', '--enable-gpu-rasterization', '--ignore-gpu-blocklist'] });   // Edge récent : plus d'ancien mode headless
  const p = await b.newPage({ viewport: { width: +W, height: +H } });
  p.on('console', m => m.type() === 'error' && console.error('page:', m.text()));
  await p.goto(`http://127.0.0.1:${port}/${page_.replace(/\\/g, '/')}`);
  await p.waitForFunction('window.ready === true', null, { timeout: 60000 });
  const n = Math.round(duree * fps);
  const ff = spawn('C:\\ffmpeg\\bin\\ffmpeg.exe', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', sortie]);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.renderAt(t), i / fps);
    ff.stdin.write(await p.screenshot({ type: 'png' }));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await b.close(); serveur.close(); console.log('OK', sortie, n, 'images');
});
