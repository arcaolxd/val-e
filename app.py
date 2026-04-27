import streamlit as st
import database
import os
import random

# Page configuration
st.set_page_config(page_title="Val-e | Denuncias Escolares", page_icon="📝", layout="wide")

# El sistema ahora usa Firebase Firestore

# Load CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

import sys

# Check Admin Mode via URL parameter OR Command Line Argument
query_params = st.query_params
is_admin_mode = (query_params.get("mode") == "admin") or ("--mode" in sys.argv and sys.argv[sys.argv.index("--mode") + 1] == "admin")

# Session State for Mock Login
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Sidebar for navigation
st.sidebar.title("🎒 Val-e Menu")

nav_options = ["🏠 Inicio", "✍️ Enviar Val-e", "📋 Mis Val-es"]
if is_admin_mode:
    nav_options.append("🕵️ Monitor Humano")

view = st.sidebar.radio("Ir a:", nav_options)

# Helper function to render paper scraps
def render_paper_scraps(reports, limit=None):
    if not reports:
        st.info("No hay denuncias recientes.")
        return
    
    cols = st.columns(3)
    for i, d in enumerate(reports[:limit] if limit else reports):
        # Result structure: id_denuncia, inst, cat, msg, url, fecha, user_id, email, alias
        _, inst, cat, msg, url, fecha, _, _, alias = d
        
        col_idx = i % 3
        rotation = random.randint(-2, 2)
        cat_color = "var(--pencil-red)" if cat in ["Bullying", "Acoso"] else "var(--pencil-blue)"
        
        display_name = alias if alias else "Anónimo"
        
        with cols[col_idx]:
            st.markdown(f"""
            <div class="paper-scrap" style="--rotation: {rotation};">
                <p style="color: {cat_color}; font-weight: bold; margin: 0;">{cat.upper()}</p>
                <p style="font-size: 0.8rem; margin: 0; color: #666;">Por: {display_name}</p>
                <p style="font-size: 0.9rem; margin: 0;"><b>Inst:</b> {inst}</p>
                <p style="margin-top: 10px;">{msg}</p>
                <p style="font-size: 0.7rem; text-align: right; margin-top: 10px;">{fecha}</p>
            </div>
            """, unsafe_allow_html=True)

if view == "🏠 Inicio":
    st.title("Val-e: cuando una voz sola no alcanza, la comunidad responde")
    
    st.markdown("""
    Vivimos una época en la que casi todo exige exposición. Opinar, denunciar, organizarse o simplemente participar parece requerir nombre, rostro y presencia constante. La vida digital dejó de ser un territorio de exploración colectiva y se convirtió, muchas veces, en una vitrina donde cada persona debe mostrarse para ser escuchada.
    
    **Val-e nace desde la memoria de lo colectivo.**
    
    Este sitio propone recuperar el valor de participar sin quedar expuesto, de señalar una problemática sin convertirla en espectáculo y de construir soluciones desde muchas voces. Aquí, el anonimato no significa ausencia: **significa protección**.
    
    ---
    ### 📌 Voces Colectivas Recientes
    *Explora los temas que la comunidad está señalando.*
    """)
    
    recent_reports = database.get_denuncias()
    render_paper_scraps(recent_reports, limit=6)

