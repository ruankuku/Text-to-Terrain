# src/theme_analyzer.py
import os
import json
from typing import Dict, List
from config.settings import THEME_EXTRACTION_PROMPT
from src.ai_client import AIClient
from src.utils import save_json, load_json

class ThemeAnalyzer:
    def __init__(self):
        self.ai_client = AIClient()
    
    def extract_themes_from_summaries(self) -> Dict:
        """
        Extract core themes from stage summaries
        """
        try:
            all_summaries = load_json("roman_history_stage1/data/summaries/all_stages_summary.json")
        except FileNotFoundError:
            print("Stage summary file not found, please run stage summarization first")
            return {}
        
        analysis_text = self._prepare_analysis_text(all_summaries)
        
        print("Extracting core themes...")
        response = self.ai_client.call_ai(THEME_EXTRACTION_PROMPT)
        result = self.ai_client.extract_json_from_response(response)
        
        if self._validate_themes(result):
            save_json(result, "roman_history_stage1/data/summaries/core_themes.json")
            print("✓ Theme extraction completed")
            return result
        else:
            print("✗ Theme extraction validation failed")
            return {}
    
    def _prepare_analysis_text(self, all_summaries: Dict) -> str:
        """Prepare text for theme analysis"""
        analysis_parts = []
        
        for stage_key, stage_data in all_summaries["stages"].items():
            analysis_parts.append(
                f"Stage {stage_key} ({stage_data['years']}): {stage_data['summary']}"
            )
        
        return "\n\n".join(analysis_parts)
    
    def _validate_themes(self, themes_data: Dict) -> bool:
        """Validate theme data"""
        if "themes" not in themes_data:
            return False
        
        themes = themes_data["themes"]
        
        if len(themes) < 8 or len(themes) > 12:
            print(f"Abnormal theme count: {len(themes)}")
            return False
        
        required_fields = ["name", "description", "evolution"]
        for theme in themes:
            for field in required_fields:
                if field not in theme or not theme[field]:
                    print(f"Theme missing field: {field}")
                    return False
        
        return True
    
    def extract_themes_directly(self, sample_text: str = None) -> Dict:
        """
        Extract themes directly from sample text (fallback method)
        """
        if sample_text is None:
            sample_text = self._create_sample_text()
        
        prompt = f"{THEME_EXTRACTION_PROMPT}\n\nRelevant text sample:\n{sample_text}"
        
        response = self.ai_client.call_ai(prompt)
        result = self.ai_client.extract_json_from_response(response)
        
        if self._validate_themes(result):
            save_json(result, "roman_history_stage1/data/summaries/core_themes_direct.json")
            return result
        return {}
    
    def _create_sample_text(self) -> str:
        """Create sample text from stage files"""
        sample_parts = []
        summarizer = StageSummarizer()
        
        for stage_key in summarizer.stage_config.keys():
            content = summarizer.load_stage_content(stage_key)
            if content:
                sample_parts.append(f"=== {stage_key} ===\n{content[:2000]}")
        
        return "\n\n".join(sample_parts)