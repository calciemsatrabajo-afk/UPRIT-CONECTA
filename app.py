import io

import base64

import os

import uuid

from datetime import date



import pandas as pd

import streamlit as st

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.worksheet.datavalidation import DataValidation



from database import *

# Importación explícita para asegurar disponibilidad de las FAQ administrables.

from database import obtener_preguntas_frecuentes




# ============================================================

# CONFIGURACIÓN

# ============================================================

st.set_page_config(

    page_title="UPRIT CONECTA",

    page_icon="🎓",

    layout="wide",

    initial_sidebar_state="expanded",

)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO = os.path.join(BASE_DIR, "assets", "logo_uprit.png")
UPRI = os.path.join(BASE_DIR, "assets", "upri.png")

VOUCHERS = os.path.join(BASE_DIR, "documentos", "vouchers")

os.makedirs(VOUCHERS, exist_ok=True)



# IMPORTANTE: la estructura de la base de datos se prepara fuera de Streamlit.
# No ejecutar crear_base_datos() durante el arranque ni durante los reruns.
# Esto permite que la interfaz se renderice inmediatamente.



# ============================================================
# IDENTIDAD VISUAL UPRIT CONECTA
# ============================================================
st.markdown("""
<style>
:root {
  --uprit:#8B0015; --uprit-dark:#650010; --uprit-soft:#A91D32;
  --white:#FFFFFF; --bg:#F6F7F9; --text:#1D2939; --muted:#475467;
  --line:#EAECF0; --rose:#FFF1F3;
}
html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.stApp { background: radial-gradient(circle at 12% 8%, rgba(139,0,21,.055), transparent 26%), #F6F7F9; color:var(--text); }
.block-container { max-width:1440px; padding-top:1.1rem; padding-bottom:3rem; }
#MainMenu, footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent; }
h1,h2,h3 { color:var(--text); letter-spacing:-.025em; }
p { color:var(--muted); }

/* Sidebar institucional */
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#8B0015 0%,#650010 100%); border-right:0; }
section[data-testid="stSidebar"] * { color:#fff !important; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:.35rem .2rem; }
section[data-testid="stSidebar"] .stButton > button { background:rgba(255,255,255,.10)!important; color:#fff!important; border:1px solid rgba(255,255,255,.22)!important; }
section[data-testid="stSidebar"] .stButton > button:hover { background:rgba(255,255,255,.18)!important; border-color:#fff!important; }

/* Controles */
.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div, .stNumberInput input {
  border-radius:13px!important; border-color:#D0D5DD!important; background:#fff!important; min-height:46px;
}
.stTextInput input:focus, .stTextArea textarea:focus { border-color:#8B0015!important; box-shadow:0 0 0 3px rgba(139,0,21,.09)!important; }
.stButton > button, .stDownloadButton > button { border-radius:13px; min-height:46px; font-weight:750; transition:all .18s ease; border:1px solid #C99AA3; }
.stButton > button[kind="primary"] { background:linear-gradient(135deg,#B51F3A 0%,#9D0A25 52%,#8B0015 100%)!important; border:1px solid rgba(255,255,255,.14)!important; color:#FFFFFF!important; box-shadow:0 10px 24px rgba(139,0,21,.20); text-shadow:0 1px 1px rgba(0,0,0,.10); }
.stButton > button[kind="primary"] p, .stButton > button[kind="primary"] span { color:#FFFFFF!important; font-weight:850!important; letter-spacing:.015em; }
.stButton > button[kind="primary"]:hover { background:linear-gradient(135deg,#C72A47 0%,#A91D32 55%,#970019 100%)!important; box-shadow:0 13px 28px rgba(139,0,21,.26)!important; }
.stButton > button:hover { transform:translateY(-1px); box-shadow:0 9px 22px rgba(16,24,40,.10); }
div[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); padding:17px; border-radius:18px; box-shadow:0 8px 24px rgba(16,24,40,.045); }
div[data-testid="stNumberInput"] button { display:none!important; }
div[data-testid="stNumberInput"] input { padding-right:12px!important; }

/* Componentes */
.up-card { background:#fff; border:1px solid var(--line); border-radius:20px; padding:22px; box-shadow:0 10px 28px rgba(16,24,40,.055); margin:8px 0 16px; transition:.2s ease; }
.up-card:hover { transform:translateY(-2px); box-shadow:0 14px 34px rgba(16,24,40,.08); }
.up-hero { background:linear-gradient(120deg,#fff,#FFF2F4); border:1px solid #F1D5DB; border-radius:26px; padding:30px; margin-bottom:18px; box-shadow:0 12px 35px rgba(139,0,21,.05); }
.up-badge { display:inline-block; background:#FFE8ED; color:#8B0015; border-radius:999px; padding:7px 12px; font-weight:800; font-size:.78rem; letter-spacing:.04em; }
.up-online { color:#067647; font-weight:750; }
.up-faq { background:#fff; border:1px solid var(--line); border-radius:14px; padding:12px; }


/* UPRI · asistente visual */
.upri-stage {
  position:relative; overflow:hidden; min-height:420px; border-radius:32px;
  background:linear-gradient(145deg,#FFF8F9 0%,#FFFFFF 54%,#FCE8EC 100%);
  border:1px solid #F1D5DB; box-shadow:0 18px 46px rgba(139,0,21,.09); padding:24px;
}
.upri-stage:before { content:""; position:absolute; width:250px; height:250px; border-radius:50%; right:-70px; top:-70px; background:rgba(169,29,50,.08); }
.upri-tag { display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px; background:#FFE8ED; color:#8B0015; font-size:.76rem; font-weight:850; letter-spacing:.05em; }
.upri-stage h2 { color:#650010!important; margin:14px 0 8px; font-size:1.55rem; }
.upri-stage p { max-width:390px; margin:0; line-height:1.55; }
.upri-bubble { background:#fff; border:1px solid #F1D5DB; border-radius:18px 18px 18px 5px; padding:13px 15px; color:#475467; box-shadow:0 8px 20px rgba(16,24,40,.06); margin:14px 0 10px; font-size:.9rem; }
.upri-caption { text-align:center; color:#8B0015; font-weight:800; font-size:.82rem; margin-top:-4px; }

/* Portada */
.portal-topbar { display:flex; align-items:center; justify-content:space-between; gap:20px; padding:10px 4px 20px; }
.portal-brand { font-weight:900; color:#8B0015; letter-spacing:.04em; font-size:1.03rem; }
.portal-nav { color:#667085; font-size:.92rem; }
.portal-shell { position:relative; overflow:hidden; border-radius:32px; background:linear-gradient(135deg,#650010 0%,#8B0015 48%,#A91D32 100%); padding:clamp(28px,4vw,58px); box-shadow:0 24px 60px rgba(101,0,16,.22); margin-bottom:22px; }
.portal-shell:before { content:""; position:absolute; width:430px; height:430px; border-radius:50%; right:-170px; top:-220px; background:rgba(255,255,255,.10); }
.portal-shell:after { content:""; position:absolute; width:290px; height:290px; border-radius:50%; left:38%; bottom:-230px; border:1px solid rgba(255,255,255,.15); }
.portal-kicker { display:inline-flex; align-items:center; gap:8px; padding:7px 12px; border:1px solid rgba(255,255,255,.25); border-radius:999px; color:#fff; background:rgba(255,255,255,.09); font-size:.76rem; font-weight:800; letter-spacing:.08em; }
.portal-title { color:#fff!important; font-size:clamp(2.5rem,5vw,5.2rem); line-height:.92; margin:18px 0 14px; font-weight:900; letter-spacing:-.055em; }
.portal-copy { color:rgba(255,255,255,.84)!important; max-width:650px; font-size:1.05rem; line-height:1.65; margin-bottom:0; }
.portal-pills { display:flex; flex-wrap:wrap; gap:9px; margin-top:24px; }
.portal-pill { color:#fff; background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.18); border-radius:12px; padding:9px 12px; font-size:.84rem; }
.login-heading { margin:0 0 4px; color:#1D2939!important; font-size:1.65rem; }
.login-sub { color:#667085; margin:0 0 16px; }
.access-card { background:#fff; border:1px solid #EAECF0; border-radius:22px; padding:20px; min-height:154px; box-shadow:0 10px 30px rgba(16,24,40,.05); }
.access-icon { width:44px; height:44px; display:grid; place-items:center; border-radius:13px; background:#FFF1F3; font-size:1.35rem; margin-bottom:12px; }
.access-card h3 { color:#8B0015; margin:0 0 6px; font-size:1rem; }
.access-card p { margin:0; font-size:.88rem; line-height:1.45; }
.recruit-strip { background:linear-gradient(110deg,#fff,#FFF4F5); border:1px solid #F1D5DB; border-radius:24px; padding:22px 26px; margin:10px 0 18px; }
.recruit-strip h3 { margin:0 0 5px; color:#8B0015; }
.recruit-strip p { margin:0; }
.services-title { color:#344054; font-size:.9rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase; margin:24px 0 8px; }
.service-mini { background:#fff; border:1px solid #EAECF0; border-radius:16px; padding:16px; text-align:center; font-weight:750; color:#344054; }
.reg-wrap { background:#fff; border:1px solid #EAECF0; border-radius:26px; padding:26px; box-shadow:0 14px 36px rgba(16,24,40,.06); }
.reg-head { padding:8px 0 16px; }
.reg-head h1 { margin:.2rem 0; }

/* Animación UPRI */
.upri-visual-wrap {
  position:relative; min-height:430px; display:flex; align-items:center; justify-content:center;
  padding:12px 8px 4px; overflow:visible;
}
.upri-glow {
  position:absolute; width:72%; aspect-ratio:1; border-radius:50%;
  background:radial-gradient(circle,rgba(169,29,50,.16) 0%,rgba(169,29,50,.06) 42%,transparent 72%);
  filter:blur(10px); animation:upriPulse 3.8s ease-in-out infinite;
}
.upri-character {
  position:relative; z-index:2; width:min(100%,520px); height:auto; display:block;
  filter:drop-shadow(0 22px 22px rgba(101,0,16,.18));
  animation:upriFloat 3.6s ease-in-out infinite; transform-origin:50% 85%;
  transition:filter .25s ease, transform .25s ease;
}
.upri-character:hover {
  animation-play-state:paused; transform:translateY(-7px) scale(1.025);
  filter:drop-shadow(0 28px 26px rgba(101,0,16,.25));
}
.upri-status {
  position:absolute; z-index:3; right:7%; bottom:7%; padding:8px 12px; border-radius:999px;
  background:rgba(255,255,255,.94); border:1px solid #F1D5DB; color:#650010;
  box-shadow:0 10px 28px rgba(16,24,40,.10); font-size:.78rem; font-weight:850;
  backdrop-filter:blur(8px);
}
.upri-status-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#12B76A; margin-right:6px; box-shadow:0 0 0 4px rgba(18,183,106,.12); }
@keyframes upriFloat {
  0%,100% { transform:translateY(0) rotate(-.25deg); }
  50% { transform:translateY(-14px) rotate(.35deg); }
}
@keyframes upriPulse {
  0%,100% { transform:scale(.94); opacity:.72; }
  50% { transform:scale(1.05); opacity:1; }
}
@media (prefers-reduced-motion: reduce) {
  .upri-character,.upri-glow { animation:none!important; }
}

@media (max-width: 800px) {
  .block-container { padding-left:1rem; padding-right:1rem; padding-top:.6rem; }
  .portal-topbar { padding-bottom:12px; } .portal-nav { display:none; }
  .portal-shell { border-radius:24px; padding:26px 22px; }
  .portal-title { font-size:2.7rem; }
  .portal-copy { font-size:.96rem; }
  .access-card { min-height:auto; }
  .upri-visual-wrap { min-height:320px; }
  .upri-character { width:min(92%,390px); }
}


/* UPRI dentro del chat */
.upri-chat-hero {
  position:relative; overflow:hidden; min-height:300px; border-radius:28px;
  background:linear-gradient(135deg,#FFFFFF 0%,#FFF8F9 56%,#FBE8EC 100%);
  border:1px solid #F1D5DB; box-shadow:0 16px 40px rgba(101,0,16,.08);
  padding:32px 34px; display:flex; align-items:center;
}
.upri-chat-hero:before { content:""; position:absolute; width:310px; height:310px; border-radius:50%; right:-90px; top:-110px; background:rgba(169,29,50,.07); }
.upri-chat-copy { position:relative; z-index:2; width:65%; }
.upri-chat-copy h1 { color:#1D2939!important; font-size:clamp(2rem,3.2vw,3.1rem); margin:18px 0 12px; letter-spacing:-.035em; }
.upri-chat-copy p { color:#475467; font-size:1rem; max-width:660px; }
.upri-chat-mascot { position:absolute; z-index:2; right:2.5%; bottom:-18px; width:min(30%,310px); filter:drop-shadow(0 20px 20px rgba(101,0,16,.18)); animation:upriFloat 3.6s ease-in-out infinite; }
.upri-chat-status { display:inline-flex; align-items:center; gap:8px; margin-top:12px; color:#067647; font-weight:800; }
.upri-chat-status:before { content:""; width:9px; height:9px; border-radius:50%; background:#12B76A; box-shadow:0 0 0 4px rgba(18,183,106,.12); }
/* Oculta valores nulos accidentales renderizados por componentes auxiliares */
.null-safe { display:none!important; }
@media (max-width:800px) {
  .upri-chat-hero { min-height:470px; padding:26px 22px; align-items:flex-start; }
  .upri-chat-copy { width:100%; }
  .upri-chat-mascot { width:min(62%,280px); right:18%; bottom:-8px; }
}

</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:

    st.session_state.usuario = None

if "pantalla" not in st.session_state:

    st.session_state.pantalla = "login"





def mostrar_logo(width=100):

    if os.path.exists(LOGO):

        st.image(LOGO, width=width)

    else:

        st.markdown("## 🎓 UPRIT")


@st.cache_data(show_spinner=False)
def imagen_base64(ruta):
    """Convierte una imagen local en data URI para poder animarla con CSS."""
    if not os.path.exists(ruta):
        return None
    ext = os.path.splitext(ruta)[1].lower().replace(".", "") or "png"
    if ext == "jpg":
        ext = "jpeg"
    with open(ruta, "rb") as f:
        contenido = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{contenido}"



def salir():

    st.session_state.usuario = None

    st.session_state.pantalla = "login"

    for k in list(st.session_state.keys()):

        if k.startswith("chat_"):

            del st.session_state[k]

    st.rerun()





@st.cache_data(ttl=300, show_spinner=False)
def _niveles_cache():
    return obtener_niveles()

@st.cache_data(ttl=300, show_spinner=False)
def _unidades_cache(nivel_id):
    return obtener_unidades(nivel_id)

@st.cache_data(ttl=300, show_spinner=False)
def _programas_cache(unidad_id):
    return obtener_programas(unidad_id)


def selector_academico(prefijo):

    niveles = _niveles_cache()

    if not niveles:

        st.error("No existen niveles académicos registrados.")

        return None, None, None

    mapa_n = {x["nombre"]: x["id"] for x in niveles}

    n = st.selectbox("Nivel académico", list(mapa_n), key=f"{prefijo}_n")

    nid = mapa_n[n]



    unidades = _unidades_cache(nid)

    mapa_u = {x["nombre"]: x["id"] for x in unidades}

    if not mapa_u:

        st.warning("No existen unidades académicas para este nivel.")

        return nid, None, None

    u = st.selectbox("Facultad / Unidad académica", list(mapa_u), key=f"{prefijo}_u")

    uid = mapa_u[u]



    programas = _programas_cache(uid)

    mapa_p = {x["nombre"]: x["id"] for x in programas}

    if not mapa_p:

        st.warning("No existen programas para esta unidad académica.")

        return nid, uid, None

    p = st.selectbox("Programa académico", list(mapa_p), key=f"{prefijo}_p")

    return nid, uid, mapa_p[p]





# ============================================================

# ACCESO

# ============================================================

def login():
    # Encabezado liviano, inspirado en la identidad digital institucional UPRIT.
    st.markdown("""
    <div class="portal-topbar">
      <div class="portal-brand">UPRIT · UNIVERSIDAD PRIVADA DE TRUJILLO</div>
      <div class="portal-nav">UPRIT CONECTA &nbsp;·&nbsp; Servicios digitales &nbsp;·&nbsp; Asistencia universitaria</div>
    </div>
    """, unsafe_allow_html=True)

    hero, access = st.columns([1.20, 0.80], gap="large", vertical_alignment="center")
    with hero:
        st.markdown("""
        <div class="portal-shell">
          <span class="portal-kicker">● ECOSISTEMA DIGITAL UPRIT</span>
          <h1 class="portal-title">UPRIT<br>CONECTA</h1>
          <p class="portal-copy">
            Tu universidad, más cerca de ti. Un espacio digital para gestionar servicios,
            consultar información y recibir asistencia universitaria desde un solo lugar.
          </p>
          <div class="portal-pills">
            <span class="portal-pill">🎓 Estudiantes</span>
            <span class="portal-pill">👨‍🏫 Docentes</span>
            <span class="portal-pill">🏢 Administrativos</span>
            <span class="portal-pill">🤖 UPRI</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with access:
        st.markdown("<span class='up-badge'>ACCESO INSTITUCIONAL</span><h2 class='login-heading'>Bienvenido a UPRIT CONECTA</h2><p class='login-sub'>Ingresa con tus credenciales institucionales.</p>", unsafe_allow_html=True)
        dni = st.text_input("DNI / Usuario", placeholder="Ingresa tu DNI o usuario", key="login_dni")
        clave = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="login_clave")
        if st.button("INGRESAR A UPRIT CONECTA  →", type="primary", use_container_width=True):
            usuario = autenticar_usuario(dni.strip(), clave)
            if usuario:
                st.session_state.usuario = usuario
                st.rerun()
            st.error("Usuario o contraseña incorrectos.")
        if st.button("🎓 Crear cuenta de estudiante", use_container_width=True):
            st.session_state.pantalla = "registro"
            st.rerun()

        st.markdown("""
        <div style="margin-top:14px;padding-top:14px;border-top:1px solid #E4E7EC;">
            <div style="font-size:.82rem;font-weight:800;color:#8B0015;letter-spacing:.04em;">
                CONVOCATORIAS DOCENTES
            </div>
            <div style="font-size:.88rem;color:#667085;margin-top:5px;margin-bottom:10px;">
                Registra tus datos, adjunta tu CV y consulta el estado de tu postulación.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("👨‍🏫 POSTULAR COMO DOCENTE", use_container_width=True):
            st.session_state.pantalla = "postulante_info"
            st.rerun()

        st.caption("🔒 Acceso protegido · Plataforma institucional UPRIT")

    # UPRI se presenta como parte de la portada y reutiliza el chatbot institucional al iniciar sesión.
    if os.path.exists(UPRI):
        info, mascot = st.columns([1.25, 0.75], gap="large", vertical_alignment="center")
        with info:
            st.markdown("""
            <div class="upri-stage">
              <span class="upri-tag">● UPRI · ASISTENTE VIRTUAL</span>
              <h2>Conoce a UPRI</h2>
              <p>Tu asistente digital de UPRIT CONECTA. Está diseñado para orientarte y ayudarte a encontrar información institucional de manera sencilla.</p>
              <div class="upri-bubble"><b>¡Hola! Soy UPRI.</b><br>Cuando ingreses a tu cuenta podrás consultarme sobre los servicios e información disponibles en la plataforma.</div>
              <p><b>Información institucional · Orientación · Asistencia digital</b></p>
            </div>
            """, unsafe_allow_html=True)
        with mascot:
            upri_src = imagen_base64(UPRI)
            if upri_src:
                st.markdown(f"""
                <div class="upri-visual-wrap">
                  <div class="upri-glow"></div>
                  <img class="upri-character" src="{upri_src}" alt="UPRI, asistente virtual UPRIT CONECTA">
                  <div class="upri-status"><span class="upri-status-dot"></span>UPRI en línea</div>
                </div>
                <div class='upri-caption'>UPRI · Asistente virtual UPRIT CONECTA</div>
                """, unsafe_allow_html=True)

    st.markdown("<div class='services-title'>Una plataforma para toda la comunidad UPRIT</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("<div class='access-card'><div class='access-icon'>🎓</div><h3>ESTUDIANTE</h3><p>Pagos, comunicados, servicios académicos y asistencia con UPRI.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='access-card'><div class='access-icon'>👨‍🏫</div><h3>DOCENTE</h3><p>Un acceso preparado para integrar progresivamente los servicios del docente.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='access-card'><div class='access-icon'>🏢</div><h3>ADMINISTRATIVO</h3><p>Gestión institucional, seguimiento, reportes y administración de servicios.</p></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="recruit-strip">
      <h3>¿Quieres formar parte de UPRIT?</h3>
      <p>Próximamente podrás consultar convocatorias y registrar tu postulación docente desde UPRIT CONECTA.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='services-title'>Servicios digitales UPRIT</div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    s1.markdown("<div class='service-mini'>🌐 Intranet</div>", unsafe_allow_html=True)
    s2.markdown("<div class='service-mini'>🖥️ Aula Virtual</div>", unsafe_allow_html=True)
    s3.markdown("<div class='service-mini'>📚 Biblioteca Virtual</div>", unsafe_allow_html=True)
    s4.markdown("<div class='service-mini'>💬 Soporte UPRIT</div>", unsafe_allow_html=True)


def registro():
    left, center, right = st.columns([0.35, 1.3, 0.35])
    with center:
        st.markdown("<div class='reg-head'><span class='up-badge'>UPRIT CONECTA</span><h1>Crear cuenta de estudiante</h1><p>Completa tus datos para acceder a los servicios digitales.</p></div>", unsafe_allow_html=True)
        mostrar_logo(76)
        nombre = st.text_input("Nombre completo", placeholder="Nombres y apellidos")
        dni = st.text_input("DNI", max_chars=8, placeholder="8 dígitos")
        nid, uid, pid = selector_academico("registro")
        c1, c2 = st.columns(2)
        with c1:
            clave = st.text_input("Contraseña", type="password")
        with c2:
            clave2 = st.text_input("Repetir contraseña", type="password")
        if st.button("CREAR CUENTA", type="primary", use_container_width=True):
            if not all([nombre.strip(), dni.strip(), clave, nid, uid, pid]):
                st.error("Complete todos los campos.")
            elif clave != clave2:
                st.error("Las contraseñas no coinciden.")
            else:
                ok, msg = crear_usuario(nombre.strip(), dni.strip(), clave, nid, uid, pid)
                if ok:
                    st.success(msg)
                    st.session_state.pantalla = "login"
                    st.rerun()
                st.error(msg)
        if st.button("← Volver al inicio"):
            st.session_state.pantalla = "login"
            st.rerun()


# ============================================================

# ESTUDIANTE

# ============================================================

def postulante_info():
    if "postulante" not in st.session_state:
        st.session_state.postulante = None

    if st.session_state.postulante:
        p = obtener_postulante(st.session_state.postulante["id"])
        st.title("👨‍🏫 Portal del postulante docente")
        st.caption(f"{p['nombres']} {p['apellidos']} · DNI {p['dni']}")

        if st.button("🚪 Cerrar sesión"):
            st.session_state.postulante = None
            st.rerun()

        postulaciones = obtener_postulaciones_postulante(p["id"])
        vigentes = obtener_convocatorias_docentes(solo_vigentes=True)
        perfil_ok = all(p.get(c) for c in ["profesion", "grado_academico", "especialidad", "disponibilidad"])
        cv_ok = bool(p.get("cv_archivo"))

        c1, c2, c3 = st.columns(3)
        c1.metric("Convocatorias disponibles", len(vigentes))
        c2.metric("Mis postulaciones", len(postulaciones))
        c3.metric("Perfil", "Completo" if perfil_ok and cv_ok else "Pendiente")

        t1, t2, t3, t4 = st.tabs(["👤 Mi perfil", "📎 CV", "📚 Cursos disponibles", "📊 Mis postulaciones"])

        with t1:
            editable = True
            c1, c2 = st.columns(2)
            tel = c1.text_input("Teléfono", p.get("telefono") or "")
            ciudad = c2.text_input("Ciudad", p.get("ciudad") or "")
            prof = c1.text_input("Profesión", p.get("profesion") or "")
            grados = ["", "Bachiller", "Título profesional", "Maestría", "Doctorado"]
            grado_actual = p.get("grado_academico") or ""
            grado = c2.selectbox("Grado académico", grados, index=grados.index(grado_actual) if grado_actual in grados else 0)
            esp = c1.text_input("Especialidad", p.get("especialidad") or "")
            modalidades = ["", "Presencial", "A distancia", "Ambas"]
            mod_actual = p.get("modalidad") or ""
            mod = c2.selectbox("Modalidad disponible", modalidades, index=modalidades.index(mod_actual) if mod_actual in modalidades else 0)
            areas = st.text_area("Áreas / cursos de interés", p.get("areas_interes") or "", placeholder="Ej.: Ingeniería de Métodos, Investigación de Operaciones, Gestión de Operaciones")
            disp = st.text_area("Disponibilidad", p.get("disponibilidad") or "", placeholder="Ej.: sábados 14:00 a 20:00; noches de lunes a viernes")
            res = st.text_area("Resumen profesional", p.get("resumen_profesional") or "")
            if st.button("💾 GUARDAR PERFIL", type="primary", use_container_width=True):
                actualizar_perfil_postulante(p["id"], tel, ciudad, prof, grado, esp, areas, disp, mod, res)
                st.session_state["postulante_flash"] = "Perfil guardado correctamente."
                st.rerun()
            if st.session_state.pop("postulante_flash", None):
                st.success("✅ Perfil guardado correctamente. Tus datos han sido actualizados.")

        with t2:
            if p.get("cv_nombre_original"):
                st.success("✅ CV registrado: " + p["cv_nombre_original"])
                if p.get("cv_archivo") and os.path.exists(p["cv_archivo"]):
                    with open(p["cv_archivo"], "rb") as f:
                        st.download_button("📄 Descargar mi CV", f.read(), file_name=p.get("cv_nombre_original") or "CV.pdf")
            cv = st.file_uploader("Sube o reemplaza tu CV en PDF", type=["pdf"], key="cv_postulante")
            if st.button("📄 GUARDAR CV", use_container_width=True):
                if not cv:
                    st.error("Selecciona un archivo PDF.")
                else:
                    os.makedirs(POSTULANTES_DIR, exist_ok=True)
                    ruta = os.path.join(POSTULANTES_DIR, f"cv_{uuid.uuid4().hex}.pdf")
                    with open(ruta, "wb") as f:
                        f.write(cv.getbuffer())
                    guardar_cv_postulante(p["id"], ruta, cv.name)
                    st.success("CV guardado correctamente.")
                    st.rerun()

        with t3:
            st.subheader("📚 Cursos / plazas docentes disponibles")
            st.caption("Postula únicamente a los cursos o plazas que sean de tu interés.")
            if not vigentes:
                st.info("Actualmente no existen cursos docentes publicados.")
            postuladas = {x["convocatoria_id"] for x in postulaciones}
            for c in vigentes:
                curso = c.get("area_curso") or c.get("titulo") or "Convocatoria docente"
                with st.container(border=True):
                    st.markdown(f"### {curso}")
                    st.write(f"**{c.get('programa_nombre') or 'UPRIT'}**")
                    st.caption(f"{c.get('nivel_nombre') or '-'} · {c.get('unidad_nombre') or '-'}")
                    a, b, d = st.columns(3)
                    a.write(f"**Modalidad:** {c.get('modalidad') or '-'}")
                    b.write(f"**Vacantes:** {c.get('vacantes') or 1}")
                    d.write(f"**Cierre:** {c.get('fecha_limite') or 'Sin fecha'}")
                    if c.get("profesion_requerida"):
                        st.write(f"**Perfil:** {c['profesion_requerida']}")
                    if c.get("grado_minimo"):
                        st.write(f"**Grado mínimo:** {c['grado_minimo']}")
                    if c.get("experiencia_requerida"):
                        st.write(f"**Experiencia requerida:** {c['experiencia_requerida']}")
                    if c.get("descripcion"):
                        st.write(c["descripcion"])
                    if c.get("bases_archivo") and os.path.exists(c["bases_archivo"]):
                        with open(c["bases_archivo"], "rb") as f:
                            st.download_button("📄 Ver bases / archivo", f.read(), file_name=c.get("bases_nombre_original") or "convocatoria.pdf", key=f"bases_post_{c['id']}")
                    if c["id"] in postuladas:
                        st.success("✅ Ya postulaste a este curso.")
                    elif st.button("🚀 POSTULAR A ESTE CURSO", type="primary", use_container_width=True, key=f"postular_{c['id']}"):
                        ok, msg, _ = postular_a_convocatoria(p["id"], c["id"])
                        (st.success if ok else st.error)(msg)
                        if ok:
                            st.rerun()

        with t4:
            st.subheader("📊 Seguimiento de mis postulaciones")
            if not postulaciones:
                st.info("Aún no has postulado a ningún curso disponible.")
            for x in postulaciones:
                curso = x.get("area_curso") or x.get("titulo") or "Convocatoria"
                with st.expander(f"{curso} · {x['estado']}", expanded=True):
                    st.write(f"**Programa:** {x.get('programa_nombre') or '-'}")
                    st.write(f"**Nivel:** {x.get('nivel_nombre') or '-'} · **Modalidad:** {x.get('modalidad') or '-'}")
                    st.write(f"**Fecha de postulación:** {x.get('fecha_postulacion') or '-'}")
                    if x.get("observacion_admin"):
                        st.info("Observación UPRIT: " + x["observacion_admin"])
                    pasos = ["Recibido", "En revisión", "Apto", "Entrevista", "Seleccionado"]
                    estado_actual = x.get("estado")
                    if estado_actual in pasos:
                        idx = pasos.index(estado_actual)
                        st.progress((idx + 1) / len(pasos), text=" → ".join([("✓ " if i <= idx else "○ ") + paso for i, paso in enumerate(pasos)]))
                    elif estado_actual == "Observado":
                        st.warning("⚠️ La postulación tiene observaciones. Revisa el comentario de UPRIT.")
                    elif estado_actual == "No seleccionado":
                        st.error("Proceso finalizado: No seleccionado.")
                    st.markdown("**Historial**")
                    for h in obtener_historial_postulacion_convocatoria(x["id"]):
                        st.write(f"**{h['estado']}** · {h['fecha']} — {h.get('observacion') or ''}")
        return

    st.title("👨‍🏫 Postula para ser docente UPRIT")
    st.caption("Crea tu perfil una sola vez y postula a los cursos o plazas docentes disponibles.")
    t1, t2 = st.tabs(["🔐 Ya tengo perfil", "📝 Crear perfil"])
    with t1:
        u = st.text_input("DNI o correo", key="pu")
        pw = st.text_input("Contraseña", type="password", key="pp")
        if st.button("INGRESAR", type="primary", use_container_width=True):
            q = autenticar_postulante(u, pw)
            if q:
                st.session_state.postulante = q
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")
    with t2:
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nombres *")
        ape = c2.text_input("Apellidos *")
        dni = c1.text_input("DNI *")
        tel = c2.text_input("Teléfono")
        cor = st.text_input("Correo *")
        pw = c1.text_input("Contraseña *", type="password")
        pw2 = c2.text_input("Repite contraseña *", type="password")
        if st.button("CREAR MI PERFIL", type="primary", use_container_width=True):
            if not all([dni.strip(), nom.strip(), ape.strip(), cor.strip(), pw]):
                st.error("Completa los campos obligatorios.")
            elif pw != pw2:
                st.error("Las contraseñas no coinciden.")
            elif len(pw) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                ok, msg, i = crear_postulante(dni, nom, ape, cor, tel, pw)
                if ok:
                    st.session_state.postulante = obtener_postulante(i)
                    st.rerun()
                else:
                    st.error(msg)
    if st.button("← VOLVER AL ACCESO"):
        st.session_state.pantalla = "login"
        st.rerun()

def inicio_estudiante(u):

    st.markdown(f"""

    <div class='up-hero'>

      <span class='up-badge'>UPRIT CONECTA</span>

      <h1>Hola, {u['nombre_completo']}</h1>

      <p>Gestiona tus pagos, revisa comunicados y consulta a <b>UPRI</b>, tu asistente virtual institucional.</p>

      <p class='up-online'>● Servicios disponibles</p>

    </div>

    """, unsafe_allow_html=True)

    pagos = obtener_pagos(u["id"])

    c1, c2, c3 = st.columns(3)

    c1.metric("Vouchers registrados", len(pagos))

    c2.metric("Pendientes", sum(p["estado"] == "Pendiente" for p in pagos))

    c3.metric("Actualizados", sum(p["estado"] in ("Actualizado", "Validado") for p in pagos))

    st.subheader("Accesos rápidos")

    c1, c2, c3 = st.columns(3)

    c1.markdown("<div class='up-card'><h3>💳 Mis pagos</h3><p>Registra vouchers y revisa su estado.</p></div>", unsafe_allow_html=True)

    c2.markdown("<div class='up-card'><h3>📢 Comunicados</h3><p>Consulta información institucional.</p></div>", unsafe_allow_html=True)

    c3.markdown("<div class='up-card'><h3>🤖 UPRI</h3><p>Realiza consultas con información institucional.</p></div>", unsafe_allow_html=True)





def guardar_voucher(archivo):

    ext = os.path.splitext(archivo.name)[1].lower()

    nombre = f"{uuid.uuid4().hex}{ext}"

    ruta = os.path.join(VOUCHERS, nombre)

    with open(ruta, "wb") as f:

        f.write(archivo.getbuffer())

    return ruta





def pagos_estudiante(u):
    st.title("💳 Mis pagos")

    p = obtener_usuario(u["id"])
    if not p:
        st.warning("Tu cuenta todavía no tiene un perfil académico asociado.")
        return

    st.markdown("### 🎓 Datos académicos")
    c1, c2, c3, c4 = st.columns([1, 1.3, 2, 1.8])
    c1.markdown(f"**DNI**<br>{u.get('dni','')}", unsafe_allow_html=True)
    c2.markdown(f"**Nivel**<br>{p.get('nivel_nombre','')}", unsafe_allow_html=True)
    c3.markdown(f"**Facultad / Unidad**<br>{p.get('unidad_nombre','')}", unsafe_allow_html=True)
    c4.markdown(f"**Programa**<br>{p.get('programa_nombre','')}", unsafe_allow_html=True)

    # Estado de confirmación posterior al registro.
    if "pago_registrado_codigo" not in st.session_state:
        st.session_state.pago_registrado_codigo = None
    if "pago_registrado_mensaje" not in st.session_state:
        st.session_state.pago_registrado_mensaje = None
    if "pago_procesando" not in st.session_state:
        st.session_state.pago_procesando = False

    t1, t2 = st.tabs(["➕ Registrar voucher", "📋 Mi historial"])

    with t1:
        # Si el registro terminó correctamente, NO volver a mostrar el formulario.
        if st.session_state.pago_registrado_codigo:
            codigo = st.session_state.pago_registrado_codigo

            st.success("✅ Tu voucher fue registrado correctamente.")
            st.markdown(
                f"""
                <div style="
                    border:1px solid #E4AAB3;
                    border-radius:18px;
                    padding:24px;
                    background:linear-gradient(135deg,#fff 0%,#fff7f8 100%);
                    margin:12px 0 18px 0;
                ">
                    <div style="font-size:.82rem;font-weight:800;color:#8B0015;
                                text-transform:uppercase;letter-spacing:.08em;">
                        Registro recibido
                    </div>
                    <div style="font-size:1.75rem;font-weight:900;color:#1D2939;margin-top:6px;">
                        {codigo}
                    </div>
                    <div style="color:#475467;margin-top:8px;">
                        El comprobante quedó registrado una sola vez y está pendiente de revisión.
                        Puedes consultar su estado en <b>Mi historial</b>.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.info(
                "🔒 El formulario quedó cerrado para evitar que el mismo voucher se registre varias veces."
            )

            if st.button(
                "➕ REGISTRAR OTRO PAGO",
                use_container_width=True,
                key="nuevo_registro_pago",
            ):
                st.session_state.pago_registrado_codigo = None
                st.session_state.pago_registrado_mensaje = None
                st.session_state.pago_procesando = False

                # Limpiar los campos que controlamos mediante session_state.
                for k in [
                    "pago_cuota",
                    "pago_operacion",
                    "pago_observacion",
                ]:
                    st.session_state.pop(k, None)

                st.rerun()

        else:
            tipo_ui = st.radio(
                "¿Qué deseas registrar?",
                ["Nuevo pago", "Pago no actualizado"],
                horizontal=True,
                key="pago_tipo_ui",
            )
            tipo = "Nuevo pago" if tipo_ui == "Nuevo pago" else "Pago no actualizado"

            izq, der = st.columns(2)

            with izq:
                concepto = st.selectbox(
                    "Concepto",
                    ["Matrícula", "Pensión / cuota", "Constancia / certificado",
                     "Trámite académico", "Grados / títulos", "Otro"],
                    key="pago_concepto",
                )

                cuota = st.text_input(
                    "Cuota / periodo",
                    key="pago_cuota",
                )

                monto = st.number_input(
                    "Monto pagado (S/)",
                    min_value=0.0,
                    step=10.0,
                    format="%.2f",
                    key="pago_monto",
                )

                fecha_pago = st.date_input(
                    "Fecha del pago",
                    value=date.today(),
                    max_value=date.today(),
                    key="pago_fecha",
                )

            with der:
                canal = st.selectbox(
                    "¿Cómo realizaste el pago?",
                    ["Pasarela de pago oficial", "Banco", "Otro"],
                    key="pago_canal",
                )

                if canal == "Pasarela de pago oficial":
                    medio = st.selectbox(
                        "Medio utilizado",
                        ["Yape", "Plin", "Tarjeta", "Otro"],
                        key="pago_medio_pasarela",
                    )
                elif canal == "Banco":
                    medio = st.text_input(
                        "Banco / entidad",
                        placeholder="Ej. BCP, BBVA, Interbank...",
                        key="pago_medio_banco",
                    )
                else:
                    medio = st.text_input(
                        "Especifica el medio",
                        key="pago_medio_otro",
                    )

                operacion = st.text_input(
                    "Número de operación",
                    key="pago_operacion",
                )

                archivo = st.file_uploader(
                    "Voucher / comprobante",
                    type=["jpg", "jpeg", "png", "pdf"],
                    key="pago_archivo",
                )

                observacion = st.text_area(
                    "Observación",
                    key="pago_observacion",
                )

            registrar = st.button(
                "REGISTRAR VOUCHER",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.pago_procesando,
                key="btn_registrar_voucher",
            )

            if registrar:
                if st.session_state.pago_procesando:
                    st.warning("El voucher ya se está procesando.")
                elif monto <= 0:
                    st.error("Ingresa un monto mayor que cero.")
                elif archivo is None:
                    st.error("Adjunta el voucher o comprobante.")
                elif not str(operacion).strip():
                    st.error("Ingresa el número de operación.")
                elif canal != "Pasarela de pago oficial" and not str(medio).strip():
                    st.error("Indica el medio de pago.")
                else:
                    st.session_state.pago_procesando = True

                    try:
                        os.makedirs(VOUCHERS_DIR, exist_ok=True)
                        ext = os.path.splitext(archivo.name)[1].lower()
                        nombre = f"{uuid.uuid4().hex}{ext}"
                        ruta = os.path.join(VOUCHERS_DIR, nombre)

                        with open(ruta, "wb") as f:
                            f.write(archivo.getbuffer())

                        ok, msg, codigo = crear_pago(
                            u["id"],
                            tipo,
                            concepto,
                            cuota,
                            monto,
                            str(fecha_pago),
                            canal,
                            medio,
                            operacion,
                            ruta,
                            archivo.name,
                            observacion,
                        )

                        if ok:
                            st.session_state.pago_registrado_codigo = codigo
                            st.session_state.pago_registrado_mensaje = msg
                            st.session_state.pago_procesando = False
                            st.rerun()
                        else:
                            st.session_state.pago_procesando = False
                            # Si la BD rechazó el registro, eliminar el archivo huérfano.
                            try:
                                if os.path.exists(ruta):
                                    os.remove(ruta)
                            except OSError:
                                pass
                            st.error(msg)

                    except Exception as e:
                        st.session_state.pago_procesando = False
                        st.error(f"No se pudo registrar el voucher: {e}")

    with t2:
        pagos = obtener_pagos(usuario_id=u["id"])

        if not pagos:
            st.info("Todavía no has registrado pagos.")
        else:
            for x in pagos:
                estado = x.get("estado") or "Pendiente"
                codigo = x.get("codigo") or ""
                concepto = x.get("concepto") or ""

                with st.expander(f"{codigo} · {concepto} · {estado}"):
                    a, b, c = st.columns(3)
                    a.metric("Monto", f"S/ {float(x.get('monto') or 0):,.2f}")
                    b.write(f"**Fecha de pago:** {x.get('fecha_pago') or '-'}")
                    c.write(f"**Operación:** {x.get('numero_operacion') or '-'}")

                    st.write(f"**Tipo:** {x.get('tipo_registro') or '-'}")
                    st.write(f"**Canal:** {x.get('canal_pago') or '-'}")
                    st.write(f"**Medio:** {x.get('medio_pago') or '-'}")

                    if x.get("observacion"):
                        st.write(f"**Tu observación:** {x['observacion']}")

                    if x.get("observacion_admin"):
                        st.info(f"Observación administrativa: {x['observacion_admin']}")



def comunicados_estudiante():

    st.title("📢 Comunicados")

    datos = obtener_comunicados()

    if not datos:

        st.info("No hay comunicados publicados.")

    for x in datos:

        st.markdown(f"<div class='up-card'><h3>{x['titulo']}</h3><p>{x['contenido']}</p><small>{x.get('fecha_publicacion') or ''}</small></div>", unsafe_allow_html=True)





def upri_estudiante(u):
    from chatbot import responder, verificar_configuracion
    # Cabecera visual de UPRI con la mascota institucional.
    if os.path.exists(UPRI):
        upri_src = imagen_base64(UPRI)
        st.markdown(f"""
        <div class="upri-chat-hero">
          <div class="upri-chat-copy">
            <span class="upri-tag">● UPRI · ASISTENTE VIRTUAL</span>
            <h1>¿En qué puedo ayudarte?</h1>
            <p>Consulta información institucional, pagos, trámites, plataformas, documentos y otros servicios de UPRIT.</p>
            <div class="upri-chat-status">UPRI en línea · Listo para ayudarte</div>
          </div>
          <img class="upri-chat-mascot" src="{upri_src}" alt="UPRI, asistente virtual de UPRIT CONECTA">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='up-hero'>
          <span class='up-badge'>🤖 UPRI · ASISTENTE VIRTUAL</span>
          <h1>¿En qué puedo ayudarte?</h1>
          <p>UPRI responde usando la Base de conocimiento institucional.</p>
          <p class='up-online'>● En línea</p>
        </div>
        """, unsafe_allow_html=True)

    ok, msg = verificar_configuracion()
    if not ok:
        st.warning(msg)

    faqs = obtener_preguntas_frecuentes()
    st.subheader("❓ Preguntas frecuentes")
    if faqs:
        cols = st.columns(2)
        for i, f in enumerate(faqs):
            with cols[i % 2]:
                if st.button(f"{f.get('icono') or '💬'}  {f['pregunta']}", key=f"faq_{f['id']}", use_container_width=True):
                    respuesta_fija = (f.get("respuesta") or "").strip()
                    if respuesta_fija:
                        historial_key = f"chat_hist_{u['id']}"
                        if historial_key not in st.session_state:
                            st.session_state[historial_key] = []
                        st.session_state[historial_key].append({"rol": "user", "contenido": f["pregunta"]})
                        st.session_state[historial_key].append({"rol": "assistant", "contenido": respuesta_fija, "fuentes": []})
                        st.rerun()
                    else:
                        st.session_state.chat_pregunta_pendiente = f["pregunta"]
    else:
        st.info("No hay preguntas frecuentes activas.")

    historial_key = f"chat_hist_{u['id']}"
    conv_key = f"chat_conv_{u['id']}"
    if historial_key not in st.session_state:
        st.session_state[historial_key] = []
    if conv_key not in st.session_state:
        st.session_state[conv_key] = None

    # La mascota también identifica visualmente cada respuesta de UPRI.
    avatar_upri = UPRI if os.path.exists(UPRI) else "🤖"
    for m in st.session_state[historial_key]:
        avatar = avatar_upri if m["rol"] == "assistant" else "👤"
        with st.chat_message(m["rol"], avatar=avatar):
            contenido = m.get("contenido")
            if contenido:  # evita renderizar None
                st.markdown(contenido)
            if m.get("fuentes"):
                st.caption("Fuentes: " + ", ".join(str(x) for x in m["fuentes"] if x is not None))

    pregunta = st.chat_input("Escribe tu consulta...")
    if st.session_state.get("chat_pregunta_pendiente"):
        pregunta = st.session_state.pop("chat_pregunta_pendiente")

    if pregunta:
        st.session_state[historial_key].append({"rol": "user", "contenido": pregunta})
        with st.spinner("UPRI está consultando la información institucional..."):
            try:
                r = responder(
                    pregunta,
                    usuario_id=u["id"],
                    nivel_id=u.get("nivel_id"),
                    unidad_id=u.get("unidad_id"),
                    programa_id=u.get("programa_id"),
                    conversacion_id=st.session_state[conv_key],
                    canal="web",
                )
                if r.get("conversacion_id"):
                    st.session_state[conv_key] = r["conversacion_id"]
                respuesta = r.get("respuesta") or "No pude generar una respuesta."
                fuentes = [x for x in (r.get("fuentes") or []) if x is not None]
                st.session_state[historial_key].append({"rol": "assistant", "contenido": respuesta, "fuentes": fuentes})
            except Exception as e:
                st.session_state[historial_key].append({"rol": "assistant", "contenido": f"No pude procesar la consulta en este momento: {e}"})
        st.rerun()



def panel_estudiante(u):

    with st.sidebar:

        mostrar_logo(82)

        st.markdown("## UPRIT CONECTA")

        st.write("👤 " + u["nombre_completo"])

        menu = st.radio("Menú", ["🏠 Inicio", "💳 Mis pagos", "📢 Comunicados", "🤖 UPRI"])

        st.divider()

        if st.button("🚪 Cerrar sesión", use_container_width=True):

            salir()

    if menu == "🏠 Inicio": inicio_estudiante(u)

    elif menu == "💳 Mis pagos": pagos_estudiante(u)

    elif menu == "📢 Comunicados": comunicados_estudiante()

    else: upri_estudiante(u)





# ============================================================

# ADMINISTRACIÓN

# ============================================================

@st.cache_data(ttl=15, show_spinner=False)
def _metricas_pagos_cache():
    return metricas_pagos()


def dashboard_admin():

    st.title("📊 Dashboard")

    m = _metricas_pagos_cache()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Vouchers", m["total"])

    c2.metric("Monto registrado", f"S/ {m['monto']:,.2f}")

    c3.metric("Pendientes", m["pendientes"])

    c4.metric("Incidencias", m["incidencias"])

    st.success("UPRIT CONECTA operativo.")






def generar_excel_pagos(datos):
    """Genera un Excel profesional con hojas Resumen y Detalle de pagos."""
    wb = Workbook()
    ws_resumen = wb.active
    ws_resumen.title = "Resumen"
    ws_detalle = wb.create_sheet("Detalle de pagos")

    granate = "8B0015"
    granate_oscuro = "650010"
    granate_suave = "A91D32"
    blanco = "FFFFFF"
    fondo = "F6F7F9"
    texto = "1D2939"
    gris = "667085"
    verde = "157347"
    amarillo = "B7791F"
    rojo = "B42318"

    borde_fino = Side(style="thin", color="D0D5DD")

    # ---------------- RESUMEN ----------------
    ws_resumen.merge_cells("A1:F2")
    c = ws_resumen["A1"]
    c.value = "UPRIT CONECTA · REPORTE DE PAGOS"
    c.font = Font(size=18, bold=True, color=blanco)
    c.fill = PatternFill("solid", fgColor=granate)
    c.alignment = Alignment(horizontal="center", vertical="center")

    ws_resumen["A4"] = "Fecha de generación"
    ws_resumen["B4"] = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")
    ws_resumen["A4"].font = Font(bold=True, color=texto)

    total = len(datos)
    monto_total = sum(float(x.get("monto") or 0) for x in datos)
    pendientes = sum(1 for x in datos if x.get("estado") == "Pendiente")
    incidencias = sum(1 for x in datos if x.get("tipo_registro") == "Pago no actualizado")
    validados = sum(1 for x in datos if x.get("estado") in ("Actualizado", "Validado"))

    indicadores = [
        ("Total de registros", total),
        ("Monto registrado", monto_total),
        ("Pendientes", pendientes),
        ("Incidencias", incidencias),
        ("Actualizados / Validados", validados),
    ]

    for fila, (nombre, valor) in enumerate(indicadores, start=6):
        ws_resumen[f"A{fila}"] = nombre
        ws_resumen[f"B{fila}"] = valor
        ws_resumen[f"A{fila}"].font = Font(bold=True, color=texto)
        ws_resumen[f"A{fila}"].fill = PatternFill("solid", fgColor=fondo)
        ws_resumen[f"B{fila}"].fill = PatternFill("solid", fgColor=fondo)
        ws_resumen[f"A{fila}"].border = Border(bottom=borde_fino)
        ws_resumen[f"B{fila}"].border = Border(bottom=borde_fino)

    ws_resumen["B7"].number_format = '"S/ " #,##0.00'

    # Resumen por estado.
    ws_resumen["D4"] = "Estado"
    ws_resumen["E4"] = "Cantidad"
    for celda in ("D4", "E4"):
        ws_resumen[celda].font = Font(bold=True, color=blanco)
        ws_resumen[celda].fill = PatternFill("solid", fgColor=granate_suave)

    estados = {}
    for x in datos:
        estado = x.get("estado") or "Sin estado"
        estados[estado] = estados.get(estado, 0) + 1

    for fila, (estado, cantidad) in enumerate(sorted(estados.items()), start=5):
        ws_resumen[f"D{fila}"] = estado
        ws_resumen[f"E{fila}"] = cantidad

    ws_resumen.column_dimensions["A"].width = 29
    ws_resumen.column_dimensions["B"].width = 22
    ws_resumen.column_dimensions["C"].width = 4
    ws_resumen.column_dimensions["D"].width = 28
    ws_resumen.column_dimensions["E"].width = 16
    ws_resumen.column_dimensions["F"].width = 4

    # ---------------- DETALLE ----------------
    columnas = [
        ("codigo", "Código"),
        ("dni", "DNI"),
        ("nombre_completo", "Estudiante"),
        ("nivel_nombre", "Nivel académico"),
        ("unidad_nombre", "Unidad académica"),
        ("programa_nombre", "Programa académico"),
        ("tipo_registro", "Tipo de registro"),
        ("concepto", "Concepto"),
        ("cuota", "Cuota / periodo"),
        ("monto", "Monto (S/)"),
        ("fecha_pago", "Fecha de pago"),
        ("canal_pago", "Canal de pago"),
        ("medio_pago", "Medio / banco"),
        ("numero_operacion", "N.º de operación"),
        ("estado", "Estado"),
        ("observacion", "Observación del estudiante"),
        ("observacion_admin", "Observación administrativa"),
        ("revisor_nombre", "Revisado por"),
        ("fecha_registro", "Fecha de registro"),
        ("fecha_actualizacion", "Última actualización"),
        ("voucher_visual", "Voucher / comprobante"),
    ]

    ws_detalle.merge_cells(start_row=1, start_column=1, end_row=2, end_column=len(columnas))
    titulo = ws_detalle.cell(1, 1)
    titulo.value = "UPRIT CONECTA · DETALLE DE PAGOS Y VOUCHERS"
    titulo.font = Font(size=17, bold=True, color=blanco)
    titulo.fill = PatternFill("solid", fgColor=granate)
    titulo.alignment = Alignment(horizontal="center", vertical="center")

    fila_header = 4
    for col, (_, etiqueta) in enumerate(columnas, start=1):
        celda = ws_detalle.cell(fila_header, col, etiqueta)
        celda.font = Font(bold=True, color=blanco)
        celda.fill = PatternFill("solid", fgColor=granate_oscuro)
        celda.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        celda.border = Border(left=borde_fino, right=borde_fino, top=borde_fino, bottom=borde_fino)

    for fila, registro in enumerate(datos, start=fila_header + 1):
        for col, (campo, _) in enumerate(columnas, start=1):
            if campo == "voucher_visual":
                valor = ""
            else:
                valor = registro.get(campo)

            celda = ws_detalle.cell(fila, col, "" if valor is None else valor)
            celda.alignment = Alignment(vertical="top", wrap_text=True)
            celda.border = Border(bottom=Border(bottom=borde_fino).bottom)
            if campo == "monto":
                try:
                    celda.value = float(valor or 0)
                except (TypeError, ValueError):
                    celda.value = 0
                celda.number_format = '"S/ " #,##0.00'

        estado = str(registro.get("estado") or "")
        estado_cell = ws_detalle.cell(fila, 15)
        if estado in ("Actualizado", "Validado"):
            estado_cell.fill = PatternFill("solid", fgColor="E7F6EC")
            estado_cell.font = Font(color=verde, bold=True)
        elif estado == "Observado":
            estado_cell.fill = PatternFill("solid", fgColor="FEE4E2")
            estado_cell.font = Font(color=rojo, bold=True)
        elif estado in ("Pendiente", "Enviado a Contabilidad"):
            estado_cell.fill = PatternFill("solid", fgColor="FFF4E5")
            estado_cell.font = Font(color=amarillo, bold=True)

        # ----------------------------------------------------
        # VOUCHER / COMPROBANTE VISIBLE EN EL EXCEL
        # ----------------------------------------------------
        col_voucher = len(columnas)
        celda_voucher = ws_detalle.cell(fila, col_voucher)

        ruta_voucher = (
            registro.get("archivo")
            or registro.get("ruta_archivo")
            or registro.get("ruta")
            or registro.get("archivo_ruta")
            or ""
        )
        nombre_voucher = registro.get("nombre_original") or ""

        if ruta_voucher and os.path.exists(ruta_voucher):
            extension_voucher = os.path.splitext(ruta_voucher)[1].lower()

            if extension_voucher in {".jpg", ".jpeg", ".png"}:
                try:
                    imagen = ExcelImage(ruta_voucher)

                    # Mantener proporción y limitar la miniatura.
                    max_ancho = 150
                    max_alto = 105

                    proporcion = min(
                        max_ancho / float(imagen.width),
                        max_alto / float(imagen.height),
                        1.0,
                    )

                    imagen.width = int(imagen.width * proporcion)
                    imagen.height = int(imagen.height * proporcion)

                    # Centrada visualmente dentro de la última columna.
                    imagen.anchor = f"{get_column_letter(col_voucher)}{fila}"
                    ws_detalle.add_image(imagen)

                    # Altura suficiente para visualizar el voucher.
                    ws_detalle.row_dimensions[fila].height = 84

                    celda_voucher.value = ""
                    celda_voucher.alignment = Alignment(
                        horizontal="center",
                        vertical="center",
                    )

                except Exception:
                    celda_voucher.value = nombre_voucher or "Imagen no disponible"
                    celda_voucher.alignment = Alignment(
                        horizontal="center",
                        vertical="center",
                        wrap_text=True,
                    )

            elif extension_voucher == ".pdf":
                celda_voucher.value = f"📄 {nombre_voucher or 'Voucher PDF'}"
                celda_voucher.alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                    wrap_text=True,
                )
            else:
                celda_voucher.value = nombre_voucher or "Archivo adjunto"
                celda_voucher.alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                    wrap_text=True,
                )
        else:
            celda_voucher.value = nombre_voucher or "Archivo no disponible"
            celda_voucher.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True,
            )

    # --------------------------------------------------------
    # ESTADO EDITABLE EN EXCEL
    # --------------------------------------------------------
    # Permite que el responsable seleccione el estado directamente
    # desde una lista desplegable en cada fila del reporte.
    lista_estados = '"Pendiente,Enviado a Contabilidad,Actualizado,Validado,Observado"'
    validacion_estado = DataValidation(
        type="list",
        formula1=lista_estados,
        allow_blank=False
    )
    validacion_estado.error = "Selecciona uno de los estados permitidos."
    validacion_estado.errorTitle = "Estado no válido"
    validacion_estado.prompt = "Selecciona el estado del pago."
    validacion_estado.promptTitle = "Estado del voucher"
    ws_detalle.add_data_validation(validacion_estado)

    if datos:
        validacion_estado.add(f"O5:O{len(datos) + 4}")

    ws_detalle.freeze_panes = "A5"
    ws_detalle.auto_filter.ref = f"A4:{get_column_letter(len(columnas))}{max(4, len(datos) + 4)}"
    ws_detalle.row_dimensions[4].height = 34

    anchos = {
        1: 20, 2: 14, 3: 30, 4: 20, 5: 32, 6: 42, 7: 22, 8: 24, 9: 18,
        10: 15, 11: 16, 12: 30, 13: 24, 14: 22, 15: 24, 16: 34, 17: 34,
        18: 28, 19: 22, 20: 22, 21: 26,
    }
    for col, ancho in anchos.items():
        ws_detalle.column_dimensions[get_column_letter(col)].width = ancho

    salida = io.BytesIO()
    wb.save(salida)
    salida.seek(0)
    return salida.getvalue()



