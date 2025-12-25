# main.py
import os
import sys
from src.theme_mapper import ThemeMapper
from src.event_analyzer import EventAnalyzer
from src.period_analyzer import PeriodAnalyzer
from src.utils import load_json, save_json, create_timestamp, combine_stage_summaries, get_period_summaries
from config.settings import STAGE1_INPUT_PATH

def main():
    print("=== Roman Empire Historical Terrain Mapping Project - Stage 2 ===")
    print("Event Analysis and Period Rating")
    
    # Create necessary directories
    os.makedirs("roman_history_stage2/data/processed", exist_ok=True)
    os.makedirs("roman_history_stage2/outputs", exist_ok=True)
    
    # 1. Load stage1 output
    print("1. Loading stage1 output data...")
    stage1_data = load_json(STAGE1_INPUT_PATH)
    if not stage1_data:
        print("Error: Cannot load stage1 output file")
        return
    
    print(f"✓ Successfully loaded stage1 data, containing {len(stage1_data.get('core_themes', {}).get('themes', []))} original themes")
    
    # 2. Theme mapping
    print("\n2. Performing theme mapping...")
    theme_mapper = ThemeMapper()
    mapping_result = theme_mapper.map_themes_from_stage1(stage1_data)
    print(f"✓ Completed theme mapping: 10 themes → 6 core themes")
    
    # Get core theme descriptions for prompts
    core_themes_description = theme_mapper.get_core_themes_for_prompt()
    
    # 3. Event analysis
    print("\n3. Performing event analysis...")
    event_analyzer = EventAnalyzer()
    
    # Combine all stage summaries as input for event analysis
    combined_summaries = combine_stage_summaries(stage1_data.get("stage_summaries", {}))
    events_data = event_analyzer.extract_events(combined_summaries, core_themes_description)
    
    if events_data:
        print(f"✓ Successfully extracted {len(events_data.get('events', []))} historical events")
    else:
        print("✗ Event analysis failed")
        return
    
    # 4. Period analysis
    print("\n4. Performing period analysis...")
    period_analyzer = PeriodAnalyzer()
    
    # Get period summaries as input for period analysis
    period_summaries = get_period_summaries(stage1_data.get("stage_summaries", {}))
    period_data = period_analyzer.analyze_periods(period_summaries, core_themes_description)
    
    if period_data:
        print("✓ Successfully completed period rating analysis")
    else:
        print("✗ Period analysis failed")
        return
    
    # 5. Generate final report
    print("\n5. Generating final report...")
    final_report = {
        "metadata": {
            "project": "Roman Empire Terrain Mapping - Stage 2",
            "timestamp": create_timestamp(),
            "period": "180-337 CE",
            "source": "The History of the Decline and Fall of the Roman Empire",
            "stage1_input": STAGE1_INPUT_PATH
        },
        "theme_mapping": mapping_result,
        "historical_events": events_data,
        "period_analysis": period_data
    }
    
    save_json(final_report, f"roman_history_stage2/outputs/stage2_final_analysis_{create_timestamp()}.json")
    
    print("\n=== Stage 2 Completed ===")
    print("Output Files:")
    print("- Theme mapping process: data/processed/theme_mapping_process.json")
    print("- Historical events: data/processed/historical_events.json") 
    print("- Period analysis: data/processed/period_analysis.json")
    print("- Complete report: outputs/stage2_final_analysis_*.json")

if __name__ == "__main__":
    main()