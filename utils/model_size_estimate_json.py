from pathlib import Path
import requests
import os
import json

def traverse_and_get_converted_filenames(root_dirs):
    converted_filenames = []  # List to store all "converted" filenames
    for root_dir in root_dirs:
      for dirpath, dirnames, filenames in os.walk(root_dir):
          # Check if metadata.json exists in the current folder
          if 'metadata.json' in filenames:
              metadata_file_path = os.path.join(dirpath, 'metadata.json')
              try:
                  # Open and read the metadata.json file
                  with open(metadata_file_path, 'r') as metadata_file:
                      data = json.load(metadata_file)
                      
                      # Retrieve the "converted" property if it exists
                      if 'file' in data:
                          converted_filenames.append(data['file'])
                      else:
                          print(f"No 'converted' key found in {metadata_file_path}")
              except (json.JSONDecodeError, KeyError) as e:
                  print(f"Error reading {metadata_file_path}: {e}")

    return converted_filenames

def get_file_size(url):
    try:
        # Send a HEAD request to get only headers
        response = requests.head(url, allow_redirects=True)
        if 'Content-Length' in response.headers:
            file_size = int(response.headers['Content-Length'])
            print(f"File size: {file_size / (1024 * 1024):.2f} MB")
            return file_size
        else:
            print("File size information is not available.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

current_parent_path = Path(__file__).resolve().parent.parent
root_directories = [current_parent_path / "models", current_parent_path / "loras", current_parent_path / "embeddings"]  # Replace with the root directory path
converted_files = traverse_and_get_converted_filenames(root_directories)
file_sizes_metadata = []
# Output the collected converted filenames
for file in converted_files:
    print("Converted file", file)
    url = "https://static.libnnc.org/" + file
    file_size = get_file_size(url)
    file_sizes_metadata.append({
        "file": file,
        "size": file_size
    })

# Write the converted data to the output file
with open("file_sizes_metadata.json", 'w') as outfile:
    json.dump(file_sizes_metadata, outfile, indent=4)