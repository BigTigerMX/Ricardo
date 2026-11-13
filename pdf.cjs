// Imprime un HTML a PDF tamaño carta con Chromium. Uso: node pdf.cjs entrada.html salida.pdf [png]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [ent, sal, png] = process.argv.slice(2);
  const nav = await chromium.launch({ args: ['--no-sandbox'] });
  const pg = await nav.newPage({ viewport: { width: 816, height: 1056 } });
  await pg.goto('file://' + ent, { waitUntil: 'load' });
  await pg.evaluate(() => document.fonts.ready);
  const alto = await pg.evaluate(() => document.querySelector('.hoja').scrollHeight);
  await pg.pdf({ path: sal, format: 'Letter', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
  if (png) { await pg.setViewportSize({ width: 816, height: 1056 }); await pg.screenshot({ path: png, fullPage: true }); }
  console.log(alto);
  await nav.close();
})();
