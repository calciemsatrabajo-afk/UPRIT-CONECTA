import sqlite3
import os
import bcrypt
from datetime import datetime


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCUMENTOS_DIR = os.path.join(BASE_DIR, "documentos")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCUMENTOS_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "uprit_conecta.db")


# ============================================================
# CONEXIÓN
# ============================================================

def conectar():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


# ============================================================
# SEGURIDAD
# ============================================================

def generar_hash(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verificar_password(password, password_hash):
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )
    except Exception:
        return False


# ============================================================
# BASE DE DATOS
# ============================================================

def crear_base_datos():

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS facultades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            activo INTEGER DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS escuelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facultad_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (facultad_id) REFERENCES facultades(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            rol TEXT DEFAULT 'usuario',
            facultad_id INTEGER,
            escuela_id INTEGER,
            estado TEXT DEFAULT 'activo',
            fecha_registro TEXT,
            ultimo_acceso TEXT,
            FOREIGN KEY (facultad_id) REFERENCES facultades(id),
            FOREIGN KEY (escuela_id) REFERENCES escuelas(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS directorio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id INTEGER,
            responsable TEXT,
            cargo TEXT,
            correo TEXT,
            correo_copia TEXT,
            telefono TEXT,
            whatsapp TEXT,
            anexo TEXT,
            horario TEXT,
            ubicacion TEXT,
            descripcion TEXT,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (area_id) REFERENCES areas(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS comunicados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            tipo TEXT DEFAULT 'Informativo',
            facultad_id INTEGER,
            escuela_id INTEGER,
            mostrar_novedad INTEGER DEFAULT 1,
            fecha_publicacion TEXT,
            fecha_vencimiento TEXT,
            creado_por INTEGER,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (facultad_id) REFERENCES facultades(id),
            FOREIGN KEY (escuela_id) REFERENCES escuelas(id),
            FOREIGN KEY (creado_por) REFERENCES usuarios(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT,
            archivo TEXT,
            nombre_original TEXT,
            tipo_archivo TEXT,
            facultad_id INTEGER,
            escuela_id INTEGER,
            fecha_publicacion TEXT,
            fecha_actualizacion TEXT,
            version INTEGER DEFAULT 1,
            creado_por INTEGER,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (facultad_id) REFERENCES facultades(id),
            FOREIGN KEY (escuela_id) REFERENCES escuelas(id),
            FOREIGN KEY (creado_por) REFERENCES usuarios(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS procedimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT,
            descripcion TEXT,
            pasos TEXT,
            requisitos TEXT,
            documentos_necesarios TEXT,
            area_id INTEGER,
            facultad_id INTEGER,
            escuela_id INTEGER,
            fecha_actualizacion TEXT,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (area_id) REFERENCES areas(id),
            FOREIGN KEY (facultad_id) REFERENCES facultades(id),
            FOREIGN KEY (escuela_id) REFERENCES escuelas(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS calendario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            tipo TEXT,
            facultad_id INTEGER,
            escuela_id INTEGER,
            importante INTEGER DEFAULT 0,
            creado_por INTEGER,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (facultad_id) REFERENCES facultades(id),
            FOREIGN KEY (escuela_id) REFERENCES escuelas(id),
            FOREIGN KEY (creado_por) REFERENCES usuarios(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS preguntas_frecuentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            categoria TEXT,
            area_id INTEGER,
            facultad_id INTEGER,
            escuela_id INTEGER,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (area_id) REFERENCES areas(id),
            FOREIGN KEY (facultad_id) REFERENCES facultades(id),
            FOREIGN KEY (escuela_id) REFERENCES escuelas(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            accion TEXT,
            modulo TEXT,
            detalle TEXT,
            fecha TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    con.commit()
    con.close()

    cargar_datos_iniciales()


# ============================================================
# DATOS INICIALES
# ============================================================

def cargar_datos_iniciales():

    con = conectar()
    cur = con.cursor()

    facultades = [
        "Facultad de Ingeniería",
        "Facultad de Ciencias Empresariales",
        "Facultad de Derecho y Humanidades"
    ]

    for nombre in facultades:
        cur.execute(
            "INSERT OR IGNORE INTO facultades(nombre) VALUES (?)",
            (nombre,)
        )

    con.commit()

    cur.execute("SELECT id,nombre FROM facultades")
    fac = {x["nombre"]: x["id"] for x in cur.fetchall()}

    escuelas = [
        (fac["Facultad de Ingeniería"], "Ingeniería Industrial"),
        (
            fac["Facultad de Ingeniería"],
            "Ingeniería de Sistemas e Inteligencia Artificial"
        ),
        (
            fac["Facultad de Ciencias Empresariales"],
            "Administración"
        ),
        (
            fac["Facultad de Ciencias Empresariales"],
            "Contabilidad"
        ),
        (
            fac["Facultad de Derecho y Humanidades"],
            "Derecho"
        )
    ]

    for facultad_id, nombre in escuelas:
        cur.execute("""
            SELECT id FROM escuelas
            WHERE facultad_id=? AND nombre=?
        """, (facultad_id, nombre))

        if not cur.fetchone():
            cur.execute("""
                INSERT INTO escuelas(facultad_id,nombre)
                VALUES (?,?)
            """, (facultad_id, nombre))

    areas = [
        ("Tesorería", "Pagos, pensiones y asuntos económicos."),
        (
            "Registros Académicos",
            "Matrícula y trámites académicos."
        ),
        (
            "Bienestar Universitario",
            "Bienestar y orientación al estudiante."
        ),
        ("Secretaría", "Atención administrativa."),
        (
            "Soporte Tecnológico / DTI",
            "Moodle, intranet y soporte tecnológico."
        ),
        (
            "Coordinación Académica",
            "Notas, docentes y convalidaciones."
        )
    ]

    for nombre, descripcion in areas:
        cur.execute("""
            INSERT OR IGNORE INTO areas(nombre,descripcion)
            VALUES (?,?)
        """, (nombre, descripcion))

    con.commit()

    contactos = [
        (
            "Tesorería",
            "tesoreria@uprit.edu.pe",
            "elser.guevara@uprit.edu.pe"
        ),
        (
            "Registros Académicos",
            "registro.academico@uprit.edu.pe",
            ""
        ),
        (
            "Bienestar Universitario",
            "bienestar.universitario@uprit.edu.pe",
            ""
        ),
        ("Secretaría", "sonia.cuba@uprit.edu.pe", ""),
        (
            "Soporte Tecnológico / DTI",
            "carlos.haro@uprit.edu.pe",
            ""
        ),
        (
            "Coordinación Académica",
            "enrique.boy@uprit.edu.pe",
            ""
        )
    ]

    for area, correo, copia in contactos:

        cur.execute(
            "SELECT id FROM areas WHERE nombre=?",
            (area,)
        )

        fila = cur.fetchone()

        if fila:
            cur.execute(
                "SELECT id FROM directorio WHERE area_id=?",
                (fila["id"],)
            )

            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO directorio(
                        area_id,correo,correo_copia
                    ) VALUES (?,?,?)
                """, (fila["id"], correo, copia))

    cur.execute(
        "SELECT id FROM usuarios WHERE dni='admin'"
    )

    if not cur.fetchone():
        cur.execute("""
            INSERT INTO usuarios(
                nombre_completo,
                dni,
                password_hash,
                rol,
                estado,
                fecha_registro
            )
            VALUES (?,?,?,?,?,?)
        """, (
            "Administrador General",
            "admin",
            generar_hash("Admin123*"),
            "administrador",
            "activo",
            ahora()
        ))

    con.commit()
    con.close()


# ============================================================
# UTILIDADES
# ============================================================

def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def filas(sql, parametros=()):
    con = conectar()
    cur = con.cursor()
    cur.execute(sql, parametros)
    resultado = [dict(x) for x in cur.fetchall()]
    con.close()
    return resultado


def ejecutar(sql, parametros=()):
    con = conectar()
    cur = con.cursor()
    cur.execute(sql, parametros)
    ultimo_id = cur.lastrowid
    con.commit()
    con.close()
    return ultimo_id


# ============================================================
# AUDITORÍA
# ============================================================

def registrar_auditoria(usuario_id, accion, modulo, detalle=""):
    ejecutar("""
        INSERT INTO auditoria(
            usuario_id,accion,modulo,detalle,fecha
        ) VALUES (?,?,?,?,?)
    """, (usuario_id, accion, modulo, detalle, ahora()))


def obtener_auditoria():
    return filas("""
        SELECT
            a.*,
            u.nombre_completo AS usuario_nombre
        FROM auditoria a
        LEFT JOIN usuarios u ON a.usuario_id=u.id
        ORDER BY a.id DESC
        LIMIT 500
    """)


# ============================================================
# FACULTADES / ESCUELAS
# ============================================================

def obtener_facultades(incluir_inactivas=False):
    if incluir_inactivas:
        return filas(
            "SELECT * FROM facultades ORDER BY nombre"
        )

    return filas("""
        SELECT * FROM facultades
        WHERE activo=1 ORDER BY nombre
    """)


def obtener_escuelas(facultad_id, incluir_inactivas=False):
    if incluir_inactivas:
        return filas("""
            SELECT * FROM escuelas
            WHERE facultad_id=?
            ORDER BY nombre
        """, (facultad_id,))

    return filas("""
        SELECT * FROM escuelas
        WHERE facultad_id=? AND activo=1
        ORDER BY nombre
    """, (facultad_id,))


def crear_facultad(nombre, usuario_id):
    try:
        ejecutar(
            "INSERT INTO facultades(nombre) VALUES (?)",
            (nombre.strip(),)
        )
        registrar_auditoria(
            usuario_id, "Crear", "Facultades", nombre
        )
        return True, "Facultad creada correctamente."
    except sqlite3.IntegrityError:
        return False, "La facultad ya existe."


def crear_escuela(facultad_id, nombre, usuario_id):
    ejecutar("""
        INSERT INTO escuelas(facultad_id,nombre)
        VALUES (?,?)
    """, (facultad_id, nombre.strip()))

    registrar_auditoria(
        usuario_id, "Crear", "Escuelas", nombre
    )

    return True, "Escuela creada correctamente."


def cambiar_estado_facultad(id_, activo, usuario_id):
    ejecutar(
        "UPDATE facultades SET activo=? WHERE id=?",
        (activo, id_)
    )
    registrar_auditoria(
        usuario_id, "Cambiar estado", "Facultades", str(id_)
    )


def cambiar_estado_escuela(id_, activo, usuario_id):
    ejecutar(
        "UPDATE escuelas SET activo=? WHERE id=?",
        (activo, id_)
    )
    registrar_auditoria(
        usuario_id, "Cambiar estado", "Escuelas", str(id_)
    )


# ============================================================
# USUARIOS
# ============================================================

def registrar_usuario(
    nombre,
    dni,
    password,
    facultad_id,
    escuela_id
):
    nombre = nombre.strip()
    dni = dni.strip()

    if not nombre:
        return False, "Ingrese su nombre completo."

    if not dni.isdigit() or len(dni) != 8:
        return False, "El DNI debe tener 8 números."

    if len(password) < 4:
        return False, "La contraseña debe tener mínimo 4 caracteres."

    if filas(
        "SELECT id FROM usuarios WHERE dni=?",
        (dni,)
    ):
        return False, "El DNI ya está registrado."

    ejecutar("""
        INSERT INTO usuarios(
            nombre_completo,dni,password_hash,rol,
            facultad_id,escuela_id,estado,fecha_registro
        )
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        nombre,
        dni,
        generar_hash(password),
        "usuario",
        facultad_id,
        escuela_id,
        "activo",
        ahora()
    ))

    return True, "Cuenta creada correctamente."


def autenticar_usuario(dni, password):

    resultado = filas("""
        SELECT
            u.*,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre
        FROM usuarios u
        LEFT JOIN facultades f ON u.facultad_id=f.id
        LEFT JOIN escuelas e ON u.escuela_id=e.id
        WHERE u.dni=?
    """, (dni.strip(),))

    if not resultado:
        return None

    usuario = resultado[0]

    if usuario["estado"] != "activo":
        return None

    if not verificar_password(
        password,
        usuario["password_hash"]
    ):
        return None

    ejecutar(
        "UPDATE usuarios SET ultimo_acceso=? WHERE id=?",
        (ahora(), usuario["id"])
    )

    return usuario


def obtener_usuarios():
    return filas("""
        SELECT
            u.id,u.nombre_completo,u.dni,u.rol,
            u.estado,u.fecha_registro,u.ultimo_acceso,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre
        FROM usuarios u
        LEFT JOIN facultades f ON u.facultad_id=f.id
        LEFT JOIN escuelas e ON u.escuela_id=e.id
        ORDER BY u.id DESC
    """)


def cambiar_estado_usuario(usuario_id, estado, admin_id):
    ejecutar(
        "UPDATE usuarios SET estado=? WHERE id=?",
        (estado, usuario_id)
    )
    registrar_auditoria(
        admin_id,
        "Cambiar estado",
        "Usuarios",
        f"Usuario #{usuario_id}: {estado}"
    )


# ============================================================
# COMUNICADOS / ALERTAS
# ============================================================

def crear_comunicado(
    titulo,
    contenido,
    tipo,
    facultad_id,
    escuela_id,
    creado_por,
    fecha_vencimiento=None,
    mostrar_novedad=1
):
    if not titulo.strip() or not contenido.strip():
        return False, "Título y contenido son obligatorios."

    id_ = ejecutar("""
        INSERT INTO comunicados(
            titulo,contenido,tipo,facultad_id,escuela_id,
            mostrar_novedad,fecha_publicacion,
            fecha_vencimiento,creado_por,activo
        )
        VALUES (?,?,?,?,?,?,?,?,?,1)
    """, (
        titulo.strip(),
        contenido.strip(),
        tipo,
        facultad_id,
        escuela_id,
        mostrar_novedad,
        ahora(),
        fecha_vencimiento,
        creado_por
    ))

    registrar_auditoria(
        creado_por,
        "Publicar",
        "Comunicados",
        f"#{id_} {titulo}"
    )

    return True, "Publicado correctamente."


def obtener_comunicados_admin():
    return filas("""
        SELECT
            c.*,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre,
            u.nombre_completo AS autor_nombre
        FROM comunicados c
        LEFT JOIN facultades f ON c.facultad_id=f.id
        LEFT JOIN escuelas e ON c.escuela_id=e.id
        LEFT JOIN usuarios u ON c.creado_por=u.id
        ORDER BY c.id DESC
    """)


def obtener_comunicados_usuario(facultad_id, escuela_id):
    fecha = datetime.now().strftime("%Y-%m-%d")

    return filas("""
        SELECT
            c.*,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre
        FROM comunicados c
        LEFT JOIN facultades f ON c.facultad_id=f.id
        LEFT JOIN escuelas e ON c.escuela_id=e.id
        WHERE c.activo=1
        AND (c.facultad_id IS NULL OR c.facultad_id=?)
        AND (c.escuela_id IS NULL OR c.escuela_id=?)
        AND (
            c.fecha_vencimiento IS NULL
            OR c.fecha_vencimiento=''
            OR substr(c.fecha_vencimiento,1,10)>=?
        )
        ORDER BY
        CASE c.tipo
            WHEN 'Urgente' THEN 1
            WHEN 'Importante' THEN 2
            ELSE 3
        END,
        c.id DESC
    """, (facultad_id, escuela_id, fecha))


def cambiar_estado_comunicado(id_, activo, usuario_id):
    ejecutar(
        "UPDATE comunicados SET activo=? WHERE id=?",
        (activo, id_)
    )
    registrar_auditoria(
        usuario_id,
        "Cambiar estado",
        "Comunicados",
        str(id_)
    )


def eliminar_comunicado(id_, usuario_id):
    ejecutar(
        "DELETE FROM comunicados WHERE id=?",
        (id_,)
    )
    registrar_auditoria(
        usuario_id,
        "Eliminar",
        "Comunicados",
        str(id_)
    )


# ============================================================
# DOCUMENTOS
# ============================================================

def crear_documento(
    titulo,
    descripcion,
    categoria,
    archivo,
    nombre_original,
    tipo_archivo,
    facultad_id,
    escuela_id,
    creado_por
):
    id_ = ejecutar("""
        INSERT INTO documentos(
            titulo,descripcion,categoria,archivo,
            nombre_original,tipo_archivo,
            facultad_id,escuela_id,
            fecha_publicacion,fecha_actualizacion,
            version,creado_por,activo
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,1,?,1)
    """, (
        titulo.strip(),
        descripcion.strip(),
        categoria,
        archivo,
        nombre_original,
        tipo_archivo,
        facultad_id,
        escuela_id,
        ahora(),
        ahora(),
        creado_por
    ))

    registrar_auditoria(
        creado_por,
        "Subir",
        "Documentos",
        f"#{id_} {titulo}"
    )

    return True, "Documento publicado."


def obtener_documentos_admin():
    return filas("""
        SELECT
            d.*,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre
        FROM documentos d
        LEFT JOIN facultades f ON d.facultad_id=f.id
        LEFT JOIN escuelas e ON d.escuela_id=e.id
        ORDER BY d.id DESC
    """)


def obtener_documentos_usuario(facultad_id, escuela_id):
    return filas("""
        SELECT
            d.*,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre
        FROM documentos d
        LEFT JOIN facultades f ON d.facultad_id=f.id
        LEFT JOIN escuelas e ON d.escuela_id=e.id
        WHERE d.activo=1
        AND (d.facultad_id IS NULL OR d.facultad_id=?)
        AND (d.escuela_id IS NULL OR d.escuela_id=?)
        ORDER BY d.id DESC
    """, (facultad_id, escuela_id))


def cambiar_estado_documento(id_, activo, usuario_id):
    ejecutar(
        "UPDATE documentos SET activo=? WHERE id=?",
        (activo, id_)
    )
    registrar_auditoria(
        usuario_id,
        "Cambiar estado",
        "Documentos",
        str(id_)
    )


def eliminar_documento(id_, usuario_id):

    docs = filas(
        "SELECT archivo FROM documentos WHERE id=?",
        (id_,)
    )

    ejecutar(
        "DELETE FROM documentos WHERE id=?",
        (id_,)
    )

    if docs:
        ruta = docs[0]["archivo"]

        if ruta and os.path.exists(ruta):
            try:
                os.remove(ruta)
            except Exception:
                pass

    registrar_auditoria(
        usuario_id,
        "Eliminar",
        "Documentos",
        str(id_)
    )


# ============================================================
# ÁREAS / DIRECTORIO
# ============================================================

def obtener_areas():
    return filas("""
        SELECT * FROM areas
        WHERE activo=1
        ORDER BY nombre
    """)


def obtener_directorio(incluir_inactivos=False):

    condicion = "" if incluir_inactivos else "WHERE d.activo=1"

    return filas(f"""
        SELECT
            d.*,
            a.nombre AS area_nombre
        FROM directorio d
        LEFT JOIN areas a ON d.area_id=a.id
        {condicion}
        ORDER BY a.nombre
    """)


def crear_contacto_directorio(
    area_id,
    responsable,
    cargo,
    correo,
    correo_copia,
    telefono,
    whatsapp,
    anexo,
    horario,
    ubicacion,
    descripcion,
    usuario_id
):
    id_ = ejecutar("""
        INSERT INTO directorio(
            area_id,responsable,cargo,correo,correo_copia,
            telefono,whatsapp,anexo,horario,ubicacion,
            descripcion,activo
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,1)
    """, (
        area_id,
        responsable,
        cargo,
        correo,
        correo_copia,
        telefono,
        whatsapp,
        anexo,
        horario,
        ubicacion,
        descripcion
    ))

    registrar_auditoria(
        usuario_id,
        "Crear",
        "Directorio",
        str(id_)
    )


def actualizar_contacto_directorio(
    id_,
    responsable,
    cargo,
    correo,
    correo_copia,
    telefono,
    whatsapp,
    anexo,
    horario,
    ubicacion,
    descripcion,
    usuario_id
):
    ejecutar("""
        UPDATE directorio SET
            responsable=?,
            cargo=?,
            correo=?,
            correo_copia=?,
            telefono=?,
            whatsapp=?,
            anexo=?,
            horario=?,
            ubicacion=?,
            descripcion=?
        WHERE id=?
    """, (
        responsable,
        cargo,
        correo,
        correo_copia,
        telefono,
        whatsapp,
        anexo,
        horario,
        ubicacion,
        descripcion,
        id_
    ))

    registrar_auditoria(
        usuario_id,
        "Actualizar",
        "Directorio",
        str(id_)
    )


def eliminar_contacto_directorio(id_, usuario_id):
    ejecutar(
        "DELETE FROM directorio WHERE id=?",
        (id_,)
    )
    registrar_auditoria(
        usuario_id,
        "Eliminar",
        "Directorio",
        str(id_)
    )


# ============================================================
# PROCEDIMIENTOS
# ============================================================

def crear_procedimiento(
    titulo,
    categoria,
    descripcion,
    pasos,
    requisitos,
    documentos,
    area_id,
    facultad_id,
    escuela_id,
    usuario_id
):
    id_ = ejecutar("""
        INSERT INTO procedimientos(
            titulo,categoria,descripcion,pasos,requisitos,
            documentos_necesarios,area_id,facultad_id,
            escuela_id,fecha_actualizacion,activo
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,1)
    """, (
        titulo,
        categoria,
        descripcion,
        pasos,
        requisitos,
        documentos,
        area_id,
        facultad_id,
        escuela_id,
        ahora()
    ))

    registrar_auditoria(
        usuario_id,
        "Crear",
        "Procedimientos",
        f"#{id_} {titulo}"
    )


def obtener_procedimientos(
    facultad_id=None,
    escuela_id=None,
    admin=False
):
    if admin:
        return filas("""
            SELECT
                p.*,
                a.nombre AS area_nombre,
                f.nombre AS facultad_nombre,
                e.nombre AS escuela_nombre
            FROM procedimientos p
            LEFT JOIN areas a ON p.area_id=a.id
            LEFT JOIN facultades f ON p.facultad_id=f.id
            LEFT JOIN escuelas e ON p.escuela_id=e.id
            ORDER BY p.id DESC
        """)

    return filas("""
        SELECT
            p.*,
            a.nombre AS area_nombre,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre
        FROM procedimientos p
        LEFT JOIN areas a ON p.area_id=a.id
        LEFT JOIN facultades f ON p.facultad_id=f.id
        LEFT JOIN escuelas e ON p.escuela_id=e.id
        WHERE p.activo=1
        AND (p.facultad_id IS NULL OR p.facultad_id=?)
        AND (p.escuela_id IS NULL OR p.escuela_id=?)
        ORDER BY p.id DESC
    """, (facultad_id, escuela_id))


def cambiar_estado_procedimiento(id_, activo, usuario_id):
    ejecutar(
        "UPDATE procedimientos SET activo=? WHERE id=?",
        (activo, id_)
    )
    registrar_auditoria(
        usuario_id,
        "Cambiar estado",
        "Procedimientos",
        str(id_)
    )


def eliminar_procedimiento(id_, usuario_id):
    ejecutar(
        "DELETE FROM procedimientos WHERE id=?",
        (id_,)
    )
    registrar_auditoria(
        usuario_id,
        "Eliminar",
        "Procedimientos",
        str(id_)
    )


# ============================================================
# CALENDARIO
# ============================================================

def crear_evento(
    titulo,
    descripcion,
    fecha_inicio,
    fecha_fin,
    tipo,
    facultad_id,
    escuela_id,
    importante,
    usuario_id
):
    id_ = ejecutar("""
        INSERT INTO calendario(
            titulo,descripcion,fecha_inicio,fecha_fin,tipo,
            facultad_id,escuela_id,importante,
            creado_por,activo
        )
        VALUES (?,?,?,?,?,?,?,?,?,1)
    """, (
        titulo,
        descripcion,
        fecha_inicio,
        fecha_fin,
        tipo,
        facultad_id,
        escuela_id,
        importante,
        usuario_id
    ))

    registrar_auditoria(
        usuario_id,
        "Crear",
        "Calendario",
        f"#{id_} {titulo}"
    )


def obtener_eventos(
    facultad_id=None,
    escuela_id=None,
    admin=False
):
    if admin:
        return filas("""
            SELECT
                c.*,
                f.nombre AS facultad_nombre,
                e.nombre AS escuela_nombre
            FROM calendario c
            LEFT JOIN facultades f ON c.facultad_id=f.id
            LEFT JOIN escuelas e ON c.escuela_id=e.id
            ORDER BY c.fecha_inicio DESC
        """)

    return filas("""
        SELECT
            c.*,
            f.nombre AS facultad_nombre,
            e.nombre AS escuela_nombre
        FROM calendario c
        LEFT JOIN facultades f ON c.facultad_id=f.id
        LEFT JOIN escuelas e ON c.escuela_id=e.id
        WHERE c.activo=1
        AND (c.facultad_id IS NULL OR c.facultad_id=?)
        AND (c.escuela_id IS NULL OR c.escuela_id=?)
        ORDER BY c.fecha_inicio ASC
    """, (facultad_id, escuela_id))


def cambiar_estado_evento(id_, activo, usuario_id):
    ejecutar(
        "UPDATE calendario SET activo=? WHERE id=?",
        (activo, id_)
    )
    registrar_auditoria(
        usuario_id,
        "Cambiar estado",
        "Calendario",
        str(id_)
    )


def eliminar_evento(id_, usuario_id):
    ejecutar(
        "DELETE FROM calendario WHERE id=?",
        (id_,)
    )
    registrar_auditoria(
        usuario_id,
        "Eliminar",
        "Calendario",
        str(id_)
    )


# ============================================================
# PREGUNTAS FRECUENTES
# ============================================================

def crear_pregunta(
    pregunta,
    respuesta,
    categoria,
    area_id,
    facultad_id,
    escuela_id,
    usuario_id
):
    id_ = ejecutar("""
        INSERT INTO preguntas_frecuentes(
            pregunta,respuesta,categoria,area_id,
            facultad_id,escuela_id,activo
        )
        VALUES (?,?,?,?,?,?,1)
    """, (
        pregunta,
        respuesta,
        categoria,
        area_id,
        facultad_id,
        escuela_id
    ))

    registrar_auditoria(
        usuario_id,
        "Crear",
        "Preguntas frecuentes",
        f"#{id_} {pregunta}"
    )


def obtener_preguntas(
    facultad_id=None,
    escuela_id=None,
    admin=False
):
    if admin:
        return filas("""
            SELECT
                p.*,
                a.nombre AS area_nombre,
                f.nombre AS facultad_nombre,
                e.nombre AS escuela_nombre
            FROM preguntas_frecuentes p
            LEFT JOIN areas a ON p.area_id=a.id
            LEFT JOIN facultades f ON p.facultad_id=f.id
            LEFT JOIN escuelas e ON p.escuela_id=e.id
            ORDER BY p.id DESC
        """)

    return filas("""
        SELECT
            p.*,
            a.nombre AS area_nombre
        FROM preguntas_frecuentes p
        LEFT JOIN areas a ON p.area_id=a.id
        WHERE p.activo=1
        AND (p.facultad_id IS NULL OR p.facultad_id=?)
        AND (p.escuela_id IS NULL OR p.escuela_id=?)
        ORDER BY p.categoria,p.id
    """, (facultad_id, escuela_id))


def cambiar_estado_pregunta(id_, activo, usuario_id):
    ejecutar(
        "UPDATE preguntas_frecuentes SET activo=? WHERE id=?",
        (activo, id_)
    )
    registrar_auditoria(
        usuario_id,
        "Cambiar estado",
        "Preguntas frecuentes",
        str(id_)
    )


def eliminar_pregunta(id_, usuario_id):
    ejecutar(
        "DELETE FROM preguntas_frecuentes WHERE id=?",
        (id_,)
    )
    registrar_auditoria(
        usuario_id,
        "Eliminar",
        "Preguntas frecuentes",
        str(id_)
    )


# ============================================================
# MÉTRICAS
# ============================================================

def obtener_metricas():

    def contar(tabla, condicion="1=1"):
        resultado = filas(
            f"SELECT COUNT(*) AS total FROM {tabla} WHERE {condicion}"
        )
        return resultado[0]["total"]

    return {
        "usuarios": contar("usuarios", "rol='usuario'"),
        "comunicados": contar("comunicados", "activo=1"),
        "alertas": contar(
            "comunicados",
            "activo=1 AND tipo='Urgente'"
        ),
        "documentos": contar("documentos", "activo=1"),
        "procedimientos": contar("procedimientos", "activo=1"),
        "eventos": contar("calendario", "activo=1"),
        "preguntas": contar(
            "preguntas_frecuentes",
            "activo=1"
        )
    }


# ============================================================
# INICIALIZACIÓN
# ============================================================

if __name__ == "__main__":
    crear_base_datos()

    print("======================================")
    print("UPRIT CONECTA")
    print("======================================")
    print("Base de datos preparada.")
    print("Administrador: admin")
    print("Contraseña: Admin123*")