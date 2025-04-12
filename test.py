import os
from dotenv import load_dotenv
from model.metta_queries import MettaKnowledgeBase
from model.gemini_model import GeminiChain
import traceback

def main():
    # Load environment variables
    print("Starting test script...")
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"API Key found: {'Yes, length='+str(len(api_key)) if api_key else 'No'}")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("ERROR: Please set your Gemini API key in the .env file")
        return
    
    print("Testing Gemini API integration with Cybersecurity MeTTa KB")
    
    try:
        # Initialize MeTTa knowledge base
        print("Initializing MeTTa knowledge base...")
        kb = MettaKnowledgeBase()
        
        # Print some basic KB information
        print(f"Loaded {kb.get_total_threats()} threat entities")
        print(f"Loaded {kb.get_total_defenses()} defense technologies")
        
        # Initialize Gemini chain
        print("Initializing Gemini chain...")
        gemini_chain = GeminiChain(kb)
        
        # Test with a simple query
        test_query = "What are the most common cybersecurity threats and how can they be mitigated?"
        print(f"\nTest Query: {test_query}")
        
        print("Sending request to Gemini API...")
        response = gemini_chain.generate_response(test_query)
        print(f"\nGemini Response:\n{response}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()