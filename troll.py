import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="InfoLatam - Noticias", page_icon=":newspaper:", layout="centered")

st.markdown(
    "<style>#MainMenu,header,footer{visibility:hidden;}"
    ".block-container{padding:0 !important;max-width:100% !important;}"
    "iframe{border:none !important;}</style>",
    unsafe_allow_html=True,
)

HTML = r"""
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family:'Segoe UI',system-ui,sans-serif; background:#f4f4f4; color:#222; }
  a { color:inherit; text-decoration:none; cursor:pointer; }

  /* NAV */
  nav { background:#c0392b; color:#fff; padding:0 24px; display:flex; align-items:center; height:52px; gap:28px; position:sticky; top:0; z-index:10; box-shadow:0 2px 6px rgba(0,0,0,.25); }
  nav .brand { font-size:1.35em; font-weight:800; letter-spacing:1px; }
  nav .links { display:flex; gap:20px; font-size:.92em; }
  nav .links a:hover { text-decoration:underline; }
  nav .sub-btn { margin-left:auto; background:#fff; color:#c0392b; border:none; border-radius:4px; padding:7px 16px; font-weight:700; font-size:.88em; cursor:pointer; }
  nav .sub-btn:hover { background:#ffe0de; }

  /* BREAKING */
  .breaking { background:#222; color:#fff; font-size:.82em; padding:6px 24px; display:flex; gap:12px; align-items:center; }
  .breaking .tag { background:#c0392b; padding:2px 8px; border-radius:2px; font-weight:700; flex-shrink:0; }
  .breaking .ticker { overflow:hidden; white-space:nowrap; }

  /* HERO */
  .hero { position:relative; overflow:hidden; cursor:pointer; }
  .hero-img { width:100%; height:360px; object-fit:cover; display:block; background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); }
  .hero-img-inner { width:100%; height:360px; background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
    display:flex; align-items:center; justify-content:center; }
  .hero-img-inner span { font-size:80px; }
  .hero-overlay { position:absolute; bottom:0; left:0; right:0; background:linear-gradient(transparent,rgba(0,0,0,.82)); padding:28px 24px 22px; color:#fff; }
  .hero-cat { background:#c0392b; font-size:.75em; font-weight:700; padding:2px 10px; border-radius:2px; display:inline-block; margin-bottom:8px; }
  .hero-title { font-size:1.7em; font-weight:800; line-height:1.25; margin-bottom:8px; }
  .hero-meta { font-size:.82em; opacity:.75; }
  .hero:hover .hero-title { text-decoration:underline; }

  /* LAYOUT */
  .container { max-width:1100px; margin:0 auto; padding:24px 16px; display:grid; grid-template-columns:1fr 320px; gap:24px; }
  @media(max-width:720px){ .container{ grid-template-columns:1fr; } }

  /* ARTICLE GRID */
  .grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-bottom:24px; }
  @media(max-width:540px){ .grid{ grid-template-columns:1fr; } }
  .card { background:#fff; border-radius:6px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,.1); cursor:pointer; transition:box-shadow .15s; }
  .card:hover { box-shadow:0 4px 16px rgba(0,0,0,.18); }
  .card-thumb { width:100%; height:140px; display:flex; align-items:center; justify-content:center; font-size:52px; }
  .card-body { padding:14px; }
  .card-cat { font-size:.72em; font-weight:700; color:#c0392b; text-transform:uppercase; margin-bottom:4px; }
  .card-title { font-size:.97em; font-weight:700; line-height:1.3; margin-bottom:8px; }
  .card-title:hover { text-decoration:underline; }
  .card-meta { font-size:.75em; color:#777; display:flex; justify-content:space-between; align-items:center; }
  .read-more { font-size:.78em; font-weight:700; color:#c0392b; border:1px solid #c0392b; padding:3px 10px; border-radius:3px; cursor:pointer; margin-top:8px; display:inline-block; }
  .read-more:hover { background:#c0392b; color:#fff; }

  /* LIST ARTICLE */
  .list-art { display:flex; gap:12px; background:#fff; border-radius:6px; padding:12px; margin-bottom:12px; cursor:pointer; box-shadow:0 1px 3px rgba(0,0,0,.08); }
  .list-art:hover { box-shadow:0 4px 12px rgba(0,0,0,.14); }
  .list-thumb { width:80px; height:62px; flex-shrink:0; border-radius:4px; display:flex; align-items:center; justify-content:center; font-size:30px; }
  .list-body .cat { font-size:.7em; font-weight:700; color:#c0392b; }
  .list-body .title { font-size:.88em; font-weight:600; line-height:1.3; margin:2px 0 4px; }
  .list-body .meta { font-size:.72em; color:#888; }

  /* SIDEBAR */
  .sidebar {}
  .widget { background:#fff; border-radius:6px; padding:16px; margin-bottom:18px; box-shadow:0 1px 4px rgba(0,0,0,.1); }
  .widget h3 { font-size:.9em; font-weight:800; text-transform:uppercase; letter-spacing:.5px; border-bottom:2px solid #c0392b; padding-bottom:6px; margin-bottom:12px; }
  .trending-item { display:flex; gap:10px; align-items:flex-start; margin-bottom:10px; cursor:pointer; }
  .trending-item:hover .t-title { text-decoration:underline; }
  .t-num { font-size:1.4em; font-weight:900; color:#e0e0e0; line-height:1; }
  .t-title { font-size:.85em; font-weight:600; line-height:1.3; }
  .weather-box { text-align:center; padding:8px 0; }
  .weather-city { font-size:.85em; color:#777; margin-bottom:4px; }
  .weather-icon { font-size:2.8em; }
  .weather-temp { font-size:2em; font-weight:300; margin:4px 0; }
  .weather-desc { font-size:.82em; color:#555; }
  .weather-row { display:flex; justify-content:space-around; margin-top:12px; font-size:.78em; color:#666; }
  .weather-row div { text-align:center; }
  .weather-row span { display:block; font-size:1.3em; }
  .newsletter-input { width:100%; padding:8px 10px; border:1px solid #ccc; border-radius:4px; font-size:.88em; margin-bottom:8px; }
  .newsletter-btn { width:100%; background:#c0392b; color:#fff; border:none; border-radius:4px; padding:9px; font-weight:700; font-size:.88em; cursor:pointer; }
  .newsletter-btn:hover { background:#a93226; }

  /* MORE BTN */
  .more-btn { display:block; width:100%; background:#fff; border:2px solid #c0392b; color:#c0392b; border-radius:5px; padding:11px; font-weight:700; font-size:.95em; cursor:pointer; text-align:center; margin-bottom:24px; }
  .more-btn:hover { background:#c0392b; color:#fff; }

  /* FOOTER */
  footer { background:#1a1a1a; color:#aaa; text-align:center; padding:22px; font-size:.82em; }
  footer strong { color:#fff; }
  footer nav { background:transparent; padding:0; height:auto; justify-content:center; gap:18px; flex-wrap:wrap; margin-bottom:10px; color:#aaa; font-size:.9em; }
  footer nav a:hover { color:#fff; }

  /* OVERLAYS */
  #bsod,#black,#bios,#popups,#flash { display:none; position:fixed; inset:0; }
  #bsod { z-index:1000; background:#0067c0; color:#fff; flex-direction:column;
    align-items:center; justify-content:center; text-align:center; padding:6vw;
    font-family:'Segoe UI',system-ui,sans-serif; }
  #spinner { width:64px; height:64px; margin-bottom:34px; border:7px solid rgba(255,255,255,.25);
    border-top-color:#fff; border-radius:50%; animation:spin 1s linear infinite; }
  #black { z-index:1001; background:#000; color:#e8e8e8; font-family:'Consolas','Courier New',monospace;
    font-size:14px; line-height:1.35; padding:40px 18px; overflow:hidden; }
  #log { white-space:pre-wrap; height:100%; overflow:hidden; }
  .safemode { position:fixed; color:#fff; font-size:13px; opacity:.9; font-family:'Segoe UI',system-ui,sans-serif; z-index:2; }
  .sm-tl{top:10px;left:16px}.sm-tr{top:10px;right:16px}.sm-bl{bottom:10px;left:16px}.sm-br{bottom:10px;right:16px}
  .sm-top{top:10px;left:50%;transform:translateX(-50%);text-align:center;opacity:.8}
  #bios { z-index:1001; background:#0000a8; color:#c6c6c6; font-family:'Courier New',monospace; }
  #popups { z-index:1002; pointer-events:none; }
  #flash { z-index:1005; pointer-events:none; background:rgba(0,0,0,0); }

  @keyframes spin { to { transform:rotate(360deg); } }
  @keyframes blink { 50% { opacity:0; } }
  @keyframes popin { from { transform:scale(.96); opacity:0; } to { transform:scale(1); opacity:1; } }
  #cur { animation:blink 1s step-end infinite; }
  .err { color:#ff4d4d; font-weight:bold; }
  .okline { color:#56d364; }

  /* Windows dialogs */
  .win { position:fixed; background:#f0f0f0; border:1px solid #808080; color:#000;
    font-family:'Segoe UI',system-ui,sans-serif; font-size:13px; box-shadow:0 12px 34px rgba(0,0,0,.5); pointer-events:auto; animation:popin .1s ease-out; }
  .w10-title { display:flex; align-items:center; height:30px; background:#fff; }
  .w10-ic { margin:0 8px 0 10px; display:flex; }
  .w10-ic svg,.w10-big svg { display:block; }
  .w10-name { font-size:12px; color:#000; flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .w10-x { width:46px; height:30px; display:flex; align-items:center; justify-content:center; cursor:pointer; color:#555; font-size:11px; }
  .w10-x:hover { background:#e81123; color:#fff; }
  .w10-body { display:flex; gap:14px; align-items:flex-start; padding:20px 20px 22px; background:#fff; }
  .w10-big { flex-shrink:0; }
  .w10-body .msg { padding-top:4px; line-height:1.45; color:#1a1a1a; }
  .w10-btns { display:flex; justify-content:flex-end; align-items:center; gap:0; padding:12px 14px 14px; background:#f0f0f0; }
  .w10-b { min-width:76px; height:26px; padding:0 14px; margin-left:8px; background:#e1e1e1;
    border:1px solid #adadad; color:#000; font-size:13px; cursor:pointer; }
  .w10-b:hover { background:#e5f1fb; border-color:#0078d7; }
  .w10-b.def { border-color:#0078d7; }
  .w10-b.def:hover { background:#cce4f7; }
</style>

<!-- NAV -->
<nav>
  <span class="brand">INFO<span style="font-weight:300">latam</span></span>
  <div class="links">
    <a>Mundo</a><a>Tecnolog&iacute;a</a><a>Econom&iacute;a</a><a>Deportes</a><a>Ciencia</a>
  </div>
  <button class="sub-btn">Suscribirse</button>
</nav>

<!-- BREAKING NEWS TICKER -->
<div class="breaking">
  <span class="tag">AHORA</span>
  <span class="ticker">Mercados mundiales cierran en verde por tercera semana consecutiva &nbsp;&bull;&nbsp; Cient&iacute;ficos anuncian avance en almacenamiento de energ&iacute;a &nbsp;&bull;&nbsp; Nuevo acuerdo comercial entre bloques econ&oacute;micos entra en vigor este lunes</span>
</div>

<!-- HERO -->
<div class="hero" id="hero">
  <div class="hero-img-inner"><span>&#127758;</span></div>
  <div class="hero-overlay">
    <span class="hero-cat">Internacional</span>
    <div class="hero-title">Cumbre global de tecnolog&iacute;a: los pa&iacute;ses debaten nuevas regulaciones para la inteligencia artificial</div>
    <div class="hero-meta">Redacci&oacute;n &middot; Hace 38 minutos</div>
  </div>
</div>

<!-- MAIN CONTENT -->
<div class="container">
  <div class="main">
    <!-- GRID 2 COLUMNAS -->
    <div class="grid">
      <div class="card">
        <div class="card-thumb" style="background:#eaf4fb;">&#128752;</div>
        <div class="card-body">
          <div class="card-cat">Econom&iacute;a</div>
          <div class="card-title">Banco Central mantiene tasa de inter&eacute;s ante se&ntilde;ales de inflaci&oacute;n moderada</div>
          <div class="card-meta"><span>Hace 1 hora</span><span>4 min</span></div>
          <div class="read-more">Leer m&aacute;s &rarr;</div>
        </div>
      </div>
      <div class="card">
        <div class="card-thumb" style="background:#fef9e7;">&#9917;</div>
        <div class="card-body">
          <div class="card-cat">Deportes</div>
          <div class="card-title">Copa Am&eacute;rica: selecciones confirman planteles para el torneo de julio</div>
          <div class="card-meta"><span>Hace 2 horas</span><span>3 min</span></div>
          <div class="read-more">Leer m&aacute;s &rarr;</div>
        </div>
      </div>
      <div class="card">
        <div class="card-thumb" style="background:#f0fff4;">&#129516;</div>
        <div class="card-body">
          <div class="card-cat">Ciencia</div>
          <div class="card-title">Nueva cepa de bacteria capaz de degradar pl&aacute;sticos en ambientes fr&iacute;os</div>
          <div class="card-meta"><span>Hace 3 horas</span><span>5 min</span></div>
          <div class="read-more">Leer m&aacute;s &rarr;</div>
        </div>
      </div>
      <div class="card">
        <div class="card-thumb" style="background:#fdf2f8;">&#128248;</div>
        <div class="card-body">
          <div class="card-cat">Tecnolog&iacute;a</div>
          <div class="card-title">El nuevo procesador que promete duplicar la autonom&iacute;a en dispositivos m&oacute;viles</div>
          <div class="card-meta"><span>Hace 4 horas</span><span>6 min</span></div>
          <div class="read-more">Leer m&aacute;s &rarr;</div>
        </div>
      </div>
    </div>

    <!-- MAS NOTICIAS (lista) -->
    <div class="list-art">
      <div class="list-thumb" style="background:#fdebd0;">&#127946;</div>
      <div class="list-body">
        <div class="cat">Salud</div>
        <div class="title">OMS recomienda nuevas pautas para el descanso nocturno en adultos mayores de 40 a&ntilde;os</div>
        <div class="meta">Hace 5 horas &middot; 4 min de lectura</div>
      </div>
    </div>
    <div class="list-art">
      <div class="list-thumb" style="background:#eaf4fb;">&#9992;</div>
      <div class="list-body">
        <div class="cat">Mundo</div>
        <div class="title">Acuerdo de paz en zona de conflicto: negociadores anuncian cese al fuego indefinido</div>
        <div class="meta">Hace 6 horas &middot; 7 min de lectura</div>
      </div>
    </div>
    <div class="list-art">
      <div class="list-thumb" style="background:#f0fff4;">&#127807;</div>
      <div class="list-body">
        <div class="cat">Medio Ambiente</div>
        <div class="title">Estudio revela r&eacute;cord hist&oacute;rico en reforestaci&oacute;n: 40 millones de &aacute;rboles plantados este a&ntilde;o</div>
        <div class="meta">Hace 7 horas &middot; 3 min de lectura</div>
      </div>
    </div>

    <button class="more-btn">Cargar m&aacute;s noticias &#8595;</button>
  </div>

  <!-- SIDEBAR -->
  <div class="sidebar">
    <!-- WEATHER -->
    <div class="widget">
      <h3>El tiempo hoy</h3>
      <div class="weather-box">
        <div class="weather-city">Santiago, Chile</div>
        <div class="weather-icon">&#9925;</div>
        <div class="weather-temp">19&deg;C</div>
        <div class="weather-desc">Parcialmente nublado</div>
        <div class="weather-row">
          <div><span>&#127774;</span>M&aacute;x 22&deg;</div>
          <div><span>&#127770;</span>M&iacute;n 11&deg;</div>
          <div><span>&#127783;</span>Lluvia 10%</div>
        </div>
      </div>
    </div>

    <!-- TRENDING -->
    <div class="widget">
      <h3>Lo m&aacute;s le&iacute;do</h3>
      <div class="trending-item">
        <div class="t-num">1</div>
        <div class="t-title">Gigante tecnol&oacute;gico anuncia despidos masivos y reestructuraci&oacute;n global</div>
      </div>
      <div class="trending-item">
        <div class="t-num">2</div>
        <div class="t-title">C&oacute;mo afectar&aacute; el nuevo impuesto digital a los usuarios de plataformas de streaming</div>
      </div>
      <div class="trending-item">
        <div class="t-num">3</div>
        <div class="t-title">Descubren ex&oacute;planeta con condiciones similares a la Tierra a 40 a&ntilde;os luz</div>
      </div>
      <div class="trending-item">
        <div class="t-num">4</div>
        <div class="t-title">Record absoluto en bolsa de valores: &iacute;ndice supera por primera vez la barrera hist&oacute;rica</div>
      </div>
      <div class="trending-item">
        <div class="t-num">5</div>
        <div class="t-title">El equipo que lidera las eliminatorias con juego impecable en defensa y ataque</div>
      </div>
    </div>

    <!-- NEWSLETTER -->
    <div class="widget">
      <h3>Newsletter</h3>
      <p style="font-size:.85em; color:#555; margin-bottom:12px;">Recibe las noticias del d&iacute;a en tu correo, gratis.</p>
      <input class="newsletter-input" type="email" placeholder="Tu correo electr&oacute;nico">
      <button class="newsletter-btn">Suscribirme gratis</button>
    </div>
  </div>
</div>

<!-- FOOTER -->
<footer>
  <nav>
    <a>Inicio</a><a>Mundo</a><a>Tecnolog&iacute;a</a><a>Econom&iacute;a</a>
    <a>Deportes</a><a>Ciencia</a><a>Contacto</a><a>Privacidad</a>
  </nav>
  &copy; 2026 <strong>INFOlatam</strong>. Todos los derechos reservados.
</footer>

<!-- OVERLAYS (efectos) -->
<div id="bsod">
  <div id="spinner"></div>
  <div style="font-size:2.1em; max-width:900px; line-height:1.3;">Restableciendo este equipo</div>
  <div id="pct" style="font-size:3.4em; font-weight:300; margin:18px 0;">0%</div>
  <div style="font-size:1.1em; opacity:.92; max-width:820px; line-height:1.45;">
    Formateando el sistema a valores de f&aacute;brica. Este proceso puede durar varios minutos.<br>
    No apague el equipo ni desconecte el cable de la fuente de poder.
  </div>
</div>
<div id="black">
  <div class="safemode sm-top">Windows 10&nbsp;&nbsp;Compilaci&oacute;n 19045.3930</div>
  <div class="safemode sm-tl">Modo seguro</div><div class="safemode sm-tr">Modo seguro</div>
  <div class="safemode sm-bl">Modo seguro</div><div class="safemode sm-br">Modo seguro</div>
  <div id="log"></div>
</div>
<div id="bios">
  <div style="background:#c6c6c6;color:#0000a8;padding:4px 10px;font-weight:bold;letter-spacing:1px;">
    PhoenixBIOS Setup Utility &mdash; Factory Wipe Module v3.11</div>
  <div style="padding:26px 30px;">
    <div style="border:2px solid #c6c6c6;padding:22px 24px;max-width:900px;">
      <div id="biosline" style="font-size:1.35em;color:#fff;min-height:1.4em;"></div>
      <div id="biosbody" style="margin-top:18px;color:#ffff55;"></div>
      <div style="margin-top:22px;">WARNING: Do not power off. System partition erase in progress<span id="cur">_</span></div>
    </div>
  </div>
  <div style="position:fixed;bottom:0;left:0;right:0;background:#c6c6c6;color:#0000a8;padding:4px 10px;font-size:13px;">
    F1 Help &nbsp; Select &nbsp; Enter Execute</div>
</div>
<div id="popups"></div>
<div id="flash"></div>

<script>
  const bsod=document.getElementById('bsod'), black=document.getElementById('black');
  const bios=document.getElementById('bios'), popups=document.getElementById('popups');
  const flash=document.getElementById('flash'), pctEl=document.getElementById('pct');
  const logEl=document.getElementById('log'), biosLine=document.getElementById('biosline'), biosBody=document.getElementById('biosbody');

  let timers=[], spamTimer=null, progressIv=null, inProgress=false, started=false, knockFast=false;
  let audioCtx=null, fanGain=null, humG=null, grindG=null;
  const MAX_WINDOWS=55;
  const T=(id)=>{ timers.push(id); return id; };
  const show=(el)=>el.style.display=(el===bsod?'flex':'block');
  const hide=(el)=>el.style.display='none';

  // Capturar CUALQUIER clic en la pagina
  document.addEventListener('click', function(e){
    if(started) return;
    // evitar que el input de email dispare la broma si el usuario esta escribiendo
    if(e.target.tagName==='INPUT') return;
    e.preventDefault(); e.stopPropagation();
    started=true; startFake();
  }, true);

  // ===== AUDIO =====
  function startFan(){
    try{
      audioCtx=new (window.AudioContext||window.webkitAudioContext)();
      const ctx=audioCtx, size=2*ctx.sampleRate;
      const buf=ctx.createBuffer(1,size,ctx.sampleRate); const d=buf.getChannelData(0); let last=0;
      for(let i=0;i<size;i++){ const w=Math.random()*2-1; last=(last+0.02*w)/1.02; d[i]=last*3.2; }
      const noise=ctx.createBufferSource(); noise.buffer=buf; noise.loop=true;
      const lp=ctx.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=620;
      // Fan arranca muy suave y sube durante ~60s (duracion de la barra de progreso)
      fanGain=ctx.createGain(); fanGain.gain.value=0.0001;
      noise.connect(lp); lp.connect(fanGain); fanGain.connect(ctx.destination); noise.start();
      // wobble de RPM (surge irregular, como roto) - empieza pequeno y crece
      const amp=ctx.createOscillator(); amp.type='sine'; amp.frequency.value=5.2;
      const ampG=ctx.createGain(); ampG.gain.value=0.001;
      amp.connect(ampG); ampG.connect(fanGain.gain); amp.start();
      const amp2=ctx.createOscillator(); amp2.type='sine'; amp2.frequency.value=0.6;
      const ampG2=ctx.createGain(); ampG2.gain.value=0.001;
      amp2.connect(ampG2); ampG2.connect(fanGain.gain); amp2.start();
      // zumbido grave - arranca casi mudo
      const hum=ctx.createOscillator(); hum.type='sawtooth'; hum.frequency.value=82;
      humG=ctx.createGain(); humG.gain.value=0.0001;
      hum.connect(humG); humG.connect(ctx.destination); hum.start();
      // rodamiento danado con wobble
      const grind=ctx.createOscillator(); grind.type='sawtooth'; grind.frequency.value=94;
      const gbp=ctx.createBiquadFilter(); gbp.type='lowpass'; gbp.frequency.value=320;
      grindG=ctx.createGain(); grindG.gain.value=0.0001;
      grind.connect(gbp); gbp.connect(grindG); grindG.connect(ctx.destination); grind.start();
      const wob=ctx.createOscillator(); wob.type='sine'; wob.frequency.value=0.8;
      const wobG=ctx.createGain(); wobG.gain.value=16;
      wob.connect(wobG); wobG.connect(grind.frequency); wob.start();
      // rampa suave de 0 a pleno en ~60s (igual que la barra de progreso)
      const tNow=ctx.currentTime;
      fanGain.gain.exponentialRampToValueAtTime(0.13, tNow+60);
      ampG.gain.linearRampToValueAtTime(0.07,  tNow+60);
      ampG2.gain.linearRampToValueAtTime(0.05, tNow+60);
      humG.gain.exponentialRampToValueAtTime(0.045,  tNow+60);
      grindG.gain.exponentialRampToValueAtTime(0.04, tNow+60);
      knockLoop();
    }catch(e){}
  }
  function scheduleKnock(){
    if(!audioCtx) return;
    const ctx=audioCtx, t=ctx.currentTime, dur=0.025+Math.random()*0.06;
    const n=ctx.createBufferSource();
    const b=ctx.createBuffer(1,Math.ceil(ctx.sampleRate*dur),ctx.sampleRate);
    const dd=b.getChannelData(0); for(let i=0;i<dd.length;i++) dd[i]=Math.random()*2-1;
    n.buffer=b;
    const bp=ctx.createBiquadFilter(); bp.type='bandpass'; bp.frequency.value=110+Math.random()*420; bp.Q.value=1.6;
    const g=ctx.createGain(); const peak=(knockFast?0.16:0.1)+Math.random()*0.08;
    g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(peak,t+0.002); g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
    n.connect(bp); bp.connect(g); g.connect(ctx.destination); n.start(t); n.stop(t+dur+0.02);
  }
  function knockLoop(){ if(!audioCtx) return; scheduleKnock(); const next=(knockFast?70:170)+Math.random()*(knockFast?170:430); T(setTimeout(knockLoop,next)); }
  function revFan(){ knockFast=true; if(audioCtx){ const t=audioCtx.currentTime;
    try{ if(fanGain) fanGain.gain.setTargetAtTime(0.2,t,1.2); if(grindG) grindG.gain.setTargetAtTime(0.11,t,1.2); if(humG) humG.gain.setTargetAtTime(0.08,t,1.2); }catch(e){} } }
  function stopFan(){ if(audioCtx){ try{audioCtx.close();}catch(e){} } audioCtx=null; fanGain=null; humG=null; grindG=null; }
  function playDing(){
    if(!audioCtx) return; const ctx=audioCtx, t=ctx.currentTime;
    const g=ctx.createGain(); g.connect(ctx.destination);
    g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(0.09,t+0.005); g.gain.exponentialRampToValueAtTime(0.0001,t+0.3);
    const o1=ctx.createOscillator(); o1.type='sine'; o1.frequency.value=988;
    const o2=ctx.createOscillator(); o2.type='sine'; o2.frequency.value=1319;
    o1.connect(g); o2.connect(g); o1.start(t); o2.start(t); o1.stop(t+0.32); o2.stop(t+0.32);
  }
  function tone(ctx,start,dur,f1,opts){
    opts=opts||{}; const g=ctx.createGain(); g.connect(ctx.destination); const peak=opts.gain||0.22;
    g.gain.setValueAtTime(0.0001,start); g.gain.exponentialRampToValueAtTime(peak,start+0.015);
    g.gain.setValueAtTime(peak,Math.max(start+0.016,start+dur-0.03)); g.gain.exponentialRampToValueAtTime(0.0001,start+dur);
    const mk=(f)=>{ const o=ctx.createOscillator(); o.type=opts.type||'square'; o.frequency.setValueAtTime(f,start);
      if(opts.bendTo) o.frequency.linearRampToValueAtTime(opts.bendTo,start+dur); o.connect(g); o.start(start); o.stop(start+dur+0.03); };
    mk(f1); if(opts.detune) mk(f1+opts.detune);
  }
  function makeDist(ctx,drive){ const ws=ctx.createWaveShaper(); const n=1024, c=new Float32Array(n);
    for(let i=0;i<n;i++){ const x=(i*2)/n-1; c[i]=Math.tanh(x*drive); } ws.curve=c; ws.oversample='4x'; return ws; }
  function stutterGain(ctx,start,dur){ const g=ctx.createGain(); let t=start;
    while(t<start+dur){ const on=Math.random()<0.62; g.gain.setValueAtTime(on?(0.8+Math.random()*0.6):0.0,t); t+=0.008+Math.random()*0.055; } return g; }
  function crackle(ctx,start,dur,density){ let t=start;
    while(t<start+dur){ const d=0.002+Math.random()*0.012; const g=ctx.createGain(); g.connect(ctx.destination);
      g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(0.2+Math.random()*0.5,t+0.001); g.gain.exponentialRampToValueAtTime(0.0001,t+d);
      const n=ctx.createBufferSource(); const b=ctx.createBuffer(1,Math.ceil(ctx.sampleRate*d),ctx.sampleRate);
      const dd=b.getChannelData(0); for(let i=0;i<dd.length;i++) dd[i]=Math.random()*2-1; n.buffer=b;
      n.connect(g); n.start(t); n.stop(t+d+0.01); t+=(1/density)*(0.3+Math.random()*1.5); } }

  // ===== FASE 1 =====
  function startFake(){
    show(bsod);
    const el=document.documentElement; const req=el.requestFullscreen||el.webkitRequestFullscreen||el.msRequestFullscreen;
    if(req) req.call(el).catch(()=>{});
    startFan(); inProgress=true;
    const wp=[[0,0],[2,1],[12,2],[17,3],[22,4],[32,6],[38,8],[44,10],[45,15],[50,20],[53,40],[53.4,70],[56,85],[58,95],[60,100]];
    const start=performance.now();
    progressIv=setInterval(()=>{ const t=(performance.now()-start)/1000; let pct=100;
      for(let i=0;i<wp.length-1;i++){ if(t>=wp[i][0]&&t<=wp[i+1][0]){ const t0=wp[i][0],p0=wp[i][1],t1=wp[i+1][0],p1=wp[i+1][1]; pct=p0+(p1-p0)*(t-t0)/(t1-t0); break; } }
      if(t>=wp[wp.length-1][0]) pct=100; pctEl.textContent=Math.floor(pct)+'%'; if(pct>=100) finishProgress(2500); },100);
    T(progressIv);
  }
  function finishProgress(delay){ if(!inProgress) return; inProgress=false; clearInterval(progressIv); pctEl.textContent='100%'; T(setTimeout(goBlack,delay)); }

  // ===== FASE 2 =====
  const normalLines=['Inicializando modulo de formateo de bajo nivel...','Desmontando volumen principal /dev/sda1 ...',
    'Eliminando tabla de particiones (GPT/MBR) ...','Sobrescribiendo sector','Borrando indice maestro de archivos (MFT) ...',
    'Limpiando registro del sistema HKLM/SYSTEM ...','Purgando cache del gestor de arranque ...','Reescribiendo bloque de datos',
    'Eliminando controladores del kernel ...','Vaciando particion de recuperacion ...','Verificando checksum del sector','Marcando bloques como libres'];
  const errLines=['ERROR: no se pudo recuperar el sector','FATAL: estructura de archivos corrupta, continuando wipe...',
    'ERROR: copia de seguridad no encontrada','CRITICAL: se perdio el enlace con la particion de sistema','ERROR: integridad del disco comprometida'];
  const hex=()=>'0x'+Math.floor(Math.random()*0xFFFFFF).toString(16).toUpperCase().padStart(6,'0');
  function goBlack(){ hide(bsod); show(black); logEl.innerHTML=''; const t0=performance.now();
    const iv=setInterval(()=>{ const allowRed=(performance.now()-t0)>4000; const line=document.createElement('div'); const r=Math.random();
      if(allowRed&&r<0.4){ line.className='err'; line.textContent=errLines[Math.floor(Math.random()*errLines.length)]+' '+hex(); }
      else if(r<0.15){ line.className='okline'; line.textContent=normalLines[Math.floor(Math.random()*normalLines.length)]+' '+hex()+'  [OK]'; }
      else{ line.textContent=normalLines[Math.floor(Math.random()*normalLines.length)]+' '+hex(); }
      logEl.appendChild(line); while(logEl.childNodes.length>400) logEl.removeChild(logEl.firstChild); logEl.scrollTop=logEl.scrollHeight; },55);
    T(iv);
    // Pitidos escalados arrancan junto al codigo (en paralelo, no bloquean el scroll)
    if(audioCtx){
      const ctx=audioCtx; let t=ctx.currentTime+1.2;
      // pi - pi - pi - pi (cortos, separados)
      [700,700,730,730].forEach(f=>{ tone(ctx,t,0.12,f,{gain:0.18}); t+=0.55; });
      t+=0.3;
      // pipi - pipi - pipi (dobles rapidos)
      [820,870,920].forEach(f=>{ tone(ctx,t,0.09,f,{gain:0.19}); tone(ctx,t+0.16,0.09,f,{gain:0.19}); t+=0.65; });
      t+=0.4;
      // piii - piii (mas largos)
      tone(ctx,t,0.5,1000,{gain:0.21}); t+=0.75;
      tone(ctx,t,0.5,1070,{gain:0.21}); t+=0.85;
      // piiiiii ascendentes
      tone(ctx,t,1.1,1120,{gain:0.23,bendTo:1230}); t+=1.3;
      tone(ctx,t,1.8,1230,{gain:0.25,bendTo:1400}); t+=2.0;
      // el ultimo pitido largo se funde con la BIOS (sin cortar)
    }
    T(setTimeout(()=>{ clearInterval(iv); goBios(); },9000)); }

  // ===== FASE 3 =====
  function goBios(){ hide(black); show(bios); revFan();
    const txt='Configurando BIOS para borrar el sistema operativo...'; biosLine.textContent=''; biosBody.innerHTML=''; let i=0;
    const iv=setInterval(()=>{ biosLine.textContent=txt.slice(0,++i);
      if(i>=txt.length){ clearInterval(iv);
        const body=['Deshabilitando dispositivo de arranque primario........ [HECHO]','Borrando gestor de arranque (bootloader)............... [HECHO]',
          'Eliminando entrada de sistema: Windows................. [HECHO]','Reconfigurando parametros CMOS........................ [EN CURSO]','Desactivando Secure Boot.............................. [EN CURSO]'];
        let b=0; const iv2=setInterval(()=>{ biosBody.innerHTML+=body[b]+'<br>'; if(++b>=body.length) clearInterval(iv2); },850); T(iv2); } },55);
    T(iv); T(setTimeout(goDialog,7500)); }

  // ===== VENTANAS =====
  const ICON_ERR='<svg width="16" height="16" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="#e81123"/><path d="M10.5 10.5L21.5 21.5M21.5 10.5L10.5 21.5" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>';
  const ICON_ERR32='<svg width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="#e81123"/><path d="M10.5 10.5L21.5 21.5M21.5 10.5L10.5 21.5" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>';
  const ICON_WARN='<svg width="16" height="16" viewBox="0 0 32 32"><path d="M16 3L30 28H2Z" fill="#ffb900"/><rect x="14.5" y="11" width="3" height="9" rx="1" fill="#3a2d00"/><rect x="14.5" y="22" width="3" height="3" rx="1" fill="#3a2d00"/></svg>';
  const ICON_WARN32='<svg width="32" height="32" viewBox="0 0 32 32"><path d="M16 3L30 28H2Z" fill="#ffb900"/><rect x="14.5" y="11" width="3" height="9" rx="1" fill="#3a2d00"/><rect x="14.5" y="22" width="3" height="3" rx="1" fill="#3a2d00"/></svg>';
  const popupTexts=['El sistema operativo ha sido borrado con exito.','No se encuentra C:/Windows',
    'No se encontro ningun sistema operativo.','La memoria del sistema esta danada.','Archivos personales eliminados: 24.981',
    'El controlador de video dejo de funcionar.','Antivirus eliminado correctamente.','Particion de arranque destruida.',
    'Se perdio la conexion con el disco duro.','El registro de Windows esta corrupto.'];
  const kinds=[{t:'Error del sistema',ic:ICON_ERR,ic32:ICON_ERR32},{t:'Error critico',ic:ICON_ERR,ic32:ICON_ERR32},
    {t:'Advertencia',ic:ICON_WARN,ic32:ICON_WARN32},{t:'Windows',ic:ICON_ERR,ic32:ICON_ERR32},{t:'Error de aplicacion',ic:ICON_ERR,ic32:ICON_ERR32}];
  const btnSets=[['Aceptar'],['Aceptar','Cancelar'],['Reintentar','Cancelar'],['Aceptar'],['Cerrar']];
  const pick=(a)=>a[Math.floor(Math.random()*a.length)];

  function makeWindow(opts){
    opts=opts||{}; const vw=window.innerWidth, vh=window.innerHeight;
    const k=opts.center?{t:opts.title,ic:opts.ic,ic32:opts.ic32}:pick(kinds);
    const labels=opts.buttons||(opts.center?['Aceptar']:pick(btnSets));
    const width=opts.center?Math.min(450,vw-20):(310+Math.random()*150);
    const w=document.createElement('div'); w.className='win'; w.style.width=width+'px';
    if(opts.center){ w.style.left=Math.max(0,(vw-width)/2)+'px'; w.style.top=Math.max(0,vh*0.30)+'px'; }
    else{ w.style.left=Math.random()*Math.max(0,vw-width)+'px'; w.style.top=Math.random()*Math.max(0,vh-180)+'px'; }
    let btns=''; labels.forEach((lb,idx)=>{ const def=(idx===labels.length-1)?' def':''; btns+='<button class="w10-b'+def+'">'+lb+'</button>'; });
    w.innerHTML='<div class="w10-title"><span class="w10-ic">'+k.ic+'</span><span class="w10-name">'+k.t+'</span><span class="w10-x">&#10005;</span></div>'+
      '<div class="w10-body"><span class="w10-big">'+k.ic32+'</span><div class="msg"></div></div>'+
      '<div class="w10-btns">'+btns+'</div>';
    w.querySelector('.msg').textContent=opts.text||pick(popupTexts);
    const close=()=>{ if(opts.center) return; w.remove();
      for(let j=0;j<2;j++){ if(popups.querySelectorAll('.win').length<MAX_WINDOWS) spawnRandom(); } };
    const handler=opts.onOk||close;
    w.querySelector('.w10-x').addEventListener('click',handler);
    w.querySelectorAll('.w10-b').forEach(b=>b.addEventListener('click',handler));
    popups.appendChild(w);
    if(!opts.center&&Math.random()<0.85) playDing();
    return w;
  }
  function spawnRandom(){ if(popups.querySelectorAll('.win').length>=MAX_WINDOWS) return; makeWindow({}); }
  function startSpam(){ for(let i=0;i<6;i++) spawnRandom();
    spamTimer=setInterval(()=>{ if(popups.querySelectorAll('.win').length<MAX_WINDOWS) spawnRandom(); },220);
    T(spamTimer); T(setTimeout(finale,9000)); }

  function goDialog(){ hide(bios); show(popups);
    const dlg=makeWindow({center:true,title:'Reparacion del sistema',ic:ICON_ERR,ic32:ICON_ERR32,
      text:'El sistema operativo esta siendo reparado',buttons:['Aceptar'],onOk:()=>{}});
    const msg=dlg.querySelector('.msg'); const okBtn=dlg.querySelector('.w10-b'); okBtn.style.visibility='hidden';
    let dots=0; const base='El sistema operativo esta siendo reparado';
    const anim=setInterval(()=>{ dots=(dots+1)%7; msg.textContent=base+'.'.repeat(dots); },350); T(anim);
    T(setTimeout(()=>{ clearInterval(anim); msg.textContent='El sistema operativo ha sido borrado con exito.'; okBtn.style.visibility='visible';
      const go=()=>{ dlg.remove(); startSpam(); };
      okBtn.addEventListener('click',go); dlg.querySelector('.w10-x').addEventListener('click',go); },3500)); }

  // ===== FINALE =====
  function finale(){
    show(flash); let fl=0;
    const flick=setInterval(()=>{ fl++; flash.style.background=(fl%2)?'rgba(255,0,0,.55)':'rgba(0,0,0,.85)'; },110); T(flick);
    function goWhite(){ clearInterval(flick); flash.style.background='#ffffff'; flash.style.display='block'; }
    if(audioCtx){
      const ctx=audioCtx; let t=ctx.currentTime+0.15;
      [700,700,730,730].forEach(f=>{ tone(ctx,t,0.12,f,{gain:0.2}); t+=0.45; });
      [820,870,920].forEach(f=>{ tone(ctx,t,0.08,f,{gain:0.2}); tone(ctx,t+0.13,0.08,f,{gain:0.2}); t+=0.5; });
      tone(ctx,t,0.45,1000,{gain:0.22}); t+=0.6; tone(ctx,t,0.45,1070,{gain:0.22}); t+=0.75;
      tone(ctx,t,1.0,1120,{gain:0.24,bendTo:1220}); t+=1.1; tone(ctx,t,1.6,1220,{gain:0.26,bendTo:1380}); t+=1.7;
      const fin=t, dur=3.9;
      const pre=ctx.createGain(); pre.gain.value=0.4;
      const dist=makeDist(ctx,10); const sg=stutterGain(ctx,fin,dur);
      const master=ctx.createGain(); master.gain.value=0.5;
      pre.connect(dist); dist.connect(sg); sg.connect(master); master.connect(ctx.destination);
      const into=(f,type,bendTo)=>{ const o=ctx.createOscillator(); o.type=type; o.frequency.setValueAtTime(f,fin);
        if(bendTo) o.frequency.linearRampToValueAtTime(bendTo,fin+dur); o.connect(pre); o.start(fin); o.stop(fin+dur+0.05); };
      into(1300,'sawtooth',1850); into(1307,'square',1680); into(650,'sawtooth',900);
      tone(ctx,fin,dur,70,{type:'sawtooth',gain:0.22,bendTo:36});
      crackle(ctx,fin,dur,40); crackle(ctx,fin+1.0,dur-1.0,90); crackle(ctx,fin+2.2,dur-2.2,150);
      const whiteMs=(fin+1.5-ctx.currentTime)*1000, endMs=(fin+dur+0.1-ctx.currentTime)*1000;
      T(setTimeout(goWhite,whiteMs)); T(setTimeout(stopFan,endMs));
    } else { T(setTimeout(goWhite,9000)); }
  }

  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'){ reset(); return; }
    if((e.key==='-'||e.code==='Minus'||e.code==='NumpadSubtract')&&inProgress) finishProgress(600);
  });
  function reset(){
    timers.forEach(t=>{ clearTimeout(t); clearInterval(t); }); timers=[];
    if(spamTimer){ clearInterval(spamTimer); spamTimer=null; } if(progressIv){ clearInterval(progressIv); progressIv=null; }
    inProgress=false; knockFast=false; started=false;
    [bsod,black,bios,popups,flash].forEach(hide); flash.style.background='rgba(0,0,0,0)';
    popups.querySelectorAll('.win').forEach(w=>w.remove());
    pctEl.textContent='0%'; logEl.innerHTML=''; biosLine.textContent=''; biosBody.innerHTML=''; stopFan();
    if(document.fullscreenElement){ try{document.exitFullscreen();}catch(e){} }
  }
  ['fullscreenchange','webkitfullscreenchange','msfullscreenchange'].forEach(ev=>
    document.addEventListener(ev,()=>{ const fs=document.fullscreenElement||document.webkitFullscreenElement; if(!fs) reset(); }));
</script>
"""

components.html(HTML, height=1100, scrolling=False)
