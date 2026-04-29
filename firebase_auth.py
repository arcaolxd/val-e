"""
Componente de autenticación con Google usando Firebase
"""
import streamlit as st
import streamlit.components.v1 as components
import json

def show_google_login_button():
    """
    Muestra un botón para iniciar sesión con Google
    Retorna el usuario autenticado si existe
    """
    
    try:
        firebase_config = {
            "apiKey": st.secrets.get("firebase", {}).get("apiKey", ""),
            "authDomain": st.secrets.get("firebase", {}).get("authDomain", ""),
            "projectId": st.secrets.get("firebase", {}).get("projectId", ""),
            "storageBucket": st.secrets.get("firebase", {}).get("storageBucket", ""),
            "messagingSenderId": st.secrets.get("firebase", {}).get("messagingSenderId", ""),
            "appId": st.secrets.get("firebase", {}).get("appId", ""),
        }
    except:
        st.error("⚠️ Secretos de Firebase no configurados. Contacta al administrador.")
        return
    
    config_json = json.dumps(firebase_config)
    
    # HTML + JavaScript para el componente de login
    html_code = f"""
    <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js"></script>
    
    <div id="google-login-container" style="padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
        <button id="google-login-btn" style="
            background-color: white;
            color: #333;
            padding: 12px 24px;
            border: 1px solid #ccc;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
            font-weight: 500;
            transition: all 0.3s ease;
        "
        onmouseover="this.style.backgroundColor='#f0f0f0'; this.style.borderColor='#999';"
        onmouseout="this.style.backgroundColor='white'; this.style.borderColor='#ccc';">
            🔴 Entrar con Google (Protegido)
        </button>
        <div id="auth-status" style="margin-top: 10px; padding: 10px; border-radius: 5px;"></div>
    </div>
    
    <script>
        const firebaseConfig = {config_json};
        
        // Inicializar Firebase
        if (!firebase.apps || !firebase.apps.length) {{
            firebase.initializeApp(firebaseConfig);
        }}
        
        const auth = firebase.auth();
        
        // Monitorear cambios de autenticación
        auth.onAuthStateChanged(user => {{
            if (user) {{
                console.log("Usuario autenticado:", user.email);
                
                // Guardar el email en localStorage para que Streamlit lo lea
                localStorage.setItem('valle_user_email', user.email);
                localStorage.setItem('valle_user_uid', user.uid);
                localStorage.setItem('valle_user_name', user.displayName || user.email);
                
                // Mostrar mensaje de éxito
                const statusDiv = document.getElementById('auth-status');
                statusDiv.innerHTML = '<p style="color: green; margin: 0;">✅ Conectado como: ' + user.email + '</p>';
                statusDiv.style.backgroundColor = '#e8f5e9';
                statusDiv.style.borderLeft = '4px solid green';
                
                // Notificar a Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: user.email
                }}, '*');
            }}
        }});
        
        // Botón de login
        document.getElementById('google-login-btn').addEventListener('click', async () => {{
            const provider = new firebase.auth.GoogleAuthProvider();
            provider.setCustomParameters({{ prompt: 'select_account' }});
            
            try {{
                const result = await auth.signInWithPopup(provider);
                console.log("Login exitoso:", result.user.email);
                
                // Actualizar UI
                const statusDiv = document.getElementById('auth-status');
                statusDiv.innerHTML = '<p style="color: green; margin: 0;">✅ Iniciando sesión...</p>';
            }} catch (error) {{
                let msg = "Error al iniciar sesión con Google.";
                if (error.code === "auth/popup-blocked") {{
                    msg = "⚠️ El navegador bloqueó la ventana. Habilita los pop-ups para este sitio.";
                }} else if (error.code === "auth/unauthorized-domain") {{
                    msg = "⚠️ Dominio no autorizado. Contacta al administrador.";
                }} else {{
                    msg = "⚠️ Error: " + error.message;
                }}
                console.error("Error:", error.code);
                const statusDiv = document.getElementById('auth-status');
                statusDiv.innerHTML = '<p style="color: red; margin: 0;">' + msg + '</p>';
                statusDiv.style.backgroundColor = '#ffebee';
                statusDiv.style.borderLeft = '4px solid red';
            }}
        }});
        
        // Verificar si ya hay usuario logueado
        const savedEmail = localStorage.getItem('valle_user_email');
        if (savedEmail) {{
            const statusDiv = document.getElementById('auth-status');
            statusDiv.innerHTML = '<p style="color: green; margin: 0;">✅ Sesión activa: ' + savedEmail + '</p>';
            statusDiv.style.backgroundColor = '#e8f5e9';
            statusDiv.style.borderLeft = '4px solid green';
            document.getElementById('google-login-btn').innerHTML = '🔄 Cambiar Cuenta';
        }}
    </script>
    """
    
    components.html(html_code, height=140)


def check_google_login():
    """
    Verifica si el usuario se ha autenticado con Google
    Debe ejecutarse después de show_google_login_button()
    """
    # Este es un workaround para capturar la autenticación
    # En una versión futura, esto sería más elegante con un CustomComponent
    pass


def get_current_user():
    """
    Obtiene el usuario autenticado de la sesión
    """
    return st.session_state.get("user_email")


def logout():
    """
    Cierra la sesión del usuario
    """
    if "user_email" in st.session_state:
        del st.session_state.user_email
    st.rerun()
