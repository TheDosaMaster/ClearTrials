from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from google import genai
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)
client = genai.Client(api_key=os.getenv("gemeni_api_key"))

@app.route("/solve", methods=["POST"])
def solve_equation():
    data = request.get_json()
    prompt = data.get("question", "Solve equation 2x+3 = 7")
    
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents= prompt
    )
    return jsonify({"answer": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True, port=5000)