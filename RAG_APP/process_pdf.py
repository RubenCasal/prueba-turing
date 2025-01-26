from unstructured.partition.pdf import partition_pdf
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.chains import SimpleSequentialChain
from langchain_ollama import ChatOllama
import ollama



def processing_pipeline(file_path):
    chunks = process_pdf(file_path)
    texts, images = divide_chunks(chunks)

    text_summaries, images_summaries = summarize(texts,images)

 
    return texts, images, text_summaries, images_summaries
   
   




def process_pdf(file_path):
    chunks = partition_pdf(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables

        extract_image_block_types=["Image"],   # Add 'Table' to list to extract image of tables
        # image_output_dir_path=output_path,   # if None, images and tables will saved in base64

        extract_image_block_to_payload=True,   # if true, will extract base64 for API usage

        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,

        extract_images_in_pdf=True,         
    )
    return chunks


def divide_chunks(chunks):
    texts = []
    images = []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            texts.append(chunk)
            
            chunk_elements = chunk.metadata.orig_elements
            for element in chunk_elements:
                if "Image" in str(type(element)):
                    images.append(element.metadata.image_base64)
                    
                    
              

    return   texts, images


def summarize(texts, images):
    text_summaries = [summarize_text(text) for text in texts]

    
    images_summaries = [summarize_images(image) for image in images]

    return text_summaries, images_summaries
   
   

def summarize_images(element):
    prompt_template = f"""
You are an advanced assistant trained to analyze images and provide detailed descriptions. Focus entirely on the visual details of the image to generate a precise and comprehensive description. Be descriptive, specific, and include as much relevant information as possible.
"""
    model = ChatOllama(
        model='llava:latest',
        base_url='http://ollama:11434',
        temperature=0.5
    )
    messages = [
    (
        "user",
        [
            {"type": "text", "text": prompt_template},
            {
                "type": "image_url",
                "image_url": {"url": "data:image/jpeg;base64,{element}"},
            },
        ],
    )
]
    prompt = ChatPromptTemplate.from_messages(messages)
    
    input_prompt = prompt.format(element=element)
    response = model.invoke([{"role": "user", "content": input_prompt}])
   
    
    
    return response.content


def summarize_text(element):
    prompt_text = """
You are an assistant tasked with summarizing tables and text.
Give a concise summary of the table or text.

Respond only with the summary, no additional comment.
Do not start your message by saying "Here is a summary" or anything like that.
Just give the summary as it is.

Table or text chunk: {element}
"""
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOllama(
        model='llama3.1:latest',
        base_url='http://ollama:11434',  
        temperature=0.5
)
    input_prompt = prompt.format(element=element)
    response = model.invoke([{"role": "user", "content": input_prompt}])
    
    return response.content



