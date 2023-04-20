# ChatGPT 3.5 Slack Bot

Este proyecto integra el modelo de lenguaje ChatGPT 3.5 de OpenAI con Slack utilizando la biblioteca Slack Bolt para Python. El bot responde a preguntas y solicitudes en Slack, y también incluye funciones adicionales como programación de reuniones y generación de resúmenes. **Ten en cuenta que este es solo un ejemplo y puede tener defectos o limitaciones en su funcionalidad**.

![maxresdefault](https://user-images.githubusercontent.com/91167097/233241085-c35d2a28-a65a-4934-abdb-ec0101327906.jpg)
![Slack_RGB](https://user-images.githubusercontent.com/91167097/233241097-a8d70d32-02fb-4ef5-a97b-2740253da391.png)


## Requisitos previos

- Cuenta de Slack con permisos para crear aplicaciones y bots
- Clave API de ChatGPT 3.5 de OpenAI
- Python 3.6 o superior

## Instalación

1. Clona este repositorio: 
 
```bash
git clone https://github.com/Estebanjgg/chatgpt---slackt

```
cd chatgpt-slackbot

2. Instala las dependencias necesarias:

pip install -r requirements.txt

3. Configura tus tokens de API en el archivo `.env`. Reemplaza `YOUR_SLACK_APP_TOKEN` y `YOUR_SLACK_BOT_TOKEN` con los tokens de tu aplicación de Slack, y `YOUR_OPENAI_API_KEY` con tu clave API de ChatGPT 3.5.


## Uso

1. Ejecuta el bot:

```bash
python app.py
```

2. Invita al bot a un canal de Slack utilizando el comando `/invite @nombre_de_tu_bot`.

3. Interactúa con el bot enviando mensajes que incluyan su nombre de usuario, como `@nombre_de_tu_bot Hola`.

4. Para programar una reunión, escribe un mensaje que incluya la palabra clave "programar reunión" seguida de la hora de la reunión, por ejemplo: `@nombre_de_tu_bot Programar una reunión a las 3:00 PM`.

5. Para generar un resumen, escribe un mensaje que incluya la palabra clave "resumir" seguida del texto que deseas resumir, por ejemplo: `@nombre_de_tu_bot Resumir La inteligencia artificial es una rama de la informática que busca desarrollar algoritmos y técnicas para que las máquinas puedan aprender y resolver problemas complejos de forma autónoma.`.


