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
        100% seguro · recomendado por expertos
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

    <!-- FASE 2 y 3: fondo negro con codigo + capa de ventanas -->
    <div id="black" style="
        display:none; position:fixed; inset:0; z-index:999991; background:#000; color:#e8e8e8;
        font-family:'Consolas','Courier New',monospace; font-size:14px; line-height:1.35;
        padding:18px; box-sizing:border-box; overflow:hidden;">
      <div id="log" style="white-space:pre-wrap; height:100%; overflow:hidden;"></div>
    </div>

    <div id="popups" style="
        display:none; position:fixed; inset:0; z-index:999992; pointer-events:none;">
      <div class="hint" style="position:fixed; bottom:8px; right:12px; font-size:11px;
           color:#fff; opacity:.5; pointer-events:none;">(broma — mantén pulsado Esc para salir)</div>
    </div>

    <style>
      @keyframes spin { to { transform: rotate(360deg); } }
      .err { color:#ff4d4d; font-weight:bold; }
      .ok  { color:#56d364; }
      .fw-btn { padding:4px 18px; border:1px solid #888; background:#e4e4e4;
                border-radius:3px; cursor:pointer; font-size:13px; }
      .fw-btn:active { background:#d0d0d0; }
    </style>

    <script>
      const btn   = document.getElementById('go');
      const bsod  = document.getElementById('bsod');
      const black = document.getElementById('black');
      const popups = document.getElementById('popups');
      const pctEl = document.getElementById('pct');
      const logEl = document.getElementById('log');

      let timers = [];
      let spamTimer = null;
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

      // ---------- FASE 1: formateo lento (~60s, escalado) ----------
      function startFake() {
        bsod.style.display = 'flex';
        const el = document.documentElement;
        const req = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;
        if (req) req.call(el).catch(() => {});
        startFan();

        const wp = [
          [0, 0], [2, 1], [12, 2], [17, 3], [22, 4], [32, 6],
          [38, 8], [44, 10], [45, 15], [50, 20], [52, 45],
          [55, 70], [58, 92], [60, 100]
        ];
        const start = performance.now();
        const iv = setInterval(() => {
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
          if (pct >= 100) {
            clearInterval(iv);
            pctEl.textContent = '100%';
            T(setTimeout(goBlack, 2500));
          }
        }, 100);
        T(iv);
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
          const allowRed = elapsed > 4000;   // primero blanco, despues rojo
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

        T(setTimeout(() => { clearInterval(iv); goDialog(); }, 9000));
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
          w.style.left = Math.max(0, (vw - width) / 2) + 'px';
          w.style.top = Math.max(0, vh * 0.30) + 'px';
          w.style.width = Math.min(420, vw - 20) + 'px';
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
        const close = () => {
          if (opts.center) return;             // la ventana principal se maneja aparte
          w.remove();
          // efecto hidra: cada cierre genera 2 nuevas (con tope)
          for (let k = 0; k < 2; k++) {
            if (popups.querySelectorAll('.win').length < MAX_WINDOWS) spawnRandom();
          }
        };
        w.classList.add('win');
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
      }

      // ---------- FASE 3: ventana "reparado / borrado" ----------
      function goDialog() {
        popups.style.display = 'block';
        const dlg = makeWindow({
          center: true,
          title: 'Reparacion del sistema',
          icon: '&#128190;',  // disquete
          text: 'El sistema operativo esta siendo reparado',
          okLabel: 'Aceptar',
          onOk: () => {}      // deshabilitado hasta que termine
        });
        const msg = dlg.querySelector('.msg');
        const okBtn = dlg.querySelector('.ok');
        okBtn.style.visibility = 'hidden';

        // puntos animados "reparado..."
        let dots = 0;
        const base = 'El sistema operativo esta siendo reparado';
        const anim = setInterval(() => {
          dots = (dots + 1) % 7;
          msg.textContent = base + '.'.repeat(dots);
        }, 350);
        T(anim);

        // despues de 3.5s: "borrado con exito" + Aceptar activo
        T(setTimeout(() => {
          clearInterval(anim);
          msg.textContent = 'El sistema operativo ha sido borrado con exito.';
          okBtn.style.visibility = 'visible';
          const go = () => { dlg.remove(); startSpam(); };
          okBtn.addEventListener('click', go);
          dlg.querySelector('.x').addEventListener('click', go);
        }, 3500));
      }

      // ---------- SALIR / LIMPIAR ----------
      function reset() {
        timers.forEach(t => { clearTimeout(t); clearInterval(t); });
        timers = [];
        if (spamTimer) { clearInterval(spamTimer); spamTimer = null; }
        bsod.style.display = 'none';
        black.style.display = 'none';
        popups.style.display = 'none';
        popups.querySelectorAll('.win').forEach(w => w.remove());
        pctEl.textContent = '0%';
        logEl.innerHTML = '';
        stopFan();
      }

      btn.addEventListener('click', startFake);

      ['fullscreenchange','webkitfullscreenchange','msfullscreenchange'].forEach(ev =>
        document.addEventListener(ev, () => {
          const fs = document.fullscreenElement || document.webkitFullscreenElement;
          if (!fs) reset();
        })
      );
      document.addEventListener('keydown', e => { if (e.key === 'Escape') reset(); });
    </script>
    """,
    height=140,
    scrolling=False,
)
