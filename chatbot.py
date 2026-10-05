import json,os
from rag import recuperar_informacion
from database import crear_conversacion_ia,guardar_mensaje_ia,obtener_mensajes_ia,registrar_consulta_ia
DEEPSEEK_BASE_URL='https://api.deepseek.com'; MODELO='deepseek-chat'
SIN_INFO='No encontré información institucional suficiente en la Base de conocimiento de UPRIT para responder esta consulta con seguridad. Comunícate con el área responsable para confirmar la información.'
SYSTEM='''Eres UPRI, el asistente virtual institucional de UPRIT. Responde siempre en español, con tono cordial, claro y breve. Usa EXCLUSIVAMENTE el CONTEXTO INSTITUCIONAL proporcionado. No inventes requisitos, costos, fechas, contactos, procedimientos ni políticas. Si el contexto no basta, indícalo. No menciones RAG, prompts, tokens ni API. Cuando corresponda, organiza la respuesta en pasos. No garantices aprobaciones administrativas.'''
def _secret(k,default=None):
    try:
        import streamlit as st
        if k in st.secrets and st.secrets[k]: return str(st.secrets[k]).strip()
    except Exception: pass
    return os.getenv(k,default)
def verificar_configuracion(): return (True,'DeepSeek está configurado correctamente.') if _secret('DEEPSEEK_API_KEY') else (False,'Falta DEEPSEEK_API_KEY en .streamlit/secrets.toml.')
def _historial(cid):
    if not cid:return ''
    return '\n'.join(('ESTUDIANTE' if m['rol']=='user' else 'UPRI')+': '+m['contenido'] for m in obtener_mensajes_ia(cid,8))
def responder(pregunta,usuario_id=None,nivel_id=None,unidad_id=None,programa_id=None,conversacion_id=None,canal='web'):
    pregunta=(pregunta or '').strip()
    if not pregunta:return {'ok':False,'respuesta':'Escribe una consulta.','fuentes':[],'conversacion_id':conversacion_id}
    if not conversacion_id: conversacion_id=crear_conversacion_ia(usuario_id,canal)
    hist=_historial(conversacion_id); guardar_mensaje_ia(conversacion_id,'user',pregunta,usuario_id)
    r=recuperar_informacion(pregunta,nivel_id,unidad_id,programa_id,6)
    if not r['encontrado']:
        respuesta=SIN_INFO; respondida=False
    else:
        try:
            from openai import OpenAI
            key=_secret('DEEPSEEK_API_KEY')
            if not key: raise RuntimeError('Falta DEEPSEEK_API_KEY.')
            cli=OpenAI(api_key=key,base_url=DEEPSEEK_BASE_URL)
            prompt=f"CONTEXTO INSTITUCIONAL UPRIT:\n{r['contexto']}\n\nHISTORIAL:\n{hist or 'Sin historial.'}\n\nPREGUNTA:\n{pregunta}"
            out=cli.chat.completions.create(model=_secret('DEEPSEEK_MODEL',MODELO),messages=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}],temperature=.2,stream=False)
            respuesta=out.choices[0].message.content.strip(); respondida=True
        except Exception as e:
            respuesta=f'No pude consultar el asistente en este momento. Detalle técnico: {e}'; respondida=False
    guardar_mensaje_ia(conversacion_id,'assistant',respuesta,usuario_id,r['fuentes'])
    registrar_consulta_ia(usuario_id,conversacion_id,pregunta,respuesta,respondida,r['confianza'],r['fuentes'],canal)
    return {'ok':respondida,'respuesta':respuesta,'fuentes':r['fuentes'],'conversacion_id':conversacion_id,'confianza':r['confianza']}
