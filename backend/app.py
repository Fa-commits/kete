from flask import Flask, request, jsonify
from flask_cors import CORS
from main import main

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:8080", "http://0.0.0.0:8080", "http://192.168.1.127:8080", "http://localhost:5173"]}})

# Your routes go here
@app.route('/api/query', methods=['POST'])
def handle_query():
    try:
        query = request.json['query']
        result = main(query)
        return jsonify({'result': str(result)})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Ein Fehler ist aufgetreten beim Verarbeiten der Anfrage.'}), 500

if __name__ == '__main__':
    app.run(debug=True)