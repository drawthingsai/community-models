import copy
import subprocess
import os
import json

def collect_metadata_from_list(file_path):
  metadata_array = []
  with open(file_path, 'r') as file:
    # Read each line in the file
    for line in file:
      directory_path = line.strip()  # Remove newline and whitespace
      print(directory_path)
      metadata_path = os.path.join('configs', directory_path, 'metadata.json')
      # Check if metadata.json exists in this directory
      if os.path.exists(metadata_path):
        # Open and load the JSON content
        with open(metadata_path, 'r') as json_file:
          metadata = json.load(json_file)
          metadata_array.append(copy.deepcopy(metadata))
  return metadata_array

# Replace 'models.txt' with the path to your actual file if it's located elsewhere
configs_file_path = 'configs.txt'
metadata_array = collect_metadata_from_list(configs_file_path)
# Convert the array to a JSON string for printing or further processing
with open('configs.json', 'w') as file:
  metadata_json_string = json.dumps(metadata_array, indent=2)
  file.write(metadata_json_string)
