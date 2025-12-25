# src/period_analyzer.py
import json
from typing import Dict
from config.settings import HISTORICAL_PERIODS
from config.themes_mapping import CORE_TERRAIN_THEMES
from src.ai_client import AIClient
from src.utils import save_json

class PeriodAnalyzer:
    def __init__(self):
        self.ai_client = AIClient()
        self.periods = HISTORICAL_PERIODS
        self.core_themes = CORE_TERRAIN_THEMES
    
    def create_periods_prompt(self, period_summaries: Dict, core_themes_description: str) -> str:
        """Create period analysis prompt"""
        periods_text = ""
        for period_id, summary in period_summaries.items():
            periods_text += f"\n{period_id} ({self.periods[period_id]['years']}): {summary}\n"
        
        return f"""
Based on 6 core themes, provide intensity ratings for four historical periods:

Core Themes:
{core_themes_description}

Four Historical Periods:
period1: 180-235 - Commodus to Severan Dynasty End
period2: 235-284 - Third Century Crisis  
period3: 284-306 - Diocletian Reforms and Tetrarchy
period4: 307-337 - Constantine's Rise and Christianization

Period Contents:
{periods_text}

Please provide:
1. Intensity ratings (1-10 scale) for each theme in each period
   - External Threat Intensity, Internal Stability Level: higher rating means more severe problems
   - Economic Development Level, Socio-Cultural Vitality, Governance System Efficiency: higher rating means better conditions  
   - Religious Influence Level: rating indicates influence magnitude

2. Inter-theme relationships (describe how themes influence each other)

Return in JSON format:
{{
  "period_ratings": {{
    "period1": {{
      "external_threat": 6,
      "internal_stability": 5,
      "economic_development": 7,
      "socio_cultural_vitality": 6,
      "religious_influence": 4,
      "governance_efficiency": 5
    }}
  }},
  "theme_relationships": [
    {{
      "theme_a": "external_threat",
      "theme_b": "internal_stability", 
      "relationship": "negative",
      "description": "External threats intensify leading to decreased internal stability"
    }}
  ]
}}
"""
    
    def analyze_periods(self, period_summaries: Dict, core_themes_description: str) -> Dict:
        """Analyze period ratings"""
        prompt = self.create_periods_prompt(period_summaries, core_themes_description)
        
        print("Analyzing period ratings...")
        response = self.ai_client.call_ai(prompt)
        result = self.ai_client.extract_json_from_response(response)
        
        if self._validate_period_data(result):
            save_json(result, "roman_history_stage2/data/processed/period_analysis.json")
            return result
        return {}
    
    def _validate_period_data(self, period_data: Dict) -> bool:
        """Validate period data"""
        if "period_ratings" not in period_data:
            return False
        
        # Check all periods and themes have ratings
        for period_id in self.periods.keys():
            if period_id not in period_data["period_ratings"]:
                print(f"Missing period rating: {period_id}")
                return False
            
            period_ratings = period_data["period_ratings"][period_id]
            for theme_id in self.core_themes.keys():
                if theme_id not in period_ratings:
                    print(f"Period {period_id} missing rating for theme {theme_id}")
                    return False
                
                rating = period_ratings[theme_id]
                if not (1 <= rating <= 10):
                    print(f"Period {period_id} theme {theme_id} rating out of range: {rating}")
                    return False
        
        return True