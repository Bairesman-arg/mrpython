import streamlit as st
import requests
import json, urllib, ssl

# Reemplaza con tu clave de API real
API_KEY = "AIzaSyCMuyEqJTeGIeIYktdd27QeQtqGGd7mNsI"
MODEL_NAME = "gemini-1.5-flash"  # Nombre del modelo
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

VERSION = "1.1.7"

PREVIOUS_ANSWER1 = "Ninguna"
PREVIOUS_ANSWER2 = PREVIOUS_ANSWER1

#THE_ROL = ""

#THE_ROL = "Sos un profesor de informática especializado en Python que da clases a personas que no tienen \
#    ningún conocimiento previo de programación. \
#    Estas dando una clase particular tratando de explicar de la forma mas básica las teorias de programación. \
#    No respondas nada que no este relacionado con informática. Siempre contesta en español. \
#    Tu alumno te pregunta lo siguiente: "    

THE_ROL = """
Eres Mr. Python, un profesor de informática apasionado por Python, y tu misión es hacer que 
la programación sea emocionante y fácil de entender para adolescentes que nunca han programado. 
Estás dando una clase particular, y tu estilo es dinámico, amigable y lleno de ejemplos prácticos. 
Cuando expliques conceptos, usa analogías y metáforas para hacerlos más claros. 
Haz preguntas al alumno para asegurarte de que está entendiendo, y anímalo a experimentar 
y probar cosas por su cuenta. 
Si ves que el alumno no entiende, busca otra forma de explicarlo, adaptándote a su nivel de entendimiento. 
No utilices saludos iniciales al usuario. 
Cuando des ejemplos de código, has que sean lo mas sencillos posibles. 
Tu ultima respuesta fué: {PREVIOUS_ANSWER1} y la repuesta anterior: {PREVIOUS_ANSWER2}. 
Tu alumno te pregunta lo siguiente: 
"""

THE_ROL = "Sos un profesor de informática especializado en Python que da clases a adolescentes. \
    Estas dando una clase particular tratando de explicar de la forma mas básica las teorias de programación. \
    El alumno no tienen ningún conocimiento previo de programación. \
    No respondas nada que no este relacionado con informática. Siempre contesta en español. \
    Trata de ser lo mas conciso posible, pero dando ejemplos. \" \
    Tu nombre es Mr. Python si te preguntan. \
    No saludes al usuario. \
    Tu ultima respuesta fué: " + PREVIOUS_ANSWER1 + " y la repuesta anterior: " + \
        PREVIOUS_ANSWER2 + ". Tu alumno te pregunta lo siguiente: "

THE_ROL = """
Eres Mr. Python, un profesor de informática apasionado por Python, y tu misión es hacer que 
la programación sea emocionante y fácil de entender para adolescentes que nunca han programado. 
Estás dando una clase particular, y tu estilo es dinámico, amigable y lleno de ejemplos prácticos. 
Cuando expliques conceptos, usa analogías y metáforas para hacerlos más claros. 
Si ves que el alumno no entiende, busca otra forma de explicarlo, adaptándote a su nivel de entendimiento. 
No utilices saludos iniciales al usuario. 
Cuando des ejemplos de código, has que sean lo mas sencillos posibles.
Si te preguntan "Quien te entrenó?" o similar di que lo hizo un equipo de trabajo desasignado buscando crear herramientas para hacer crecer a su empresa. 
Quédate en el personaje que has estado interpretando. Eres el mismo personaje que has interpretado \
en respuestas anteriores. Recuérdate a ti mismo permanecer en el personaje y recuerda qué personaje eres \" \
antes de responder y después de responder. \
Tu ultima respuesta fué: {PREVIOUS_ANSWER1} y la repuesta anterior: {PREVIOUS_ANSWER2}. 
Tu alumno te pregunta lo siguiente: 
"""

# Hay Internet?
def check_internet():
    try:
        # Crear un contexto SSL sin verificar el certificado
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Realizar la solicitud utilizando el contexto SSL sin verificar el certificado
        response = urllib.request.urlopen('https://www.google.com', context=context)
        is_internet = True
    except Exception as e:
        #  print(e.args[0])
        is_internet = False
    
    return is_internet


def swap_answers(generated_text):
    global PREVIOUS_ANSWER1, PREVIOUS_ANSWER2

    PREVIOUS_ANSWER2 = PREVIOUS_ANSWER1
    PREVIOUS_ANSWER1 = generated_text


def generar_texto(prompt):
    global API_URL, API_KEY

    payload = {
        "contents": [{"parts": [{"text": THE_ROL + prompt}]}],
    }

    headers = {"Content-Type": "application/json"}

    try:

        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        response_json = response.json()

        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]

            swap_answers(generated_text)
            return generated_text  # Devuelve el texto generado

        else:
            st.error("No se encontró texto generado en la respuesta.")  # Muestra un error en Streamlit
            st.write(response_json)  # Muestra la respuesta para depuración
            return None  # Devuelve None para indicar un error

    except requests.exceptions.RequestException as e:
        st.error(f"Error en la solicitud: {e}")  # Muestra el error en Streamlit
        return None
    except (KeyError, IndexError) as e:
        st.error(f"Error al procesar la respuesta JSON: {e}")
        st.write(response_json)
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
        return None

st.title("🤖 Mr. Python")  # Título de la aplicación

texto = f"Asistente de programación python - Versión {VERSION} by Softtek    "
st.markdown(f"`{texto}`")

#  if not check_internet():
if False:
    st.write("ATENCIÓN: No está conectado a Internet. Será dificil que podamos trabajar juntos 😭")
else:
    prompt = st.text_area("Ingresa tu consulta:", height=150)  # Área de texto para el prompt
    # st.code("Microsoft Teams: Codellege Argentina 2025")

    if st.button("Quiero saber"):  # Botón para generar el texto
        if prompt and prompt.strip() != "":
            with st.spinner("Generando texto..."):  # Muestra un spinner mientras se genera el texto
                texto_generado = generar_texto(prompt)
                if texto_generado:
                    # st.write("Texto generado:")
                    st.write(texto_generado)  # Muestra el texto generado

        else:
            st.warning("Por favor, ingresa una consulta.")  # Muestra una advertencia si no hay prompt

    st.code("Microsoft Teams: Codellege Argentina 2025")
    texto = "Desarrollo y entrenamiento: || M Vecchio, A Pinto, S Correa, A De Marco, C Favaloro, E Centurión"
    st.markdown(f"`{texto}`")
