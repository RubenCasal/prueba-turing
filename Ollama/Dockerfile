# Usa la imagen oficial de Ollama como base
FROM ollama/ollama:latest

# Establece un directorio de trabajo (opcional)
WORKDIR /root/.ollama

# Copia el script de inicialización al contenedor
COPY wait_for_ollama.sh /wait_for_ollama.sh

# Asegúrate de que el script sea ejecutable
RUN chmod +x /wait_for_ollama.sh

# Expone el puerto del servidor Ollama
EXPOSE 11434

# Usa el script de inicialización como entrypoint
ENTRYPOINT ["/bin/sh", "/wait_for_ollama.sh"]
