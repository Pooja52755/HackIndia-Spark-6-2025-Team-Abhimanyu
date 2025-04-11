from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS  # Import CORS for cross-origin support

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock cybersecurity knowledge base data
mock_kb = {
    "threat_entities": ["Malware", "Ransomware", "Trojan", "Spyware", "Rootkit", "Keylogger", "Worm", "Virus", "Adware", "Botnet"],
    "defense_technologies": ["Firewall", "IDS", "IPS", "Antivirus", "WAF", "EDR", "SIEM", "DLP", "VPN", "MFA"],
    "attack_vectors": ["SQLInjection", "XSS", "CSRF", "PhishingEmail", "SocialEngineering", "BruteForce", "DDoS", "MitM", "SupplyChain", "ZeroDay"],
    "mitigations": {
        "SQLInjection": ["WAF", "Input Validation"],
        "Ransomware": ["EDR", "Backups", "Email Filtering"],
        "Malware": ["Antivirus", "EDR", "Network Segmentation"],
        "PhishingEmail": ["Security Awareness", "Email Filtering", "DLP"]
    }
}

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok", "message": "API is running"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
        
        # Create context from mock data
        context = f"""
        CYBERSECURITY KNOWLEDGE BASE CONTEXT:
        - Threat Entities: {', '.join(mock_kb['threat_entities'])}
        - Defense Technologies: {', '.join(mock_kb['defense_technologies'])}
        - Attack Vectors: {', '.join(mock_kb['attack_vectors'])}
        
        MITIGATIONS:
        - SQL Injection: {', '.join(mock_kb['mitigations']['SQLInjection'])}
        - Ransomware: {', '.join(mock_kb['mitigations']['Ransomware'])}
        - Malware: {', '.join(mock_kb['mitigations']['Malware'])}
        - Phishing Email: {', '.join(mock_kb['mitigations']['PhishingEmail'])}
        
        INSTRUCTIONS:
        1. Be factual and use the cybersecurity context above
        2. Explain cybersecurity concepts clearly
        3. When discussing threats, also mention applicable defenses
        4. When discussing attack vectors, explain how they can be mitigated
        5. For technical questions, provide accurate and practical explanations
        """
        
        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(
            f"Context: {context}\n\nQuestion: {user_message}\n\nProvide a helpful response about cybersecurity."
        )
        
        return jsonify({'response': response.text})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"API Key configured: {'Yes' if api_key else 'No'}")
    print("Starting cybersecurity chatbot API...")
    app.run(debug=True, port=8006)