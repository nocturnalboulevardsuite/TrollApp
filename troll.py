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
        display:none; position:fixed; inset:0; z-index:999999; background:#0067c0; color:#fff;
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

    <!-- FASE 2: pantalla negra con codigo y errores -->
    <div id="black" style="
        display:none; position:fixed; inset:0; z-index:999999; background:#000; color:#e8e8e8;
        font-family:'Consolas','Courier New',monospace; font-size:14px; line-height:1.35;
        padding:18px; box-sizing:border-box; overflow:hidden;">
      <div id="log" style="white-space:pre-wrap; height:100%; overflow:hidden;"></div>
      <div class="hint" style="position:fixed; bottom:8px; right:12px; font-size:11px; opacity:.3;">
        (broma — Esc)
      </div>
    </div>

    <!-- FASE 3: BIOS retro -->
    <div id="bios" style="
        display:none; position:fixed; inset:0; z-index:999999; background:#0000a8; color:#c6c6c6;
        font-family:'Courier New',monospace; padding:0; box-sizing:border-box;">
      <div style="background:#c6c6c6; color:#0000a8; padding:4px 10px; font-weight:bold; letter-spacing:1px;">
        PhoenixBIOS Setup Utility &nbsp;—&nbsp; Factory Wipe Module v3.11
      </div>
      <div style="padding:26px 30px;">
        <div style="border:2px solid #c6c6c6; padding:22px 24px; max-width:900px;">
          <div id="biosline" style="font-size:1.35em; color:#ffffff; min-height:1.4em;"></div>
          <div id="biosbody" style="margin-top:18px; color:#ffff55; white-space:pre-wrap;"></div>
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

    <style>
      @keyframes spin { to { transform: rotate(360deg); } }
      @keyframes blink { 50% { opacity:0; } }
      #cur { animation: blink 1s step-end infinite; }
      .err { color:#ff4d4d; font-weight:bold; }
      .ok  { color:#56d364; }
    </style>

    <script>
      const btn   = document.getElementById('go');
      const bsod  = document.getElementById('bsod');
      const black = document.getElementById('black');
      const bios  = document.getElementById('bios');
      const pctEl = document.getElementById('pct');
      const logEl = document.getElementById('log');
      const biosLine = document.getElementById('biosline');
      const biosBody = document.getElementById('biosbody');

      let timers = [];
      let audioCtx = null, fanGain = null, humG = null;
      const T = (id) => { timers.push(id); return id; };

      // ---------- SONIDO DE VENTILADOR (generado, sin archivos) ----------
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

      // ---------- FASE 1: formateo lento ----------
      function startFake() {
        bsod.style.display = 'flex';
        const el = document.documentElement;
        const req = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;
        if (req) req.call(el).catch(() => {});
        startFan();

        let p = 0;
        const iv = setInterval(() => {
          let step;
          if (p < 20)      step = Math.random() * 0.9 + 0.2;
          else if (p < 45) step = Math.random() * 0.5 + 0.1;
          else if (p < 70) step = Math.random() * 0.35;
          else if (p < 92) step = Math.random() * 0.25;
          else if (p < 99) step = Math.random() * 0.08;
          else             step = 0;
          p = Math.min(100, p + step);
          pctEl.textContent = Math.floor(p) + '%';
          if (p >= 100) {
            clearInterval(iv);
            pctEl.textContent = '100%';
            T(setTimeout(goBlack, 2500));
          }
        }, 380);
        T(iv);
      }

      // ---------- FASE 2: pantalla negra con codigo/errores ----------
      const normalLines = [
        'Inicializando modulo de formateo de bajo nivel...',
        'Desmontando volumen principal /dev/sda1 ...',
        'Eliminando tabla de particiones (GPT/MBR) ...',
        'Sobrescribiendo sector',
        'Borrando indice maestro de archivos (MFT) ...',
        'Limpiando registro del sistema HKLM\\\\SYSTEM ...',
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

        const iv = setInterval(() => {
          const line = document.createElement('div');
          const r = Math.random();
          if (r < 0.18) {
            line.className = 'err';
            line.textContent = errLines[Math.floor(Math.random() * errLines.length)] + ' ' + hex();
          } else if (r < 0.28) {
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

        T(setTimeout(() => { clearInterval(iv); goBios(); }, 8000));
      }

      // ---------- FASE 3: BIOS retro ----------
      function goBios() {
        black.style.display = 'none';
        bios.style.display = 'block';
        const txt = 'Configurando BIOS para borrar el sistema operativo...';
        biosLine.textContent = '';
        biosBody.textContent = '';
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
              biosBody.textContent += body[b] + '\\n';
              if (++b >= body.length) clearInterval(iv2);
            }, 900);
            T(iv2);
          }
        }, 55);
        T(iv);
      }

      // ---------- SALIR / LIMPIAR ----------
      function reset() {
        timers.forEach(t => { clearTimeout(t); clearInterval(t); });
        timers = [];
        bsod.style.display = 'none';
        black.style.display = 'none';
        bios.style.display = 'none';
        pctEl.textContent = '0%';
        logEl.innerHTML = '';
        biosLine.textContent = '';
        biosBody.textContent = '';
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
