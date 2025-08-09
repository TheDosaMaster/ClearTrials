from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from google import genai
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)
client = genai.Client(api_key=os.getenv("gemeni_api_key"))

@app.route('/get_data')
def get_data():
    return jsonify({
        'message': 'Hello, this is a response from the server!'})
if __name__ == '__main__':
    app.run(debug=True, port=8080)