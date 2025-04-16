# services/report_parser.py
import re
import logging
from typing import Dict, Any, Optional, List, Tuple

logger = logging.getLogger(__name__)

class ReportParser:
    """
    Utility for parsing and extracting information from medical reports.
    """
    
    @staticmethod
    def extract_sections(report_text: str) -> Dict[str, str]:
        """
        Extract common sections from a medical report.
        
        Args:
            report_text: The full text of the medical report
            
        Returns:
            Dictionary mapping section names to their content
        """
        # Common section headers in medical reports
        common_sections = [
            "Patient ID", "Name", "Age", "Gender", "Date of Report",
            "Chief Complaint", "Medical History", "Family History",
            "Personal Medical History", "Medications", "Lab Results",
            "Diagnostic Results", "Physical Examination", "Assessment",
            "Plan", "Recommendations", "Follow-up"
        ]
        
        sections = {}
        
        # Basic pattern match for sections
        for section in common_sections:
            pattern = rf"{section}:?\s*(.*?)(?=\n\n|\n[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*:|$)"
            match = re.search(pattern, report_text, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                sections[section] = content
        
        # If no sections were found, return the entire report
        if not sections:
            logger.warning("No structured sections found in the report")
            sections["Full Report"] = report_text
            
        return sections
    
    @staticmethod
    def extract_patient_info(report_text: str) -> Dict[str, str]:
        """
        Extract basic patient information from a medical report.
        
        Args:
            report_text: The full text of the medical report
            
        Returns:
            Dictionary with patient information
        """
        info = {}
        
        # Try to extract key patient information
        patterns = {
            "patient_id": r"Patient ID:?\s*([A-Za-z0-9]+)",
            "name": r"Name:?\s*([A-Za-z\s]+)",
            "age": r"Age:?\s*(\d+)",
            "gender": r"Gender:?\s*([A-Za-z]+)",
            "date": r"Date(?:\s+of\s+Report)?:?\s*([A-Za-z0-9\-\/\.]+)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, report_text)
            if match:
                info[key] = match.group(1).strip()
        
        return info
    
    @staticmethod
    def extract_symptoms(report_text: str) -> List[str]:
        """
        Attempt to extract symptoms from the report text.
        
        Args:
            report_text: The full text of the medical report
            
        Returns:
            List of identified symptoms
        """
        symptoms = []
        
        # First, try to find the chief complaint section
        sections = ReportParser.extract_sections(report_text)
        
        if "Chief Complaint" in sections:
            complaint_text = sections["Chief Complaint"]
            
            # Common symptom terms
            symptom_terms = [
                "pain", "ache", "discomfort", "fatigue", "weakness", 
                "nausea", "vomiting", "dizziness", "vertigo", "headache",
                "fever", "cough", "shortness of breath", "breathing difficulty",
                "chest pain", "palpitations", "sweating", "anxiety", "depression",
                "numbness", "tingling", "swelling", "insomnia", "rash"
            ]
            
            # Extract symptoms from the complaint
            for term in symptom_terms:
                if re.search(rf"\b{term}\b", complaint_text, re.IGNORECASE):
                    # Try to get the full phrase
                    matches = re.finditer(rf"[^.;,]*\b{term}\b[^.;,]*", complaint_text, re.IGNORECASE)
                    for match in matches:
                        symptom = match.group(0).strip()
                        if symptom and len(symptom) > len(term):
                            symptoms.append(symptom)
                        else:
                            symptoms.append(term)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(symptoms))
    
    @staticmethod
    def summarize_report(report_text: str, max_length: int = 500) -> str:
        """
        Create a concise summary of the medical report.
        
        Args:
            report_text: The full text of the medical report
            max_length: Maximum length of the summary in characters
            
        Returns:
            Summary of the report
        """
        # Extract patient info and key sections
        patient_info = ReportParser.extract_patient_info(report_text)
        sections = ReportParser.extract_sections(report_text)
        
        # Build the summary
        summary_parts = []
        
        # Add patient basics
        patient_str = []
        if "name" in patient_info:
            patient_str.append(f"Patient: {patient_info['name']}")
        if "age" in patient_info and "gender" in patient_info:
            patient_str.append(f"{patient_info['age']}y {patient_info['gender']}")
        
        summary_parts.append(", ".join(patient_str))
        
        # Add chief complaint
        if "Chief Complaint" in sections:
            complaint = sections["Chief Complaint"]
            # Shorten if needed
            if len(complaint) > 200:
                complaint = complaint[:197] + "..."
            summary_parts.append(f"Complaint: {complaint}")
        
        # Add key diagnostic info if available
        for key_section in ["Assessment", "Diagnostic Results", "Lab Results"]:
            if key_section in sections:
                content = sections[key_section]
                if len(content) > 150:
                    content = content[:147] + "..."
                summary_parts.append(f"{key_section}: {content}")
        
        # Join with newlines
        summary = "\n".join(summary_parts)
        
        # Ensure it doesn't exceed max length
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
            
        return summary