import json
import re
from pathlib import Path

path = Path().absolute().parent

input_path = path / 'data/processed' / 'merged_output.json'
output_path = path / 'data/processed' / 'marwari_sft.json'

def clean_marwari_data(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cleaned_data = []
    
    # Regex pattern to match web citations like[cite: 1] or[cite: 1] including leading spaces
    citation_pattern = re.compile(r'\s*\[cite:\s*[^\]]+\]')
    
    for item in data:
        # Clean both instruction and output from stray citation tags
        instruction_text = citation_pattern.sub('', item.get("instruction", "")).strip()
        output_text = citation_pattern.sub('', item.get("output", "")).strip()
        
        cleaned_item = {
            "instruction": instruction_text,
            "input": item.get("input", "").strip(),
            "output": output_text
        }
        cleaned_data.append(cleaned_item)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully cleaned {len(cleaned_data)} records saved to {output_path}")

if __name__ == "__main__":
    clean_marwari_data(input_path, output_path)

    