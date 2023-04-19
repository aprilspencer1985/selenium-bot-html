FROM ubuntu:latest

RUN apt-get update && apt-get install -y chromium-browser

CMD ["chromium-browser", "--version"]