elif view == "✍️ Enviar Val-e":
    st.title("✍️ Aportar al Espacio Colectivo")
    st.markdown("_Tu voz es protegida. Tu mensaje es compartido._")
    
    if not st.session_state.user_email:
        st.warning("Para cuidar la integridad de la red, regístrate de forma segura.")
        if st.button("🔴 Entrar con Google (Protegido)"):
            st.session_state.user_email = "usuario_demo@gmail.com"
            st.rerun()
    else:
        st.info(f"Conectado como parte de la red: {st.session_state.user_email}")
        
        with st.form("denuncia_form"):
            st.markdown("### Detalles de la situación")
            alias = st.text_input("Alias (¿Cómo quieres que te identifique la comunidad?)", placeholder="Ej. El Vigilante, Estudiante X...")
            institucion = st.text_input("¿En qué espacio/institución sucede?")
            categoria = st.selectbox("Naturaleza del tema", [
                "Bullying", 
                "Acoso", 
                "Falta de maestros", 
                "Inconsistencias en cursos/materias",
                "Malversación de Fondos", 
                "Manipulación Política", 
                "Otros"
            ])
            mensaje = st.text_area("Relato de la problemática (Recuerda: la fuerza está en la claridad)")
            url_drive = st.text_input("Evidencias para el seguimiento (Opcional)")
            
            submitted = st.form_submit_button("Enviar al Colectivo")
            
            if submitted:
                if not institucion or not mensaje:
                    st.error("La claridad es necesaria para poder actuar.")
                else:
                    user_id = database.get_or_create_user(st.session_state.user_email)
                    database.submit_denuncia(user_id, alias, institucion, categoria, mensaje, url_drive)
                    st.success("Tu voz ha sido integrada al espacio colectivo. Gracias por cuidar la red.")
                    st.balloons()

elif view == "📋 Mis Val-es":
    st.title("📋 Seguimiento de mis Aportes")
    st.markdown("Revisa el camino que han seguido tus mensajes.")
    if not st.session_state.user_email:
        st.warning("Inicia sesión para ver tus denuncias.")
        if st.button("🔴 Iniciar Sesión con Google"):
            st.session_state.user_email = "usuario_demo@gmail.com"
            st.rerun()
    else:
        st.write(f"Aquí puedes ver el historial de denuncias enviadas desde **{st.session_state.user_email}**")
        all_reports = database.get_denuncias()
        my_reports = [r for r in all_reports if r[7] == st.session_state.user_email]
        render_paper_scraps(my_reports)

elif view == "🕵️ Monitor Humano" and is_admin_mode:
    st.title("🕵️ Dashboard del Monitor")
    search_query = st.text_input("🔍 Buscar denuncias", placeholder="Ej. Prepa 5")
    denuncias = database.get_denuncias(search_query)
    
    cols = st.columns(3)
    for i, d in enumerate(denuncias):
        id_denuncia, inst, cat, msg, url, fecha, user_id, email, alias = d
        report_count = database.count_recent_reports(user_id)
        is_spam = report_count > 3
        col_idx = i % 3
        
        with cols[col_idx]:
            rotation = random.randint(-2, 2)
            card_class = "paper-scrap warning-card" if is_spam else "paper-scrap"
            cat_color = "var(--pencil-red)" if cat in ["Bullying", "Acoso"] else "var(--pencil-blue)"
            
            st.markdown(f"""
            <div class="{card_class}" style="--rotation: {rotation};">
                <p style="color: {cat_color}; font-weight: bold; margin: 0;">{cat.upper()}</p>
                <p style="font-size: 0.8rem; margin: 0; color: #666;">Alias: {alias if alias else 'Sin alias'}</p>
                <p style="font-size: 0.9rem; margin: 0;"><b>Inst:</b> {inst}</p>
                <p style="margin-top: 10px;">{msg}</p>
                {f'<p><a href="{url}" target="_blank">🔗 Ver Evidencia</a></p>' if url else ''}
                <p style="font-size: 0.7rem; text-align: right; margin-top: 10px;">{fecha}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if is_spam:
                st.warning(f"⚠️ Alerta de Spam/Operador ({report_count} msgs/sem)")
            
            if st.button(f"Ver Detalles Ocultos #{id_denuncia}"):
                st.info(f"**Identidad Real:** {email}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Recuperar el anonimato como cuidado.**  
**Recuperar la colectividad como fuerza.**
""")

if st.session_state.user_email:
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user_email = None
        st.rerun()
st.sidebar.write("Val-e v1.2 - Resistencia Digital")
