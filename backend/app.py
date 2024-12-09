from flask import Flask, request, jsonify
from main import main

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def handle_query():
    query = request.json['query']
    result = main(query)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)