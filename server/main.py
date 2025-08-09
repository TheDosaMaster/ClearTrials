from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from google import genai
from flask_cors import CORS
import json
load_dotenv()
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
client = genai.Client(api_key=os.getenv("gemeni_api_key"))
def search_clinical_trials(query_term):
  
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    
    params = {
        'query.cond': query_term,
        'fields': 'NCTId,BriefTitle,OverallStatus,Condition',
        'pageSize': 5 
    }
    
    print(f"Searching ClinicalTrials.gov for: {query_term}")

    try:
       
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        data = response.json()
        
        
        studies = []
        
        if data and 'studies' in data and isinstance(data['studies'], list):
            for study in data['studies']:
                protocol_section = study.get('protocolSection', {})
                identification_module = protocol_section.get('identificationModule', {})
                status_module = protocol_section.get('statusModule', {})
                conditions_module = protocol_section.get('conditionsModule', {})

                
                conditions = conditions_module.get('conditions', ['N/A'])
                
                studies.append({
                    'NCTId': identification_module.get('nctId'),
                    'BriefTitle': identification_module.get('briefTitle'),
                    'OverallStatus': status_module.get('overallStatus'),
                    'Conditions': ', '.join(conditions) 
                })
        
        return studies

    except requests.exceptions.RequestException as e:
        print(f"Error calling ClinicalTrials.gov API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from ClinicalTrials.gov: {e}")
        return None
@app.route('/chatbot', methods=['POST'])
def chatbot():
   
    if not client:
        return jsonify({"error": "Gemini API client not initialized. Check your API key."}), 500

   
    try:
        data = request.get_json()
        user_message = data.get("message")
        if not user_message:
            return jsonify({"error": "No 'message' field in request body."}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON in request body."}), 400

 
    model = client.models.get("gemini-pro")

    try:
      
        response = model.generate_content(user_message)
        
       
        if response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "I'm sorry, I couldn't generate a response."}), 500

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)