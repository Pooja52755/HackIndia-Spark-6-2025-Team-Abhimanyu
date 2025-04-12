from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
import google.generativeai as genai
import re

class GeminiChain:
    def __init__(self, metta_kb):
        # Get the API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        # Configure with correct model name and endpoint
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",  # model name
            google_api_key=api_key,  # Explicitly pass the API key here
            temperature=0.3,
            convert_system_message_to_human=True,
        )
        self.metta_kb = metta_kb
        self.chain = self._create_chain()

    def _create_chain(self):
        prompt = ChatPromptTemplate.from_template(
            """Answer the question based only on the following context:
            {context}
            
            Question: {question}
            
            Provide a helpful response about cybersecurity using both the context and your general knowledge.
            Focus on explaining cybersecurity concepts clearly and accurately.
            
            FORMATTING GUIDELINES:
            1. Use proper paragraph breaks between different topics or ideas
            2. Use bullet points for lists
            3. Include appropriate spacing between sentences
            4. Bold important terms or headings using markdown (**term**)
            5. Organize information in a readable structure
            6. For any technical terms, provide a brief definition in parentheses
            7. Use short, clear sentences for better readability"""
        )

        return (
            {"context": self._get_metta_context, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
            | self._format_response
        )

    def _get_metta_context(self, _):
        """Build comprehensive context from Cybersecurity MeTTa KB"""
        context = {
            'threat_entities': self.metta_kb.getthreatentities(),
            'defense_technologies': self.metta_kb.getdefensetechnologies(),
            'attack_vectors': self.metta_kb.getattackvectors(),
            'data_theft_threats': self.metta_kb.getdatatheftthreats(),
            'network_security_tools': self.metta_kb.getnetworksecuritytools(),
            'endpoint_security_tools': self.metta_kb.getendpointsecuritytools(),
            'security_monitoring_tools': self.metta_kb.getsecuritymonitoringtools(),
            'all_mitigations': self.metta_kb.getallmitigations(),
            'threat_detection_tools': self.metta_kb.getthreatdetectiontools(),
            'attack_vector_defenses': self.metta_kb.getdefensesforattackvector()
        }
        return self._build_prompt(context)

    def _build_prompt(self, context):
        """Format the context into the structured prompt"""
        return f"""
        CYBERSECURITY KNOWLEDGE BASE CONTEXT:
        - Threat Entities: {', '.join(context['threat_entities'])}
        - Defense Technologies: {', '.join(context['defense_technologies'])}
        - Attack Vectors: {', '.join(context['attack_vectors'])}
        - Data Theft Threats: {', '.join(context['data_theft_threats'])}
        - Network Security Tools: {', '.join(context['network_security_tools'])}
        - Endpoint Security Tools: {', '.join(context['endpoint_security_tools'])}
        - Security Monitoring Tools: {', '.join(context['security_monitoring_tools'])}
        
        RELATIONSHIPS:
        - Threat Mitigations: {', '.join(context['all_mitigations'])}
        - Threat Detection: {', '.join(context['threat_detection_tools'])}
        - Attack Vector Defenses: {', '.join(context['attack_vector_defenses'])}

        INSTRUCTIONS:
        1. Be factual and use the cybersecurity context above
        2. Explain cybersecurity concepts clearly
        3. When discussing threats, also mention applicable defenses
        4. When discussing attack vectors, explain how they can be mitigated
        5. For technical questions, provide accurate and practical explanations
        6. Format your answer with proper spacing and structure
        7. Use markdown formatting for readability (headers, bold, lists)
        8. Create visually organized responses with clear sections
        """

    def _format_response(self, text):
        """Post-process the response to ensure proper formatting"""
        if not text:
            return text
            
        # Ensure proper spacing after punctuation
        text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
        
        # Ensure proper spacing between sentences
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\n\2', text)
        
        # Format bullet points consistently
        text = re.sub(r'^\s*[-*]\s*', '\n• ', text, flags=re.MULTILINE)
        
        # Format numbered lists consistently
        text = re.sub(r'^\s*(\d+)[.)] ', r'\n\1. ', text, flags=re.MULTILINE)
        
        # Ensure consistent paragraph breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Add spacing after colons if followed by text
        text = re.sub(r':\s*([A-Za-z])', r': \1', text)
        
        # Clean up any multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        
        # Add proper spacing around markdown elements
        text = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', text)
        
        return text.strip()

    def generate_response(self, question):
        try:
            return self.chain.invoke(question)
        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}")




