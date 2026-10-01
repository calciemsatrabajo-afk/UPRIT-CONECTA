import streamlit as st

import os

import uuid

from datetime import date



from database import *





# ============================================================

# CONFIGURACIÓN

# ============================================================



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO = os.path.join(BASE_DIR, "assets", "logo_uprit.png")



st.set_page_config(

    page_title="UPRIT CONECTA",

    page_icon=LOGO if os.path.exists(LOGO) else "🎓",

    layout="wide",

    initial_sidebar_state="expanded"

)



crear_base_datos()





# ============================================================

# ESTILO

# ============================================================



st.markdown("""
<style>
:root { color-scheme: light !important; }
html, body, [data-testid="stAppViewContainer"], .stApp { background:#F6F7F9 !important; color:#1D2939 !important; }
.block-container { padding-top:1.4rem; padding-bottom:3rem; max-width:1450px; }
h1,h2,h3 { color:#8B0015 !important; }
p,li,label,.stMarkdown { color:#1D2939; }
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#8B0015 0%,#650010 100%) !important; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] [data-testid="stRadio"] label * { color:#FFFFFF !important; }
section[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.28) !important; }
div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="textarea"],
div[data-baseweb="select"] > div, [data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input, [data-testid="stDateInput"] input, textarea {
 background:#FFFFFF !important; color:#101828 !important; }
input,textarea { color:#101828 !important; -webkit-text-fill-color:#101828 !important; caret-color:#101828 !important; }
input::placeholder,textarea::placeholder { color:#667085 !important; -webkit-text-fill-color:#667085 !important; opacity:1 !important; }
div[data-baseweb="select"] span,div[data-baseweb="select"] svg { color:#101828 !important; fill:#101828 !important; }
section[data-testid="stFileUploaderDropzone"] { background:#FFFFFF !important; border:1px dashed #98A2B3 !important; }
section[data-testid="stFileUploaderDropzone"] * { color:#344054 !important; }
section[data-testid="stFileUploaderDropzone"] button { background:#FFFFFF !important; color:#8B0015 !important; border:1px solid #8B0015 !important; }
.stButton > button,.stDownloadButton > button { border-radius:8px !important; min-height:40px; font-weight:700 !important; background:#FFFFFF !important; color:#8B0015 !important; border:1px solid #8B0015 !important; }
.stButton > button *,.stDownloadButton > button * { color:inherit !important; }
.stButton > button:hover,.stDownloadButton > button:hover { background:#FFF1F3 !important; color:#650010 !important; border-color:#650010 !important; }
.stButton > button[kind="primary"],button[data-testid="stBaseButton-primary"] { background:#8B0015 !important; color:#FFFFFF !important; border-color:#8B0015 !important; }
.stButton > button[kind="primary"] *,button[data-testid="stBaseButton-primary"] * { color:#FFFFFF !important; }
.stButton > button[kind="primary"]:hover,button[data-testid="stBaseButton-primary"]:hover { background:#650010 !important; color:#FFFFFF !important; border-color:#650010 !important; }
.stButton > button[kind="primary"]:hover *,button[data-testid="stBaseButton-primary"]:hover * { color:#FFFFFF !important; }
section[data-testid="stSidebar"] .stButton > button { background:#FFFFFF !important; color:#8B0015 !important; border:1px solid #FFFFFF !important; }
section[data-testid="stSidebar"] .stButton > button * { color:#8B0015 !important; }
section[data-testid="stSidebar"] .stButton > button:hover { background:#FDECEF !important; color:#650010 !important; }
section[data-testid="stSidebar"] .stButton > button:hover * { color:#650010 !important; }
button[data-baseweb="tab"] { color:#475467 !important; }
button[data-baseweb="tab"] * { color:inherit !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:#8B0015 !important; font-weight:700 !important; }
div[data-testid="stExpander"] { background:#FFFFFF !important; border:1px solid #D0D5DD !important; border-radius:10px !important; }
div[data-testid="stExpander"] summary,div[data-testid="stExpander"] summary * { color:#1D2939 !important; }
div[data-testid="stAlert"],div[data-testid="stAlert"] p,div[data-testid="stAlert"] * { color:#1D2939 !important; }
div[data-testid="stMetric"] { background:#FFFFFF !important; border:1px solid #EAECF0 !important; border-radius:12px !important; padding:16px !important; }
div[data-testid="stMetric"] * { color:#1D2939 !important; }
[data-testid="stVerticalBlockBorderWrapper"] > div { background:#FFFFFF; }
.tarjeta { background:#FFFFFF; border:1px solid #EAECF0; border-left:5px solid #8B0015; border-radius:10px; padding:18px; margin-bottom:14px; }
.tarjeta h3 { margin-top:0; }
[data-testid="stCheckbox"] label *,main [data-testid="stRadio"] label * { color:#1D2939 !important; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label * { color:#FFFFFF !important; }
[data-testid="stDataFrame"],[data-testid="stTable"] { background:#FFFFFF !important; color:#1D2939 !important; }
.stButton > button:disabled,.stDownloadButton > button:disabled { background:#EAECF0 !important; color:#98A2B3 !important; border-color:#D0D5DD !important; opacity:1 !important; }
</style>
""", unsafe_allow_html=True)





