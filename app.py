import streamlit as st
import requests
from datetime import datetime
import pytz
import time

# URL del webhook de producción de tu workflow en n8n
WEBHOOK_URL = "https://nowbit.app.n8n.cloud/webhook/fedb82e6-11f2-4749-9e3b-99e8051e7ae6"

st.set_page_config(page_title="🤖 IntiBot", layout="centered")

# Emoji grande de bienvenida
st.markdown("<h1 style='text-align: center;'>☀️</h1>", unsafe_allow_html=True)
st.title("IntiBot - Tu asistente en Quechua")

# Instrucciones breves
with st.expander("ℹ️ ¿Cómo usar IntiBot?"):
    st.markdown(
        """
        IntiBot es un asistente diseñado para ayudarte a **aprender y practicar el idioma quechua boliviano**.  
        
        Puedes escribir:
        - **Palabras o frases en español** para traducirlas al quechua.
        - **Consultas gramaticales** como: “¿Qué significa el sufijo -chka?”
        - **Saludos o conversaciones básicas** como: “Buenos días” o “¿Cómo estás?”

        👉 IntiBot te responderá con explicaciones claras, fonética y respeto por la cosmovisión andina.
        """
    )

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy **IntiBot** ☀️ Tu compañero para aprender quechua.\n\n¿Sobre qué te gustaría aprender hoy?"}
    ]

# Mostrar historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
prompt = st.chat_input("✏️ Escribe tu pregunta")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("⏳ Pensando...")

    try:
        # Obtener hora local
        tz = pytz.timezone('America/La_Paz')
        now = datetime.now(tz)

        # Enviar a webhook
        response = requests.post(
            WEBHOOK_URL,
            json={
                "mensaje": prompt,
                "sessionId": "Workflow was started",
                "fecha": now.strftime("%Y-%m-%d"),
                "hora": now.strftime("%H:%M:%S")
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            output = data.get("output", "🤷‍♀️ No entendí la respuesta del bot.")
        else:
            output = f"❌ Error del servidor ({response.status_code})"

    except Exception as e:
        output = f"🚨 Error de conexión: {str(e)}"

    response_placeholder.markdown(output)
    st.session_state.messages.append({"role": "assistant", "content": output})
    time.sleep(0.5)
    st.rerun()
