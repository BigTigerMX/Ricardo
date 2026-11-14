/* Motor del sitio. Sin dependencias.
   Un solo requestAnimationFrame reparte el trabajo: el scroll sólo levanta una
   bandera y el dibujo ocurre una vez por fotograma. Si algo falla al arrancar
   se quita la clase .js y el sitio queda entero y quieto: nunca a medias. */
(function () {
  'use strict';
  var raiz = document.documentElement;
  /* con «reducir movimiento» se mueve igual, sin paralaje y más despacio: ver el final de estilo.css */
  var suave = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var limita = function (v, a, b) { return v < a ? a : v > b ? b : v; };

  try { arrancar(); } catch (e) { raiz.classList.remove('js'); if (window.console) console.error(e); }

  function arrancar() {
    /* ───────── foliador: tres ruedas de dígitos ───────── */
    var caja = $('#foliador'), ruedas = [];
    if (caja) {
      caja.textContent = '';
      for (var k = 0; k < 3; k++) {
        var rueda = document.createElement('span'), tira = document.createElement('span');
        rueda.className = 'rueda'; tira.className = 'rueda__tira';
        for (var d = 0; d < 10; d++) { var i = document.createElement('i'); i.textContent = d; tira.appendChild(i); }
        rueda.appendChild(tira); caja.appendChild(rueda); ruedas.push(tira);
      }
    }
    var folioActual = -1;
    function folio(n) {
      if (n === folioActual) return; folioActual = n;
      var s = ('00' + n).slice(-3);
      ruedas.forEach(function (t, j) { t.style.setProperty('--n', s.charAt(j)); });
    }

    /* ───────── revelados ─────────
       No se usa IntersectionObserver: un elemento tapado por su propio
       clip-path, o desplazado fuera de una máscara con overflow oculto, tiene
       intersección cero y el observador nunca avisa. Se mira la caja (que el
       recorte no altera) desde el mismo bucle que ya atiende el scroll. */
    var porRevelar = $$('.rv, .rv-ln, .rv-x, .mat, .sello--cierre, .pliego').map(function (el) {
      return { el: el, sensor: el.classList.contains('rv-ln') ? el.parentNode : el };
    });
    function revelar(vh) {
      if (!porRevelar.length) return;
      var lote = 0, quedan = [];
      for (var i = 0; i < porRevelar.length; i++) {
        var it = porRevelar[i], r = it.sensor.getBoundingClientRect();
        if (r.top < vh * 0.9 && r.bottom > -40) {
          it.el.style.setProperty('--r', (Math.min(lote++, 8) * 0.07) + 's');   // los que entran juntos, escalonados
          it.el.classList.add('visto');
        } else quedan.push(it);
      }
      porRevelar = quedan;
    }

    /* ───────── índice activo ───────── */
    var enlaces = $$('.indice a'), secciones = enlaces.map(function (a) { return $(a.getAttribute('href')); });

    /* ───────── grabado: roseta de guilloché ─────────
       Cada banda es una familia de curvas r(θ) = r0 + a·sen(nθ + φ) con la fase
       repartida: al superponerse tejen el entrelazado del papel seguridad. */
    function Roseta(lienzo, opc) {
      this.c = lienzo; this.x = lienzo.getContext('2d'); this.o = opc;
      this.fase = 0; this.prog = 0; this.px = 0; this.py = 0; this.tx = 0; this.ty = 0; this.lado = 0;
    }
    Roseta.prototype.medir = function () {
      var r = this.c.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      var lado = Math.round(Math.max(r.width, 10) * dpr);
      if (lado !== this.lado) { this.lado = lado; this.c.width = lado; this.c.height = lado; this.dpr = dpr; }
    };
    Roseta.prototype.pintar = function () {
      var x = this.x, L = this.lado, R = L / 2 * 0.985, o = this.o, fin = Math.PI * 2 * this.prog, pasos = Math.max(24, Math.round(540 * this.prog));
      x.clearRect(0, 0, L, L); x.save(); x.translate(L / 2, L / 2);
      x.lineWidth = o.grosor * this.dpr; x.strokeStyle = o.color; x.lineJoin = 'round';
      for (var b = 0; b < o.bandas.length; b++) {
        var B = o.bandas[b], amp = B.a * (1 + this.px * 0.35 * (b % 2 ? -1 : 1));
        x.globalAlpha = B.alfa;
        for (var j = 0; j < B.k; j++) {
          var fi = (Math.PI * 2 * j) / B.k + this.fase * (b % 2 ? -1 : 1) * B.v;
          x.beginPath();
          for (var s = 0; s <= pasos; s++) {
            var t = fin * s / pasos;
            var r = R * (B.r + amp * Math.sin(B.n * t + fi) * (0.78 + 0.22 * Math.cos(B.m * t - this.fase * 0.6 + this.py * 2)));
            var X = r * Math.cos(t - Math.PI / 2), Y = r * Math.sin(t - Math.PI / 2);
            if (s) x.lineTo(X, Y); else x.moveTo(X, Y);
          }
          x.stroke();
        }
      }
      x.globalAlpha = o.alfaAro;
      for (var a = 0; a < o.aros.length; a++) { x.beginPath(); x.arc(0, 0, R * o.aros[a], -Math.PI / 2, -Math.PI / 2 + fin); x.stroke(); }
      x.restore();
    };

    var bandas = [
      { r: 0.86, a: 0.105, n: 24, m: 3, k: 12, v: 1.0, alfa: 0.28 },
      { r: 0.625, a: 0.115, n: 16, m: 4, k: 12, v: 1.4, alfa: 0.32 },
      { r: 0.39, a: 0.105, n: 10, m: 2, k: 10, v: 1.9, alfa: 0.36 },
      { r: 0.175, a: 0.085, n: 6, m: 3, k: 8, v: 2.6, alfa: 0.40 }
    ];
    var r1 = $('#roseta') && new Roseta($('#roseta'), { color: '#8FB1E6', grosor: 0.7, bandas: bandas, aros: [0.985, 0.745, 0.505, 0.275], alfaAro: 0.5 });
    var r2 = $('#roseta2') && new Roseta($('#roseta2'), { color: '#8FB1E6', grosor: 0.7, bandas: bandas.map(function (b) { return { r: b.r, a: b.a, n: b.n, m: b.m, k: b.k, v: b.v, alfa: b.alfa * 0.55 }; }), aros: [0.985, 0.745, 0.505, 0.275], alfaAro: 0.3 });
    var caratula = $('#caratula'), carbon = $('#contacto');
    var veR1 = true, veR2 = false;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.target === caratula) veR1 = e.isIntersecting; else veR2 = e.isIntersecting; }); }).observe(caratula);
      var o2 = new IntersectionObserver(function (es) { veR2 = es[0].isIntersecting; if (veR2 && r2 && !r2.hecho) { r2.hecho = true; r2.medir(); r2.prog = 1; r2.pintar(); } });
      o2.observe(carbon);
    }

    /* cenefa de la cédula: bandas onduladas de papel seguridad, se pintan una vez */
    function cenefa() {
      var c = $('#cenefa'); if (!c) return;
      var r = c.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      c.width = Math.round(r.width * dpr); c.height = Math.round(r.height * dpr);
      var x = c.getContext('2d'), W = c.width, H = c.height;
      x.clearRect(0, 0, W, H); x.lineWidth = 0.6 * dpr; x.strokeStyle = '#8FB1E6';
      function banda(y0, alto, n, k, alfa) {
        x.globalAlpha = alfa;
        for (var j = 0; j < k; j++) {
          x.beginPath();
          for (var px = 0; px <= W; px += 3 * dpr) {
            var t = px / W, y = y0 + alto * Math.sin(n * Math.PI * 2 * t + (Math.PI * 2 * j) / k) * (0.6 + 0.4 * Math.cos(Math.PI * 2 * t * 2));
            if (px) x.lineTo(px, y); else x.moveTo(px, y);
          }
          x.stroke();
        }
      }
      banda(H * 0.5, H * 0.46, 3, 26, 0.13);
      banda(H * 0.5, H * 0.3, 5, 18, 0.12);
      banda(H * 0.965, H * 0.03, 22, 4, 0.5);
      banda(H * 0.035, H * 0.03, 22, 4, 0.5);
    }

    /* ───────── legajo: fojas que se apilan ─────────
       La posición de cada foja se calcula con aritmética de scroll, no leyendo
       su caja ya transformada: medir lo que uno mismo acaba de mover da un
       valor distinto en cada fotograma. */
    var legajo = $('#legajo'), fojas = $$('.foja', legajo), geo = [], plano = false;
    function medirLegajo() {
      if (!legajo) return;
      legajo.classList.remove('legajo--plano');
      fojas.forEach(function (f) { f.style.transform = ''; });
      var sy = window.pageYOffset, libre = window.innerHeight, cabe = true;
      geo = fojas.map(function (f) {
        var cs = getComputedStyle(f), tope = parseFloat(cs.top) || 0, alto = f.offsetHeight;
        if (alto > libre - tope - 16) cabe = false;
        return { tope: tope, alto: alto, mb: parseFloat(cs.marginBottom) || 0 };
      });
      plano = !cabe;
      legajo.classList.toggle('legajo--plano', plano);
      if (plano) return;
      // tope natural (en documento) de cada foja: se obtiene soltándolas un instante
      fojas.forEach(function (f) { f.style.position = 'relative'; f.style.top = 'auto'; });
      fojas.forEach(function (f, i) { geo[i].nat = f.getBoundingClientRect().top + sy; });
      geo.fin = legajo.getBoundingClientRect().top + sy + legajo.offsetHeight;
      fojas.forEach(function (f) { f.style.position = ''; f.style.top = ''; });
    }
    function moverLegajo(sy) {
      if (plano || !geo.length) return;
      var n = fojas.length, y = [], i;
      for (i = 0; i < n; i++) {
        var g = geo[i], pos = Math.max(g.nat - sy, g.tope);
        pos = Math.min(pos, geo.fin - sy - g.alto - g.mb);         // el contenedor las arrastra al terminar
        y.push(pos);
      }
      var prof = 0;
      for (i = n - 1; i >= 0; i--) {
        var tapa = i < n - 1 ? limita((y[i] + geo[i].alto - y[i + 1]) / geo[i].alto, 0, 1) : 0;
        prof += tapa;
        var giro = (i % 2 ? 0.5 : -0.5) * Math.min(1, tapa * 1.4);
        fojas[i].style.transform = prof > 0.001 ? 'translateY(' + (-prof * 4).toFixed(2) + 'px) scale(' + (1 - 0.026 * prof).toFixed(4) + ') rotate(' + giro.toFixed(3) + 'deg)' : '';
      }
    }

    /* el grabado se centra en el sello: se mide la caja de maquetación (offset*),
       que no cambia mientras el sello cae girando */
    var selloC = $('.sello--caratula');
    function centrarGrabado() {
      if (!selloC || !caratula) return;
      caratula.style.setProperty('--cx', (selloC.offsetLeft + selloC.offsetWidth / 2).toFixed(1) + 'px');
      caratula.style.setProperty('--cy', (selloC.offsetTop + selloC.offsetHeight / 2).toFixed(1) + 'px');
    }

    /* ───────── bucle ───────── */
    var hilo = $('.margen__hilo'), nudo = $('.margen__nudo'), barra = $('#barra'), selloA = $$('.sello__anillo'), titulo = $('.clausula--clara .clausula__t');
    var cedula = $('#cedula'), marcas = $$('[data-foja]'), sucio = true, ultimo = 0, T0 = raiz.classList.contains('sin-telon') ? 0 : 1300, inicio = performance.now() + T0;
    var titulos = $$('.clausula__t'), foco = $('#foco'), cinta = $('#cinta');
    function alScroll() { sucio = true; }
    window.addEventListener('scroll', alScroll, { passive: true });
    window.addEventListener('resize', function () { centrarGrabado(); medirLegajo(); if (r1) r1.medir(); cenefa(); if (r2 && r2.hecho) { r2.medir(); r2.pintar(); } sucio = true; });

    function cuadro(ahora) {
      requestAnimationFrame(cuadro);
      var sy = window.pageYOffset, vh = window.innerHeight;
      if (sucio) {
        sucio = false;
        var total = Math.max(1, document.documentElement.scrollHeight - vh), p = limita(sy / total, 0, 1);
        if (hilo) hilo.style.setProperty('--p', (p * 100).toFixed(2) + '%');
        if (nudo) nudo.style.transform = 'translateY(' + (p * vh).toFixed(1) + 'px)';
        if (barra) barra.classList.toggle('barra--raya', sy > 8);
        for (var a = 0; a < selloA.length; a++) selloA[a].style.setProperty('--giro', (sy * 0.06).toFixed(2) + 'deg');
        if (r1) r1.c.style.setProperty('--giro', (sy * 0.022).toFixed(2) + 'deg');
        if (titulo && carbon) { var rc = carbon.getBoundingClientRect(); titulo.style.setProperty('--calco', (2 + limita(rc.top / vh, 0, 1) * 9).toFixed(1)); }
        if (cedula && !sobreCedula) cedula.style.setProperty('--ka', (30 + sy * 0.25).toFixed(1));
        moverLegajo(sy);
        revelar(vh);
        if (!suave) for (var ti = 0; ti < titulos.length; ti++) { var rt = titulos[ti].getBoundingClientRect(); if (rt.bottom > -200 && rt.top < vh + 200) titulos[ti].style.setProperty('--par', (((rt.top + rt.height / 2) / vh - 0.5) * (window.innerWidth < 700 ? 22 : 64)).toFixed(1)); }
        // foja en curso: la última marca cuyo borde superior ya pasó el 58 % de la ventana
        var n = 1;
        for (var m = 0; m < marcas.length; m++) { if (marcas[m].getBoundingClientRect().top < vh * 0.58) n = +marcas[m].getAttribute('data-foja'); }
        folio(n);
        var act = -1;
        for (var s = 0; s < secciones.length; s++) { if (secciones[s] && secciones[s].getBoundingClientRect().top < vh * 0.5) act = s; }
        enlaces.forEach(function (el, j) { el.classList.toggle('activo', j === act); });
      }
      // la roseta de la carátula: ~30 fps, sólo mientras se ve
      if (r1 && veR1 && !document.hidden && ahora - ultimo > 32) {
        var dt = Math.min(64, ahora - ultimo) / 1000; ultimo = ahora;
        if (r1.prog < 1) { var u = limita((ahora - inicio - 150) / 2300, 0, 1); r1.prog = 1 - Math.pow(1 - u, 3); }
        r1.fase += dt * (suave ? 0.05 : 0.11);
        r1.px += (r1.tx - r1.px) * 0.06; r1.py += (r1.ty - r1.py) * 0.06;
        r1.pintar();
      }
    }

    /* ───────── puntero ───────── */
    var sobreCedula = false;
    window.addEventListener('pointermove', function (e) {
      if (suave || !r1 || !veR1) return;   // el grabado no sigue al cursor
      r1.tx = (e.clientX / window.innerWidth - 0.5) * 2; r1.ty = (e.clientY / window.innerHeight - 0.5) * 2;
    }, { passive: true });
    var marco = $('.cedula-marco'), ced = $('#cedula');
    if (marco && ced) {
      marco.addEventListener('pointermove', function (e) {
        var r = marco.getBoundingClientRect(), fx = limita((e.clientX - r.left) / r.width, 0, 1), fy = limita((e.clientY - r.top) / r.height, 0, 1);
        sobreCedula = true;
        ced.style.setProperty('--ry', ((fx - 0.5) * 22).toFixed(2) + 'deg'); ced.style.setProperty('--rx', ((0.5 - fy) * 16).toFixed(2) + 'deg');
        ced.style.setProperty('--kx', (fx * 100).toFixed(1)); ced.style.setProperty('--ky', (fy * 100).toFixed(1)); ced.style.setProperty('--ka', (fx * 240).toFixed(1));
      });
      marco.addEventListener('pointerleave', function () { sobreCedula = false; ced.style.removeProperty('--rx'); ced.style.removeProperty('--ry'); });
    }
    // el golpe del sello sacude un instante el texto de la carátula
    setTimeout(function () { caratula.classList.add('caratula--golpe'); }, 1590 + T0);
    /* el foco sigue al cursor; las fojas llevan su propia luz por dentro */
    window.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch' || !foco) return;
      foco.style.setProperty('--fx', e.clientX + 'px'); foco.style.setProperty('--fy', e.clientY + 'px'); foco.classList.add('foco--on');
      var f = e.target.closest && e.target.closest('.foja');
      if (f) { var r = f.getBoundingClientRect(); f.style.setProperty('--px', (e.clientX - r.left) + 'px'); f.style.setProperty('--py', (e.clientY - r.top) + 'px'); }
    }, { passive: true });
    /* botones con imán: se acercan un poco al cursor */
    if (window.matchMedia('(hover: hover)').matches) $$('.boton, .ficha').forEach(function (b) {
      b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); b.style.translate = ((e.clientX - r.left - r.width / 2) * 0.16).toFixed(1) + 'px ' + ((e.clientY - r.top - r.height / 2) * 0.26).toFixed(1) + 'px'; });
      b.addEventListener('pointerleave', function () { b.style.translate = ''; });
    });

    /* ───────── idioma ───────── */
    var boton = $('.idioma'), traducibles = $$('[data-en]'), conAttr = $$('*').filter(function (el) {
      for (var i = 0; i < el.attributes.length; i++) if (el.attributes[i].name.indexOf('data-en-') === 0) return true; return false;
    });
    var titulos = { es: document.title, en: 'Luis Ricardo Garrido Mendoza · Attorney' };
    /* la cinta se arma con las materias de la tabla, en el idioma que esté puesto */
    function armarCinta() {
      if (!cinta) return;
      var m = $$('.mat__t').map(function (e) { return e.textContent; }); if (!m.length) return;
      var fila = function (lista) { var h = lista.map(function (t) { return '<span>' + t.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span><i></i>'; }).join(''); return '<div class="cinta__fila">' + h + h + '</div>'; };
      cinta.innerHTML = fila(m) + fila(m.slice().reverse());
    }
    function poner(l) {
      traducibles.forEach(function (el) {
        if (el.dataset.es === undefined) el.dataset.es = el.innerHTML;
        el.innerHTML = l === 'en' ? el.dataset.en : el.dataset.es;
      });
      conAttr.forEach(function (el) {
        Array.prototype.slice.call(el.attributes).forEach(function (at) {
          if (at.name.indexOf('data-en-') !== 0) return;
          var destino = at.name.slice(8), guarda = 'data-es-' + destino;
          if (!el.hasAttribute(guarda)) el.setAttribute(guarda, el.getAttribute(destino) || '');
          el.setAttribute(destino, l === 'en' ? at.value : el.getAttribute(guarda));
        });
      });
      raiz.lang = l; document.title = titulos[l];
      try { localStorage.setItem('idioma', l); } catch (e) {}
      armarCinta(); centrarGrabado(); medirLegajo(); sucio = true;
    }
    var barrido = null;
    function cambiar() {
      var l = raiz.lang === 'es' ? 'en' : 'es';
      if (!document.body.animate) { poner(l); return; }
      // una hoja de tinta cruza la pantalla y el texto cambia cuando la tapa entera
      if (!barrido) { barrido = document.createElement('div'); barrido.setAttribute('aria-hidden', 'true'); barrido.style.cssText = 'position:fixed;inset:0;z-index:40;background:#14284A;transform:translateY(-101%);pointer-events:none'; document.body.appendChild(barrido); }
      var an = barrido.animate([{ transform: 'translateY(-101%)' }, { transform: 'translateY(0)', offset: 0.5 }, { transform: 'translateY(101%)' }], { duration: 820, easing: 'cubic-bezier(.7,0,.3,1)' });
      setTimeout(function () { poner(l); }, 410);
      an.onfinish = function () { barrido.style.transform = 'translateY(-101%)'; };
    }
    if (boton) boton.addEventListener('click', cambiar);
    var guardado = null; try { guardado = localStorage.getItem('idioma'); } catch (e) {}
    if (guardado === 'en') poner('en');

    /* ───────── copiar el correo ───────── */
    $$('.copiar').forEach(function (b) {
      b.addEventListener('click', function () {
        var txt = b.getAttribute('data-copiar'), et = $('span', b), antes = et.innerHTML;
        function listo() { b.classList.add('hecho'); et.textContent = b.getAttribute('data-ok'); setTimeout(function () { b.classList.remove('hecho'); et.innerHTML = antes; }, 1700); }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(listo, listo);
        else { var t = document.createElement('textarea'); t.value = txt; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (e) {} t.remove(); listo(); }
      });
    });

    /* ───────── arranque ───────── */
    armarCinta(); centrarGrabado(); if (r1) r1.medir();
    cenefa(); medirLegajo();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { centrarGrabado(); medirLegajo(); cenefa(); sucio = true; });
    window.addEventListener('load', function () { centrarGrabado(); medirLegajo(); sucio = true; });
    requestAnimationFrame(cuadro);
  }
})();
