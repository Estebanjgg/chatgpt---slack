import os
import re
from dateparser import parse as parse_date
from dotenv import load_dotenv
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_bot_user_id(app_token):
    client = WebClient(token=app_token)
    response = client.auth_test()
    return response["user_id"]

BOT_USER_ID = get_bot_user_id(SLACK_APP_TOKEN)

def generate_summary(text, length=100):
    return process_openai_response(
        prompt=f"Resumen en {length} palabras: {text}",
        max_tokens=length,
        language="es"
    )

def process_openai_response(prompt, max_tokens, language="en"):
    response = openai.Completion.create(
        engine=f"text-davinci-002-{language}",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
        top_p=1,
    )
    return response.choices[0].text.strip()

def handle_schedule_meeting(text):
    match = re.search(r"\d{1,2}:\d{2}(\s?[apAP]\.?[mM]\.?)?", text)
    if match:
        time_str = match.group()
        parsed_date = parse_date(time_str)
        if parsed_date:
            return f"Reunión programada para las {parsed_date.strftime('%I:%M %p')}."
        else:
            return "Lo siento, no pude entender la hora que proporcionaste."
    else:
        return "No encontré una hora en tu mensaje. Por favor, incluye la hora de la reunión."

def handle_generate_summary(text):
    match = re.search(r"resum(?:e|ir|en)\s+(.+)", text, re.IGNORECASE)
    if match:
        summary_text = match.group(1)
        return generate_summary(summary_text, length=100)
    else:
        return "No encontré texto para resumir. Por favor, proporciona el texto que deseas resumir."

def handle_other_query(text):
    prompt = f"Tengo una pregunta: {text}"
    return process_openai_response(prompt, max_tokens=50, language="es")

@app.event("app_mention")
def command_handler(body, say):
    text = body["event"]["text"]
    user_id = body["event"]["user"]
    event_ts = body["event"]["event_ts"]
    bot_response_sent = False

    if user_id != BOT_USER_ID and not body["event"].get("bot_id"):
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
