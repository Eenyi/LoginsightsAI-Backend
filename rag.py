import os
from dotenv import load_dotenv

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

import google.generativeai as genai
from model import Model
from session import LocalSession

genModel = Model()

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        emModel = 'models/embedding-001'
        title = "Custom query"
        return genai.embed_content(model=emModel,
                                   content=input,
                                   task_type="retrieval_document",
                                   title=title)["embedding"]
      
class RagModel:
   config = {
      "max_output_tokens": 2048,
      "temperature": 1,
      "top_p": 1,
      }
   def get_relevant_passages(cls, query, db, n_results=10):
      passages = db.query(query_texts=[query], n_results=n_results)['documents'][0]
      return passages


   def make_prompt(cls, query, relevant_passage):
      escaped = relevant_passage.replace(
         "'", "").replace('"', "").replace("\n", " ")
      
      
      prompt = f"""{query}.\n
      Additional information:\n {escaped}\n
      If you find that the question has no relation to the additional information, 
      then answer on your own in the form of bullets.\n
      """
      return prompt


   def convert_pasages_to_string(cls, passages):
      context = ""

      for passage in passages:
         context += passage + "\n"

      return context

   def setUpGoogleAPI(cls):
      load_dotenv()
      api_key = os.getenv('GEMINI_API_KEY')
      genai.configure(api_key=api_key)


   def loadVectorDataBase(cls):
      chroma_client = chromadb.PersistentClient(path="database/")

      db = chroma_client.get_or_create_collection(
         name="sme_db", embedding_function=GeminiEmbeddingFunction())

      LocalSession.set('db', db)
      
      
   def main(cls, message):
      cls.setUpGoogleAPI()
      cls.loadVectorDataBase()
      question = message['content']
      db = LocalSession.get('db')
      passages = cls.get_relevant_passages(question, db, 5)
      
      prompt = cls.make_prompt(question, cls.convert_pasages_to_string(passages))
      
      answer = genModel.generate_content(prompt)
      return answer
      
    
    