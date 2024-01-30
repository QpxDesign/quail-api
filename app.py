from flask import Flask, request
from flask_cors import CORS
import redis
import json
import time
import uuid

r = redis.Redis(host='127.0.0.1', port=6379, db=0)
app = Flask(__name__,static_url_path='',static_folder="static/")

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/gen-summary",methods=["POST"])
def run_summarize():
    try:
        sum_id = str(uuid.uuid4())
        data = request.get_json()
        r.set(f"job:{sum_id}", json.dumps({
            "id": sum_id,
            "time": time.time(),
            "text":data["passage_input"],
            "question":data["passage_input"],
            "response": "",
            "isComplete":False
            }))
        return {
            "error":False, 
            "id":sum_id
        }
    except Exception as error: 
        print(error)
        return {
            "error":True, 
        }  
    
@app.route("/poll")
def poll():
    try:
        print(f"job:{request.args.get('id')}")
        item = r.get(f"job:{request.args.get('id')}")
        if item is None:
            return {
            "error":True,
            "response":"error"
            }      
        else:
            return item 
    except Exception as error: 
        print(error)
        return {
            "error":True,
            "response":"error"
        }

if __name__ == '__main__':
    app.run(debug=True)
