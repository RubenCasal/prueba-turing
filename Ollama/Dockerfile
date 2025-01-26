FROM ollama/ollama:latest


WORKDIR /root/.ollama

COPY wait_for_ollama.sh /wait_for_ollama.sh

RUN chmod +x /wait_for_ollama.sh

EXPOSE 11434

ENTRYPOINT ["/bin/sh", "/wait_for_ollama.sh"]