# ============================================================

# SESIÓN

# ============================================================



if "usuario" not in st.session_state:

    st.session_state.usuario = None



if "pantalla_acceso" not in st.session_state:

    st.session_state.pantalla_acceso = "login"





# ============================================================

# AUXILIARES

# ============================================================



def logo():

    if os.path.exists(LOGO):

        c1, c2, c3 = st.columns([2, 1, 2])

        with c2:

            st.image(LOGO, use_container_width=True)





def sidebar_logo():

    if os.path.exists(LOGO):

        st.image(LOGO, width=90)





def cerrar_sesion():

    st.session_state.usuario = None

    st.session_state.pantalla_acceso = "login"

    st.rerun()





def destino(item):



    if item.get("escuela_nombre"):

        return item["escuela_nombre"]



    if item.get("facultad_nombre"):

        return item["facultad_nombre"]



    return "Toda la universidad"





def selector_destino(key):



    alcance = st.selectbox(

        "Destinatarios",

        [

            "Toda la universidad",

            "Una facultad",

            "Una escuela"

        ],

        key=f"{key}_alcance"

    )



    facultad_id = None

    escuela_id = None



    if alcance != "Toda la universidad":



        facultades = obtener_facultades()



        mapa = {

            x["nombre"]: x["id"]

            for x in facultades

        }



        nombre = st.selectbox(

            "Facultad",

            list(mapa.keys()),

            key=f"{key}_fac"

        )



        facultad_id = mapa[nombre]



        if alcance == "Una escuela":



            escuelas = obtener_escuelas(facultad_id)



            mapa_e = {

                x["nombre"]: x["id"]

                for x in escuelas

            }



            if mapa_e:

                nombre_e = st.selectbox(

                    "Escuela",

                    list(mapa_e.keys()),

                    key=f"{key}_esc"

                )



                escuela_id = mapa_e[nombre_e]



    return facultad_id, escuela_id





def guardar_archivo(archivo):



    extension = os.path.splitext(

        archivo.name

    )[1]



    nombre = (

        uuid.uuid4().hex +

        extension.lower()

    )



    ruta = os.path.join(

        DOCUMENTOS_DIR,

        nombre

    )



    with open(ruta, "wb") as f:

        f.write(archivo.getbuffer())



    return ruta





# ============================================================

# LOGIN

# ============================================================



def login():



    logo()



    st.markdown(

        "<h1 style='text-align:center'>UPRIT CONECTA</h1>",

        unsafe_allow_html=True

    )



    st.markdown(

        "<p style='text-align:center'>"

        "Centro de Información y Comunicación Universitaria"

        "</p>",

        unsafe_allow_html=True

    )



    _, centro, _ = st.columns([1, 1, 1])



    with centro:



        st.subheader("🔐 Iniciar sesión")



        dni = st.text_input(

            "DNI / Usuario",

            key="login_dni"

        )



        password = st.text_input(

            "Contraseña",

            type="password",

            key="login_pass"

        )



        if st.button(

            "INGRESAR",

            type="primary",

            use_container_width=True

        ):



            usuario = autenticar_usuario(

                dni,

                password

            )



            if usuario:



                st.session_state.usuario = usuario



                registrar_auditoria(

                    usuario["id"],

                    "Inicio de sesión",

                    "Autenticación",

                    ""

                )



                st.rerun()



            else:

                st.error(

                    "Usuario o contraseña incorrectos."

                )



        if st.button(

            "👤 Crear mi cuenta",

            use_container_width=True

        ):

            st.session_state.pantalla_acceso = "registro"

            st.rerun()





# ============================================================

# REGISTRO

# ============================================================



def registro():



    logo()



    _, centro, _ = st.columns([1, 1, 1])



    with centro:



        st.title("Crear cuenta")



        nombre = st.text_input(

            "Nombre completo"

        )



        dni = st.text_input(

            "DNI",

            max_chars=8

        )



        facultades = obtener_facultades()



        mapa = {

            x["nombre"]: x["id"]

            for x in facultades

        }



        facultad = st.selectbox(

            "Facultad",

            list(mapa.keys())

        )



        facultad_id = mapa[facultad]



        escuelas = obtener_escuelas(

            facultad_id

        )



        mapa_e = {

            x["nombre"]: x["id"]

            for x in escuelas

        }



        escuela = st.selectbox(

            "Escuela",

            list(mapa_e.keys())

        )



        escuela_id = mapa_e[escuela]



        password = st.text_input(

            "Contraseña",

            type="password"

        )



        confirmar = st.text_input(

            "Confirmar contraseña",

            type="password"

        )



        if st.button(

            "CREAR CUENTA",

            type="primary",

            use_container_width=True

        ):



            if password != confirmar:

                st.error(

                    "Las contraseñas no coinciden."

                )

            else:



                ok, mensaje = registrar_usuario(

                    nombre,

                    dni,

                    password,

                    facultad_id,

                    escuela_id

                )



                if ok:

                    st.success(mensaje)

                else:

                    st.error(mensaje)



        if st.button(

            "← Volver",

            use_container_width=True

        ):

            st.session_state.pantalla_acceso = "login"

            st.rerun()





# ============================================================

# COMUNICADOS ADMIN

# ============================================================



