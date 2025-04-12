import os
from hyperon import MeTTa

class MettaKnowledgeBase:
    def _init_(self):
        self.metta = None
        self._load_knowledge()

    def _load_knowledge(self):
        """Load knowledge base entries from cybersec_knowledge.metta using Hyperon"""
        try:
            # Initialize the MeTTa runtime
            self.metta = MeTTa()
            
            # Get paths to knowledge base files
            kb_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(_file_))), "metta")
            kb_path = os.path.join(kb_dir, "cybersec_knowledge.metta")
            queries_path = os.path.join(kb_dir, "cybersec_queries.metta")
            
            # Load the main knowledge base file using with open
            if os.path.exists(kb_path):
                with open(kb_path, 'r') as file:
                    kb_content = file.read()
                self.metta.run(kb_content)
                print(f"Loaded knowledge base from {kb_path}")
            else:
                print(f"Knowledge base file not found: {kb_path}")
            
            # Load the queries file using with open
            if os.path.exists(queries_path):
                with open(queries_path, 'r') as file:
                    queries_content = file.read()
                self.metta.run(queries_content)
                print(f"Loaded queries from {queries_path}")
            else:
                print(f"Queries file not found: {queries_path}")
                
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            # Initialize empty MeTTa runtime as fallback
            self.metta = MeTTa()

    def execute_query(self, query_string, *args):
        """Execute a query using the Hyperon MeTTa runtime"""
        try:
            # Format the query string with arguments
            formatted_query = query_string
            for arg in args:
                formatted_query = formatted_query.replace('?', f'"{arg}"', 1)
            
            # Execute the query
            result = self.metta.run(formatted_query)
            
            # Convert result to a list of strings
            string_results = []
            for item in result:
                string_results.append(str(item).replace('(', '').replace(')', '').strip())
            
            return string_results
        except Exception as e:
            print(f"Query execution failed: {str(e)}")
            return []

    def getthreatentities(self):
        return self.execute_query("!(getThreatEntities)")
    
    def getdefensetechnologies(self):
        return self.execute_query("!(getDefenseTechnologies)")
    
    def getattackvectors(self):
        return self.execute_query("!(getAttackVectors)")
    
    def getdatatheftthreats(self):
        return self.execute_query("!(getDataTheftThreats)")
    
    def getnetworksecuritytools(self):
        return self.execute_query("!(getNetworkSecurityTools)")
    
    def getendpointsecuritytools(self):
        return self.execute_query("!(getEndpointSecurityTools)")
    
    def getsecuritymonitoringtools(self):
        return self.execute_query("!(getSecurityMonitoringTools)")
    
    def getthreatmitigations(self, threat):
        return self.execute_query(f'!(getThreatMitigations "{threat}")')
    
    def getallmitigations(self):
        results = self.execute_query("!(getAllMitigations)")
        formatted_results = []
        for result in results:
            parts = result.split()
            if len(parts) >= 2:
                formatted_results.append(f"{parts[0]}, {parts[1]}")
        return formatted_results
    
    def getdefensesforattackvector(self):
        results = self.execute_query("!(getDefensesForAttackVector)")
        formatted_results = []
        for result in results:
            parts = result.split()
            if len(parts) >= 2:
                formatted_results.append(f"{parts[0]}, {parts[1]}")
        return formatted_results
    
    def getthreatdetectiontools(self):
        results = self.execute_query("!(getThreatDetectionTools)")
        formatted_results = []
        for result in results:
            parts = result.split()
            if len(parts) >= 2:
                formatted_results.append(f"{parts[0]}, {parts[1]}")
        return formatted_results
    
    def gettoolsbysecuritydomain(self, domain):
        return self.execute_query(f'!(getToolsBySecurityDomain "{domain}")')
    
    def findmitigationsbydefensetool(self, tool):
        return self.execute_query(f'!(findMitigationsByDefenseTool "{tool}")')
    
    def get_total_threats(self):
        return len(self.getthreatentities())
    
    def get_total_defenses(self):
        return len(self.getdefensetechnologies())
        
    def gethighseveritythreats(self):
        return self.execute_query("!(getHighSeverityThreats)")
    
    def hello(self):
        try:
            result = self.metta.run("!(hello)")
            # Extract the string value directly from the MeTTa Atom result
            if result and len(result) > 0:
                # Convert the Atom to a string and remove quotes if present
                value = str(result[0])
                # Remove any surrounding quotes and parentheses
                value = value.strip('"\'()').strip()
                return value
            return "No result"
        except Exception as e:
            print(f"Error executing hello function: {str(e)}")
            return f"Error: {str(e)}"

# Add a main block to run the code when executed directly
if _name_ == "_main_":
    try:
        kb = MettaKnowledgeBase()
        
        # Call the hello function
        name = kb.hello()
        print(f"\nHello function returns: {name}")
        
        # Get high severity threats
        high_severity_threats = kb.gethighseveritythreats()
        print("\nHigh Severity Threats:")
        for threat in high_severity_threats:
            print(threat)
            
        # Get all mitigations
        mitigations = kb.getallmitigations()
        print("\nAll Mitigations:")
        for item in mitigations:
            print(item)
            
    except Exception as e:
        print(f"Error running script: {str(e)}")
