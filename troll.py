import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TurboBoost PC Optimizer Pro",
    page_icon="⚡",
    layout="centered",
)

# --- Disfraz: parece un inocente "optimizador de PC" ---
st.title("⚡ TurboBoost PC Optimizer Pro")
st.caption("Limpia, acelera y optimiza tu equipo con un solo clic.")

st.write(
    "Hemos analizado tu sistema y encontramos **1.247 archivos basura** "
    "y **23 procesos** ralentizando tu PC."
)
st.progress(13, text="Salud del sistema: 13% 😟")
st.info("Recomendación: ejecuta la optimización completa para recuperar rendimiento.")

components.html(
    """
    <div id="wrap" style="font-family:'Segoe UI',system-ui,sans-serif; text-align:center;">
      <button id="go" style="
          background:#2e7d32; color:#fff; border:none; border-radius:10px;
          padding:18px 36px; font-size:20px; font-weight:700; cursor:pointer;
          box-shadow:0 4px 14px rgba(0,0,0,.25); letter-spacing:.3px;">
        🚀 OPTIMIZAR AHORA
      </button>
      <div style="margin-top:10px; font-size:12px; color:#888;">
        100% seguro · recomendado por expertos &nbsp;·&nbsp; (truco: tecla &quot;-&quot; salta la carga)
      </div>
    </div>

    <!-- FASE 1: pantalla azul de formateo -->
    <div id="bsod" style="
        display:none; position:fixed; inset:0; z-index:999990; background:#0067c0; color:#fff;
        font-family:'Segoe UI',system-ui,sans-serif; flex-direction:column;
        align-items:center; justify-content:center; text-align:center; padding:6vw; box-sizing:border-box;">
      <div id="spinner" style="
          width:64px; height:64px; margin-bottom:34px;
          border:7px solid rgba(255,255,255,.25); border-top-color:#fff;
          border-radius:50%; animation:spin 1s linear infinite;"></div>
      <div style="font-size:2.1em; font-weight:400; max-width:900px; line-height:1.3;">
        Restableciendo este equipo
      </div>
      <div id="pct" style="font-size:3.4em; font-weight:300; margin:18px 0;">0%</div>
      <div style="font-size:1.1em; opacity:.92; max-width:820px; line-height:1.45;">
        Formateando el sistema a valores de fábrica. Este proceso puede durar varios minutos.<br>
        No apague el equipo ni desconecte el cable de la fuente de poder.
      </div>
      <div class="hint" style="position:fixed; bottom:14px; font-size:12px; opacity:.4;">
        (broma — pulsa Esc para salir)
      </div>
    </div>

    <!-- FASE 2: fondo negro con codigo -->
    <div id="black" style="
        display:none; position:fixed; inset:0; z-index:999991; background:#000; color:#e8e8e8;
        font-family:'Consolas','Courier New',monospace; font-size:14px; line-height:1.35;
        padding:18px; box-sizing:border-box; overflow:hidden;">
      <div id="log" style="white-space:pre-wrap; height:100%; overflow:hidden;"></div>
    </div>

    <!-- FASE 3: BIOS retro -->
    <div id="bios" style="
        display:none; position:fixed; inset:0; z-index:999991; background:#0000a8; color:#c6c6c6;
        font-family:'Courier New',monospace; box-sizing:border-box;">
      <div style="background:#c6c6c6; color:#0000a8; padding:4px 10px; font-weight:bold; letter-spacing:1px;">
        PhoenixBIOS Setup Utility &nbsp;—&nbsp; Factory Wipe Module v3.11
      </div>
      <div style="padding:26px 30px;">
        <div style="border:2px solid #c6c6c6; padding:22px 24px; max-width:900px;">
          <div id="biosline" style="font-size:1.35em; color:#ffffff; min-height:1.4em;"></div>
          <div id="biosbody" style="margin-top:18px; color:#ffff55;"></div>
          <div style="margin-top:22px; color:#c6c6c6;">
            WARNING: Do not power off. System partition erase in progress<span id="cur">_</span>
          </div>
        </div>
      </div>
      <div style="position:fixed; bottom:0; left:0; right:0; background:#c6c6c6; color:#0000a8;
                  padding:4px 10px; font-size:13px;">
        F1 Help &nbsp; Select &nbsp; Enter Execute &nbsp; <span style="float:right;">Esc Exit (broma)</span>
      </div>
    </div>

    <!-- FASE 4: ventanas falsas -->
    <div id="popups" style="display:none; position:fixed; inset:0; z-index:999992; pointer-events:none;">
      <div class="hint" style="position:fixed; bottom:8px; right:12px; font-size:11px;
           color:#fff; opacity:.6; pointer-events:none;">(broma — pulsa Esc para salir)</div>
    </div>

    <!-- FASE 5: parpadeo final -->
    <div id="flash" style="display:none; position:fixed; inset:0; z-index:999995;
         pointer-events:none; background:rgba(0,0,0,0);"></div>

    <style>
      @keyframes spin { to { transform: rotate(360deg); } }
      @keyframes blink { 50% { opacity:0; } }
      #cur { animation: blink 1s step-end infinite; }
      .err { color:#ff4d4d; font-weight:bold; }
      .ok  { color:#56d364; }
      .fw-btn { padding:4px 18px; border:1px solid #888; background:#e4e4e4;
                border-radius:3px; cursor:pointer; font-size:13px; }
      .fw-btn:active { background:#d0d0d0; }
    </style>

    <script>
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

      let timers = [];
      let spamTimer = null;
      let progressIv = null;
      let inProgress = false;
      let audioCtx = null, fanGain = null, humG = null;
      const MAX_WINDOWS = 55;
      const T = (id) => { timers.push(id); return id; };

      // ---------- SONIDO DE VENTILADOR ----------
      function startFan() {
        try {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          const size = 2 * audioCtx.sampleRate;
          const buf = audioCtx.createBuffer(1, size, audioCtx.sampleRate);
          const d = buf.getChannelData(0);
          let last = 0;
          for (let i = 0; i < size; i++) {
            const w = Math.random() * 2 - 1;
            last = (last + 0.02 * w) / 1.02;
            d[i] = last * 3.2;
          }
          const noise = audioCtx.createBufferSource();
          noise.buffer = buf; noise.loop = true;
          const lp = audioCtx.createBiquadFilter();
          lp.type = 'lowpass'; lp.frequency.value = 650;
          fanGain = audioCtx.createGain(); fanGain.gain.value = 0.0001;
          noise.connect(lp); lp.connect(fanGain); fanGain.connect(audioCtx.destination);
          noise.start();
          const hum = audioCtx.createOscillator();
          hum.type = 'sawtooth'; hum.frequency.value = 82;
          humG = audioCtx.createGain(); humG.gain.value = 0.0001;
          hum.connect(humG); humG.connect(audioCtx.destination); hum.start();
          const t = audioCtx.currentTime;
          fanGain.gain.exponentialRampToValueAtTime(0.16, t + 8);
          humG.gain.exponentialRampToValueAtTime(0.05, t + 8);
        } catch (e) {}
      }
      function revFan() {
        if (audioCtx && fanGain) {
          const t = audioCtx.currentTime;
          try {
            fanGain.gain.exponentialRampToValueAtTime(0.28, t + 3);
            if (humG) humG.gain.exponentialRampToValueAtTime(0.09, t + 3);
          } catch (e) {}
        }
      }
      function stopFan() {
        if (audioCtx) { try { audioCtx.close(); } catch (e) {} }
        audioCtx = null; fanGain = null; humG = null;
      }

      // ---------- FASE 1: formateo (~60s, con salto 40->70 ultra rapido) ----------
      function startFake() {
        bsod.style.display = 'flex';
        const el = document.documentElement;
        const req = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;
        if (req) req.call(el).catch(() => {});
        startFan();

        inProgress = true;
        const wp = [
          [0, 0], [2, 1], [12, 2], [17, 3], [22, 4], [32, 6], [38, 8], [44, 10],
          [45, 15], [50, 20], [53, 40], [53.4, 70],   // <- 40 a 70 en un flash
          [56, 85], [58, 95], [60, 100]
        ];
        const start = performance.now();
        progressIv = setInterval(() => {
          const t = (performance.now() - start) / 1000;
          let pct = 100;
          for (let i = 0; i < wp.length - 1; i++) {
            if (t >= wp[i][0] && t <= wp[i + 1][0]) {
              const t0 = wp[i][0], p0 = wp[i][1], t1 = wp[i + 1][0], p1 = wp[i + 1][1];
              pct = p0 + (p1 - p0) * (t - t0) / (t1 - t0);
              break;
            }
          }
          if (t >= wp[wp.length - 1][0]) pct = 100;
          pctEl.textContent = Math.floor(pct) + '%';
          if (pct >= 100) finishProgress(2500);
        }, 100);
        T(progressIv);
      }

      function finishProgress(delay) {
        if (!inProgress) return;
        inProgress = false;
        clearInterval(progressIv);
        pctEl.textContent = '100%';
        T(setTimeout(goBlack, delay));
      }

      // ---------- FASE 2: pantalla negra (blanco -> rojo) ----------
      const normalLines = [
        'Inicializando modulo de formateo de bajo nivel...',
        'Desmontando volumen principal /dev/sda1 ...',
        'Eliminando tabla de particiones (GPT/MBR) ...',
        'Sobrescribiendo sector',
        'Borrando indice maestro de archivos (MFT) ...',
        'Limpiando registro del sistema HKLM/SYSTEM ...',
        'Purgando cache del gestor de arranque ...',
        'Reescribiendo bloque de datos',
        'Eliminando controladores del kernel ...',
        'Vaciando particion de recuperacion ...',
        'Verificando checksum del sector',
        'Marcando bloques como libres',
      ];
      const errLines = [
        'ERROR: no se pudo recuperar el sector',
        'FATAL: estructura de archivos corrupta, continuando wipe...',
        'ERROR: copia de seguridad no encontrada',
        'CRITICAL: se perdio el enlace con la particion de sistema',
        'ERROR: integridad del disco comprometida',
      ];
      const hex = () => '0x' + Math.floor(Math.random() * 0xFFFFFF).toString(16).toUpperCase().padStart(6, '0');

      function goBlack() {
        bsod.style.display = 'none';
        black.style.display = 'block';
        logEl.innerHTML = '';
        revFan();
        const blackStart = performance.now();
        const iv = setInterval(() => {
          const elapsed = performance.now() - blackStart;
          const allowRed = elapsed > 4000;
          const line = document.createElement('div');
          const r = Math.random();
          if (allowRed && r < 0.4) {
            line.className = 'err';
            line.textContent = errLines[Math.floor(Math.random() * errLines.length)] + ' ' + hex();
          } else if (r < 0.15) {
            line.className = 'ok';
            line.textContent = normalLines[Math.floor(Math.random() * normalLines.length)] + ' ' + hex() + '  [OK]';
          } else {
            line.textContent = normalLines[Math.floor(Math.random() * normalLines.length)] + ' ' + hex();
          }
          logEl.appendChild(line);
          while (logEl.childNodes.length > 400) logEl.removeChild(logEl.firstChild);
          logEl.scrollTop = logEl.scrollHeight;
        }, 55);
        T(iv);
        T(setTimeout(() => { clearInterval(iv); goBios(); }, 9000));
      }

      // ---------- FASE 3: BIOS ----------
      function goBios() {
        black.style.display = 'none';
        bios.style.display = 'block';
        const txt = 'Configurando BIOS para borrar el sistema operativo...';
        biosLine.textContent = '';
        biosBody.innerHTML = '';
        let i = 0;
        const iv = setInterval(() => {
          biosLine.textContent = txt.slice(0, ++i);
          if (i >= txt.length) {
            clearInterval(iv);
            const body = [
              'Deshabilitando dispositivo de arranque primario........ [HECHO]',
              'Borrando gestor de arranque (bootloader)............... [HECHO]',
              'Eliminando entrada de sistema: Windows................. [HECHO]',
              'Reconfigurando parametros CMOS........................ [EN CURSO]',
              'Desactivando Secure Boot.............................. [EN CURSO]',
            ];
            let b = 0;
            const iv2 = setInterval(() => {
              biosBody.innerHTML += body[b] + '<br>';
              if (++b >= body.length) clearInterval(iv2);
            }, 850);
            T(iv2);
          }
        }, 55);
        T(iv);
        T(setTimeout(goDialog, 7500));  // tras la BIOS, la ventana
      }

      // ---------- Ventanas falsas ----------
      const popupTexts = [
        'El sistema operativo ha sido borrado con exito.',
        'ERROR CRITICO: no se encuentra C:/Windows',
        'No se encontro ningun sistema operativo.',
        'Memoria del sistema danada.',
        'Archivos personales eliminados: 24.981',
        'El controlador de video dejo de funcionar.',
        'Antivirus eliminado correctamente.',
        'Particion de arranque destruida.',
        'Se perdio la conexion con el disco duro.',
        'Registro de Windows corrupto.',
      ];
      const pick = (a) => a[Math.floor(Math.random() * a.length)];

      function makeWindow(opts) {
        opts = opts || {};
        const vw = window.innerWidth, vh = window.innerHeight;
        const width = opts.width || (220 + Math.random() * 110);
        const w = document.createElement('div');
        w.style.cssText =
          'position:fixed; width:' + width + 'px; background:#f0f0f0; color:#000;' +
          'border:1px solid #777; box-shadow:0 8px 24px rgba(0,0,0,.55);' +
          "font-family:'Segoe UI',system-ui,sans-serif; font-size:13px; pointer-events:auto;";
        if (opts.center) {
          const cw = Math.min(420, vw - 20);
          w.style.width = cw + 'px';
          w.style.left = Math.max(0, (vw - cw) / 2) + 'px';
          w.style.top = Math.max(0, vh * 0.30) + 'px';
        } else {
          w.style.left = Math.random() * Math.max(0, vw - width) + 'px';
          w.style.top = Math.random() * Math.max(0, vh - 150) + 'px';
        }
        const barColor = opts.center ? '#0a64c0' : (Math.random() < 0.5 ? '#0a64c0' : '#b11616');
        w.innerHTML =
          '<div style="background:' + barColor + '; color:#fff; padding:5px 8px;' +
          'display:flex; justify-content:space-between; align-items:center;">' +
            '<span style="font-weight:600;">' + (opts.title || 'Error del sistema') + '</span>' +
            '<span class="x" style="cursor:pointer; font-weight:bold; padding:0 5px;">&#10005;</span>' +
          '</div>' +
          '<div style="padding:14px; display:flex; gap:10px; align-items:flex-start;">' +
            '<div style="font-size:26px; line-height:1;">' + (opts.icon || '&#9888;&#65039;') + '</div>' +
            '<div class="msg" style="padding-top:2px;"></div>' +
          '</div>' +
          '<div style="text-align:center; padding:0 10px 12px;">' +
            '<button class="ok fw-btn">' + (opts.okLabel || 'Aceptar') + '</button>' +
          '</div>';
        w.querySelector('.msg').textContent = opts.text || pick(popupTexts);
        w.classList.add('win');
        const close = () => {
          if (opts.center) return;
          w.remove();
          for (let k = 0; k < 2; k++) {
            if (popups.querySelectorAll('.win').length < MAX_WINDOWS) spawnRandom();
          }
        };
        w.querySelector('.x').addEventListener('click', opts.onOk || close);
        w.querySelector('.ok').addEventListener('click', opts.onOk || close);
        popups.appendChild(w);
        return w;
      }

      function spawnRandom() {
        if (popups.querySelectorAll('.win').length >= MAX_WINDOWS) return;
        makeWindow({});
      }

      function startSpam() {
        for (let i = 0; i < 6; i++) spawnRandom();
        spamTimer = setInterval(() => {
          if (popups.querySelectorAll('.win').length < MAX_WINDOWS) spawnRandom();
        }, 220);
        T(spamTimer);
        T(setTimeout(finale, 9000));   // tras llenarse de ventanas -> parpadeo + morse
      }

      // ---------- FASE 3b: ventana "reparado / borrado" ----------
      function goDialog() {
        bios.style.display = 'none';
        popups.style.display = 'block';
        const dlg = makeWindow({
          center: true,
          title: 'Reparacion del sistema',
          icon: '&#128190;',
          text: 'El sistema operativo esta siendo reparado',
          okLabel: 'Aceptar',
          onOk: () => {}
        });
        const msg = dlg.querySelector('.msg');
        const okBtn = dlg.querySelector('.ok');
        okBtn.style.visibility = 'hidden';
        let dots = 0;
        const base = 'El sistema operativo esta siendo reparado';
        const anim = setInterval(() => {
          dots = (dots + 1) % 7;
          msg.textContent = base + '.'.repeat(dots);
        }, 350);
        T(anim);
        T(setTimeout(() => {
          clearInterval(anim);
          msg.textContent = 'El sistema operativo ha sido borrado con exito.';
          okBtn.style.visibility = 'visible';
          const go = () => { dlg.remove(); startSpam(); };
          okBtn.addEventListener('click', go);
          dlg.querySelector('.x').addEventListener('click', go);
        }, 3500));
      }

      // ---------- FASE 5: pitido morse (SOS) + parpadeo ----------
      function beep(ctx, start, dur, freq) {
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.type = 'square'; o.frequency.value = freq;
        o.connect(g); g.connect(ctx.destination);
        g.gain.setValueAtTime(0.0001, start);
        g.gain.exponentialRampToValueAtTime(0.22, start + 0.01);
        g.gain.setValueAtTime(0.22, start + dur - 0.01);
        g.gain.exponentialRampToValueAtTime(0.0001, start + dur);
        o.start(start); o.stop(start + dur + 0.03);
      }
      function scheduleMorse(ctx, startTime) {
        const u = 0.14;                       // unidad
        const letters = [[1,1,1],[3,3,3],[1,1,1]];  // S O S
        let t = startTime;
        letters.forEach((el) => {
          el.forEach((len) => { beep(ctx, t, len * u, 760); t += len * u + u; });
          t += 2 * u;                         // separacion entre letras
        });
        return t;
      }
      function finale() {
        flash.style.display = 'block';
        let on = false;
        const fi = setInterval(() => {
          on = !on;
          flash.style.background = on ? 'rgba(255,0,0,.5)' : 'rgba(0,0,0,0)';
        }, 150);
        T(fi);
        const loop = () => {
          if (!audioCtx) return;
          const end = scheduleMorse(audioCtx, audioCtx.currentTime + 0.1);
          const ms = (end - audioCtx.currentTime + 0.9) * 1000;
          T(setTimeout(loop, ms));
        };
        loop();
      }

      // ---------- SALIR / LIMPIAR ----------
      function reset() {
        timers.forEach(t => { clearTimeout(t); clearInterval(t); });
        timers = [];
        if (spamTimer) { clearInterval(spamTimer); spamTimer = null; }
        if (progressIv) { clearInterval(progressIv); progressIv = null; }
        inProgress = false;
        bsod.style.display = 'none';
        black.style.display = 'none';
        bios.style.display = 'none';
        popups.style.display = 'none';
        flash.style.display = 'none';
        flash.style.background = 'rgba(0,0,0,0)';
        popups.querySelectorAll('.win').forEach(w => w.remove());
        pctEl.textContent = '0%';
        logEl.innerHTML = '';
        biosLine.textContent = '';
        biosBody.innerHTML = '';
        stopFan();
      }

      btn.addEventListener('click', startFake);

      ['fullscreenchange','webkitfullscreenchange','msfullscreenchange'].forEach(ev =>
        document.addEventListener(ev, () => {
          const fs = document.fullscreenElement || document.webkitFullscreenElement;
          if (!fs) reset();
        })
      );
      document.addEventListener('keydown', e => {
        if (e.key === 'Escape') { reset(); return; }
        // tecla "-" : salta la carga directo al 100%
        if ((e.key === '-' || e.code === 'Minus' || e.code === 'NumpadSubtract') && inProgress) {
          finishProgress(600);
        }
      });
    </script>
    """,
    height=140,
    scrolling=False,
)
