# 🔧 Google Login en Val-e - Guía de Configuración

## ✅ Para Pruebas Locales

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
pip install streamlit-components-v1
```

### 2. Ejecutar la App Localmente
```bash
streamlit run app.py
```

La app cargará los secretos de Firebase desde `.streamlit/secrets.toml`

### 3. Probar el Login
1. Ve a la sección **"✍️ Enviar Val-e"**
2. Haz clic en el botón **"🔴 Entrar con Google (Protegido)"**
3. Deberías ver un popup del navegador para iniciar sesión con Google
4. Después de autenticarte, deberías ver un mensaje verde: ✅ Conectado como: tu-email@gmail.com

---

## 🚀 Para Desplegar en Streamlit Cloud

### 1. Ir a [Streamlit Cloud](https://share.streamlit.io)

### 2. Crear un deployment nuevo
- Conecta tu repositorio GitHub: `https://github.com/arcaolxd/vall-e`
- Selecciona `app.py` como archivo principal
- Haz clic en **"Deploy"**

### 3. Configurar los Secretos en Streamlit Cloud
Una vez desplegada la app:

1. Haz clic en el menú **"⋮"** (arriba a la derecha)
2. Selecciona **"⚙️ Settings"**
3. Ve a la sección **"Secrets"**
4. Copia y pega esto en el campo de texto:

```toml
[firebase]
apiKey = "AIzaSyDfmTH6IAHHtZdavcLFApsDc-mCfa6Rsfg"
authDomain = "duelomichoacan.firebaseapp.com"
projectId = "duelomichoacan"
storageBucket = "duelomichoacan.firebasestorage.app"
messagingSenderId = "757565651758"
appId = "1:757565651758:android:8b640908c9abb9cd2d58bf"
```

5. Haz clic en **"Save"**
6. La app se reiniciará automáticamente con los secretos cargados

### 4. Verificar que Firebase Console esté Configurado Correctamente

Antes de probar, asegúrate de que en la [Consola de Firebase](https://console.firebase.google.com/):

1. **Habilitar Google Sign-in**
   - Project: `duelomichoacan`
   - Authentication → Sign-in method → Google → Enable

2. **Autorizar los Dominios**
   - Authentication → Settings → Authorized domains → Add domain
   - Agregar:
     - `localhost` (para pruebas locales)
     - `vall-e.streamlit.app` (tu dominio de Streamlit Cloud)
     - `share.streamlit.io` (para preview)

3. **Configurar Redirect URIs (Opcional, para APK)**
   - Authentication → Sign-in method → Google → Authorized redirect URIs
   - Agregar: `https://vall-e.streamlit.app/__/auth/handler`

---

## 🛠️ Solución de Problemas

### ❌ "auth/popup-blocked"
**Solución:** Habilita los pop-ups en tu navegador. Busca el ícono de bloqueo en la barra de direcciones.

### ❌ "auth/unauthorized-domain"
**Solución:** Vuelve a verificar que el dominio (localhost o vall-e.streamlit.app) esté en Firebase Console → Authorization → Authorized domains.

### ❌ Firebase config no cargada
**Solución:** Verifica que `.streamlit/secrets.toml` esté presente localmente (ya incluido en el repo). En Streamlit Cloud, abre el panel de Secrets y verifica que figuren correctamente.

### ❌ El botón no hace nada
**Solución:** Abre la consola del navegador (F12) y busca errores JavaScript. Si ves errores de Firebase, comprueba que la config sea correcta.

---

## 📱 Para el Juego Móvil (APK/Capacitor)

Si quieres que Google Login funcione también en la app móvil, necesitarás:

1. **firebase-auth.js** con soporte para `signInWithRedirect` (para evitar bloqueos de popup)
2. **Configurar el OAuth2 Consent Screen** en Google Cloud Console
3. **Agregar el Redirect URI** en Firebase

Avísame si necesitas ayuda con esto.

---

## 📝 Notas

- El token de autenticación se almacena en el localStorage del navegador
- La sesión persiste mientras no cierres el navegador
- Para la producción, considera implementar un backend que verifique los tokens JWT de Firebase

¡Listo! Prueba el login y avísame si funciona 🚀
