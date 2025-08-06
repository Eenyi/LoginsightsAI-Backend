import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from tqdm import tqdm
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

import google.generativeai as genai
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = 'models/embedding-001'
        # for better results, try to provide a title for each input if the corpus is covering a lot of domains
        title = "Systeme de management de l'environnement"

        return genai.embed_content(
            model=model,
            content=input,
            task_type="retrieval_document",
            title=title)["embedding"]

class Embeddings:
   def extract_text_from_pdf(cls, file_path):
    pdf_reader = PdfReader(file_path)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page in range(num_pages):
        text += pdf_reader.pages[page].extract_text()
    return text
   
   def createEmbeddings(cls):
      # Directory containing the books
      books_directory = 'books/'
      all_text = ""
      
      # Iterate through all PDF files in the directory
      for file_name in os.listdir(books_directory):
         if file_name.endswith('.pdf'):
            file_path = os.path.join(books_directory, file_name)
            all_text += cls.extract_text_from_pdf(file_path)
      
      all_text = cls.clean_extracted_text(all_text)
      text_splitter = RecursiveCharacterTextSplitter(
         chunk_size=1000,
         chunk_overlap=100,
         length_function=len,
         add_start_index=True,
      )
      texts = text_splitter.create_documents([all_text])
      documents = []

      for chunk in texts:
         documents.append(chunk.page_content)
         
      db = cls.create_chroma_db(documents, "sme_db")
      return db.count()

      
   
   def clean_extracted_text(cls, text):
    cleaned_text = ""

    for i, line in enumerate(text.split('\n')):
        if len(line) > 10 and i > 70:
            cleaned_text += line + '\n'

    cleaned_text = cleaned_text.replace('.', '')
    cleaned_text = cleaned_text.replace('~', '')
    cleaned_text = cleaned_text.replace('©', '')
    cleaned_text = cleaned_text.replace('_', '')
    cleaned_text = cleaned_text.replace(';:;', '')
    return cleaned_text
   
   def create_pdf(cls, text, filename):
    # Set up the canvas with the specified filename and page size
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set up the text object
    text_object = c.beginText()
    text_object.setTextOrigin(50, height - 50)
    text_object.setFont("Helvetica", 12)

    # Add the text to the text object
    for line in text.split('\n'):
        text_object.textLine(line)

    # Draw the text object on the canvas
    c.drawText(text_object)
    c.showPage()
    c.save()
    
   def create_chroma_db(cls, documents, name):
    chroma_client = chromadb.PersistentClient(path="database/")

    db = chroma_client.get_or_create_collection(
        name=name, embedding_function=GeminiEmbeddingFunction())

    initiali_size = db.count()
    for i, d in tqdm(enumerate(documents), total=len(documents), desc="Creating Chroma DB"):
        db.add(
            documents=d,
            ids=str(i + initiali_size)
        )
        time.sleep(0.5)
    return db


   def get_chroma_db(cls, name):
      chroma_client = chromadb.PersistentClient(path="database/")
      return chroma_client.get_collection(name=name, embedding_function=GeminiEmbeddingFunction())
 