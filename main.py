import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai
from dotenv import load_dotenv

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

openai.api_key = os.environ["OPENAI_API_KEY"]

@app.event("app_mention")
def command_handler(body, say):
    text = body['event']['text']
    if not body["event"].get("bot_id"):
        prompt = f"Tengo una pregunta: {text}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50, # Personaliza el número máximo de tokens en la respuesta
            n=1,
            stop=None,
            temperature=0.3, # Personaliza la temperatura (aleatoriedad) de las respuestas
            top_p=1, # Personaliza el parámetro top_p para controlar la diversidad de las respuestas
        )
        response_text = response.choices[0].text.strip()
        say(response_text)

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()                                                                                                                         