FROM ubuntu

# Instalar las dependencias necesarias
RUN apt-get update && \
    apt-get install -y wget unzip xvfb python3-pip nodejs npm

# Descargar e instalar Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    google-chrome --version

# Descargar e instalar ChromeDriver
RUN CHROME_DRIVER_VERSION=112.0.5615.49 && \
    wget -q https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/

# Crear la carpeta profile y copiar la extensión SingleFile.crx desde GitHub
RUN mkdir /app/profile
RUN wget https://raw.githubusercontent.com/aprilspencer1985/singlefile.crx/main/singlefile.crx -P /app/profile/

# Crear la carpeta Descargas y establecerla como directorio de descargas predeterminado en Chrome
RUN mkdir /app/Descargas
RUN echo '{"download": {"default_directory": "/app/Descargas"}}' > /app/profile/Preferences

# Establecer las variables de entorno para la carpeta de descargas de Chrome
ENV XDG_DOWNLOAD_DIR=/app/Descargas
ENV DOWNLOAD_DIR=/app/Descargas

# Copiar los archivos de la aplicación
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

# Instalar las dependencias de Python
RUN pip3 install -r requirements.txt

# Ejecutar la aplicación
CMD xvfb-run -a python3 main.py