def admin_comunicados(usuario, solo_alertas=False):



    if solo_alertas:

        st.title("⚡ Alertas")

        st.caption(

            "Publica información urgente para los usuarios."

        )

    else:

        st.title("📢 Comunicados")



    tab1, tab2 = st.tabs([

        "➕ Publicar",

        "📋 Administrar"

    ])



    with tab1:



        titulo = st.text_input(

            "Título",

            key=f"ct_{solo_alertas}"

        )



        contenido = st.text_area(

            "Contenido",

            height=170,

            key=f"cc_{solo_alertas}"

        )



        if solo_alertas:

            tipo = "Urgente"

            st.warning(

                "Esta publicación será marcada como URGENTE."

            )

        else:

            tipo = st.selectbox(

                "Prioridad",

                [

                    "Informativo",

                    "Importante",

                    "Urgente"

                ],

                key="tipo_com"

            )



        fac, esc = selector_destino(

            f"com_{solo_alertas}"

        )



        tiene_vencimiento = st.checkbox(

            "Tiene fecha de vencimiento",

            key=f"vence_{solo_alertas}"

        )



        vencimiento = None



        if tiene_vencimiento:

            vencimiento = st.date_input(

                "Visible hasta",

                key=f"fv_{solo_alertas}"

            ).strftime("%Y-%m-%d")



        if st.button(

            "PUBLICAR",

            type="primary",

            use_container_width=True,

            key=f"pub_{solo_alertas}"

        ):



            ok, mensaje = crear_comunicado(

                titulo,

                contenido,

                tipo,

                fac,

                esc,

                usuario["id"],

                vencimiento,

                1

            )



            if ok:

                st.success(mensaje)

                st.rerun()

            else:

                st.error(mensaje)



    with tab2:



        datos = obtener_comunicados_admin()



        if solo_alertas:

            datos = [

                x for x in datos

                if x["tipo"] == "Urgente"

            ]



        if not datos:

            st.info("No existen publicaciones.")



        for x in datos:



            estado = (

                "🟢 ACTIVO"

                if x["activo"]

                else "⚪ INACTIVO"

            )



            with st.expander(

                f"{estado} · {x['titulo']}"

            ):



                st.write(x["contenido"])

                st.caption(

                    f"{x['tipo']} · {destino(x)} · "

                    f"{x['fecha_publicacion']}"

                )



                c1, c2 = st.columns(2)



                with c1:

                    nuevo = 0 if x["activo"] else 1



                    if st.button(

                        "Desactivar"

                        if x["activo"]

                        else "Activar",

                        key=f"estado_com_{x['id']}"

                    ):

                        cambiar_estado_comunicado(

                            x["id"],

                            nuevo,

                            usuario["id"]

                        )

                        st.rerun()



                with c2:

                    if st.button(

                        "🗑️ Eliminar",

                        key=f"del_com_{x['id']}"

                    ):

                        eliminar_comunicado(

                            x["id"],

                            usuario["id"]

                        )

                        st.rerun()





# ============================================================

# DOCUMENTOS ADMIN

# ============================================================



def admin_documentos(usuario):



    st.title("📂 Documentos")



    t1, t2 = st.tabs([

        "⬆️ Subir documento",

        "📋 Administrar"

    ])



    with t1:



        titulo = st.text_input(

            "Título del documento"

        )



        descripcion = st.text_area(

            "Descripción"

        )



        categoria = st.selectbox(

            "Categoría",

            [

                "Académicos",

                "Matrícula",

                "Pagos",

                "Reglamentos",

                "Formatos",

                "Cronogramas",

                "Grados y títulos",

                "Otros"

            ]

        )



        fac, esc = selector_destino("documento")



        archivo = st.file_uploader(

            "Archivo",

            type=[

                "pdf", "doc", "docx",

                "xls", "xlsx",

                "png", "jpg", "jpeg"

            ]

        )



        if st.button(

            "PUBLICAR DOCUMENTO",

            type="primary",

            use_container_width=True

        ):



            if not titulo.strip():

                st.error("Ingrese el título.")



            elif archivo is None:

                st.error("Seleccione un archivo.")



            else:



                ruta = guardar_archivo(archivo)



                crear_documento(

                    titulo,

                    descripcion,

                    categoria,

                    ruta,

                    archivo.name,

                    archivo.type,

                    fac,

                    esc,

                    usuario["id"]

                )



                st.success(

                    "Documento publicado."

                )



                st.rerun()



    with t2:



        for x in obtener_documentos_admin():



            with st.expander(

                f"{'🟢' if x['activo'] else '⚪'} "

                f"{x['titulo']}"

            ):



                st.write(x["descripcion"] or "")

                st.caption(

                    f"{x['categoria']} · {destino(x)}"

                )



                c1, c2 = st.columns(2)



                with c1:

                    if st.button(

                        "Desactivar"

                        if x["activo"]

                        else "Activar",

                        key=f"edoc{x['id']}"

                    ):

                        cambiar_estado_documento(

                            x["id"],

                            0 if x["activo"] else 1,

                            usuario["id"]

                        )

                        st.rerun()



                with c2:

                    if st.button(

                        "🗑️ Eliminar",

                        key=f"ddoc{x['id']}"

                    ):

                        eliminar_documento(

                            x["id"],

                            usuario["id"]

                        )

                        st.rerun()





