import os
import re
from dateparser import parse as parse_date
from dotenv import load_dotenv
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_summary(text, length=100):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Resumen en {length} palabras: {text}",
        max_tokens=length,
        n=1,
        stop=None,
        temperature=0.5,
        top_p=1,
    )
    return response.choices[0].text.strip()


@app.event("app_mention")
def command_handler(body, say):
    text = body["event"]["text"]

    if not body["event"].get("bot_id"):
        # Programar reunión
        if re.search(r"programa(?:r|dme)?\s+una\s+reuni[oó]n", text, re.IGNORECASE):
            match = re.search(r"\d{1,2}:\d{2}(\s?[apAP]\.?[mM]\.?)?", text)
            if match:
                time_str = match.group()
                parsed_date = parse_date(time_str)
                if parsed_date:
                    response_text = f"Reunión programada para las {parsed_date.strftime('%I:%M %p')}."
                else:
                    response_text = "Lo siento, no pude entender la hora que proporcionaste."
            else:
                response_text = "No encontré una hora en tu mensaje. Por favor, incluye la hora de la reunión."

        # Generar resumen
        elif re.search(r"resum(?:e|ir|en)", text, re.IGNORECASE):
            match = re.search(r"resum(?:e|ir|en)\s+(.+)", text, re.IGNORECASE)
            if match:
                summary_text = match.group(1)
                response_text = generate_summary(summary_text)
            else:
                response_text = "No encontré texto para resumir. Por favor, proporciona el texto que deseas resumir."

        # Consultas y generación de texto en varios idiomas
        else:
            prompt = f"Tengo una pregunta: {text}"
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.3,
                top_p=1,
            )
            response_text = response.choices[0].text.strip()

        say(response_text)


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
