# from flask import Flask, request, jsonify
# from model.metta_queries import MettaKnowledgeBase
# from model.gemini_model import GeminiChat
# import os

from flask import Flask, request, jsonify
from model.metta_queries import MettaKnowledgeBase
from model.gemini_model import GeminiChain

from dotenv import load_dotenv
import os

from dotenv import load_dotenv
load_dotenv()  # Add this at the top before other imports

app = Flask(__name__)


try:
    knowledge_base = MettaKnowledgeBase()
    chat_chain = GeminiChain(knowledge_base)
except Exception as e:
    raise RuntimeError(f"Initialization failed: {str(e)}")

@app.route("/chat",methods=["GET"])
def root():
    return {"message":"Hello"}

@app.route("/chat", methods=["POST"])
def chat_handler():
    try:
        user_input = request.json.get("message", "")
        if not user_input.strip():
            return jsonify({"error": "Empty message"}), 400
        
        response = chat_chain.generate_response(user_input)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8006, debug=os.getenv("FLASK_DEBUG", False))


# # Initialize components
# try:
#     knowledge_base = MettaKnowledgeBase()
#     chat_model = GeminiChat()
# except Exception as e:
#     raise RuntimeError(f"Initialization failed: {str(e)}")

# @app.route("/chat",methods=["GET"])
# def root():
#     return {"message":"Hello"}


# @app.route("/chat", methods=["POST"])
# def chat_handler():
#     try:
#         user_input = request.json.get("message", "")
#         if not user_input.strip():
#             return jsonify({"error": "Empty message"}), 400
        
#         context = knowledge_base.get_context()
#         response = chat_model.generate_response(context, user_input)
#         return jsonify({"response": response})
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8001, debug=os.getenv("FLASK_DEBUG", False))