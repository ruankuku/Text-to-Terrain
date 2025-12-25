# src/theme_mapper.py
import json
from typing import Dict, List
from config.themes_mapping import CORE_TERRAIN_THEMES
from src.utils import save_json

class ThemeMapper:
    def __init__(self):
        self.core_themes = CORE_TERRAIN_THEMES
    
    def map_themes_from_stage1(self, stage1_data: Dict) -> Dict:
        """
        Map from 10 themes in stage1 to 6 core themes
        """
        original_themes = stage1_data.get("core_themes", {}).get("themes", [])
        
        mapping_process = {
            "original_theme_count": len(original_themes),
            "mapping_rules": {},
            "mapped_themes": []
        }
        
        # Build mapping process record
        for core_id, core_theme in self.core_themes.items():
            source_names = core_theme["source_themes"]
            mapping_process["mapping_rules"][core_id] = {
                "core_theme_name": core_theme["name"],
                "source_themes": source_names
            }
        
        # Create mapped theme list
        for core_id, core_theme in self.core_themes.items():
            mapped_theme = {
                "id": core_id,
                "name": core_theme["name"],
                "description": core_theme["description"],
                "rating_direction": core_theme["rating_direction"],
                "source_themes": core_theme["source_themes"],
                "combined_description": self._combine_descriptions(original_themes, core_theme["source_themes"])
            }
            mapping_process["mapped_themes"].append(mapped_theme)
        
        # Save mapping process
        save_json(mapping_process, "roman_history_stage2/data/processed/theme_mapping_process.json")
        
        return mapping_process
    
    def _combine_descriptions(self, original_themes: List[Dict], source_theme_names: List[str]) -> str:
        """Combine descriptions from source themes"""
        descriptions = []
        for theme in original_themes:
            if theme["name"] in source_theme_names:
                descriptions.append(theme["description"])
        return " ".join(descriptions)
    
    def get_core_themes_for_prompt(self) -> str:
        """Generate core theme descriptions for prompts"""
        theme_descriptions = []
        for theme_id, theme in self.core_themes.items():
            theme_descriptions.append(f"{theme_id}: {theme['name']} - {theme['description']}")
        return "\n".join(theme_descriptions)