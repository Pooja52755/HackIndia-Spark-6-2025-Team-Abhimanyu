import os
import re

class MettaKnowledgeBase:
    def __init__(self):
        self.kb_data = {}
        self._load_knowledge()

    def _load_knowledge(self):
        """Load knowledge base entries from cybersec_knowledge.metta without using hyperon"""
        try:
            # Create a simplified knowledge structure for demo purposes
            self.kb_data = {
                "ThreatEntity": ["Malware", "Ransomware", "Phishing", "DDoS", "SQL Injection", "XSS"],
                "DefenseTechnology": ["Firewall", "Antivirus", "IDS/IPS", "Encryption", "WAF", "MFA"],
                "AttackVector": ["Email", "Web", "Network", "Physical", "Social Engineering"],
                "DataTheft": ["PII Theft", "Credential Theft", "IP Theft"],
                "NetworkSecurity": ["Firewall", "VPN", "NGFW", "NAC"],
                "EndpointSecurity": ["Antivirus", "EDR", "Host Firewall", "DLP"],
                "SecurityMonitoring": ["SIEM", "IDS", "NDR", "UBA"],
                "MitigatedBy": {
                    "Malware": ["Antivirus", "EDR", "Patching"],
                    "Ransomware": ["Backup Solutions", "EDR", "User Training"],
                    "Phishing": ["Email Security", "User Training", "MFA"],
                    "SQL Injection": ["WAF", "Secure Coding", "Database Firewalls"],
                    "DDoS": ["Anti-DDoS Services", "Network Filtering", "CDN"]
                },
                "DetectedBy": {
                    "Malware": ["Antivirus", "EDR", "SIEM"],
                    "Phishing": ["Email Security", "User Reports", "UEBA"],
                    "DDoS": ["NDR", "NetFlow Analysis", "Traffic Monitoring"],
                    "AnomalousActivity": ["SIEM"],
                    "EndpointThreat": ["EDR"],
                    "DataLeakage": ["DLP"],
                    "NetworkAttack": ["IDS"]
                }
            }
            print("Loaded mock knowledge base successfully")
        except Exception as e:
            print(f"Error loading mock knowledge base: {str(e)}")

    def execute_query(self, query_template, *args):
        """Mock query execution that returns data from our simplified structure"""
        # We'll just parse the query name from the template
        query_match = re.search(r"!\((get[A-Za-z]+|find[A-Za-z]+)", query_template)
        if not query_match:
            return ["Query not recognized"]
        
        query_name = query_match.group(1)
        try:
            # Map query functions to data retrieval
            return getattr(self, query_name.lower())(*args)
        except AttributeError:
            return [f"Function {query_name} not implemented in mock"]
        except Exception as e:
            return [f"Query execution failed: {str(e)}"]

    def getthreatentities(self):
        return self.kb_data.get("ThreatEntity", [])
    
    def getdefensetechnologies(self):
        return self.kb_data.get("DefenseTechnology", [])
    
    def getattackvectors(self):
        return self.kb_data.get("AttackVector", [])
    
    def getdatatheftthreats(self):
        return self.kb_data.get("DataTheft", [])
    
    def getnetworksecuritytools(self):
        return self.kb_data.get("NetworkSecurity", [])
    
    def getendpointsecuritytools(self):
        return self.kb_data.get("EndpointSecurity", [])
    
    def getsecuritymonitoringtools(self):
        return self.kb_data.get("SecurityMonitoring", [])
    
    def getthreatmitigations(self, threat):
        return self.kb_data.get("MitigatedBy", {}).get(threat, [])
    
    def getallmitigations(self):
        result = []
        for threat, mitigations in self.kb_data.get("MitigatedBy", {}).items():
            for mitigation in mitigations:
                result.append(f"{threat}, {mitigation}")
        return result
    
    def getdefensesforattackvector(self):
        result = []
        for attack in self.kb_data.get("AttackVector", []):
            mitigations = self.kb_data.get("MitigatedBy", {}).get(attack, [])
            for mitigation in mitigations:
                result.append(f"{attack}, {mitigation}")
        return result
    
    def getthreatdetectiontools(self):
        result = []
        for threat, tools in self.kb_data.get("DetectedBy", {}).items():
            for tool in tools:
                result.append(f"{threat}, {tool}")
        return result
    
    def gettoolsbysecuritydomain(self, domain):
        return self.kb_data.get(domain, [])
    
    def findmitigationsbydefensetool(self, tool):
        result = []
        for threat, mitigations in self.kb_data.get("MitigatedBy", {}).items():
            if tool in mitigations:
                result.append(threat)
        return result
    
    def get_total_threats(self):
        return len(self.getthreatentities())
    
    def get_total_defenses(self):
        return len(self.getdefensetechnologies())