import math,re,unicodedata
from collections import Counter
from database import obtener_fragmentos_conocimiento
STOP={'a','al','de','del','el','la','las','los','en','y','o','que','como','para','por','un','una','me','mi','quiero','necesito','puedo','hola','gracias','informacion','consulta'}
SIN=[{'pago','pagos','pagar','cuota','cuotas','pension','pensiones','tesoreria','voucher','comprobante'},
     {'matricula','matricular','inscripcion'},{'convalidacion','convalidar','equivalencia'},
     {'moodle','campus','plataforma','intranet'},{'titulo','titulacion','grado','bachiller'},
     {'certificado','constancia'},{'fecha','cronograma','calendario','plazo'}]
def normalizar(t):
    t=unicodedata.normalize('NFD',str(t or '').lower()); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9\s]',' ',t)).strip()
def tokens(t): return [x for x in re.findall(r'[a-z0-9]{2,}',normalizar(t)) if x not in STOP]
def expand(ts):
    s=set(ts)
    for x in list(s):
        for g in SIN:
            if x in g:s.update(g)
    return s
def score(q,d):
    qt=tokens(q); dt=tokens(f"{d.get('fuente_titulo','')} {d.get('fuente_categoria','')} {d.get('contenido','')}")
    if not qt or not dt:return 0.0
    qs=expand(qt); ds=set(dt); cobertura=len(set(qt)&ds)/len(set(qt)); sem=min(len(qs&ds)/len(set(qt)),1)
    a=Counter(qs); b=Counter(dt); comunes=set(a)&set(b); prod=sum(a[x]*b[x] for x in comunes)
    na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values())); cos=prod/(na*nb) if na and nb else 0
    return .45*cobertura+.30*sem+.25*cos
def recuperar_informacion(pregunta,nivel_id=None,unidad_id=None,programa_id=None,limite_resultados=6):
    docs=obtener_fragmentos_conocimiento(nivel_id,unidad_id,programa_id)
    scored=[(score(pregunta,d),d) for d in docs]; scored=[x for x in scored if x[0]>=.03]; scored.sort(key=lambda x:x[0],reverse=True)
    top=scored[:limite_resultados]
    fuentes=[]; partes=[]
    for s,d in top:
        nombre=d.get('fuente_titulo') or 'Fuente institucional'
        if nombre not in fuentes:fuentes.append(nombre)
        partes.append(f"FUENTE: {nombre}\n{d['contenido']}")
    return {'encontrado':bool(top),'contexto':'\n\n---\n\n'.join(partes),'fuentes':fuentes,'confianza':round(top[0][0],4) if top else 0.0}
