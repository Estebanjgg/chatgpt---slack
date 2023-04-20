import os
import re
from dateparser import parse as parse_date
from dotenv import load_dotenv
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"] # Obtiene el token de la app de Slack
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"] # Obtiene el token del bot de Slack

app = App(token=SLACK_BOT_TOKEN) # Inicializa la aplicación de Slack

openai.api_key = os.environ["OPENAI_API_KEY"] # Establece la API key de OpenAI

# Función para obtener el ID del bot
def get_bot_user_id(app_token):
     # Crea una instancia del cliente de la API de Slack
    client = WebClient(token=app_token)
     # Realiza una prueba de autenticación con el cliente
    response = client.auth_test()
    # Devuelve el ID del usuario del bot
    return response["user_id"]

BOT_USER_ID = get_bot_user_id(SLACK_APP_TOKEN) # Obtiene el ID del bot de Slack

#Función que genera un resumen de un texto usando el motor de OpenAI
def generate_summary(text, length=100):
    # Procesa la respuesta de OpenAI para generar un resumen del texto dado
    return process_openai_response(
        prompt=f"Resumen en {length} palabras: {text}",
        max_tokens=length,
        language="es"
    )

#Función que se comunica con el API de OpenAI para obtener una respuesta
def process_openai_response(prompt, max_tokens, language="en"):
 # Crea una instancia de la API de OpenAI para completar una tarea con el modelo 'davinci'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
        top_p=1,
    )
     # Devuelve la respuesta generada por el modelo
    return response.choices[0].text.strip()

#Función que maneja la solicitud de programación de reunión
def handle_schedule_meeting(text): 
    # Busca la hora en el texto usando una expresión regular   
    match = re.search(r"\d{1,2}:\d{2}(\s?[apAP]\.?[mM]\.?)?", text)
    if match:
         # Obtiene la hora en formato de cadena
        time_str = match.group()
        # Intenta convertir la cadena a un objeto de fecha y hora
        parsed_date = parse_date(time_str)
        if parsed_date:
             # Devuelve la hora programada
            return f"Reunión programada para las {parsed_date.strftime('%I:%M %p')}."
        else:
            # Si la cadena no se puede convertir en un objeto de fecha y hora, devuelve un mensaje de error
            return "Lo siento, no pude entender la hora que proporcionaste."
    else:
        return "No encontré una hora en tu mensaje. Por favor, incluye la hora de la reunión."

#Función que maneja la solicitud de generación de resumen
def handle_generate_summary(text):
    match = re.search(r"resum(?:e|ir|en)\s+(.+)", text, re.IGNORECASE)
    if match:
        summary_text = match.group(1)
        return generate_summary(summary_text, length=100)
    else:
        return "No encontré texto para resumir. Por favor, proporciona el texto que deseas resumir."

def handle_other_query(text):
#Función que maneja otras consultas y utiliza el motor de OpenAI para generar una respuesta
    prompt = f"Tengo una pregunta: {text}"
    # Busca el texto para resumir usando una expresión regular
    return process_openai_response(prompt, max_tokens=50, language="es")

#Función que maneja las menciones del bot en Slack
@app.event("app_mention")
def command_handler(body, say):
    text = body["event"]["text"]
    user_id = body["event"]["user"]
    event_ts = body["event"]["event_ts"]
    bot_response_sent = False
        # Si el mensaje no es del bot y no proviene de otro bot     
    if user_id != BOT_USER_ID and not body["event"].get("bot_id"):
         # Programar reunión   
        if re.search(r"programa(?:r|dme)?\s+una\s+reuni[oó]n", text, re.IGNORECASE):
            response_text = handle_schedule_meeting(text)
            bot_response_sent = True
        elif re.search(r"resum(?:e|ir|en)", text, re.IGNORECASE):
            response_text = handle_generate_summary(text)
            bot_response_sent = True
        else:
            response_text = handle_other_query(text)
            bot_response_sent = True

        if bot_response_sent:
            app.client.chat_postMessage(
                channel=body["event"]["channel"],
                text=response_text,
                thread_ts=event_ts
            )

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
