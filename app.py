from flask import Flask, request, jsonify, send_file
from flask_restx import Resource, Api
from flask_cors import CORS
from model import Model
from rag import RagModel
from graph import Graph
from session import LocalSession
from embeddings import Embeddings
from datetime import datetime

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
model = Model()
rag = RagModel()
graph = Graph()
embeddings = Embeddings()
ns = api.namespace('graph', description='Graph operations')

@api.route('/query_prompt')
class Query_Prompt(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        _request = {
            "content": request.json["query"],
        }
        # _response = rag.main(_request)
        _response = model.getGeminiResponse(_request)
        if _response:
            return jsonify({"status": True, "message": "Request sent successfully", "error": None, "response": _response})
        else:
            return jsonify({"status": False, "message": "Request not sent successfully", "error": "Something went Wrong", "response": _response})


@api.route('/upload')
class Upload(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        _content = request.json["content"]
        _request = {
            "content":_content + '''\n\n Based on the above content identify any performance and 
                                    technical issues and give your answer in the bullet format. ''',
        }
        LocalSession.set("logFile", _content)
        _response = model.getGeminiResponse(_request)
        if _response:
            return jsonify({"status": True, "message": "Request sent successfully", "error": None, "response": _response})
        else:
            return jsonify({"status": False, "message": "Request not sent successfully", "error": "Something went Wrong", "response": _response})
        
        
@api.route('/graphData1')
class GraphData(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        _request = {
            "content":request.json["content"] + '''\n\n Analyze above logs data and provide response 
                    in the form of JSON data only, without any extra text, containing number 
                    of requests based on each interface Id''',
        }
        _response = rag.main(_request)
        if _response:
            return jsonify({"status": True, "message": "Request sent successfully", "error": None, "response": _response})
        else:
            return jsonify({"status": False, "message": "Request not sent successfully", "error": "Something went Wrong", "response": _response})
       
        
@api.route('/graphData2')
class Login(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        _request = {
            "content":request.json["content"] + '''\n\n Analyze above logs data and provide response 
                    in the form of JSON data only, without any extra text, containing number 
                    of success failure and timeout requests''',
        }
        _response = rag.main(_request)
        if _response:
            return jsonify({"status": True, "message": "Request sent successfully", "error": None, "response": _response})
        else:
            return jsonify({"status": False, "message": "Request not sent successfully", "error": "Something went Wrong", "response": _response})
        
@api.route('/graphData3')
class Login(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        _request = {
            "content":request.json["content"] + '''\n\n Analyze above logs data and provide response 
                    in the form of JSON data only, without any extra text, containing interface Ids 
                    of requests along with Duration''',
        }
        _response = model.getGeminiResponse(_request)
        if _response:
            return jsonify({"status": True, "message": "Request sent successfully", "error": None, "response": _response})
        else:
            return jsonify({"status": False, "message": "Request not sent successfully", "error": "Something went Wrong", "response": _response})
        

@api.route('/createEmbeddings')
class CreateEmbeddings(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        _request = {
            "content":request.json["content"]
        }
        timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        embeddings.create_pdf(request.json["content"], "books/upload_"+timestamp+".pdf")
        embeddings.createEmbeddings()
        return jsonify({"status": "Succsess", "message": ""})

@api.route('/login')
class Login(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        _request = {
            "username":request.json["username"],
            "password":request.json["password"],
        }
        _response = model.validateLogin(_request)
        return jsonify({"status": _response["status"], "message": _response["message"]})
        

@ns.route('/')
class Graph(Resource):
    def get(self):
        return {'query': 'prompt'}
    def post(self):
        try:
            buf = graph.generate_graph(request.json['data'], request.json['labels'], request.json['graph_type'], request.json['title'])
            return send_file(buf, mimetype='image/png')
        except ValueError as e:
            return jsonify({'error':str(e)}), 400
        
api.add_namespace(ns)

if __name__ == '__main__':
    app.run(debug=True)