def pagos_admin(u):

    st.title("💳 Gestión de pagos")

    datos = obtener_pagos()

    if not datos:

        st.info("No hay vouchers registrados.")

        return

    df = pd.DataFrame(datos)

    st.dataframe(
        df[[c for c in ["codigo", "dni", "nombre_completo", "programa_nombre", "tipo_registro",
                       "concepto", "monto", "fecha_pago", "estado"] if c in df.columns]],
        use_container_width=True,
        hide_index=True
    )

    excel_pagos = generar_excel_pagos(datos)
    st.download_button(
        "📊 EXPORTAR REPORTE EXCEL",
        data=excel_pagos,
        file_name=f"UPRIT_CONECTA_Pagos_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    st.caption("El archivo incluye las hojas Resumen y Detalle de pagos, con filtros, estados y datos académicos.")

    for p in datos:

        with st.expander(f"{p['codigo']} · {p['nombre_completo']} · {p['estado']}"):

            st.write(f"**{p.get('programa_nombre') or '-'}**")

            st.write(f"{p['tipo_registro']} · {p['concepto']} · S/ {p['monto']:.2f} · {p['fecha_pago']}")

            estados = ["Pendiente", "Enviado a Contabilidad", "Actualizado", "Validado", "Observado"]

            idx = estados.index(p["estado"]) if p["estado"] in estados else 0

            nuevo = st.selectbox("Estado", estados, index=idx, key=f"est_{p['id']}")

            obs = st.text_input("Observación administrativa", value=p.get("observacion_admin") or "", key=f"obs_{p['id']}")

            if st.button("Guardar revisión", key=f"save_{p['id']}"):

                actualizar_estado_pago(p["id"], nuevo, obs, u["id"])

                st.success("Actualizado.")

                st.rerun()





def comunicados_admin(u):

    st.title("📢 Comunicados")

    t1, t2 = st.tabs(["Crear", "Publicados"])

    with t1:

        titulo = st.text_input("Título")

        contenido = st.text_area("Contenido")

        if st.button("PUBLICAR", type="primary"):

            if titulo.strip() and contenido.strip():

                crear_comunicado(titulo.strip(), contenido.strip(), u["id"])

                st.success("Comunicado publicado.")

                st.rerun()

            st.error("Completa título y contenido.")

    with t2:

        for x in obtener_comunicados(admin=True):

            with st.expander(f"{'🟢' if x['activo'] else '⚪'} {x['titulo']}"):

                st.write(x["contenido"])

                if st.button("Desactivar" if x["activo"] else "Activar", key=f"com_{x['id']}"):

                    cambiar_estado_comunicado(x["id"], 0 if x["activo"] else 1)

                    st.rerun()





def faq_admin(u):
    st.title("❓ Preguntas frecuentes UPRI")
    st.info("Las preguntas y respuestas registradas aquí serán iguales para todos los usuarios y se mostrarán sin consultar a la IA.")

    t1, t2 = st.tabs(["➕ Nueva pregunta", "✏️ Administrar"])
    categorias = ["Pagos", "Matrícula", "Trámites", "Plataformas", "Documentos", "Convalidaciones", "Grados y títulos", "Fechas", "Orientación", "General"]
    iconos = ["💬", "💳", "💰", "🧾", "🎓", "📚", "📝", "📄", "📢", "📅", "✅", "⚠️", "❓", "🌐", "🖥️", "🤖", "🏫", "📌", "🔎", "☎️"]

    with t1:
        q = st.text_input("Pregunta")
        respuesta = st.text_area("Respuesta fija", height=140, placeholder="Escribe la respuesta que recibirán todos los usuarios al seleccionar esta pregunta.")
        c1, c2, c3 = st.columns([2, 1, 1])
        cat = c1.selectbox("Categoría", categorias)
        ico = c2.selectbox("Icono", iconos)
        orden = c3.number_input("Orden", min_value=0, value=100, step=10)

        if st.button("PUBLICAR PREGUNTA", type="primary"):
            if not q.strip():
                st.error("Escribe una pregunta.")
            elif not respuesta.strip():
                st.error("Escribe la respuesta fija.")
            else:
                crear_pregunta_frecuente(q.strip(), cat, ico, orden, u["id"], respuesta.strip())
                st.success("Pregunta y respuesta publicadas.")
                st.rerun()

    with t2:
        for f in obtener_preguntas_frecuentes(admin=True):
            with st.expander(f"{'🟢' if f['activo'] else '⚪'} {f.get('icono') or '💬'} {f['pregunta']}"):
                q2 = st.text_input("Pregunta", f["pregunta"], key=f"fq_q_{f['id']}")
                r2 = st.text_area("Respuesta fija", f.get("respuesta") or "", height=130, key=f"fq_r_{f['id']}")
                c1, c2, c3 = st.columns([2, 1, 1])
                cat2 = c1.selectbox("Categoría", categorias, index=categorias.index(f["categoria"]) if f.get("categoria") in categorias else len(categorias)-1, key=f"fq_c_{f['id']}")
                icono_actual = f.get("icono") or "💬"
                ico2 = c2.selectbox("Icono", iconos, index=iconos.index(icono_actual) if icono_actual in iconos else 0, key=f"fq_i_{f['id']}")
                ord2 = c3.number_input("Orden", min_value=0, value=int(f.get("orden") or 0), step=10, key=f"fq_o_{f['id']}")

                a, b, c = st.columns(3)
                if a.button("💾 Guardar", key=f"fq_s_{f['id']}"):
                    if not q2.strip() or not r2.strip():
                        st.error("La pregunta y la respuesta son obligatorias.")
                    else:
                        actualizar_pregunta_frecuente(f["id"], q2, cat2, ico2, ord2, u["id"], r2.strip())
                        st.rerun()
                if b.button("Desactivar" if f["activo"] else "Activar", key=f"fq_a_{f['id']}"):
                    cambiar_estado_pregunta_frecuente(f["id"], 0 if f["activo"] else 1, u["id"]); st.rerun()
                if c.button("🗑️ Eliminar", key=f"fq_d_{f['id']}"):
                    eliminar_pregunta_frecuente(f["id"], u["id"]); st.rerun()





def base_admin(u):
    st.title("🧠 Base de conocimiento")
    st.caption("Documentos, flyers e imágenes institucionales usados por UPRI para elaborar sus respuestas.")

    t1, t2 = st.tabs(["⬆️ Agregar", "📚 Fuentes"])

    with t1:
        titulo = st.text_input("Título de la fuente")
        descripcion = st.text_area(
            "Descripción",
            placeholder="Describe brevemente el documento, flyer o información institucional."
        )
        categoria = st.selectbox(
            "Categoría",
            ["General", "Matrícula", "Pagos", "Convalidaciones", "Reglamentos",
             "Trámites académicos", "Grados y títulos", "Moodle / Intranet",
             "Calendario académico", "Otros"]
        )
        alcance = st.selectbox("Alcance", ["Toda UPRIT", "Programa académico"])

        nid = uid = pid = None
        if alcance == "Programa académico":
            nid, uid, pid = selector_academico("bc")

        archivo = st.file_uploader(
            "Documento / imagen",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg", "webp"],
            help="Formatos admitidos: PDF, DOCX, TXT, PNG, JPG, JPEG y WEBP."
        )

        contenido_imagen = ""
        es_imagen_subida = False

        if archivo is not None:
            extension = os.path.splitext(archivo.name)[1].lower()
            es_imagen_subida = extension in {".png", ".jpg", ".jpeg", ".webp"}

            if es_imagen_subida:
                st.markdown("### 🖼️ Vista previa del flyer / imagen")
                st.image(archivo, use_container_width=True)
                st.info(
                    "Para que UPRI pueda responder usando este flyer, escribe debajo "
                    "la información importante que aparece en la imagen."
                )
                contenido_imagen = st.text_area(
                    "Información contenida en la imagen",
                    height=180,
                    placeholder=(
                        "Ejemplo:\n"
                        "Matrícula ordinaria: hasta el 20 de octubre de 2026.\n"
                        "Inicio de clases: 25 de octubre de 2026.\n"
                        "Área responsable: Registros Académicos."
                    ),
                    key="bc_contenido_imagen"
                )
                st.caption(
                    "UPRI utilizará este texto como contenido verificable del flyer. "
                    "La imagen original también quedará almacenada como fuente."
                )
            else:
                st.success(f"📄 Archivo seleccionado: {archivo.name}")

        if st.button("PROCESAR Y AGREGAR", type="primary"):
            if not titulo.strip() or archivo is None:
                st.error("Indica el título y selecciona un documento o imagen.")
            elif es_imagen_subida and not (contenido_imagen or descripcion).strip():
                st.error(
                    "Para agregar una imagen o flyer, escribe la información que contiene "
                    "o completa su descripción."
                )
            else:
                with st.spinner("Procesando imagen..." if es_imagen_subida else "Procesando documento..."):
                    from procesador_documentos import procesar_archivo_subido
                    r = procesar_archivo_subido(
                        archivo,
                        titulo.strip(),
                        descripcion,
                        categoria,
                        nid,
                        uid,
                        pid,
                        u["id"],
                        contenido_imagen=contenido_imagen if es_imagen_subida else ""
                    )

                if r.get("ok"):
                    tipo = r.get("tipo") or ("imagen" if es_imagen_subida else "documento")
                    st.success(
                        f"Fuente incorporada correctamente como {tipo}. "
                        f"Fragmentos: {r.get('fragmentos', 0)}"
                    )
                    st.rerun()
                else:
                    st.error(r.get("mensaje", "No se pudo procesar la fuente."))

    with t2:
        fuentes = obtener_fuentes_conocimiento(admin=True)

        if not fuentes:
            st.info("Todavía no existen fuentes en la Base de conocimiento.")

        for x in fuentes:
            tipo_fuente = (x.get("tipo_archivo") or x.get("tipo") or "").lower()
            icono = "🖼️" if tipo_fuente in {"imagen", "png", "jpg", "jpeg", "webp"} else "📄"

            with st.expander(f"{'🟢' if x['activo'] else '⚪'} {icono} {x['titulo']}"):
                if x.get("descripcion"):
                    st.write(x["descripcion"])

                if x.get("nombre_original"):
                    st.caption(f"Archivo: {x['nombre_original']}")

                a, b = st.columns(2)

                if a.button("Desactivar" if x["activo"] else "Activar", key=f"bc_a_{x['id']}"):
                    cambiar_estado_fuente_conocimiento(
                        x["id"], 0 if x["activo"] else 1, u["id"]
                    )
                    st.rerun()

                if b.button("🗑️ Eliminar", key=f"bc_d_{x['id']}"):
                    eliminar_fuente_conocimiento(x["id"], u["id"])
                    st.rerun()



def usuarios_admin():

    st.title("👥 Usuarios")

    datos = obtener_usuarios()

    if datos:

        st.dataframe(pd.DataFrame(datos), use_container_width=True, hide_index=True)





def postulantes_admin(u):
    st.title("👨‍🏫 Gestión docente")
    st.caption("Publica cursos disponibles y gestiona a los profesionales que postulan a cada plaza docente.")

    m = metricas_convocatorias_docentes()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cursos / convocatorias", m["convocatorias"])
    c2.metric("Publicadas", m["publicadas"])
    c3.metric("Postulaciones", m["postulaciones"])
    c4.metric("Seleccionados", m["seleccionados"])

    t1, t2, t3 = st.tabs(["➕ Publicar curso", "📚 Cursos disponibles", "👥 Banco de postulantes"])

    with t1:
        st.subheader("Nueva necesidad docente")
        st.info("Registra el curso que necesita docente. Puede ser de Pregrado, Posgrado o Segunda Especialidad.")
        nid, uid, pid = selector_academico("conv_nueva")
        c1, c2 = st.columns(2)
        curso = c1.text_input("Curso / asignatura *", placeholder="Ej.: Ingeniería de Métodos I")
        modalidad = c2.selectbox("Modalidad", ["Presencial", "A distancia", "Híbrida", "Indistinta"])
        titulo = st.text_input("Título de la convocatoria", placeholder="Ej.: Convocatoria docente – Ingeniería de Métodos I")
        c1, c2, c3 = st.columns(3)
        profesion = c1.text_input("Profesión requerida", placeholder="Ej.: Ingeniero Industrial")
        grado = c2.selectbox("Grado mínimo", ["", "Bachiller", "Título profesional", "Maestría", "Doctorado"])
        vacantes = c3.number_input("Vacantes", min_value=1, value=1, step=1)
        experiencia = st.text_input("Experiencia requerida", placeholder="Ej.: 3 años de experiencia profesional y experiencia docente")
        descripcion = st.text_area("Descripción / perfil de la plaza", placeholder="Competencias, experiencia específica, horario, requisitos adicionales, etc.")
        c1, c2 = st.columns(2)
        fecha_inicio = c1.date_input("Disponible desde", value=date.today(), key="conv_inicio")
        fecha_limite = c2.date_input("Cierre de postulación", value=date.today(), key="conv_limite")
        bases = st.file_uploader("Bases, sílabo o flyer (opcional)", type=["pdf", "png", "jpg", "jpeg"], key="conv_bases")

        if st.button("💾 CREAR CONVOCATORIA", type="primary", use_container_width=True):
            if not curso.strip() or not titulo.strip() or not all([nid, uid, pid]):
                st.error("Completa nivel, unidad, programa, curso y título de la convocatoria.")
            elif fecha_limite < fecha_inicio:
                st.error("La fecha de cierre no puede ser anterior a la fecha de inicio.")
            else:
                ruta = nombre = None
                if bases:
                    conv_dir = os.path.join(BASE_DIR, "documentos", "convocatorias")
                    os.makedirs(conv_dir, exist_ok=True)
                    ext = os.path.splitext(bases.name)[1].lower()
                    ruta = os.path.join(conv_dir, f"conv_{uuid.uuid4().hex}{ext}")
                    with open(ruta, "wb") as f:
                        f.write(bases.getbuffer())
                    nombre = bases.name
                ok, msg, cid = crear_convocatoria_docente(
                    titulo=titulo, descripcion=descripcion, nivel_id=nid, unidad_id=uid, programa_id=pid,
                    area_curso=curso, profesion_requerida=profesion, grado_minimo=grado,
                    experiencia_requerida=experiencia, modalidad=modalidad, vacantes=vacantes,
                    fecha_inicio=str(fecha_inicio), fecha_limite=str(fecha_limite),
                    bases_archivo=ruta, bases_nombre_original=nombre, admin_id=u["id"]
                )
                if ok:
                    cambiar_estado_convocatoria(cid, "Publicada", u["id"])
                    st.success("✅ Curso publicado correctamente. Ya está visible para los postulantes.")
                    st.rerun()
                else:
                    st.error(msg)

    with t2:
        estado_conv = st.selectbox("Filtrar convocatorias", ["Todos"] + ESTADOS_CONVOCATORIA, key="filtro_conv")
        convocatorias = obtener_convocatorias_docentes(estado_conv)
        if not convocatorias:
            st.info("Todavía no existen cursos o convocatorias registradas.")
        for c in convocatorias:
            curso = c.get("area_curso") or c.get("titulo")
            icono = "🟢" if c["estado"] == "Publicada" else "⚪"
            with st.expander(f"{icono} {curso} · {c.get('programa_nombre') or '-'} · {c['estado']} · {c.get('total_postulantes',0)} postulante(s)"):
                st.write(f"**Código:** {c.get('codigo') or '-'}")
                st.write(f"**Nivel:** {c.get('nivel_nombre') or '-'}")
                st.write(f"**Unidad:** {c.get('unidad_nombre') or '-'}")
                st.write(f"**Programa:** {c.get('programa_nombre') or '-'}")
                st.write(f"**Curso:** {curso}")
                st.write(f"**Modalidad:** {c.get('modalidad') or '-'} · **Vacantes:** {c.get('vacantes') or 1} · **Cierre:** {c.get('fecha_limite') or '-'}")
                if c.get("profesion_requerida"): st.write(f"**Profesión requerida:** {c['profesion_requerida']}")
                if c.get("grado_minimo"): st.write(f"**Grado mínimo:** {c['grado_minimo']}")
                if c.get("experiencia_requerida"): st.write(f"**Experiencia:** {c['experiencia_requerida']}")
                if c.get("descripcion"): st.write(c["descripcion"])
                if c.get("bases_archivo") and os.path.exists(c["bases_archivo"]):
                    with open(c["bases_archivo"], "rb") as f:
                        st.download_button("📄 Descargar bases", f.read(), file_name=c.get("bases_nombre_original") or "bases.pdf", key=f"bases_admin_{c['id']}")

                estados_c = ESTADOS_CONVOCATORIA
                ec = st.selectbox("Estado de la convocatoria", estados_c, index=estados_c.index(c["estado"]), key=f"estado_conv_{c['id']}")
                if st.button("💾 GUARDAR ESTADO", key=f"save_conv_{c['id']}"):
                    ok, msg = cambiar_estado_convocatoria(c["id"], ec, u["id"])
                    (st.success if ok else st.error)(msg)
                    st.rerun()

                st.markdown("#### 👥 Candidatos a este curso")
                candidatos = obtener_postulaciones_convocatoria(c["id"])
                if not candidatos:
                    st.caption("Aún no hay postulantes para este curso.")
                for p in candidatos:
                    with st.container(border=True):
                        st.markdown(f"**{p['nombres']} {p['apellidos']}** · {p['estado']}")
                        st.write(f"DNI: {p['dni']} · {p['correo']} · {p.get('telefono') or '-'}")
                        st.write(f"**Profesión:** {p.get('profesion') or '-'} · **Grado:** {p.get('grado_academico') or '-'} · **Especialidad:** {p.get('especialidad') or '-'}")
                        st.write(f"**Disponibilidad:** {p.get('disponibilidad') or '-'}")
                        if p.get("cv_archivo") and os.path.exists(p["cv_archivo"]):
                            with open(p["cv_archivo"], "rb") as f:
                                st.download_button("📄 Descargar CV", f.read(), file_name=p.get("cv_nombre_original") or "CV.pdf", key=f"cv_pc_{p['id']}")
                        estados_p = [x for x in ESTADOS_POSTULACION if x != "Borrador"]
                        actual = p["estado"] if p["estado"] in estados_p else "Recibido"
                        nuevo = st.selectbox("Estado del candidato", estados_p, index=estados_p.index(actual), key=f"epc_{p['id']}")
                        obs = st.text_area("Observación para el postulante", p.get("observacion_admin") or "", key=f"opc_{p['id']}")
                        if st.button("💾 ACTUALIZAR CANDIDATO", key=f"apc_{p['id']}"):
                            ok, msg = actualizar_estado_postulacion_convocatoria(p["id"], nuevo, obs, u["id"])
                            (st.success if ok else st.error)(msg)
                            st.rerun()

    with t3:
        st.subheader("Banco general de profesionales")
        estado = st.selectbox("Estado general del perfil", ["Todos"] + ESTADOS_POSTULACION, key="estado_banco")
        datos = obtener_postulantes(estado)
        if not datos:
            st.info("No hay profesionales registrados.")
        for p in datos:
            npost = len(obtener_postulaciones_postulante(p["id"]))
            with st.expander(f"{p['nombres']} {p['apellidos']} · {p.get('profesion') or 'Profesión no registrada'} · {npost} postulación(es)"):
                st.write(f"**DNI:** {p['dni']} · **Correo:** {p['correo']} · **Teléfono:** {p.get('telefono') or '-'}")
                st.write(f"**Grado:** {p.get('grado_academico') or '-'} · **Especialidad:** {p.get('especialidad') or '-'}")
                st.write(f"**Áreas / cursos de interés:** {p.get('areas_interes') or '-'}")
                st.write(f"**Disponibilidad:** {p.get('disponibilidad') or '-'}")
                if p.get("cv_archivo") and os.path.exists(p["cv_archivo"]):
                    with open(p["cv_archivo"], "rb") as f:
                        st.download_button("📄 Descargar CV", f.read(), file_name=p.get("cv_nombre_original") or "CV.pdf", key=f"cv_banco_{p['id']}")
                posts = obtener_postulaciones_postulante(p["id"])
                if posts:
                    st.markdown("**Postulaciones realizadas**")
                    for x in posts:
                        st.write(f"• {x.get('area_curso') or x.get('titulo')} — **{x['estado']}**")

def panel_admin(u):

    with st.sidebar:

        mostrar_logo(82)

        st.markdown("## UPRIT CONECTA")

        st.caption("Administración")

        menu = st.radio("Menú", ["📊 Dashboard", "💳 Gestión de pagos", "👨‍🏫 Postulantes docentes", "📢 Comunicados", "❓ Preguntas frecuentes", "🧠 Base de conocimiento", "💬 Consultas UPRI", "👥 Usuarios"])

        st.divider()

        if st.button("🚪 Cerrar sesión", use_container_width=True):

            salir()

    if menu == "📊 Dashboard": dashboard_admin()

    elif menu == "💳 Gestión de pagos": pagos_admin(u)

    elif menu == "👨‍🏫 Postulantes docentes": postulantes_admin(u)

    elif menu == "📢 Comunicados": comunicados_admin(u)

    elif menu == "❓ Preguntas frecuentes": faq_admin(u)

    elif menu == "🧠 Base de conocimiento": base_admin(u)

    elif menu == "💬 Consultas UPRI":

        st.title("💬 Consultas UPRI")

        datos = obtener_consultas_ia(500, False)

        if datos: st.dataframe(pd.DataFrame(datos), use_container_width=True, hide_index=True)

        else: st.info("Aún no hay consultas registradas.")

    else: usuarios_admin()





# ============================================================

# ENRUTADOR PRINCIPAL

# ============================================================

try:

    usuario = st.session_state.usuario

    if not usuario:
        if st.session_state.pantalla == "registro":
            registro()
        elif st.session_state.pantalla == "postulante_info":
            postulante_info()
        else:
            login()

    elif usuario.get("rol") == "administrador":

        panel_admin(usuario)

    else:

        panel_estudiante(usuario)

except Exception as e:

    st.error("UPRIT CONECTA encontró un error al cargar esta pantalla.")

    st.exception(e)

    st.info("Esta versión muestra el error en pantalla para evitar que el navegador quede completamente en blanco.")
