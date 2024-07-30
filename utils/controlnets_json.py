import copy
import subprocess
import os
import json

def sha256sum(file):
  result = subprocess.run(['sha256sum', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  if result.returncode == 0:
    return result.stdout.strip().split()[0]

def collect_metadata_from_list(file_path):
  metadata_array = []
  sha256_dict = {}
  with open(file_path, 'r') as file:
    # Read each line in the file
    for line in file:
      directory_path = line.strip()  # Remove newline and whitespace
      print(directory_path)
      metadata_path = os.path.join('controlnets', directory_path, 'metadata.json')
      # Check if metadata.json exists in this directory
      if os.path.exists(metadata_path):
        # Open and load the JSON content
        with open(metadata_path, 'r') as json_file:
          metadata = json.load(json_file)
        converted = None
        if 'converted' in metadata:
          converted = metadata['converted']
          del metadata['converted']
        if converted is None:
          continue
        if converted is not None:
          file = metadata['file']
          for key, value in converted.items():
            sha256_dict[key] = value
          metadata_array.append(copy.deepcopy(metadata))
          # Check if there are 8-bit counterpart.
          if file.endswith('_f16.ckpt'):
            # Append the 8-bit metadata if available.
            q6p_q8p_file = file[:-len('_f16.ckpt')] + '_q6p_q8p.ckpt'
            if q6p_q8p_file in converted:
              metadata['file'] = q6p_q8p_file
              metadata['name'] = metadata['name'] + ' (8-bit)'
              # Update other fields have reference to this file.
              for k, v in metadata.items():
                if v == file:
                  metadata[k] = q6p_q8p_file
              metadata_array.append(copy.deepcopy(metadata))
            else:
              q8p_file = file[:-len('_f16.ckpt')] + '_q8p.ckpt'
              if q8p_file in converted:
                metadata['file'] = q8p_file
                metadata['name'] = metadata['name'] + ' (8-bit)'
                # Update other fields have reference to this file.
                for k, v in metadata.items():
                  if v == file:
                    metadata[k] = q8p_file
                metadata_array.append(copy.deepcopy(metadata))
          elif file.endswith('_q8p.ckpt'):
            q5p_file = file[:-len('_q8p.ckpt')] + '_q5p.ckpt'
            if q5p_file in converted:
              metadata['file'] = q5p_file
              metadata['name'] = metadata['name'] + ' (8-bit)'
              # Update other fields have reference to this file.
              for k, v in metadata.items():
                if v == file:
                  metadata[k] = q5p_file
              metadata_array.append(copy.deepcopy(metadata))
  return metadata_array, sha256_dict

# Replace 'models.txt' with the path to your actual file if it's located elsewhere
models_file_path = 'controlnets.txt'
metadata_array, sha256_dict = collect_metadata_from_list(models_file_path)
with open('controlnets_sha256.json', 'w') as file:
  sha256_string = json.dumps(sha256_dict, indent=2)
  file.write(sha256_string)

# Convert the array to a JSON string for printing or further processing
with open('controlnets.json', 'w') as file:
  metadata_json_string = json.dumps(metadata_array, indent=2)
  file.write(metadata_json_string)
