#!/bin/bash


ollama serve &
r
pid=$!


sleep 5

echo "🔴 Retrieving model llama3.1:latest..."
ollama pull llama3.1:latest
echo "🟢 Model llama3.1 pulled successfully!" 

echo "🔴 Retrieving model nomic-embed-text..."
ollama pull nomic-embed-text
echo "🟢 Model nomic-embed-text pulled successfully!"

echo "🔴 Retrieving model llava..."
ollama pull llava
echo "🟢 Model llava pulled successfully!"


wait $pid
