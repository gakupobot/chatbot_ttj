import streamlit as st
import groq

# modelo

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768']

# configuracion de la pagina

def configurar_pagina():
    st.set_page_config(page_title="Mi Pirmer ChatBot con Python")
    st.title("Bienvenidos a mi Chatbot")

# cliente groq

def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)
    
# sidebar con los modelos 

def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA favorito")
    modelo = st.sidebar.selectbox('elegí tu modelo',MODELOS,index=0)
    st.write(f'**Elegiste el modelo** {modelo}')
    return modelo

# inicializacion del estado de los mensajes

def inicializar_estado_chat():
    if "mensajes"  not in st.session_state:
        st.session_state.mensajes = []

# historial

def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"]) 

# mensaje del usuario

def obtener_mensaje_usuario():
    return st.chat_input("Envia tu mensaje")

# guarda los mensajes previos

def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

# muestra los mensajes en la pantalla

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)
    

# llamar al modelo groq

def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta =  cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream= False
    )
    return respuesta.choices[0].message.content
    
    
# flujo de la app

def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    inicializar_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    #mostrar_historial_chat()
    print(mensaje_usuario)

    if mensaje_usuario :
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)
    
        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensaje_al_historial("assistant", mensaje_modelo)
        mostrar_mensaje("assistant", mensaje_modelo)
# ejecutar app

if __name__ == '__main__':
    ejecutar_chat()
