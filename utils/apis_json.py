import copy
import os
import json

def collect_metadata_from_list(file_path):
    """
    Collects metadata from API directories listed in a file.
    
    Args:
        file_path: Path to the file containing list of API directories
        
    Returns:
        list: Array of metadata dictionaries
    """
    metadata_array = []
    
    with open(file_path, 'r') as file:
        # Read each line in the file
        for line in file:
            directory_path = line.strip()  # Remove newline and whitespace
            print(f"Processing API: {directory_path}")
            
            metadata_path = os.path.join('apis', directory_path, 'metadata.json')
            
            # Check if metadata.json exists in this directory
            if os.path.exists(metadata_path):
                # Open and load the JSON content
                with open(metadata_path, 'r') as json_file:
                    metadata = json.load(json_file)
                
                # Add the directory path as an identifier if not already present
                if 'id' not in metadata:
                    metadata['id'] = directory_path
                
                metadata_array.append(copy.deepcopy(metadata))
            else:
                print(f"Warning: No metadata.json found in {metadata_path}")
    
    return metadata_array

def collect_all_apis():
    """
    Collects metadata from all directories in the apis folder.
    
    Returns:
        list: Array of metadata dictionaries
    """
    metadata_array = []
    
    # List all directories in the apis folder
    apis_root = 'apis'
    if not os.path.exists(apis_root):
        print(f"Error: APIs directory {apis_root} not found")
        return metadata_array
    
    api_directories = [d for d in os.listdir(apis_root) 
                     if os.path.isdir(os.path.join(apis_root, d))]
    
    for directory in api_directories:
        print(f"Processing API: {directory}")
        
        metadata_path = os.path.join(apis_root, directory, 'metadata.json')
        
        # Check if metadata.json exists in this directory
        if os.path.exists(metadata_path):
            # Open and load the JSON content
            with open(metadata_path, 'r') as json_file:
                metadata = json.load(json_file)
            
            # Add the directory path as an identifier if not already present
            if 'id' not in metadata:
                metadata['id'] = directory
            
            metadata_array.append(copy.deepcopy(metadata))
        else:
            print(f"Warning: No metadata.json found in {metadata_path}")
    
    return metadata_array

def main():
    # If apis.txt exists, read from it; otherwise, scan all API directories
    apis_file_path = 'apis.txt'
    
    if os.path.exists(apis_file_path):
        print(f"Reading API list from {apis_file_path}")
        metadata_array = collect_metadata_from_list(apis_file_path)
    else:
        print(f"No {apis_file_path} found, scanning all API directories")
        metadata_array = collect_all_apis()
    
    # Convert the array to a JSON string and write to file
    with open('apis.json', 'w') as file:
        metadata_json_string = json.dumps(metadata_array, indent=2)
        file.write(metadata_json_string)
    
    print(f"Successfully generated apis.json with {len(metadata_array)} APIs")

if __name__ == "__main__":
    main()