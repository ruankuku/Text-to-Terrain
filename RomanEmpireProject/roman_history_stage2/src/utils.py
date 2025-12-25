# src/utils.py
import json
import os
from datetime import datetime
from typing import Dict, Any

def save_json(data: Dict[str, Any], file_path: str):
    """Save data as JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to: {file_path}")

def load_json(file_path: str) -> Dict[str, Any]:
    """Load data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}

def create_timestamp() -> str:
    """Create timestamp"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def combine_stage_summaries(stage_data: Dict) -> str:
    """Combine stage summary texts"""
    summaries = []
    for stage_key, stage_info in stage_data.get("stages", {}).items():
        if isinstance(stage_info, dict) and "summary" in stage_info:
            summaries.append(f"=== {stage_info.get('name', stage_key)} ===\n{stage_info['summary']}")
    
    return "\n\n".join(summaries)

def get_period_summaries(stage_data: Dict) -> Dict:
    """Get period summary texts"""
    period_summaries = {}
    stages = stage_data.get("stages", {})
    
    # Map stages to periods
    period_mapping = {
        "stage1": "period1",
        "stage2": "period2", 
        "stage3": "period3",
        "stage4": "period4"
    }
    
    for stage_key, period_key in period_mapping.items():
        if stage_key in stages and "summary" in stages[stage_key]:
            period_summaries[period_key] = stages[stage_key]["summary"]
    
    return period_summaries