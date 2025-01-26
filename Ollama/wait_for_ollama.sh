#!/bin/bash

# Inicia el servidor Ollama en segundo plano
ollama serve &
# Guarda el Process ID (PID) del servidor
pid=$!

# Espera unos segundos para que el servidor Ollama se inicie
sleep 5

# Descarga los modelos necesarios
echo "🔴 Retrieving model llama3.1:latest..."
ollama pull llama3.1:latest
echo "🟢 Model llama3.1 pulled successfully!"

echo "🔴 Retrieving model nomic-embed-text..."
ollama pull nomic-embed-text
echo "🟢 Model nomic-embed-text pulled successfully!"

echo "🔴 Retrieving model llava..."
ollama pull llava
echo "🟢 Model llava pulled successfully!"

# Mantén el servidor Ollama corriendo
wait $pid
