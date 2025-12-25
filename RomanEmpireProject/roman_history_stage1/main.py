# main.py
import os
import sys
from src.stage_summarizer import StageSummarizer
from src.theme_analyzer import ThemeAnalyzer
from src.utils import create_timestamp, save_json

def main():
    print("=== Roman Empire Historical Analysis - Stage Summaries and Theme Extraction ===")
    
    os.makedirs("data/summaries", exist_ok=True)
    
    # 1. Stage Summarization
    print("Step 1: Generating Stage Summaries")
    summarizer = StageSummarizer()
    stage_summaries = summarizer.summarize_all_stages()
    
    if not stage_summaries:
        print("Stage summarization failed, exiting")
        return
    
    print(f"Successfully summarized {len(stage_summaries['stages'])} stages")
    
    # 2. Theme Extraction
    print("\nStep 2: Extracting Core Themes")
    theme_analyzer = ThemeAnalyzer()
    core_themes = theme_analyzer.extract_themes_from_summaries()
    
    if core_themes:
        print(f"Successfully extracted {len(core_themes['themes'])} core themes")
    else:
        print("Attempting direct theme extraction...")
        core_themes = theme_analyzer.extract_themes_directly()
    
    # 3. Generate Final Report
    print("\nStep 3: Generating Final Report")
    final_report = {
        "metadata": {
            "project": "Roman Empire Decline Analysis",
            "timestamp": create_timestamp(),
            "period": "180-337 CE",
            "source": "The History of the Decline and Fall of the Roman Empire"
        },
        "stage_summaries": stage_summaries,
        "core_themes": core_themes
    }
    
    save_json(final_report, f"roman_history_stage1/outputs/final_analysis_{create_timestamp()}.json")
    
    print("\n=== Analysis Complete ===")
    print("Output Files:")
    print("- Stage summaries: data/summaries/")
    print("- Core themes: data/summaries/core_themes.json")
    print("- Full report: outputs/final_analysis_*.json")

if __name__ == "__main__":
    main()