#LIBRERÍAS
import streamlit as st
from groq import Groq

#VARIABLES
altura_contenedor_chat = 600
stream_status = True

#CONSTANTES
MODELOS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama-guard-4-12b"]

#FUNCIONES

#CONFIGURA LA PÁGINA PRINCIPAL Y RETORNA EL MODELO ELEGIDO
def configurar_pagina():

    st.set_page_config(page_title="Chat piola de Marcos 😎", page_icon="🔥")

    st.title("🔥 El chat piola de Marcos 🔥")
    st.caption("Tu espacio para charlar con una IA que no te la caretea 💬")

    st.sidebar.title("⚙️ Configuración de modelo")
    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)

    return elegirModelo

#CREA EL USUARIO CON LA CLAVE API DE GROQ
def crear_usuario():    
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key=clave_secreta)

#CONFIGURA EL MODELO PARA PROCESAR EL PROMPT
def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
        model=modelo_elegido,
        messages=[{"role": "user", "content": prompt_usuario}],
        stream=stream_status
    )

#INICIALIZA EL HISTORIAL DE MENSAJES
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])

def area_chat():
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
        mostrar_historial()

def generar_respuesta(respuesta_completa_del_bot):
    respuesta_final = ""
    for frase in respuesta_completa_del_bot:
        if frase.choices[0].delta.content:
            respuesta_final += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_final

#---------------------------IMPLEMENTACIÓN-------------------------------------

def main():
    modelo_elegido_por_el_usuario = configurar_pagina()
    cliente_usuario = crear_usuario()
    inicializar_estado()
    area_chat()

    prompt_del_usuario = st.chat_input("Escribí algo, Marcos 👇")

    if prompt_del_usuario:
        actualizar_historial("user", prompt_del_usuario, "🧠")
        respuesta_del_bot = configurar_modelo(cliente_usuario, modelo_elegido_por_el_usuario, prompt_del_usuario)
        
        if respuesta_del_bot:
            with st.chat_message("assistant", avatar="🤖"):
                respuesta_posta = st.write_stream(generar_respuesta(respuesta_del_bot))
                actualizar_historial("assistant", respuesta_posta, "🤖")

                st.rerun()


if __name__ == "__main__":
    main()



