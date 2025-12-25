# src/utils.py
import json
import os
from datetime import datetime
from typing import Dict, Any

def save_json(data: Dict[str, Any], file_path: str):
    """
    Save data as JSON file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to: {file_path}")

def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load data from JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def create_timestamp() -> str:
    """
    Create timestamp string
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")