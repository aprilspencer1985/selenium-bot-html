FROM ubuntu:latest

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

# Instalar Chromium
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get -y install google-chrome-stable

# Imprimir versión de Chromium
RUN CHROME_VERSION=google-chrome --version | awk '{print $3}' && \
    echo "Chromium version: $CHROME_VERSION"

# Descargar e instalar Chromedriver compatible con la versión de Chromium
RUN CHROME_DRIVER_VERSION=curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_ && \
    echo "Chromedriver version to download: $CHROME_DRIVER_VERSION" && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    rm /tmp/chromedriver_linux64.zip

CMD ["/bin/bash"]