# ============================================================

# PROCEDIMIENTOS ADMIN

# ============================================================



def admin_procedimientos(usuario):



    st.title("📚 Procedimientos")



    t1, t2 = st.tabs([

        "➕ Crear procedimiento",

        "📋 Administrar"

    ])



    with t1:



        titulo = st.text_input(

            "Nombre del procedimiento"

        )



        categoria = st.text_input(

            "Categoría"

        )



        descripcion = st.text_area(

            "Descripción"

        )



        pasos = st.text_area(

            "Pasos a seguir",

            placeholder=(

                "1. Primer paso\n"

                "2. Segundo paso\n"

                "3. Tercer paso"

            )

        )



        requisitos = st.text_area(

            "Requisitos"

        )



        documentos = st.text_area(

            "Documentos necesarios"

        )



        areas = obtener_areas()



        mapa = {

            x["nombre"]: x["id"]

            for x in areas

        }



        area = st.selectbox(

            "Área responsable",

            list(mapa.keys())

        )



        fac, esc = selector_destino("proc")



        if st.button(

            "GUARDAR PROCEDIMIENTO",

            type="primary",

            use_container_width=True

        ):



            if not titulo.strip():

                st.error("Ingrese el título.")

            else:

                crear_procedimiento(

                    titulo,

                    categoria,

                    descripcion,

                    pasos,

                    requisitos,

                    documentos,

                    mapa[area],

                    fac,

                    esc,

                    usuario["id"]

                )



                st.success(

                    "Procedimiento creado."

                )



                st.rerun()



    with t2:



        for x in obtener_procedimientos(

            admin=True

        ):



            with st.expander(

                f"{'🟢' if x['activo'] else '⚪'} "

                f"{x['titulo']}"

            ):



                st.write(x["descripcion"] or "")

                st.write(

                    f"**Área:** "

                    f"{x['area_nombre'] or '-'}"

                )



                c1, c2 = st.columns(2)



                with c1:

                    if st.button(

                        "Desactivar"

                        if x["activo"]

                        else "Activar",

                        key=f"ep{x['id']}"

                    ):

                        cambiar_estado_procedimiento(

                            x["id"],

                            0 if x["activo"] else 1,

                            usuario["id"]

                        )

                        st.rerun()



                with c2:

                    if st.button(

                        "🗑️ Eliminar",

                        key=f"dp{x['id']}"

                    ):

                        eliminar_procedimiento(

                            x["id"],

                            usuario["id"]

                        )

                        st.rerun()





# ============================================================

# CALENDARIO ADMIN

# ============================================================



def admin_calendario(usuario):



    st.title("📅 Calendario")



    t1, t2 = st.tabs([

        "➕ Nueva fecha",

        "📋 Administrar"

    ])



    with t1:



        titulo = st.text_input(

            "Nombre del evento"

        )



        descripcion = st.text_area(

            "Descripción"

        )



        tipo = st.selectbox(

            "Tipo",

            [

                "Académico",

                "Matrícula",

                "Pagos",

                "Evaluaciones",

                "Ceremonia",

                "Administrativo",

                "Otro"

            ]

        )



        c1, c2 = st.columns(2)



        with c1:

            inicio = st.date_input(

                "Fecha de inicio",

                value=date.today()

            )



        with c2:

            fin = st.date_input(

                "Fecha final",

                value=date.today()

            )



        importante = st.checkbox(

            "Marcar como fecha importante"

        )



        fac, esc = selector_destino("cal")



        if st.button(

            "PUBLICAR FECHA",

            type="primary",

            use_container_width=True

        ):



            if not titulo.strip():

                st.error("Ingrese un título.")

            else:

                crear_evento(

                    titulo,

                    descripcion,

                    inicio.strftime("%Y-%m-%d"),

                    fin.strftime("%Y-%m-%d"),

                    tipo,

                    fac,

                    esc,

                    1 if importante else 0,

                    usuario["id"]

                )



                st.success("Fecha publicada.")

                st.rerun()



    with t2:



        for x in obtener_eventos(admin=True):



            with st.expander(

                f"{'⭐' if x['importante'] else '📅'} "

                f"{x['titulo']}"

            ):



                st.write(

                    f"**Inicio:** {x['fecha_inicio']}"

                )



                st.write(

                    f"**Fin:** {x['fecha_fin']}"

                )



                st.write(x["descripcion"] or "")



                c1, c2 = st.columns(2)



                with c1:

                    if st.button(

                        "Desactivar"

                        if x["activo"]

                        else "Activar",

                        key=f"ecal{x['id']}"

                    ):

                        cambiar_estado_evento(

                            x["id"],

                            0 if x["activo"] else 1,

                            usuario["id"]

                        )

                        st.rerun()



                with c2:

                    if st.button(

                        "🗑️ Eliminar",

                        key=f"dcal{x['id']}"

                    ):

                        eliminar_evento(

                            x["id"],

                            usuario["id"]

                        )

                        st.rerun()





# ============================================================

# DIRECTORIO ADMIN

# ============================================================



