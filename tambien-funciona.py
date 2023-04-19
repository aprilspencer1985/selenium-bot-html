import telebot
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

# Configurar el navegador de Chrome
chrome_options = Options()
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options, service=Service('/usr/local/bin/chromedriver'))

# Inicializar el bot con tu token de acceso
bot = telebot.TeleBot("6172286184:AAFANdsvgQ5m4tN47W3VRFT-YfUezAM_9qg")

# Definir el número máximo de caracteres permitidos en el nombre del archivo
MAX_FILENAME_LENGTH = 64

# Manejar el comando '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bienvenido! Envíame una URL y te enviaré su página web HTML.")

# Manejar todos los demás mensajes
@bot.message_handler(func=lambda message: True)
def send_html(message):
    url = message.text.strip()
    if not url.startswith('http'):
        url = 'http://' + url
    driver.get(url)
    while True:
        try:
            html = driver.page_source
            break
        except:
            pass
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(html.encode('utf-8'))

        # Obtener el nombre del archivo temporal
        filename = driver.title.strip() + '.html'

        # Reemplazar caracteres no permitidos por Telegram
        filename = filename.replace('"', '')
        filename = filename.replace('\'', '')
        filename = filename.replace('`', '')
        filename = filename.replace('\\', '')
        filename = filename.replace('/', '')
        filename = filename.replace('<', '')
        filename = filename.replace('>', '')
        filename = filename.replace('|', '')
        filename = filename.replace('?', '')

        # Truncar el nombre del archivo si es necesario
        if len(filename) > MAX_FILENAME_LENGTH:
            filename = filename[:MAX_FILENAME_LENGTH - 5] + '(...).html'

        # Guardar el archivo con el nombre generado
        with open(filename, 'wb') as f:
            f.write(html.encode('utf-8'))

        # Enviar el archivo como documento adjunto con el nombre truncado
        bot.send_document(message.chat.id, open(filename, 'rb'), caption=filename)

        # Eliminar el archivo temporal
        os.remove(filename)

# Ejecutar el bot
bot.polling()