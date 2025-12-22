"""
Treatment knowledge base for plant disease management.
"""
import json
import os
from typing import Dict, Optional, List


class TreatmentKnowledgeBase:
    """
    Knowledge base for plant disease treatment recommendations.
    Loads treatment data from JSON file.
    """
    
    def __init__(self, treatments_file: Optional[str] = None):
        """
        Initialize treatment knowledge base.
        
        Args:
            treatments_file: Path to treatments JSON file
        """
        if treatments_file is None:
            # Default path relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            treatments_file = os.path.join(base_dir, "data", "treatments.json")
        
        self.treatments_file = treatments_file
        self.treatments = self._load_treatments()
    
    def _load_treatments(self) -> Dict:
        """
        Load treatment data from JSON file.
        
        Returns:
            Dictionary of treatment data
        """
        if not os.path.exists(self.treatments_file):
            print(f"Warning: Treatments file not found at {self.treatments_file}")
            return self._get_default_treatments()
        
        try:
            with open(self.treatments_file, 'r') as f:
                data = json.load(f)
            print(f"Successfully loaded {len(data.get('treatments', []))} treatments")
            return data
        except Exception as e:
            print(f"Error loading treatments file: {e}")
            return self._get_default_treatments()
    
    def _get_default_treatments(self) -> Dict:
        """
        Get default treatment data if file is not found.
        
        Returns:
            Default treatment dictionary
        """
        return {
            "treatments": [
                {
                    "disease_name": "Unknown Disease",
                    "crop": "Unknown",
                    "summary": "Treatment information not available",
                    "symptoms": ["Symptoms not available"],
                    "cultural_controls": ["Consult local agricultural extension"],
                    "biological_controls": ["Consult plant disease specialist"],
                    "chemical_controls": ["Consult agricultural expert"],
                    "prevention": ["Practice good crop hygiene"],
                    "severity": "Unknown"
                }
            ]
        }
    
    def get_treatment(self, disease_name: str) -> Optional[Dict]:
        """
        Get treatment recommendations for a specific disease.
        
        Args:
            disease_name: Name of the disease (formatted or raw)
            
        Returns:
            Treatment dictionary or None if not found
        """
        # Normalize disease name for matching
        normalized_query = self._normalize_disease_name(disease_name)
        
        treatments = self.treatments.get("treatments", [])
        
        for treatment in treatments:
            treatment_name = self._normalize_disease_name(treatment.get("disease_name", ""))
            if normalized_query == treatment_name:
                return treatment
        
        # Try partial match
        for treatment in treatments:
            treatment_name = self._normalize_disease_name(treatment.get("disease_name", ""))
            if normalized_query in treatment_name or treatment_name in normalized_query:
                return treatment
        
        # Return default treatment if not found
        return {
            "disease_name": disease_name,
            "crop": "Unknown",
            "summary": f"Specific treatment information for {disease_name} is not available in our database.",
            "symptoms": ["Please consult local agricultural extension for specific symptoms"],
            "cultural_controls": [
                "Remove and destroy infected plant parts",
                "Improve air circulation around plants",
                "Avoid overhead watering",
                "Practice crop rotation"
            ],
            "biological_controls": [
                "Consult with a plant disease specialist for biological control options"
            ],
            "chemical_controls": [
                "Consult with agricultural extension for appropriate fungicides",
                "Always follow label instructions"
            ],
            "prevention": [
                "Use disease-resistant varieties when available",
                "Maintain proper plant spacing",
                "Practice good sanitation",
                "Monitor plants regularly"
            ],
            "severity": "Unknown"
        }
    
    def _normalize_disease_name(self, name: str) -> str:
        """
        Normalize disease name for matching.
        
        Args:
            name: Disease name to normalize
            
        Returns:
            Normalized disease name
        """
        return name.lower().replace('_', ' ').replace('-', ' ').strip()
    
    def get_all_diseases(self) -> List[Dict]:
        """
        Get all diseases in the knowledge base.
        
        Returns:
            List of disease dictionaries
        """
        return self.treatments.get("treatments", [])
    
    def get_diseases_by_crop(self, crop: str) -> List[Dict]:
        """
        Get all diseases for a specific crop.
        
        Args:
            crop: Crop name
            
        Returns:
            List of disease dictionaries for the crop
        """
        crop_normalized = crop.lower().strip()
        treatments = self.treatments.get("treatments", [])
        
        return [
            t for t in treatments
            if crop_normalized in t.get("crop", "").lower()
        ]
