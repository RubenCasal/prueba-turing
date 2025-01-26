# Usa la imagen base oficial de unstructured
FROM downloads.unstructured.io/unstructured-io/unstructured:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY app.py process_pdf.py rag_agent.py /app/

# Instala dependencias adicionales necesarias
RUN pip install --no-cache-dir \
    langchain \
    langchain-ollama \
    streamlit \
    ollama \
    langchain-community 

# Exponer el puerto para Streamlit
EXPOSE 8501

# Comando por defecto para ejecutar Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
