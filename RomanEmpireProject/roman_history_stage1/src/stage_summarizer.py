# src/stage_summarizer.py
import os
import json
from typing import Dict, List
from config.settings import STAGE_SUMMARY_PROMPT
from src.ai_client import AIClient
from src.chunk_processor import ChunkProcessor
from src.utils import save_json

class StageSummarizer:
    def __init__(self):
        self.ai_client = AIClient()
        self.chunk_processor = ChunkProcessor()
        
        # Stage configuration for 180-337 CE
        self.stage_config = {
            "stage1": {
                "file": "stage1_iv-vi.txt",
                "years": "180-235",
                "name": "Commodus to Severan Dynasty End"
            },
            "stage2": {
                "file": "stage2_vi-x.txt", 
                "years": "235-284",
                "name": "Third Century Crisis"
            },
            "stage3": {
                "file": "stage3_xiii-xiv.txt",
                "years": "284-305", 
                "name": "Diocletian Reforms and Tetrarchy"
            },
            "stage4": {
                "file": "stage4_xiv-xvii.txt",
                "years": "305-337",
                "name": "Constantine's Rise and Christianization"
            }
        }
    
    def load_stage_content(self, stage_key: str) -> str:
        """Load stage content from file"""
        file_path = f"roman_history_stage1/data/stages/{self.stage_config[stage_key]['file']}"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return ""
    
    def summarize_large_stage(self, stage_key: str) -> Dict:
        """
        Summarize large text stage using hierarchical strategy
        """
        print(f"Processing stage: {self.stage_config[stage_key]['name']}")
        
        content = self.load_stage_content(stage_key)
        if not content:
            return {}
        
        total_tokens = self.chunk_processor.count_tokens(content)
        print(f"Text length: {len(content)} characters, approx {total_tokens} tokens")
        
        if total_tokens <= 12000:
            print("Text length manageable, summarizing directly...")
            return self.direct_summary(stage_key, content)
        
        print("Text too long, using hierarchical summarization strategy...")
        return self.hierarchical_summary(stage_key, content)
    
    def direct_summary(self, stage_key: str, content: str) -> Dict:
        """Direct summary for manageable text length"""
        prompt = STAGE_SUMMARY_PROMPT.format(
            start_year=self.stage_config[stage_key]['years'].split('-')[0],
            end_year=self.stage_config[stage_key]['years'].split('-')[1],
            content=content[:10000]  # Limit length
        )
        
        response = self.ai_client.call_ai(prompt)
        
        return {
            "stage": stage_key,
            "name": self.stage_config[stage_key]['name'],
            "years": self.stage_config[stage_key]['years'],
            "summary": response,
            "strategy": "direct"
        }
    
    def hierarchical_summary(self, stage_key: str, content: str) -> Dict:
        """
        Hierarchical summarization for very long texts:
        1. Extract key information by chunks
        2. Generate final summary based on chunk summaries
        """
        chunks = self.chunk_processor.split_text(content)
        print(f"Split text into {len(chunks)} chunks")
        
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            
            chunk_prompt = self.chunk_processor.create_chunk_summary_prompt(
                chunk, i+1, len(chunks)
            )
            
            chunk_response = self.ai_client.call_ai(chunk_prompt)
            chunk_summaries.append({
                "chunk_index": i+1,
                "summary": chunk_response
            })
            
            if (i + 1) % 3 == 0:
                self._save_chunk_summaries(stage_key, chunk_summaries)
        
        self._save_chunk_summaries(stage_key, chunk_summaries)
        
        final_summary = self._create_final_summary(stage_key, chunk_summaries)
        
        return {
            "stage": stage_key,
            "name": self.stage_config[stage_key]['name'],
            "years": self.stage_config[stage_key]['years'],
            "summary": final_summary,
            "chunk_count": len(chunks),
            "strategy": "hierarchical"
        }
    
    def _save_chunk_summaries(self, stage_key: str, chunk_summaries: List[Dict]):
        """Save chunk summaries"""
        save_json(
            chunk_summaries, 
            f"roman_history_stage1/data/summaries/{stage_key}_chunk_summaries.json"
        )
    
    def _create_final_summary(self, stage_key: str, chunk_summaries: List[Dict]) -> str:
        """Create final summary from chunk summaries"""
        combined_summaries = "\n\n".join([
            f"Chunk {cs['chunk_index']}:\n{cs['summary']}" 
            for cs in chunk_summaries
        ])
        
        final_prompt = f"""
Based on the chunk analysis of "The History of the Decline and Fall of the Roman Empire" covering {self.stage_config[stage_key]['years']} CE, 
please write a comprehensive summary of this historical stage.

Chunk Analysis Content:
{combined_summaries}

Please write a 300-500 word comprehensive summary highlighting the core characteristics of this stage and its crucial role in the empire's decline process.
"""
        
        return self.ai_client.call_ai(final_prompt)
    
    def summarize_all_stages(self) -> Dict:
        """Summarize all stages"""
        all_summaries = {}
        
        for stage_key in self.stage_config.keys():
            print(f"\n=== Processing {stage_key} ===")
            stage_summary = self.summarize_large_stage(stage_key)
            all_summaries[stage_key] = stage_summary
            
            save_json(
                stage_summary,
                f"data/summaries/{stage_key}_summary.json"
            )
            
            print(f"Completed {stage_key} summary")
        
        combined_result = {
            "metadata": {
                "analysis_type": "stage_summaries",
                "total_stages": len(all_summaries),
                "period_covered": "180-337 CE"
            },
            "stages": all_summaries
        }
        
        save_json(combined_result, "roman_history_stage1/data/summaries/all_stages_summary.json")
        return combined_result