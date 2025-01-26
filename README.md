## **Instrucciones de instalación**

1. Clona el repositorio:
   ```bash
   git clone https://github.com/RubenCasal/prueba-turing.git
   ```
2. Asegurarse de que el archivo wait_for_ollama.sh esta en formato LF y no CRLF (esquina inferior derecha en Visual Studio)
   ![formato lf ](/formato_sh.png)
3. Ejecuta un docker-compose
     ```bash
   docker-compose up --build
   ```
4. Esperar a que se descarguen los modelos de ollama y acceder a http://localhost:8501/
