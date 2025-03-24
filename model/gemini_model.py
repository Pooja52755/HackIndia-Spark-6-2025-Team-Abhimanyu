
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

class GeminiChain:
    def __init__(self, metta_kb):
        # Configure with correct model name and endpoint
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",  #  model name
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3,
           convert_system_message_to_human=True,
        )
        self.metta_kb = metta_kb
        self.chain = self._create_chain()

    def _create_chain(self):
        print("here 3")
        google_api_key=os.getenv("GEMINI_API_KEY")
        print(google_api_key)
        prompt = ChatPromptTemplate.from_template(
            """Answer the question based only on the following context:
            {context}
            
            Question: {question}
            
            Provide a helpful response using both the context and your general knowledge.
            If mentioning sensitive attributes, maintain respectful language."""
        )

        return (
            {"context": self._get_metta_context, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )


    def _get_metta_context(self, _):
        """Build comprehensive context from MeTTa KB"""
        context = {
            'total_humans': len(self.metta_kb.get_humans()),
            'men': self.metta_kb.get_men(),
            'women': self.metta_kb.get_women(),
            'soda_drinkers': self.metta_kb.get_soda_drinkers(),
            'ugly_individuals': self.metta_kb.get_ugly(),
            'ugly_men': self.metta_kb.get_ugly_men(),
            'ugly_women': self.metta_kb.get_ugly_women(),
            'male_soda_drinkers': self.metta_kb.get_male_soda_drinkers(),
            'female_soda_drinkers': self.metta_kb.get_female_soda_drinkers()
        }
        return self._build_prompt(context)

    def _build_prompt(self, context):
        """Format the context into the structured prompt"""
        return f"""
        KNOWLEDGE BASE CONTEXT:
        - Total Humans: {context['total_humans']}
        - Men: {', '.join(context['men'])}
        - Women: {', '.join(context['women'])}
        - Soda Drinkers: {', '.join(context['soda_drinkers'])}
        - Ugly Individuals: {', '.join(context['ugly_individuals'])}
        - Ugly Men: {', '.join(context['ugly_men'])}
        - Ugly Women: {', '.join(context['ugly_women'])}
        - Male Soda Drinkers: {', '.join(context['male_soda_drinkers'])}
        - Female Soda Drinkers: {', '.join(context['female_soda_drinkers'])}

        INSTRUCTIONS:
        1. Be factual and use the context above
        2. Maintain neutral language about appearances
        3. Highlight demographic patterns when relevant
        4. If asked about sensitive attributes, respond respectfully
        5. For count questions, use the exact numbers from context
        """

    def generate_response(self, question):
        print("here2")
        try:
            return self.chain.invoke(question)
        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}")