def admin_directorio(usuario):



    st.title("👥 Directorio institucional")



    t1, t2 = st.tabs([

        "➕ Agregar contacto",

        "✏️ Administrar"

    ])



    with t1:



        areas = obtener_areas()



        mapa = {

            x["nombre"]: x["id"]

            for x in areas

        }



        area = st.selectbox(

            "Área",

            list(mapa.keys()),

            key="dir_area"

        )



        responsable = st.text_input(

            "Responsable"

        )



        cargo = st.text_input(

            "Cargo"

        )



        correo = st.text_input(

            "Correo institucional"

        )



        copia = st.text_input(

            "Correo adicional"

        )



        telefono = st.text_input(

            "Teléfono"

        )



        whatsapp = st.text_input(

            "WhatsApp"

        )



        anexo = st.text_input(

            "Anexo"

        )



        horario = st.text_input(

            "Horario de atención"

        )



        ubicacion = st.text_input(

            "Ubicación"

        )



        descripcion = st.text_area(

            "Información adicional"

        )



        if st.button(

            "GUARDAR CONTACTO",

            type="primary",

            use_container_width=True

        ):



            crear_contacto_directorio(

                mapa[area],

                responsable,

                cargo,

                correo,

                copia,

                telefono,

                whatsapp,

                anexo,

                horario,

                ubicacion,

                descripcion,

                usuario["id"]

            )



            st.success("Contacto registrado.")

            st.rerun()



    with t2:



        for x in obtener_directorio(True):



            with st.expander(

                f"🏢 {x['area_nombre']} · "

                f"{x['responsable'] or 'Sin responsable'}"

            ):



                responsable = st.text_input(

                    "Responsable",

                    value=x["responsable"] or "",

                    key=f"r{x['id']}"

                )



                cargo = st.text_input(

                    "Cargo",

                    value=x["cargo"] or "",

                    key=f"c{x['id']}"

                )



                correo = st.text_input(

                    "Correo",

                    value=x["correo"] or "",

                    key=f"co{x['id']}"

                )



                copia = st.text_input(

                    "Correo adicional",

                    value=x["correo_copia"] or "",

                    key=f"cop{x['id']}"

                )



                telefono = st.text_input(

                    "Teléfono",

                    value=x["telefono"] or "",

                    key=f"tel{x['id']}"

                )



                whatsapp = st.text_input(

                    "WhatsApp",

                    value=x["whatsapp"] or "",

                    key=f"wa{x['id']}"

                )



                anexo = st.text_input(

                    "Anexo",

                    value=x["anexo"] or "",

                    key=f"an{x['id']}"

                )



                horario = st.text_input(

                    "Horario",

                    value=x["horario"] or "",

                    key=f"ho{x['id']}"

                )



                ubicacion = st.text_input(

                    "Ubicación",

                    value=x["ubicacion"] or "",

                    key=f"ub{x['id']}"

                )



                descripcion = st.text_area(

                    "Descripción",

                    value=x["descripcion"] or "",

                    key=f"de{x['id']}"

                )



                c1, c2 = st.columns(2)



                with c1:

                    if st.button(

                        "💾 Guardar cambios",

                        key=f"save{x['id']}"

                    ):

                        actualizar_contacto_directorio(

                            x["id"],

                            responsable,

                            cargo,

                            correo,

                            copia,

                            telefono,

                            whatsapp,

                            anexo,

                            horario,

                            ubicacion,

                            descripcion,

                            usuario["id"]

                        )



                        st.success("Actualizado.")

                        st.rerun()



                with c2:

                    if st.button(

                        "🗑️ Eliminar",

                        key=f"dir_del{x['id']}"

                    ):

                        eliminar_contacto_directorio(

                            x["id"],

                            usuario["id"]

                        )

                        st.rerun()





# ============================================================

# FAQ ADMIN

# ============================================================



def admin_faq(usuario):



    st.title("❓ Preguntas frecuentes")



    t1, t2 = st.tabs([

        "➕ Crear pregunta",

        "📋 Administrar"

    ])



    with t1:



        pregunta = st.text_input(

            "Pregunta"

        )



        respuesta = st.text_area(

            "Respuesta",

            height=150

        )



        categoria = st.text_input(

            "Categoría"

        )



        areas = obtener_areas()



        opciones = {"Sin área": None}



        opciones.update({

            x["nombre"]: x["id"]

            for x in areas

        })



        area = st.selectbox(

            "Área relacionada",

            list(opciones.keys())

        )



        fac, esc = selector_destino("faq")



        if st.button(

            "PUBLICAR PREGUNTA",

            type="primary",

            use_container_width=True

        ):



            if not pregunta.strip() or not respuesta.strip():

                st.error(

                    "Pregunta y respuesta son obligatorias."

                )

            else:



                crear_pregunta(

                    pregunta,

                    respuesta,

                    categoria,

                    opciones[area],

                    fac,

                    esc,

                    usuario["id"]

                )



                st.success("Pregunta publicada.")

                st.rerun()



    with t2:



        for x in obtener_preguntas(admin=True):



            with st.expander(

                f"❓ {x['pregunta']}"

            ):



                st.write(x["respuesta"])



                c1, c2 = st.columns(2)



                with c1:

                    if st.button(

                        "Desactivar"

                        if x["activo"]

                        else "Activar",

                        key=f"efaq{x['id']}"

                    ):

                        cambiar_estado_pregunta(

                            x["id"],

                            0 if x["activo"] else 1,

                            usuario["id"]

                        )

                        st.rerun()



                with c2:

                    if st.button(

                        "🗑️ Eliminar",

                        key=f"dfaq{x['id']}"

                    ):

                        eliminar_pregunta(

                            x["id"],

                            usuario["id"]

                        )

                        st.rerun()





