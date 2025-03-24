
from hyperon import MeTTa
import os

class MettaKnowledgeBase:
    def __init__(self):
        self.metta = MeTTa()
        self.metta.run("(add-atom &self (Concept \"ChatbotKB\"))")
        self._load_knowledge()

  

    def _load_knowledge(self):
        with open("metta/kb.metta") as f:
            self.metta.run(f.read())
        with open("metta/queries.metta") as f:
            self.metta.run(f.read())
    
    def execute_query(self, query_template, *args):
        """Execute a MeTTa query and return formatted results"""
        query = query_template.format(*args)
        try:
            result = self.metta.run(query)
            return [str(item) for sublist in result for item in sublist if str(item) != 'Empty']
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")

    

    def get_humans(self):
        return self.execute_query("!(getHumans)")
    
    def get_men(self):
        return self.execute_query("!(getMen)")
    
    def get_women(self):
        return self.execute_query("!(getWomen)")
    
    def get_ugly(self):
        return self.execute_query("!(getUgly)")
    
    def get_soda_drinkers(self):
        return self.execute_query("!(getSodaDrinkers)")
    
    def get_ugly_men(self):
        return self.execute_query("!(getUglyMen)")
    
    def get_ugly_women(self):
        return self.execute_query("!(getUglyWomen)")
    
    def get_male_soda_drinkers(self):
        return self.execute_query("!(getSodaDrinkingMen)")
    
    def get_female_soda_drinkers(self):
        return self.execute_query("!(getSodaDrinkingWomen)")
    
    def get_total_humans(self):
        return len(self.get_humans())