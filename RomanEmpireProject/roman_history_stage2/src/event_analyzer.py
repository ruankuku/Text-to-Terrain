# src/event_analyzer.py
import json
from typing import Dict, List
from config.settings import HISTORICAL_PERIODS, GEOGRAPHIC_REGIONS
from src.ai_client import AIClient
from src.utils import save_json

class EventAnalyzer:
    def __init__(self):
        self.ai_client = AIClient()
        self.periods = HISTORICAL_PERIODS
        self.regions = GEOGRAPHIC_REGIONS
    
    def create_events_prompt(self, stage_summaries: str, core_themes_description: str) -> str:
        """Create event analysis prompt with strict JSON-only output"""
        return f"""
You are a data extraction model. 
Your task is to analyze the provided historical text and extract key events **strictly in JSON format**.

Do NOT include any commentary, explanation, markdown, or prose outside of the JSON.
Your response MUST be valid JSON and begin immediately with '{{' and end with '}}'.

Analyze "The History of the Decline and Fall of the Roman Empire" covering 180–337 CE, 
and extract 25–35 of the most important historical events across four stages and regions.

Use the following schema and output format exactly:

{{
  "events": [
    {{
      "year": 192,
      "name": "Assassination of Commodus",
      "primary_themes": ["internal_stability", "governance_efficiency"],
      "base_impact": -8,
      "geographic_scope": {{
        "scope_score": 7,
        "regions": ["Rome", "Italy"],
        "centrality": 0.95
      }},
      "temporal_scope": {{
        "duration_score": 6,
        "immediacy": 0.9,
        "persistence": 0.7
      }},
      "comprehensive_impact": -6.8,
      "description": "Gibbon's description of the emperor's assassination and its effects on Roman governance.",
      "cascade_effects": [
        {{
          "affected_theme": "economic_development",
          "impact_delay": 2,
          "impact_strength": -5
        }}
      ]
    }}
  ]
}}

Field meanings:
- `year`: exact or approximate year of event (integer)
- `primary_themes`: 1–2 theme IDs from the core list
- `base_impact`: integer (-10 to +10)
- `geographic_scope`: includes scope_score (1–10), regions (list), and centrality (0–1)
- `temporal_scope`: includes duration_score (1–10), immediacy (0–1), persistence (0–1)
- `comprehensive_impact`: computed as Base Impact × (Geographic Scope Score / 10) × (Duration Score / 10)
- `cascade_effects`: list of secondary impacts on other themes

Core Themes:
{core_themes_description}

Historical Periods:
{self._get_periods_description()}

Available Geographic Regions:
{', '.join(self.regions)}

Text to analyze:
{stage_summaries}

Remember: respond **only with valid JSON**, no text or comments outside JSON.
        """
    
    def _get_periods_description(self) -> str:
        """Get periods description"""
        return "\n".join([f"{pid}: {p['years']} - {p['name']}" for pid, p in self.periods.items()])
    
    def extract_events(self, stage_summaries: str, core_themes_description: str) -> Dict:
        """Extract historical events"""
        prompt = self.create_events_prompt(stage_summaries, core_themes_description)
        
        print("Analyzing historical events...")
        response = self.ai_client.call_ai(prompt)

        # print raw output for debugging if needed
        if isinstance(response, str):
            print("\n--- RAW MODEL RESPONSE ---\n", response[:500], "...\n")

        result = self.ai_client.extract_json_from_response(response)
        
        if self._validate_events(result):
            # Calculate comprehensive impact
            enriched_events = self._calculate_comprehensive_impact(result)
            save_json(enriched_events, "roman_history_stage2/data/processed/historical_events.json")
            return enriched_events
        else:
            print("✗ Event analysis failed — no valid JSON or missing fields.")
        return {}
    
    def _validate_events(self, events_data: Dict) -> bool:
        """Validate event data"""
        if not isinstance(events_data, dict) or "events" not in events_data:
            print("Invalid or empty JSON structure.")
            return False
        
        events = events_data["events"]
        if len(events) < 20 or len(events) > 40:
            print(f"Abnormal event count: {len(events)}")
            return False
        
        required_fields = ["year", "name", "primary_themes", "base_impact", 
                          "geographic_scope", "temporal_scope", "description"]
        
        for event in events:
            for field in required_fields:
                if field not in event:
                    print(f"Event missing field: {field}")
                    return False
        
        return True
    
    def _calculate_comprehensive_impact(self, events_data: Dict) -> Dict:
        """Calculate comprehensive impact values"""
        for event in events_data["events"]:
            geo_score = event["geographic_scope"]["scope_score"]
            duration_score = event["temporal_scope"]["duration_score"]
            base_impact = event["base_impact"]
            
            # Calculate comprehensive impact
            comprehensive_impact = base_impact * (geo_score / 10) * (duration_score / 10)
            event["comprehensive_impact"] = round(comprehensive_impact, 2)
        
        return events_data
