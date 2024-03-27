import copy
import subprocess
import os
import json

def download_file(url):
  result = subprocess.run(['wget', '--content-disposition', url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
  if result.returncode == 0:
    print("File downloaded successfully.")
    # Extracting file name from the wget output
    for line in result.stdout.splitlines():
      if line.startswith('Saving to:'):
        # The file path is quoted, we're extracting it
        filepath = line.split('‘')[1].split('’')[0]
        return filepath
  else:
    print(f"Failed to download file. Error: {result.stderr}")

def sha256sum(file):
  result = subprocess.run(['sha256sum', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  if result.returncode == 0:
    return result.stdout.strip().split()[0]

def download_and_convert_model(directory_path, download, metadata):
  file = download_file(download['file'])
  # Switch to a new directory to run model conversion script.
  file = os.path.abspath(file)
  try:
    os.mkdir('build')
    print(f"Directory 'build' was created successfully.")
  except FileExistsError:
    print(f"Directory 'build' already exists, so it was not created again.")
  build = os.path.abspath('build')
  cmd = ['bazel', 'run', 'Apps:LoRAConverter', '--compilation_mode=opt', '--', '--file', file, '--name', metadata['name'], '-o', build]
  original_directory = os.getcwd()
  os.chdir('../tools')
  result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  os.chdir(original_directory)
  updated_metadata = copy.deepcopy(metadata)
  converted = {}
  if result.returncode == 0:
    returned_json = json.loads(result.stdout.strip())
    for key, value in returned_json.items():
      # We current don't handle LoRA / TI mix.
      if key == 't_i_embedding' or key == 'text_embedding_length':
        continue
      updated_metadata[key] = value
      if isinstance(value, str) and value.endswith('.ckpt'):
        sha256 = sha256sum(os.path.join(build, value))
        if sha256 is not None:
          converted[value] = sha256
  else:
    print(f"Failed to convert the model.")
  # Update the files available in converted dictionary.
  for converted_file in converted.keys():
      cmd = ['aws', 's3', 'cp', os.path.join(build, converted_file), 's3://static-libnnc/', '--endpoint-url', 'https://cd96f610b0bb2657da157aca332052ec.r2.cloudflarestorage.com']
      result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
      if result.returncode != 0:
        print(f"fail to upload, stdout: {result.stdout}, stderr: {result.stderr}")
        return metadata # Didn't upload successfully. exit.
  updated_metadata['converted'] = converted
  metadata_path = os.path.join('loras', directory_path, 'metadata.json')
  # Check if metadata.json exists in this directory
  if os.path.exists(metadata_path):
    # Open and load the JSON content
    metadata_string = json.dumps(updated_metadata, indent=2)
    with open(metadata_path, 'w') as json_file:
      json_file.write(metadata_string)
  return updated_metadata

def collect_metadata_from_list(file_path):
  metadata_array = []
  sha256_dict = {}
  with open(file_path, 'r') as file:
    # Read each line in the file
    for line in file:
      directory_path = line.strip()  # Remove newline and whitespace
      print(directory_path)
      metadata_path = os.path.join('loras', directory_path, 'metadata.json')
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
          metadata = download_and_convert_model(directory_path, metadata['download'], metadata)
          if 'converted' in metatdata:
            converted = metadata['converted']
            del metadata['converted']
        if 'download' in metadata:
          del metadata['download']
        if converted is not None:
          file = metadata['file']
          for key, value in converted.items():
            sha256_dict[key] = value
          metadata_array.append(copy.deepcopy(metadata))
  return metadata_array, sha256_dict

# Replace 'models.txt' with the path to your actual file if it's located elsewhere
models_file_path = 'loras.txt'
metadata_array, sha256_dict = collect_metadata_from_list(models_file_path)
with open('loras_sha256.json', 'w') as file:
  sha256_string = json.dumps(sha256_dict, indent=2)
  file.write(sha256_string)

# Convert the array to a JSON string for printing or further processing
with open('loras.json', 'w') as file:
  metadata_json_string = json.dumps(metadata_array, indent=2)
  file.write(metadata_json_string)
