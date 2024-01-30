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
    id = uuid.uuid4()
    data = request.get_json()
    print(data)
    queue = r.get("quail_queue")
    try:
        queue = json.loads(queue)
    except:
        queue = []
    queue = [{
        "index":0,
        "id": id,
        "time": time.time(),
        "text":"",
        "question":"",
        "response": "",
        "isComplete":False
        }]
    r.set("quail_queue", json.dumps(queue))
    latest_queue = queue
    while len(list(filter(lambda a: a["id"] == id, latest_queue))) != 0 and list(filter(lambda a: a["id"] == id, latest_queue))[0]["isComplete"] == False:
        sleep(10)
        latest_queue = r.get("queue")
    return list(filter(lambda a: a["id"] == id, latest_queue))[0]

if __name__ == '__main__':
    app.run(debug=True)
