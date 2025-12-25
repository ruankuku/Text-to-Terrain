# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
AI_API_KEY = os.getenv('AI_API_KEY', 'your-api-key-here')
AI_BASE_URL = os.getenv('AI_BASE_URL', 'https://api.openai.com/v1')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4')

# Project Constants
HISTORY_START_YEAR = 180
HISTORY_END_YEAR = 337
BOOK_TITLE = "The History of the Decline and Fall of the Roman Empire"

# File Paths
STAGE1_INPUT_PATH = "roman_history_stage2/data/input/final_analysis_20251108_020704.json"
PROCESSED_DATA_PATH = "roman_history_stage2/data/processed/stage2_output.json"

# Four Historical Periods
HISTORICAL_PERIODS = {
    "period1": {"years": "180-235", "name": "Commodus to Severan Dynasty End"},
    "period2": {"years": "235-284", "name": "Third Century Crisis"},
    "period3": {"years": "284-306", "name": "Diocletian Reforms and Tetrarchy"},
    "period4": {"years": "307-337", "name": "Constantine's Rise and Christianization"}
}

# Geographic Regions
GEOGRAPHIC_REGIONS = [
    "Rome", "Italy", "Gaul", "Britain", "Spain", 
    "North Africa", "Egypt", "Syria", "Danube Border", "Rhine Border"
]