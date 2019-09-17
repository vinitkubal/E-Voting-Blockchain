from flask import Flask, request, jsonify,make_response
from flask_cors import CORS, cross_origin
import blockchain

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/": {"origins": "http://localhost:80"}})

@app.route('/', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def index():
    data = request.get_json()
    print(data)
    result = blockchain.generate_block(data)
    return jsonify(result)

@app.route('/', methods = ['GET'])
def index1():
   df = blockchain.check_the_ledger()
   return str(df)

if __name__ == '__main__':
    app.run(debug = True)