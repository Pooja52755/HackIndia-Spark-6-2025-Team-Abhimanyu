# Cybersecurity Knowledge Chatbot with Gemini Integration 

A context-aware cybersecurity chatbot that combines structured knowledge representation in MeTTa with Google Gemini's natural language capabilities.

## Features

- **Cybersecurity Knowledge Representation**: Structured representation of threats, defenses, and attack vectors using MeTTa
- **Security Relationships**: Modeling mitigations, detection methods, and security domains
- **Querying**: Extract cybersecurity relationships from knowledge base
- **LLM Integration**: Google Gemini for natural language understanding
- **Web Interface**: Flask-based REST API for easy integration

## Prerequisites

- Python 3.10+
- Google Gemini API key (obtain from https://ai.google.dev/)
- MeTTa/Hyperon environment

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cybersecurity-metta-chatbot.git
   cd cybersecurity-metta-chatbot 
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash 
   pip install -r requirements.txt 
   ```
4. Set up Gemini API key:
   - Create a .env file in the project root
   - Add your Gemini API key: `GEMINI_API_KEY=your_api_key_here`

5. Test Gemini Integration:
   ```bash
   python test_gemini_integration.py
   ```
  
### Project Structure
```
cybersecurity-metta-chatbot/
├── app.py                 # Flask application entry point
├── model/
│   ├── __init__.py
│   ├── gemini_model.py    # Gemini LLM integration
│   └── metta_queries.py   # MeTTa knowledge base handler
├── metta/
│   ├── kb.metta           # Cybersecurity knowledge base
│   └── queries.metta      # MeTTa queries
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (add your Gemini API key here)
└── README.md 
```
## Usage
1. Start the Flask server:
   ```bash
   python app.py 
   ```
2. Send queries to the API:
   ```bash
   curl -X POST http://127.0.0.1:8006/chat \
   -H "Content-Type: application/json" \
   -d '{"message": "What are the most effective defenses against ransomware?"}'
   ```

## Example Queries
- "What are the most common cybersecurity threats?"
- "How can I protect against SQL injection attacks?"
- "What tools are used for network security?"
- "What's the difference between IDS and IPS?"
- "Which threats are classified as data theft?"
- "How are ransomware attacks mitigated?"