# ============================================================

# FACULTADES ADMIN

# ============================================================



def admin_facultades(usuario):



    st.title("🏫 Facultades y escuelas")



    t1, t2 = st.tabs([

        "➕ Agregar",

        "📋 Administrar"

    ])



    with t1:



        st.subheader("Nueva facultad")



        nombre_fac = st.text_input(

            "Nombre de la facultad"

        )



        if st.button(

            "Crear facultad",

            type="primary"

        ):

            ok, mensaje = crear_facultad(

                nombre_fac,

                usuario["id"]

            )



            if ok:

                st.success(mensaje)

                st.rerun()

            else:

                st.error(mensaje)



        st.divider()



        st.subheader("Nueva escuela")



        facultades = obtener_facultades()



        mapa = {

            x["nombre"]: x["id"]

            for x in facultades

        }



        fac = st.selectbox(

            "Facultad",

            list(mapa.keys()),

            key="nueva_esc_fac"

        )



        nombre_esc = st.text_input(

            "Nombre de la escuela"

        )



        if st.button(

            "Crear escuela",

            type="primary"

        ):



            crear_escuela(

                mapa[fac],

                nombre_esc,

                usuario["id"]

            )



            st.success("Escuela creada.")

            st.rerun()



    with t2:



        for f in obtener_facultades(True):



            with st.expander(

                f"🏫 {f['nombre']}"

            ):



                st.write(

                    "Estado: "

                    + (

                        "Activo"

                        if f["activo"]

                        else "Inactivo"

                    )

                )



                if st.button(

                    "Desactivar facultad"

                    if f["activo"]

                    else "Activar facultad",

                    key=f"fac_estado{f['id']}"

                ):

                    cambiar_estado_facultad(

                        f["id"],

                        0 if f["activo"] else 1,

                        usuario["id"]

                    )

                    st.rerun()



                st.markdown("**Escuelas:**")



                for e in obtener_escuelas(

                    f["id"],

                    True

                ):



                    c1, c2 = st.columns([4, 1])



                    c1.write(

                        f"• {e['nombre']}"

                    )



                    if c2.button(

                        "❌" if e["activo"] else "✅",

                        key=f"esc_estado{e['id']}"

                    ):

                        cambiar_estado_escuela(

                            e["id"],

                            0 if e["activo"] else 1,

                            usuario["id"]

                        )

                        st.rerun()





# ============================================================

# USUARIOS ADMIN

# ============================================================



def admin_usuarios(usuario):



    st.title("👤 Usuarios")



    usuarios = obtener_usuarios()



    normales = [

        x for x in usuarios

        if x["rol"] != "administrador"

    ]



    st.metric(

        "Usuarios registrados",

        len(normales)

    )



    for x in normales:



        with st.expander(

            f"👤 {x['nombre_completo']} · "

            f"{x['dni']}"

        ):



            st.write(

                f"**Facultad:** "

                f"{x['facultad_nombre'] or '-'}"

            )



            st.write(

                f"**Escuela:** "

                f"{x['escuela_nombre'] or '-'}"

            )



            st.write(

                f"**Estado:** {x['estado']}"

            )



            st.write(

                f"**Último acceso:** "

                f"{x['ultimo_acceso'] or 'Nunca'}"

            )



            nuevo = (

                "inactivo"

                if x["estado"] == "activo"

                else "activo"

            )



            if st.button(

                "Bloquear usuario"

                if nuevo == "inactivo"

                else "Activar usuario",

                key=f"user_estado{x['id']}"

            ):



                cambiar_estado_usuario(

                    x["id"],

                    nuevo,

                    usuario["id"]

                )



                st.rerun()





# ============================================================

# ADMINISTRADOR

# ============================================================



