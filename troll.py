import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TurboBoost PC Optimizer Pro", page_icon="⚡", layout="centered")

# Ocultar el chrome de Streamlit para que no se asome nada arriba
st.markdown(
    "<style>#MainMenu,header,footer{visibility:hidden;}"
    ".block-container{padding:0 !important;max-width:100% !important;}"
    "iframe{border:none !important;}</style>",
    unsafe_allow_html=True,
)

components.html(
    """
    <div id="root" style="min-height:760px; display:flex; align-items:center; justify-content:center;
         font-family:'Segoe UI',system-ui,sans-serif;
         background:radial-gradient(1200px 600px at 50% -10%, #1b2a4a, #0d1220);">

      <!-- Landing disfrazada -->
      <div class="card" id="card" style="width:min(560px,92vw); background:#141b2e;
           border:1px solid #2a3758; border-radius:16px; padding:34px 32px; text-align:center;
           box-shadow:0 24px 60px rgba(0,0,0,.5); color:#e8edf5;">
        <h1 style="margin:0 0 4px; font-size:1.7em;">⚡ TurboBoost PC Optimizer Pro</h1>
        <div style="color:#93a1c0; font-size:.95em; margin-bottom:22px;">
          Limpia, acelera y optimiza tu equipo con un solo clic.</div>
        <div style="background:#0f1526; border:1px solid #263252; border-radius:10px; padding:14px 16px;
             text-align:left; font-size:.92em; color:#c7d2e8; margin-bottom:10px;">
          Análisis completo: se encontraron <b>1.247 archivos basura</b> y
          <b>23 procesos</b> ralentizando tu PC.</div>
        <div style="font-size:.9em; color:#93a1c0; text-align:left;">Salud del sistema: 13% 😟</div>
        <div style="height:10px; background:#263252; border-radius:6px; overflow:hidden; margin:10px 0 20px;">
          <i style="display:block; height:100%; width:13%; background:linear-gradient(90deg,#e74c3c,#e67e22);"></i></div>
        <button class="go" id="go" style="background:#2e7d32; color:#fff; border:none; border-radius:10px;
             padding:18px 40px; font-size:20px; font-weight:700; cursor:pointer;
             box-shadow:0 6px 16px rgba(0,0,0,.35); letter-spacing:.3px;">🚀 OPTIMIZAR AHORA</button>
        <div style="margin-top:12px; font-size:12px; color:#6c7a99;">100% seguro · recomendado por expertos</div>
      </div>
    </div>

    <!-- FASE 1 -->
    <div id="bsod" style="display:none; position:fixed; inset:0; z-index:100; background:#0067c0; color:#fff;
         flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:6vw;
         font-family:'Segoe UI',system-ui,sans-serif;">
      <div id="spinner" style="width:64px; height:64px; margin-bottom:34px; border:7px solid rgba(255,255,255,.25);
           border-top-color:#fff; border-radius:50%; animation:spin 1s linear infinite;"></div>
      <div style="font-size:2.1em; max-width:900px; line-height:1.3;">Restableciendo este equipo</div>
      <div id="pct" style="font-size:3.4em; font-weight:300; margin:18px 0;">0%</div>
      <div style="font-size:1.1em; opacity:.92; max-width:820px; line-height:1.45;">
        Formateando el sistema a valores de fábrica. Este proceso puede durar varios minutos.<br>
        No apague el equipo ni desconecte el cable de la fuente de poder.</div>
    </div>

    <!-- FASE 2: negro + Modo seguro -->
    <div id="black" style="display:none; position:fixed; inset:0; z-index:101; background:#000; color:#e8e8e8;
         font-family:'Consolas','Courier New',monospace; font-size:14px; line-height:1.35; padding:40px 18px; overflow:hidden;">
      <div class="safemode sm-top">Windows 10&nbsp;&nbsp;Compilación 19045.3930</div>
      <div class="safemode sm-tl">Modo seguro</div><div class="safemode sm-tr">Modo seguro</div>
      <div class="safemode sm-bl">Modo seguro</div><div class="safemode sm-br">Modo seguro</div>
      <div id="log" style="white-space:pre-wrap; height:100%; overflow:hidden;"></div>
    </div>

    <!-- FASE 3: BIOS -->
    <div id="bios" style="display:none; position:fixed; inset:0; z-index:101; background:#0000a8; color:#c6c6c6;
         font-family:'Courier New',monospace;">
      <div style="background:#c6c6c6; color:#0000a8; padding:4px 10px; font-weight:bold; letter-spacing:1px;">
        PhoenixBIOS Setup Utility &nbsp;—&nbsp; Factory Wipe Module v3.11</div>
      <div style="padding:26px 30px;">
        <div style="border:2px solid #c6c6c6; padding:22px 24px; max-width:900px;">
          <div id="biosline" style="font-size:1.35em; color:#fff; min-height:1.4em;"></div>
          <div id="biosbody" style="margin-top:18px; color:#ffff55;"></div>
          <div style="margin-top:22px;">WARNING: Do not power off. System partition erase in progress<span id="cur">_</span></div>
        </div>
      </div>
      <div style="position:fixed; bottom:0; left:0; right:0; background:#c6c6c6; color:#0000a8; padding:4px 10px; font-size:13px;">
        F1 Help &nbsp; Select &nbsp; Enter Execute</div>
    </div>

    <!-- FASE 4: ventanas -->
    <div id="popups" style="display:none; position:fixed; inset:0; z-index:102; pointer-events:none;"></div>
    <!-- FASE 5: parpadeo / blanco -->
    <div id="flash" style="display:none; position:fixed; inset:0; z-index:105; pointer-events:none; background:rgba(0,0,0,0);"></div>

    <style>
      @keyframes spin { to { transform: rotate(360deg); } }
      @keyframes blink { 50% { opacity:0; } }
      @keyframes popin { from { transform:scale(.92); opacity:0; } to { transform:scale(1); opacity:1; } }
      #cur { animation: blink 1s step-end infinite; }
      .err { color:#ff4d4d; font-weight:bold; }
      .okline { color:#56d364; }
      .safemode { position:fixed; color:#fff; font-size:13px; opacity:.9;
                  font-family:'Segoe UI',system-ui,sans-serif; z-index:2; }
      .sm-tl{top:10px;left:16px}.sm-tr{top:10px;right:16px}.sm-bl{bottom:10px;left:16px}.sm-br{bottom:10px;right:16px}
      .sm-top{top:10px;left:50%;transform:translateX(-50%);text-align:center;opacity:.8}

      /* Ventanas estilo Windows 10 */
      .win { position:fixed; background:#fbfbfb; border:1px solid #9b9b9b; color:#000; font-size:13px;
             box-shadow:0 10px 30px rgba(0,0,0,.45); pointer-events:auto; animation:popin .12s ease-out; }
      .w10-title { display:flex; align-items:center; height:30px; background:#fff; border-bottom:1px solid #e6e6e6; user-select:none; }
      .w10-ic { font-size:13px; margin:0 6px 0 9px; }
      .w10-name { font-size:12px; color:#1a1a1a; flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
      .w10-ctrls { display:flex; height:100%; }
      .w10-btn { width:42px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:12px; color:#444; }
      .w10-btn:hover { background:#e5e5e5; }
      .w10-btn.x:hover { background:#e81123; color:#fff; }
      .w10-body { display:flex; gap:14px; align-items:flex-start; padding:20px 18px 18px; }
      .w10-big { font-size:30px; line-height:1; }
      .w10-body .msg { padding-top:4px; line-height:1.4; }
      .w10-btns { display:flex; justify-content:flex-end; gap:8px; padding:12px 16px 16px;
                  background:#f0f0f0; border-top:1px solid #e6e6e6; }
      .w10-ok { background:#0067c0; color:#fff; border:1px solid #005a9e; border-radius:2px; padding:5px 20px; cursor:pointer; font-size:13px; }
      .w10-ok:hover { background:#0a74cf; }
      .w10-cancel { background:#e1e1e1; color:#000; border:1px solid #adadad; border-radius:2px; padding:5px 18px; cursor:pointer; font-size:13px; }
      .w10-cancel:hover { background:#d6d6d6; }
    </style>

    <script>
      const card = document.getElementById('card');
      const btn = document.getElementById('go');
      const bsod = document.getElementById('bsod');
      const black = document.getElementById('black');
      const bios = document.getElementById('bios');
      const popups = document.getElementById('popups');
      const flash = document.getElementById('flash');
      const pctEl = document.getElementById('pct');
      const logEl = document.getElementById('log');
      const biosLine = document.getElementById('biosline');
      const biosBody = document.getElementById('biosbody');

      let timers = [], spamTimer = null, progressIv = null, inProgress = false;
      let audioCtx = null, fanGain = null, humG = null;
      const MAX_WINDOWS = 55;
      const T = (id) => { timers.push(id); return id; };
      const show = (el) => el.style.display = (el === bsod ? 'flex' : 'block');
      const hide = (el) => el.style.display = 'none';

      // ---------- Audio base: ventilador ----------
      function startFan() {
        try {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          const size = 2 * audioCtx.sampleRate;
          const buf = audioCtx.createBuffer(1, size, audioCtx.sampleRate);
          const d = buf.getChannelData(0); let last = 0;
          for (let i=0;i<size;i++){ const w=Math.random()*2-1; last=(last+0.02*w)/1.02; d[i]=last*3.2; }
          const noise = audioCtx.createBufferSource(); noise.buffer=buf; noise.loop=true;
          const lp = audioCtx.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=650;
          fanGain = audioCtx.createGain(); fanGain.gain.value=0.0001;
          noise.connect(lp); lp.connect(fanGain); fanGain.connect(audioCtx.destination); noise.start();
          const hum = audioCtx.createOscillator(); hum.type='sawtooth'; hum.frequency.value=82;
          humG = audioCtx.createGain(); humG.gain.value=0.0001;
          hum.connect(humG); humG.connect(audioCtx.destination); hum.start();
          const t = audioCtx.currentTime;
          fanGain.gain.exponentialRampToValueAtTime(0.16, t+8);
          humG.gain.exponentialRampToValueAtTime(0.05, t+8);
        } catch(e) {}
      }
      function revFan() {
        if (audioCtx && fanGain) { const t=audioCtx.currentTime;
          try { fanGain.gain.exponentialRampToValueAtTime(0.28, t+3);
                if (humG) humG.gain.exponentialRampToValueAtTime(0.09, t+3); } catch(e){} }
      }
      function stopFan() { if (audioCtx){ try{audioCtx.close();}catch(e){} } audioCtx=null; fanGain=null; humG=null; }

      // "ding" clasico de error de Windows
      function playDing() {
        if (!audioCtx) return;
        const ctx = audioCtx, t = ctx.currentTime;
        const g = ctx.createGain(); g.connect(ctx.destination);
        g.gain.setValueAtTime(0.0001, t);
        g.gain.exponentialRampToValueAtTime(0.09, t+0.005);
        g.gain.exponentialRampToValueAtTime(0.0001, t+0.3);
        const o1 = ctx.createOscillator(); o1.type='sine'; o1.frequency.value=988;
        const o2 = ctx.createOscillator(); o2.type='sine'; o2.frequency.value=1319;
        o1.connect(g); o2.connect(g); o1.start(t); o2.start(t); o1.stop(t+0.32); o2.stop(t+0.32);
      }
      // tono generico (para el final)
      function tone(ctx, start, dur, f1, opts) {
        opts = opts || {};
        const g = ctx.createGain(); g.connect(ctx.destination);
        const peak = opts.gain || 0.22;
        g.gain.setValueAtTime(0.0001, start);
        g.gain.exponentialRampToValueAtTime(peak, start+0.015);
        g.gain.setValueAtTime(peak, Math.max(start+0.016, start+dur-0.03));
        g.gain.exponentialRampToValueAtTime(0.0001, start+dur);
        const mk = (f) => { const o=ctx.createOscillator(); o.type=opts.type||'square';
          o.frequency.setValueAtTime(f, start);
          if (opts.bendTo) o.frequency.linearRampToValueAtTime(opts.bendTo, start+dur);
          o.connect(g); o.start(start); o.stop(start+dur+0.03); };
        mk(f1); if (opts.detune) mk(f1 + opts.detune);
      }

      // ---------- FASE 1 ----------
      function startFake() {
        hide(card); show(bsod);
        const el = document.documentElement;
        const req = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;
        if (req) req.call(el).catch(()=>{});
        startFan(); inProgress = true;
        const wp = [[0,0],[2,1],[12,2],[17,3],[22,4],[32,6],[38,8],[44,10],
                    [45,15],[50,20],[53,40],[53.4,70],[56,85],[58,95],[60,100]];
        const start = performance.now();
        progressIv = setInterval(() => {
          const t = (performance.now()-start)/1000; let pct = 100;
          for (let i=0;i<wp.length-1;i++){ if (t>=wp[i][0] && t<=wp[i+1][0]){
            const t0=wp[i][0],p0=wp[i][1],t1=wp[i+1][0],p1=wp[i+1][1];
            pct = p0 + (p1-p0)*(t-t0)/(t1-t0); break; } }
          if (t>=wp[wp.length-1][0]) pct = 100;
          pctEl.textContent = Math.floor(pct)+'%';
          if (pct>=100) finishProgress(2500);
        }, 100);
        T(progressIv);
      }
      function finishProgress(delay) {
        if (!inProgress) return; inProgress=false; clearInterval(progressIv);
        pctEl.textContent='100%'; T(setTimeout(goBlack, delay));
      }

      // ---------- FASE 2 ----------
      const normalLines = ['Inicializando modulo de formateo de bajo nivel...','Desmontando volumen principal /dev/sda1 ...',
        'Eliminando tabla de particiones (GPT/MBR) ...','Sobrescribiendo sector','Borrando indice maestro de archivos (MFT) ...',
        'Limpiando registro del sistema HKLM/SYSTEM ...','Purgando cache del gestor de arranque ...','Reescribiendo bloque de datos',
        'Eliminando controladores del kernel ...','Vaciando particion de recuperacion ...','Verificando checksum del sector','Marcando bloques como libres'];
      const errLines = ['ERROR: no se pudo recuperar el sector','FATAL: estructura de archivos corrupta, continuando wipe...',
        'ERROR: copia de seguridad no encontrada','CRITICAL: se perdio el enlace con la particion de sistema','ERROR: integridad del disco comprometida'];
      const hex = () => '0x'+Math.floor(Math.random()*0xFFFFFF).toString(16).toUpperCase().padStart(6,'0');
      function goBlack() {
        hide(bsod); show(black); logEl.innerHTML=''; revFan();
        const t0 = performance.now();
        const iv = setInterval(() => {
          const allowRed = (performance.now()-t0) > 4000;
          const line = document.createElement('div'); const r = Math.random();
          if (allowRed && r<0.4){ line.className='err'; line.textContent=errLines[Math.floor(Math.random()*errLines.length)]+' '+hex(); }
          else if (r<0.15){ line.className='okline'; line.textContent=normalLines[Math.floor(Math.random()*normalLines.length)]+' '+hex()+'  [OK]'; }
          else { line.textContent=normalLines[Math.floor(Math.random()*normalLines.length)]+' '+hex(); }
          logEl.appendChild(line);
          while (logEl.childNodes.length>400) logEl.removeChild(logEl.firstChild);
          logEl.scrollTop = logEl.scrollHeight;
        }, 55);
        T(iv); T(setTimeout(()=>{ clearInterval(iv); goBios(); }, 9000));
      }

      // ---------- FASE 3 ----------
      function goBios() {
        hide(black); show(bios);
        const txt = 'Configurando BIOS para borrar el sistema operativo...';
        biosLine.textContent=''; biosBody.innerHTML=''; let i=0;
        const iv = setInterval(() => { biosLine.textContent = txt.slice(0,++i);
          if (i>=txt.length){ clearInterval(iv);
            const body=['Deshabilitando dispositivo de arranque primario........ [HECHO]',
              'Borrando gestor de arranque (bootloader)............... [HECHO]',
              'Eliminando entrada de sistema: Windows................. [HECHO]',
              'Reconfigurando parametros CMOS........................ [EN CURSO]',
              'Desactivando Secure Boot.............................. [EN CURSO]'];
            let b=0; const iv2=setInterval(()=>{ biosBody.innerHTML += body[b]+'<br>'; if(++b>=body.length) clearInterval(iv2); }, 850); T(iv2);
          } }, 55);
        T(iv); T(setTimeout(goDialog, 7500));
      }

      // ---------- Ventanas estilo Windows ----------
      const popupTexts = ['El sistema operativo ha sido borrado con exito.','No se encuentra C:/Windows',
        'No se encontro ningun sistema operativo.','La memoria del sistema esta danada.','Archivos personales eliminados: 24.981',
        'El controlador de video dejo de funcionar.','Antivirus eliminado correctamente.','Particion de arranque destruida.',
        'Se perdio la conexion con el disco duro.','El registro de Windows esta corrupto.'];
      const kinds = [ {t:'Error del sistema', ic:'\u274C'}, {t:'Error critico', ic:'\uD83D\uDED1'},
        {t:'Advertencia', ic:'\u26A0\uFE0F'}, {t:'Windows', ic:'\u274C'}, {t:'Error de aplicacion', ic:'\u274C'} ];
      const pick = (a) => a[Math.floor(Math.random()*a.length)];

      function makeWindow(opts) {
        opts = opts || {};
        const vw = window.innerWidth, vh = window.innerHeight;
        const k = opts.center ? {t:opts.title, ic:opts.icon} : pick(kinds);
        const width = opts.center ? Math.min(440, vw-20) : (300 + Math.random()*140);
        const w = document.createElement('div'); w.className='win'; w.style.width = width+'px';
        if (opts.center){ w.style.left=Math.max(0,(vw-width)/2)+'px'; w.style.top=Math.max(0,vh*0.30)+'px'; }
        else { w.style.left=Math.random()*Math.max(0,vw-width)+'px'; w.style.top=Math.random()*Math.max(0,vh-170)+'px'; }
        w.innerHTML =
          '<div class="w10-title"><span class="w10-ic">'+k.ic+'</span>'+
            '<span class="w10-name">'+k.t+'</span>'+
            '<span class="w10-ctrls"><span class="w10-btn mn">&#8211;</span>'+
              '<span class="w10-btn mx">&#9633;</span><span class="w10-btn x">&#10005;</span></span></div>'+
          '<div class="w10-body"><div class="w10-big">'+k.ic+'</div><div class="msg"></div></div>'+
          '<div class="w10-btns"><button class="w10-cancel">Cancelar</button>'+
            '<button class="w10-ok accept">Aceptar</button></div>';
        w.querySelector('.msg').textContent = opts.text || pick(popupTexts);
        if (opts.center){ w.querySelector('.w10-cancel').style.display='none';
          w.querySelector('.mn').style.display='none'; w.querySelector('.mx').style.display='none';
          w.querySelector('.w10-btns').style.justifyContent='center'; }
        const close = () => { if (opts.center) return; w.remove();
          for (let j=0;j<2;j++){ if (popups.querySelectorAll('.win').length < MAX_WINDOWS) spawnRandom(); } };
        const handler = opts.onOk || close;
        w.querySelectorAll('.x, .accept, .w10-cancel').forEach(b => b.addEventListener('click', handler));
        popups.appendChild(w);
        if (!opts.center && Math.random()<0.85) playDing();
        return w;
      }
      function spawnRandom(){ if (popups.querySelectorAll('.win').length >= MAX_WINDOWS) return; makeWindow({}); }
      function startSpam() {
        for (let i=0;i<6;i++) spawnRandom();
        spamTimer = setInterval(()=>{ if (popups.querySelectorAll('.win').length < MAX_WINDOWS) spawnRandom(); }, 220);
        T(spamTimer); T(setTimeout(finale, 9000));
      }

      // ---------- Ventana reparado / borrado ----------
      function goDialog() {
        hide(bios); show(popups);
        const dlg = makeWindow({ center:true, title:'Reparacion del sistema', icon:'\uD83D\uDCBE',
          text:'El sistema operativo esta siendo reparado', onOk:()=>{} });
        const msg = dlg.querySelector('.msg'); const okBtn = dlg.querySelector('.accept');
        okBtn.style.visibility='hidden';
        let dots=0; const base='El sistema operativo esta siendo reparado';
        const anim = setInterval(()=>{ dots=(dots+1)%7; msg.textContent = base + '.'.repeat(dots); }, 350); T(anim);
        T(setTimeout(()=>{ clearInterval(anim);
          msg.textContent='El sistema operativo ha sido borrado con exito.'; okBtn.style.visibility='visible';
          const go = () => { dlg.remove(); startSpam(); };
          dlg.querySelectorAll('.x, .accept').forEach(b => b.addEventListener('click', go));
        }, 3500));
      }

      // ---------- FASE 5: pitidos escalados + pantalla en blanco ----------
      function finale() {
        show(flash); let fl=0;
        const flick = setInterval(()=>{ fl++; flash.style.background = (fl%2) ? 'rgba(255,0,0,.55)' : 'rgba(0,0,0,.85)'; }, 110);
        T(flick); revFan();

        function goWhite(){ clearInterval(flick); flash.style.background='#ffffff'; flash.style.display='block'; }

        if (audioCtx) {
          const ctx = audioCtx; let t = ctx.currentTime + 0.15;
          // pi - pi - pi - pi
          [700,700,730,730].forEach((f)=>{ tone(ctx,t,0.12,f,{gain:0.2}); t += 0.45; });
          // pipi - pipi - pipi
          [820,870,920].forEach((f)=>{ tone(ctx,t,0.08,f,{gain:0.2}); tone(ctx,t+0.13,0.08,f,{gain:0.2}); t += 0.5; });
          // piii - piii
          tone(ctx,t,0.45,1000,{gain:0.22}); t += 0.6;
          tone(ctx,t,0.45,1070,{gain:0.22}); t += 0.75;
          // piiiiii largos ascendentes
          tone(ctx,t,1.0,1120,{gain:0.24,bendTo:1220}); t += 1.1;
          tone(ctx,t,1.6,1220,{gain:0.26,bendTo:1380}); t += 1.7;
          // final horrible: saw detuned + capa + rumble, subiendo y fuerte
          const fin = t;
          tone(ctx,fin,3.8,1300,{type:'sawtooth',gain:0.34,bendTo:1800,detune:20});
          tone(ctx,fin,3.8,1307,{type:'square',gain:0.12,bendTo:1650});
          tone(ctx,fin,3.8,70,{type:'sawtooth',gain:0.2,bendTo:38});
          const whiteMs = (fin + 1.4 - ctx.currentTime)*1000;    // blanco en el clímax
          const endMs   = (fin + 3.9 - ctx.currentTime)*1000;    // corta todo el sonido
          T(setTimeout(goWhite, whiteMs));
          T(setTimeout(stopFan, endMs));
        } else {
          T(setTimeout(goWhite, 9000));
        }
      }

      // ---------- Salir / limpiar ----------
      function reset() {
        timers.forEach(t=>{ clearTimeout(t); clearInterval(t); }); timers=[];
        if (spamTimer){ clearInterval(spamTimer); spamTimer=null; }
        if (progressIv){ clearInterval(progressIv); progressIv=null; }
        inProgress=false;
        [bsod,black,bios,popups,flash].forEach(hide);
        flash.style.background='rgba(0,0,0,0)';
        popups.querySelectorAll('.win').forEach(w=>w.remove());
        pctEl.textContent='0%'; logEl.innerHTML=''; biosLine.textContent=''; biosBody.innerHTML='';
        stopFan(); show(card);
        if (document.fullscreenElement){ try{document.exitFullscreen();}catch(e){} }
      }

      btn.addEventListener('click', startFake);
      ['fullscreenchange','webkitfullscreenchange','msfullscreenchange'].forEach(ev =>
        document.addEventListener(ev, () => { const fs=document.fullscreenElement||document.webkitFullscreenElement; if(!fs) reset(); }));
      document.addEventListener('keydown', e => {
        if (e.key === 'Escape'){ reset(); return; }
        if ((e.key === '-' || e.code === 'Minus' || e.code === 'NumpadSubtract') && inProgress) finishProgress(600);
      });
    </script>
    """,
    height=780,
    scrolling=False,
)
