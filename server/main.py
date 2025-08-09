from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from google import genai
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
client = genai.Client(api_key=os.getenv("gemeni_api_key"))
@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        response = client.models.generate_content(
    model="gemini-2.5-flash",
        contents=prompt"
    )
        return jsonify(
            {"answer": response.text}
            )
    else: 
        return "how can I assist you?"
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)