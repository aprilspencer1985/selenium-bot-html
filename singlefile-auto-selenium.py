import os
import time
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyautogui
import threading
from pyvirtualdisplay import Display

# Iniciar el bot de Telegram
bot = telebot.TeleBot("6172286184:AAFANdsvgQ5m4tN47W3VRFT-YfUezAM_9qg")

# Iniciar una sesión del navegador Chrome
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/home/taniii/Documentos/profile")
chrome_options.add_argument('--disable-extensions-except=/home/taniii/Documentos/singlefile.crx')
chrome_options.add_argument('--load-extension=/home/taniii/Documentos/singlefile.crx')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Iniciar la pantalla virtual
display = Display(visible=0, size=(1920, 1080))
display.start()

# Iniciar el navegador Chrome
driver = webdriver.Chrome(options=chrome_options)



def check_for_html_files():
    while True:
        directory = os.path.expanduser('~') + '/Descargas/'
        for file in os.listdir(directory):
            if file.endswith('.html'):
                file_path = os.path.join(directory, file)
                with open(file_path, 'rb') as f:
                    # Obtener el nombre del archivo sin la ruta
                    file_name = os.path.basename(file_path)
                    # Truncar el nombre del archivo a una longitud máxima de 64 caracteres
                    file_name = file_name[:64]
                    # Eliminar caracteres específicos que pueden causar problemas en Telegram
                    file_name = file_name.replace('"', '').replace("'", '').replace('$', '').replace('%', '')
                    print(f"Enviando archivo {file_name}...")
                    bot.send_document(5796865030, f, caption=file_name)
                os.remove(file_path)
        time.sleep(10)

# Iniciar el hilo para verificar los archivos HTML en segundo plano
html_files_thread = threading.Thread(target=check_for_html_files)
html_files_thread.daemon = True
html_files_thread.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bienvenido! Envíame una URL para descargar la página web correspondiente.")

@bot.message_handler(func=lambda message: True)
def download_website(message):
    url = message.text

    # Cargar la página web y esperar a que se cargue completamente
    print(f"Cargando página {url}...")
    driver.get(url)
    time.sleep(10)

    # Hacer clic en la combinación de teclas "Control + Shift + Y" para activar la extensión SingleFile
    print("Activando la extensión SingleFile...")
    pyautogui.hotkey('ctrl', 'shift', 'y')

bot.polling()

# Detener la pantalla virtual y cerrar el navegador Chrome
display.stop()
driver.quit()