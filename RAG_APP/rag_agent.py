import uuid
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.embeddings import OllamaEmbeddings
from langchain_ollama import ChatOllama
from base64 import b64decode

class RAG_AGENT:
    def __init__(self,persist_directory="./chroma_data"):
        self.persist_directory = persist_directory 
        self.ollama_embeddings = OllamaEmbeddings(
        base_url="http://ollama:11434",
        model="nomic-embed-text"
    )
        self.model = ChatOllama(
        model='llava:latest',
        base_url='http://ollama:11434',
        temperature=0.5
    )
        self.vectorstore = Chroma(collection_name="multi_modal_rag", embedding_function=self.ollama_embeddings, persist_directory = self.persist_directory)

        self.store = InMemoryStore()
        self.id_key = "doc_id"

        self.retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=self.store,
            id_key=self.id_key,
        )

    def add_documents(self,texts, images, text_summaries, images_summaries):

        doc_ids = [str(uuid.uuid4()) for _ in texts]
        summary_texts = [
        Document(page_content=summary, metadata={self.id_key: doc_ids[i]}) for i, summary in enumerate(text_summaries)
    ]
        self.retriever.vectorstore.add_documents(summary_texts)
        self.retriever.docstore.mset(list(zip(doc_ids, texts)))

        img_ids = [str(uuid.uuid4()) for _ in images]
      
        summary_img = [
            Document(page_content=summary, metadata={self.id_key: img_ids[i]}) for i, summary in enumerate(images_summaries)
        ]
       
        self.retriever.vectorstore.add_documents(summary_img)
        self.retriever.docstore.mset(list(zip(img_ids, images)))


    def parse_docs(self,docs):
        b64 = []
        text = []
        for doc in docs:
            try:
                b64decode(doc)
                b64.append(doc)
            except Exception as e:
                text.append(doc)
        return {"images": b64, "texts": text}

    def generate_response(self,question,docs):
        parsed_docs = self.parse_docs(docs)

        context_text = ""
        if len(parsed_docs["texts"]) > 0:
            for doc in parsed_docs["texts"]:
                context_text += doc.text

        prompt_template = f"""
    Answer the question based only on the following context.
    Context: {context_text}
    Question: {question}
    """  
        prompt_content =  [{"type": "text", "text": prompt_template}]
        if len(parsed_docs["images"]) > 0:
            for image in parsed_docs["images"]:
                prompt_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                    }
                )
                
        response = self.model.invoke([{"role": "user", "content": prompt_content}])
        return response.content
