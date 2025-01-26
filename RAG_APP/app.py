import os
import streamlit as st
from process_pdf import processing_pipeline
from rag_agent import RAG_AGENT

def save_uploaded_file(uploaded_file, save_dir="pdf_uploaded"):
    """Guarda el archivo subido en una carpeta específica."""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  

    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())  
    return file_path  

def main():
    st.title("RAG")
    st.session_state.rag_agent = RAG_AGENT()
   
    if "processed_pdf" not in st.session_state:
        st.session_state["processed_pdf"] = False
    if "pdf_path" not in st.session_state:
        st.session_state["pdf_path"] = None
    if "history" not in st.session_state:
        st.session_state.history = []
    if "rag_agent" not in st.session_state:
        st.session_state.rag_agent = RAG_AGENT()
        

    
    st.header("Carga tu archivo PDF")
    uploaded_file = st.file_uploader("Sube un archivo en formato PDF", type=["pdf"])

    if uploaded_file is not None and not st.session_state["processed_pdf"]:
        st.success("Archivo cargado exitosamente.")

       
        with st.spinner("Guardando el archivo..."):
            file_path = save_uploaded_file(uploaded_file)
            st.session_state["pdf_path"] = file_path  


        with st.spinner("Procesando el archivo PDF..."):
            try:
                texts, images, text_summaries, images_summaries = processing_pipeline(file_path)  
                st.session_state.rag_agent.add_documents(texts,images, text_summaries, images_summaries)
                st.session_state.retriever = st.session_state.rag_agent.retriever
                st.session_state["processed_pdf"] = True  
                st.success("PDF procesado correctamente. Puedes empezar a conversar.")
                
            except Exception as e:
                st.error(f"Error procesando el archivo: {str(e)}")
                return

    
    if st.session_state["processed_pdf"]:
        st.header("Chat con el contenido del PDF")

        for message in st.session_state.history:
            if message["role"] == "user":
                st.chat_message("user").markdown(message["content"])
            else:
                st.chat_message("assistant").markdown(message["content"])

        user_input = st.chat_input("Escribe tu pregunta aquí")

        if user_input:
            st.chat_message("user").markdown(user_input)
            st.session_state.history.append({"role": "user", "content": user_input})

            with st.spinner("Generando respuesta..."):
                docs = st.session_state.retriever.invoke(user_input)
                
                response = st.session_state.rag_agent.generate_response(user_input,docs)
                st.chat_message("assistant").markdown(response)
                st.session_state.history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
