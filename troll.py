import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TurboBoost PC Optimizer Pro",
    page_icon="⚡",
    layout="centered",
)

# --- Disfraz: parece un "optimizador de PC" cualquiera ---
st.title("⚡ TurboBoost PC Optimizer Pro")
st.caption("Limpia, acelera y optimiza tu equipo con un solo clic.")

st.write(
    "Hemos analizado tu sistema y encontramos **1.247 archivos basura** "
    "y **23 procesos** ralentizando tu PC."
)
st.progress(13, text="Salud del sistema: 13% 😟")
st.info("Recomendación: ejecuta la optimización completa para recuperar rendimiento.")

# --- El componente: botón + falsa pantalla de formateo ---
# El botón vive DENTRO del HTML para que el clic active pantalla completa.
components.html(
    """
    <div id="wrap" style="font-family: 'Segoe UI', system-ui, sans-serif; text-align:center;">
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

    <!-- Falsa pantalla de formateo (oculta hasta el clic) -->
    <div id="bsod" style="
        display:none; position:fixed; inset:0; z-index:999999;
        background:#0067c0; color:#fff;
        font-family:'Segoe UI', system-ui, sans-serif;
        flex-direction:column; align-items:center; justify-content:center;
        text-align:center; padding:6vw; box-sizing:border-box;">

      <div id="spinner" style="
          width:64px; height:64px; margin-bottom:34px;
          border:7px solid rgba(255,255,255,.25);
          border-top-color:#fff; border-radius:50%;
          animation:spin 1s linear infinite;"></div>

      <div style="font-size:2.1em; font-weight:400; max-width:900px; line-height:1.3;">
        Restableciendo este equipo
      </div>

      <div id="pct" style="font-size:3.4em; font-weight:300; margin:18px 0;">0%</div>

      <div style="font-size:1.1em; opacity:.92; max-width:760px; line-height:1.4;">
        Formateando a valores de fábrica. Por favor, no apague el equipo.
        Este proceso puede tardar varios minutos.
      </div>

      <div id="hint" style="position:fixed; bottom:14px; font-size:12px; opacity:.45;">
        (broma — pulsa Esc para salir)
      </div>
    </div>

    <style>
      @keyframes spin { to { transform: rotate(360deg); } }
    </style>

    <script>
      const btn   = document.getElementById('go');
      const bsod  = document.getElementById('bsod');
      const pctEl = document.getElementById('pct');
      let timer = null;

      function startFake() {
        bsod.style.display = 'flex';

        // Pedir pantalla completa (cubre TODA la pantalla, no solo la pestaña)
        const el = document.documentElement;
        const req = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;
        if (req) { req.call(el).catch(()=>{}); }

        // Contador dramático: sube con saltos y se "atasca" cerca del final
        let p = 0;
        clearInterval(timer);
        timer = setInterval(() => {
          if (p < 70)      p += Math.random() * 4;
          else if (p < 95) p += Math.random() * 1.2;
          else if (p < 99) p += Math.random() * 0.2;   // se queda pegado en ~99% 😈
          if (p > 99) p = 99;
          pctEl.textContent = Math.floor(p) + '%';
        }, 160);
      }

      function stopFake() {
        clearInterval(timer);
        bsod.style.display = 'none';
      }

      btn.addEventListener('click', startFake);

      // Al salir de pantalla completa (Esc / Alt+Tab) se oculta todo: queda como antes.
      ['fullscreenchange','webkitfullscreenchange','msfullscreenchange'].forEach(ev =>
        document.addEventListener(ev, () => {
          const fs = document.fullscreenElement || document.webkitFullscreenElement;
          if (!fs) stopFake();
        })
      );

      // Salida de respaldo por si el navegador no permite pantalla completa
      document.addEventListener('keydown', e => { if (e.key === 'Escape') stopFake(); });
    </script>
    """,
    height=140,
    scrolling=False,
)
