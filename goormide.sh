#!/bin/bash

# Actualizar el índice de paquetes e instalar las dependencias necesarias
sudo apt-get update
sudo apt-get install -y wget unzip xvfb python3-pip nodejs npm

# Descargar e instalar Google Chrome
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
google-chrome --version

# Descargar e instalar ChromeDriver
CHROME_DRIVER_VERSION=112.0.5615.49
wget -q https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/

# Descargar la extensión SingleFile.crx desde GitHub
wget https://raw.githubusercontent.com/aprilspencer1985/singlefile.crx/main/singlefile.crx -P ~/Downloads/

# Establecer la carpeta de descargas predeterminada en Chrome
echo '{"download": {"default_directory": "/home/goorm/Downloads"}}' > ~/Downloads/Preferences

# Establecer las variables de entorno para la carpeta de descargas de Chrome
export XDG_DOWNLOAD_DIR=/home/goorm/Downloads
export DOWNLOAD_DIR=/home/goorm/Downloads

# Clonar el repositorio de GitHub
git clone https://github.com/aprilspencer1985/selenium-bot-html.git

# Instalar las dependencias de Python
cd selenium-bot-html
pip3 install -r requirements.txt

# Ejecutar la aplicación
xvfb-run -a python3 main.py