def panel_admin(usuario):



    with st.sidebar:



        sidebar_logo()



        st.title("UPRIT CONECTA")

        st.caption("Administrador")



        st.divider()



        menu = st.radio(

            "Menú",

            [

                "📊 Dashboard",

                "📢 Comunicados",

                "📂 Documentos",

                "⚡ Alertas",

                "📚 Procedimientos",

                "📅 Calendario",

                "👥 Directorio",

                "❓ Preguntas frecuentes",

                "🏫 Facultades y escuelas",

                "👤 Usuarios",

                "📈 Estadísticas",

                "📖 Auditoría"

            ]

        )



        st.divider()



        if st.button(

            "🚪 Cerrar sesión",

            use_container_width=True

        ):

            cerrar_sesion()



    if menu == "📊 Dashboard":



        st.title("📊 Dashboard")



        m = obtener_metricas()



        c1, c2, c3, c4 = st.columns(4)



        c1.metric("Usuarios", m["usuarios"])

        c2.metric("Comunicados", m["comunicados"])

        c3.metric("Alertas", m["alertas"])

        c4.metric("Documentos", m["documentos"])



        c1, c2, c3 = st.columns(3)



        c1.metric(

            "Procedimientos",

            m["procedimientos"]

        )



        c2.metric(

            "Fechas",

            m["eventos"]

        )



        c3.metric(

            "Preguntas frecuentes",

            m["preguntas"]

        )



        st.success(

            "UPRIT CONECTA se encuentra operativo."

        )



    elif menu == "📢 Comunicados":

        admin_comunicados(usuario)



    elif menu == "📂 Documentos":

        admin_documentos(usuario)



    elif menu == "⚡ Alertas":

        admin_comunicados(

            usuario,

            solo_alertas=True

        )



    elif menu == "📚 Procedimientos":

        admin_procedimientos(usuario)



    elif menu == "📅 Calendario":

        admin_calendario(usuario)



    elif menu == "👥 Directorio":

        admin_directorio(usuario)



    elif menu == "❓ Preguntas frecuentes":

        admin_faq(usuario)



    elif menu == "🏫 Facultades y escuelas":

        admin_facultades(usuario)



    elif menu == "👤 Usuarios":

        admin_usuarios(usuario)



    elif menu == "📈 Estadísticas":



        st.title("📈 Estadísticas")



        m = obtener_metricas()



        st.bar_chart({

            "Cantidad": {

                "Usuarios": m["usuarios"],

                "Comunicados": m["comunicados"],

                "Alertas": m["alertas"],

                "Documentos": m["documentos"],

                "Procedimientos": m["procedimientos"],

                "Fechas": m["eventos"],

                "FAQ": m["preguntas"]

            }

        })



    elif menu == "📖 Auditoría":



        st.title("📖 Auditoría")



        for x in obtener_auditoria():



            with st.container(border=True):



                st.write(

                    f"**{x['accion']} · "

                    f"{x['modulo']}**"

                )



                st.caption(

                    f"{x['usuario_nombre'] or 'Sistema'} "

                    f"· {x['fecha']}"

                )



                if x["detalle"]:

                    st.write(x["detalle"])





# ============================================================

# PANEL USUARIO

# ============================================================



