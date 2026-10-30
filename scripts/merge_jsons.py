from pathlib import Path
import json

path = Path().absolute().parent

folder_path = path / 'data/interim'
output_path = path / 'data/processed'
merged_data = []
# Automatically find all JSON files in the folder
for file_path in folder_path.glob('*.json'):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)
            if isinstance(data, list):
                merged_data.extend(data)  # Adds items from the list
            else:
                merged_data.append(data)   # Safe fallback if it's a single object
    except json.JSONDecodeError:
        print(f"Skipping broken or empty file: {file_path}")

# Save the combined data into a new file
output_path = output_path / 'merged_output.json'
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)


print(f"Successfully merged files! Total items: {len(merged_data)}")


