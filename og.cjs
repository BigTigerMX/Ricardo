// Tarjeta para compartir (1200×630): lo que enseñan WhatsApp y LinkedIn al pegar el enlace.
const fs = require('fs'), path = require('path'); const { chromium } = require('/opt/node-tools/node_modules/playwright');
const G = JSON.parse(fs.readFileSync(path.join(__dirname, 'prueba/glifos.json'), 'utf8')).romana;
const F = 'file://' + path.join(__dirname, 'sitio/fuentes');
const html = `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:B;src:url(${F}/bodoni-moda.woff2);font-weight:400 900}
@font-face{font-family:B;src:url(${F}/bodoni-moda-cursiva.woff2);font-weight:400 900;font-style:italic}
@font-face{font-family:M;src:url(${F}/plex-mono-medium.woff2)}
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;position:relative;color:#E8EBF0;background:radial-gradient(circle 620px at 1020px 360px,#12233F 0%,rgba(18,35,63,.5) 42%,rgba(18,35,63,0) 72%),#16181C}
canvas{position:absolute;left:570px;top:-90px}
.t{position:absolute;left:72px;top:92px}
.r{font:500 19px M;letter-spacing:.17em;color:#8FB1E6;text-transform:uppercase}
h1{margin-top:26px;font:500 96px/.9 B;letter-spacing:-.035em}
h1 i{display:block;font-weight:400;color:#8FB1E6}
.m{margin-top:34px;font:italic 500 33px/1.2 B;max-width:640px}
.s{position:absolute;left:890px;top:230px;width:260px;height:260px;color:#C8D0DC;transform:rotate(-9deg);filter:drop-shadow(0 2px 0 rgba(0,0,0,.65))}
.s svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.l{position:absolute;left:36px;top:0;bottom:0;width:5px;border-inline:1px solid rgba(143,177,230,.22)}
</style><div class="l"></div><canvas id="c" width="900" height="900"></canvas>
<div class="t"><p class="r">Abogado · Cédula profesional 15649339</p><h1><i>Luis Ricardo</i>Garrido Mendoza</h1><p class="m">Derecho mercantil, contratos y asuntos corporativos.</p></div>
<div class="s"><svg viewBox="0 0 400 400"><defs><path id="ci" d="M200,200 m-158,0 a158,158 0 1,1 316,0 a158,158 0 1,1 -316,0"/></defs>
<g fill="none" stroke="currentColor"><circle cx="200" cy="200" r="194" stroke-width="3"/><circle cx="200" cy="200" r="186"/><circle cx="200" cy="200" r="134"/><circle cx="200" cy="200" r="127" stroke-width="2.5" stroke-dasharray="1.5 5.2"/></g>
<text font-family="M" font-size="19" fill="currentColor"><textPath href="#ci" textLength="984">LUIS RICARDO GARRIDO MENDOZA • ABOGADO • CÉDULA PROFESIONAL 15649339 •</textPath></text>
<svg x="112" y="118" width="176" height="150" viewBox="-60 -330 2570 2180"><path d="${G.R.d}" transform="translate(0 1250) scale(1 -1)" fill="currentColor"/><path d="${G.M.d}" transform="translate(760 1750) scale(1 -1)" fill="currentColor"/></svg></svg></div>
<script>const x=document.getElementById('c').getContext('2d'),R=445;x.translate(450,450);x.strokeStyle='#8FB1E6';x.lineWidth=.8;
[[.86,.105,24,3,12,.28],[.625,.115,16,4,12,.32],[.39,.105,10,2,10,.36],[.175,.085,6,3,8,.4]].forEach(([r0,a,n,m,k,al])=>{x.globalAlpha=al;for(let j=0;j<k;j++){x.beginPath();for(let s=0;s<=540;s++){const t=Math.PI*2*s/540,r=R*(r0+a*Math.sin(n*t+Math.PI*2*j/k)*(.78+.22*Math.cos(m*t)));s?x.lineTo(r*Math.cos(t),r*Math.sin(t)):x.moveTo(r*Math.cos(t),r*Math.sin(t))}x.stroke()}});
x.globalAlpha=.5;[.985,.745,.505,.275].forEach(q=>{x.beginPath();x.arc(0,0,R*q,0,7);x.stroke()});</script>`;
(async () => { const nav = await chromium.launch({ args: ['--no-sandbox'] }); const pg = await nav.newPage({ viewport: { width: 1200, height: 630 } });
  fs.writeFileSync(path.join(__dirname, 'cv-trabajo/og.html'), html);
  await pg.goto('file://' + path.join(__dirname, 'cv-trabajo/og.html')); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(400);
  await pg.screenshot({ path: path.join(__dirname, 'sitio/tarjeta-social.jpg'), type: 'jpeg', quality: 88 }); await nav.close(); console.log('tarjeta lista'); })();