def panel_usuario(usuario):



    with st.sidebar:



        sidebar_logo()



        st.title("UPRIT CONECTA")



        st.write(

            f"👤 {usuario['nombre_completo']}"

        )



        st.caption(

            usuario.get("escuela_nombre") or ""

        )



        st.divider()



        menu = st.radio(

            "Menú",

            [

                "🏠 Inicio",

                "📢 Comunicados",

                "⚡ Información urgente",

                "📚 Procedimientos",

                "🔎 ¿Quién resuelve esto?",

                "📂 Documentos y formatos",

                "📅 Fechas importantes",

                "👥 Directorio institucional",

                "❓ Preguntas frecuentes"

            ]

        )



        st.divider()



        if st.button(

            "🚪 Cerrar sesión",

            use_container_width=True

        ):

            cerrar_sesion()



    fac = usuario["facultad_id"]

    esc = usuario["escuela_id"]



    comunicados = obtener_comunicados_usuario(

        fac,

        esc

    )



    if menu == "🏠 Inicio":



        st.title("🏠 UPRIT CONECTA")



        st.write(

            f"Bienvenido(a), "

            f"**{usuario['nombre_completo']}**."

        )



        urgentes = [

            x for x in comunicados

            if x["tipo"] == "Urgente"

        ]



        if urgentes:

            st.error(

                f"⚡ Existen {len(urgentes)} "

                "alerta(s) urgente(s)."

            )



        st.subheader("📌 Últimas novedades")



        for x in comunicados[:5]:



            with st.container(border=True):



                st.subheader(

                    f"{'🔴' if x['tipo']=='Urgente' else '📢'} "

                    f"{x['titulo']}"

                )



                st.write(x["contenido"])



                st.caption(

                    f"{x['tipo']} · "

                    f"{x['fecha_publicacion']}"

                )



    elif menu == "📢 Comunicados":



        st.title("📢 Comunicados")



        for x in comunicados:



            with st.container(border=True):

                st.subheader(x["titulo"])

                st.write(x["contenido"])

                st.caption(x["fecha_publicacion"])



    elif menu == "⚡ Información urgente":



        st.title("⚡ Información urgente")



        urgentes = [

            x for x in comunicados

            if x["tipo"] == "Urgente"

        ]



        if not urgentes:

            st.success(

                "No existen alertas urgentes."

            )



        for x in urgentes:

            st.error(f"⚡ {x['titulo']}")

            st.write(x["contenido"])



    elif menu == "📚 Procedimientos":



        st.title("📚 Procedimientos")



        datos = obtener_procedimientos(

            fac,

            esc

        )



        if not datos:

            st.info(

                "No existen procedimientos publicados."

            )



        for x in datos:



            with st.expander(

                f"📘 {x['titulo']}"

            ):



                st.write(x["descripcion"] or "")



                st.write(

                    f"**Área responsable:** "

                    f"{x['area_nombre'] or '-'}"

                )



                if x["requisitos"]:

                    st.markdown("### Requisitos")

                    st.write(x["requisitos"])



                if x["pasos"]:

                    st.markdown("### Pasos")

                    st.text(x["pasos"])



                if x["documentos_necesarios"]:

                    st.markdown(

                        "### Documentos necesarios"

                    )

                    st.write(

                        x["documentos_necesarios"]

                    )



    elif menu == "📂 Documentos y formatos":



        st.title("📂 Documentos y formatos")



        documentos = obtener_documentos_usuario(

            fac,

            esc

        )



        if not documentos:

            st.info(

                "No existen documentos disponibles."

            )



        for x in documentos:



            with st.container(border=True):



                st.subheader(

                    f"📄 {x['titulo']}"

                )



                st.write(

                    x["descripcion"] or ""

                )



                st.caption(

                    x["categoria"] or ""

                )



                if (

                    x["archivo"]

                    and os.path.exists(x["archivo"])

                ):



                    with open(

                        x["archivo"],

                        "rb"

                    ) as f:

                        datos = f.read()



                    st.download_button(

                        "⬇️ Descargar",

                        data=datos,

                        file_name=x[

                            "nombre_original"

                        ],

                        mime=x[

                            "tipo_archivo"

                        ],

                        key=f"download{x['id']}"

                    )



    elif menu == "📅 Fechas importantes":



        st.title("📅 Fechas importantes")



        eventos = obtener_eventos(

            fac,

            esc

        )



        if not eventos:

            st.info(

                "No existen fechas publicadas."

            )



        for x in eventos:



            with st.container(border=True):



                st.subheader(

                    f"{'⭐' if x['importante'] else '📅'} "

                    f"{x['titulo']}"

                )



                st.write(x["descripcion"] or "")



                st.write(

                    f"**Desde:** {x['fecha_inicio']}"

                )



                st.write(

                    f"**Hasta:** {x['fecha_fin']}"

                )



                st.caption(

                    x["tipo"] or ""

                )



    elif menu == "👥 Directorio institucional":



        st.title("👥 Directorio institucional")



        for x in obtener_directorio():



            with st.container(border=True):



                st.subheader(

                    x["area_nombre"]

                )



                if x["responsable"]:

                    st.write(

                        f"👤 **Responsable:** "

                        f"{x['responsable']}"

                    )



                if x["cargo"]:

                    st.write(

                        f"💼 **Cargo:** {x['cargo']}"

                    )



                if x["correo"]:

                    st.write(

                        f"📧 **Correo:** {x['correo']}"

                    )



                if x["telefono"]:

                    st.write(

                        f"📞 **Teléfono:** {x['telefono']}"

                    )



                if x["whatsapp"]:

                    st.write(

                        f"💬 **WhatsApp:** {x['whatsapp']}"

                    )



                if x["anexo"]:

                    st.write(

                        f"☎️ **Anexo:** {x['anexo']}"

                    )



                if x["horario"]:

                    st.write(

                        f"🕐 **Horario:** {x['horario']}"

                    )



                if x["ubicacion"]:

                    st.write(

                        f"📍 **Ubicación:** {x['ubicacion']}"

                    )



    elif menu == "❓ Preguntas frecuentes":



        st.title("❓ Preguntas frecuentes")



        preguntas = obtener_preguntas(

            fac,

            esc

        )



        if not preguntas:

            st.info(

                "No existen preguntas publicadas."

            )



        for x in preguntas:



            with st.expander(

                f"❓ {x['pregunta']}"

            ):

                st.write(x["respuesta"])



                if x["area_nombre"]:

                    st.caption(

                        f"Área: {x['area_nombre']}"

                    )



    elif menu == "🔎 ¿Quién resuelve esto?":



        st.title("🔎 ¿Quién resuelve esto?")



        mapa = {

            "Pagos y pensiones": "Tesorería",

            "Matrícula": "Registros Académicos",

            "Carnet universitario": "Registros Académicos",

            "Trámites académicos": "Registros Académicos",

            "Moodle / Intranet": "Soporte Tecnológico / DTI",

            "Notas": "Coordinación Académica",

            "Docentes": "Coordinación Académica",

            "Convalidaciones": "Coordinación Académica",

            "Atención psicológica": "Bienestar Universitario",

            "Atención administrativa": "Secretaría"

        }



        problema = st.selectbox(

            "¿Qué necesitas resolver?",

            ["Seleccione..."] + list(mapa.keys())

        )



        if problema != "Seleccione...":



            area = mapa[problema]



            contactos = [

                x for x in obtener_directorio()

                if x["area_nombre"] == area

            ]



            st.success(

                f"Área responsable: {area}"

            )



            for x in contactos:



                if x["correo"]:

                    st.write(

                        f"📧 {x['correo']}"

                    )



                if x["telefono"]:

                    st.write(

                        f"📞 {x['telefono']}"

                    )



                if x["whatsapp"]:

                    st.write(

                        f"💬 {x['whatsapp']}"

                    )



                if x["horario"]:

                    st.write(

                        f"🕐 {x['horario']}"

                    )





# ============================================================

# EJECUCIÓN

# ============================================================



if st.session_state.usuario is None:



    if st.session_state.pantalla_acceso == "login":

        login()

    else:

        registro()



else:



    if st.session_state.usuario["rol"] == "administrador":

        panel_admin(

            st.session_state.usuario

        )

    else:

        panel_usuario(

            st.session_state.usuario

        )