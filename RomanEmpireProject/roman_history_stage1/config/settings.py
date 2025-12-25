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
PROCESSED_DATA_PATH = "data/processed/stage1_output.json"

# Prompt Templates
STAGE_SUMMARY_PROMPT = """
You are analyzing content from "The History of the Decline and Fall of the Roman Empire" covering the period {start_year}-{end_year} CE.

Based on the provided text content, write a comprehensive summary of this historical stage, focusing on the main political, military, and imperial conditions.

**Requirements:**
1. Highlight the core characteristics of this stage (e.g., "collapse of central authority", "militarization of imperial power", "reforms and stabilization")
2. Cover political systems, military situation, economic conditions, and social changes
3. Explain this stage's crucial role in the empire's decline process
4. Keep the summary between 300-500 words

Text Content:
{content}

Please write the summary in a clear, academic style:
"""

THEME_EXTRACTION_PROMPT = """
Based on "The History of the Decline and Fall of the Roman Empire" covering 180-337 CE, extract 10 core themes or factors that Gibbon emphasizes as causes for the empire's decline.

**Requirements:** For each theme provide:
1. Theme name
2. A description reflecting Gibbon's perspective (ideally quoting or closely paraphrasing his text)
3. A brief explanation of how this theme evolved during 180-337 CE (e.g., gradually intensified, intermittent outbreaks, peaked in certain periods)

Return results in JSON format:
{{
  "themes": [
    {{
      "name": "Theme Name",
      "description": "Theme Description", 
      "evolution": "Evolution Explanation"
    }}
  ]
}}
"""