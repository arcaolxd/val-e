import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import os

import json
import streamlit as st

# Nombre del archivo de credenciales (debes descargarlo de Firebase)
SERVICE_ACCOUNT_KEY = "firebase-key.json"

def init_firebase():
    if not firebase_admin._apps:
        # 1. Intentar leer desde Streamlit Secrets (Nube)
        if "firebase" in st.secrets:
            # st.secrets['firebase'] debe contener el JSON completo
            try:
                # Si es un objeto/dict en el TOML
                key_dict = dict(st.secrets["firebase"])
                # Asegurar que la clave privada procese correctamente los saltos de línea
                if "private_key" in key_dict:
                    key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(key_dict)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                st.error(f"Error al cargar secretos de Firebase: {e}")
                return None
        # 2. Intentar leer desde archivo local (Desarrollo)
        elif os.path.exists(SERVICE_ACCOUNT_KEY):
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred)
        else:
            st.error("ERROR: No se encontró configuración de Firebase (ni en Secrets ni en local).")
            return None
    return firestore.client()

db = init_firebase()

def get_or_create_user(email):
    if not db: return None
    users_ref = db.collection("Usuarios")
    query = users_ref.where("correo_google", "==", email).limit(1).get()
    
    if not query:
        user_data = {
            "correo_google": email,
            "fecha_registro": datetime.now(),
            "nivel_confianza": 1,
            "plataforma_origen": "val-e"
        }
        _, user_ref = users_ref.add(user_data)
        return user_ref.id
    else:
        return query[0].id

def submit_denuncia(user_id, alias, institucion, categoria, mensaje, url_drive):
    if not db: return
    denuncias_ref = db.collection("Denuncias")
    denuncia_data = {
        "id_usuario": user_id,
        "alias": alias,
        "institucion": institucion,
        "categoria": categoria,
        "mensaje": mensaje,
        "url_drive": url_drive,
        "fecha_envio": datetime.now(),
        "plataforma": "val-e" # Etiqueta para discernir origen
    }
    denuncias_ref.add(denuncia_data)

def get_denuncias(search_query=None):
    if not db: return []
    denuncias_ref = db.collection("Denuncias")
    
    # Filtramos por plataforma Val-e para no mezclar con otros proyectos
    query = denuncias_ref.where("plataforma", "==", "val-e").order_by("fecha_envio", direction=firestore.Query.DESCENDING)
    
    results = query.get()
    formatted_results = []
    
    for doc in results:
        d = doc.to_dict()
        
        # Simular el JOIN obteniendo el correo del usuario
        user_doc = db.collection("Usuarios").document(d["id_usuario"]).get()
        email = user_doc.to_dict().get("correo_google", "Desconocido") if user_doc.exists else "Desconocido"
        
        # Adaptamos al formato que espera app.py
        # (id_denuncia, inst, cat, msg, url, fecha, user_id, email, alias)
        formatted_results.append((
            doc.id,
            d.get("institucion", ""),
            d.get("categoria", ""),
            d.get("mensaje", ""),
            d.get("url_drive", ""),
            d.get("fecha_envio").strftime("%Y-%m-%d %H:%M:%S"),
            d.get("id_usuario"),
            email,
            d.get("alias", "Anónimo")
        ))
        
    # Filtrado por búsqueda (Firestore tiene limitaciones en LIKE, lo hacemos en memoria para este prototipo)
    if search_query:
        search_query = search_query.lower()
        formatted_results = [r for r in formatted_results if search_query in r[1].lower() or search_query in r[3].lower()]
        
    return formatted_results

def count_recent_reports(user_id):
    if not db: return 0
    denuncias_ref = db.collection("Denuncias")
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    query = denuncias_ref.where("id_usuario", "==", user_id)\
                        .where("fecha_envio", ">", seven_days_ago).get()
    
    return len(query)

if __name__ == "__main__":
    print("Módulo de base de datos Firebase listo.")
