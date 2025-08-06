import base64
# import vertexai
# from vertexai.generative_models import GenerativeModel, Part, FinishReason
# import vertexai.preview.generative_models as generative_models
# from session import LocalSession
import google.generativeai as genai
from session import LocalSession
import os

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
class Model:

  # Simulated user data
  users = {'user': 'userpass', 'admin': 'adminpass'}
  
  USER = "user"
  MODEL = "model"

  # vertexai.init(project="558200667371", location="us-central1")

  
  # model = GenerativeModel(
  #   "projects/558200667371/locations/us-central1/endpoints/2931436538115915776",
  # )

  generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0.1,
    "top_p": 1,
  }
  
  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  )
  
  history=[
    {
      "role": "user",
      "parts": [
        "In <referenceNo>PI9325031235370555</referenceNo> is a reference number\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "That's correct! `<referenceNo>PI9325031235370555</referenceNo>` looks like a reference number. \n\nIt's likely part of a structured document (like XML) where the `<referenceNo>` tags are used to identify a specific reference number. \n",
      ],
    }
  ]
  

  def getGeminiResponse(cls, request):
      # responses = cls.model.generate_content(
      # [request["content"]],
      # generation_config=cls.generation_config,
      # stream=True,
      # )
      cls.history.extend(LocalSession.session_history)
      print("History")
      print(cls.history)
      chat_session = cls.model.start_chat(
        history=cls.history
      )
      response = chat_session.send_message(request["content"])
      LocalSession.set_history(cls.USER, request["content"])
      LocalSession.set_history(cls.MODEL, response.text)
      # print(response)
      
      # myResponse = ""
      # for response in responses:
      #   myResponse += response.text
      return {"response": response.text}
   
  def generate_content(cls, request):

      # responses = cls.model.generate_content(
      # [request],
      # generation_config=cls.generation_config,
      # stream=True,
      # )
      
      # myResponse = ""
      # for response in responses:
      #   myResponse += response.text
      # cls.history.extend(LocalSession.session_history)
      print("History 2")
      print(cls.history)
      chat_session = cls.model.start_chat(
        history=cls.history
      )
      response = chat_session.send_message(request)
      # LocalSession.set_history(cls.USER, request)
      # LocalSession.set_history(cls.MODEL, response.text)
      return {"response": response.text}
  
  def validateLogin(cls, request):
     if request["username"] in cls.users and cls.users[request["username"]] == request["password"]:
        return {
           "status": True,
           "message": "Redirecting to dashboard...",
        }
     else:
        return {
           "status": False,
           "message": "Invalid Credentials!",
        }
     
  


 
  
 
 

 

 