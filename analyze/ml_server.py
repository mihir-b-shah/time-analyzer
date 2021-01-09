
from flask import Flask

app = Flask(__name__)
    
@app.route('/', methods = ['GET'])
def gen_ss():
    return 'Hello, World!'
    
LocalHostIP = '127.0.0.1'
app.run(host=LocalHostIP, port=5050)