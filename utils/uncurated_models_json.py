import copy
import subprocess
import os
import json

def download_file(url):
    """Download file using wget and return the file path"""
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
        return None

def sha256sum(file):
    """Calculate SHA256 checksum of a file"""
    result = subprocess.run(['sha256sum', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"Computing SHA256 for: {file}, {result.stdout.strip().split()[0]}")
        return result.stdout.strip().split()[0]
    return None

def download_and_convert_model(directory_path, download, metadata):
    """Download and convert model, similar to original but adapted for uncurated models"""
    file = download_file(download['file'])
    if file is None:
        print(f"Failed to download model for {directory_path}")
        return metadata
    
    autoencoder = None
    if 'autoencoder' in download and download['autoencoder'] != "":
        autoencoder = download_file(download['autoencoder'])
    
    # Switch to a new directory to run model conversion script.
    file = os.path.abspath(file)
    try:
        os.mkdir('build')
        print(f"Directory 'build' was created successfully.")
    except FileExistsError:
        print(f"Directory 'build' already exists, so it was not created again.")
    
    build = os.path.abspath('build')
    cmd = ['bazel', 'run', 'Apps:ModelConverter', '--compilation_mode=opt', '--', 
           '--file', file, '--name', metadata['name'], '-o', build]
    
    if autoencoder is not None:
        autoencoder = os.path.abspath(autoencoder)
        cmd.extend(['--autoencoder-file', autoencoder])
    
    if 'text_encoder' not in metadata:
        cmd.append('--text-encoders')
    
    original_directory = os.getcwd()
    os.chdir('../tools')
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Clean up downloaded files to save space
    try:
        os.remove(file)
    except Exception:
        pass
    if autoencoder is not None:
        try:
            os.remove(autoencoder)
        except Exception:
            pass
    
    updated_metadata = copy.deepcopy(metadata)
    converted = {}
    
    if result.returncode == 0:
        returned_json = json.loads(result.stdout.strip())
        for key, value in returned_json.items():
            updated_metadata[key] = value
            if isinstance(value, str) and value.endswith('.ckpt'):
                sha256 = sha256sum(os.path.join(build, value))
                if sha256 is not None:
                    converted[value] = sha256
        
        converted_file = updated_metadata['file']
        if converted_file.endswith('_f16.ckpt'):
            # Generate 8-bit file.
            if metadata['version'] == "flux1":
                q8p_file = converted_file[:-len('_f16.ckpt')] + '_q8p.ckpt'
            else:
                q8p_file = converted_file[:-len('_f16.ckpt')] + '_q6p_q8p.ckpt'
            cmd = ['bazel', 'run', 'Apps:ModelQuantizer', '--compilation_mode=opt', '--', '-i', os.path.join(build, converted_file),  '--model-version', metadata['version'], '-o', os.path.join(build, q8p_file)]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                sha256 = sha256sum(os.path.join(build, q8p_file))
                if sha256 is not None:
                    converted[q8p_file] = sha256
        
        os.chdir(original_directory)
    else:
        os.chdir(original_directory)
        print(f"Failed to convert the model {result.stdout} {result.stderr}.")
        return metadata
    
    updated_metadata['converted'] = converted
    
    # Fill missing metadata defaults
    if 'upcast_attention' not in updated_metadata:
        updated_metadata['upcast_attention'] = False
    
    # Upload converted files to cloud storage
    for converted_file in converted.keys():
        cmd = ['aws', 's3', 'cp', '--checksum-algorithm=CRC32', 
               os.path.join(build, converted_file), 's3://static-libnnc/', 
               '--endpoint-url', 'https://cd96f610b0bb2657da157aca332052ec.r2.cloudflarestorage.com', 
               '--region', 'auto']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"Failed to upload {converted_file}, stdout: {result.stdout}, stderr: {result.stderr}")
            return metadata  # Didn't upload successfully, exit.
        else:
            try:
                os.remove(os.path.join(build, converted_file))
            except Exception:
                pass
    
    # Update the metadata.json file
    metadata_path = os.path.join('uncurated_models', directory_path, 'metadata.json')
    if os.path.exists(metadata_path):
        metadata_string = json.dumps(updated_metadata, indent=2)
        with open(metadata_path, 'w') as json_file:
            json_file.write(metadata_string)
    
    return updated_metadata

def collect_metadata_from_list(file_path):
    """Collect metadata from uncurated models list"""
    metadata_array = []
    sha256_dict = {}
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return metadata_array, sha256_dict
    
    with open(file_path, 'r') as file:
        # Read each line in the file
        for line in file:
            directory_path = line.strip()  # Remove newline and whitespace
            if not directory_path:  # Skip empty lines
                continue
                
            print(f"Processing: {directory_path}")
            metadata_path = os.path.join('uncurated_models', directory_path, 'metadata.json')
            
            # Check if metadata.json exists in this directory
            if os.path.exists(metadata_path):
                # Open and load the JSON content
                try:
                    with open(metadata_path, 'r') as json_file:
                        metadata = json.load(json_file)
                except json.JSONDecodeError as e:
                    print(f"Error reading {metadata_path}: {e}")
                    continue
                
                converted = None
                if 'converted' in metadata:
                    converted = metadata['converted']
                    del metadata['converted']
                
                # If not already converted, attempt conversion
                if converted is None and 'download' in metadata:
                    metadata = download_and_convert_model(directory_path, metadata['download'], metadata)
                    if 'converted' in metadata:
                        converted = metadata['converted']
                        del metadata['converted']
                
                # Clean up download info from final metadata
                if 'download' in metadata:
                    del metadata['download']
                
                # Always add the model to the array, whether converted or not
                if converted is not None:
                    file = metadata['file']
                    for key, value in converted.items():
                        sha256_dict[key] = value
                    
                    metadata_array.append(copy.deepcopy(metadata))
                    
                    # Handle quantized versions (8-bit, 6-bit, 5-bit)
                    if file.endswith('_f16.ckpt'):
                        # Check for 8-bit version
                        q6p_q8p_file = file[:-len('_f16.ckpt')] + '_q6p_q8p.ckpt'
                        if q6p_q8p_file in converted:
                            metadata['file'] = q6p_q8p_file
                            metadata['name'] = metadata['name'] + ' (8-bit)'
                            # Update stage models if they exist
                            if 'stage_models' in metadata:
                                for i, stage_model in enumerate(metadata['stage_models']):
                                    q6p_q8p_stage = stage_model[:-len('_f16.ckpt')] + '_q6p_q8p.ckpt'
                                    if q6p_q8p_stage in converted:
                                        metadata['stage_models'][i] = q6p_q8p_stage
                                    else:
                                        q8p_stage = stage_model[:-len('_f16.ckpt')] + '_q8p.ckpt'
                                        if q8p_stage in converted:
                                            metadata['stage_models'][i] = q8p_stage
                            # Update other file references
                            for k, v in metadata.items():
                                if v == file:
                                    metadata[k] = q6p_q8p_file
                            metadata_array.append(copy.deepcopy(metadata))
                        else:
                            q8p_file = file[:-len('_f16.ckpt')] + '_q8p.ckpt'
                            if q8p_file in converted:
                                metadata['file'] = q8p_file
                                suffix_8bit = ' (8-bit)'
                                if metadata['version'] == "flux1":
                                    suffix_8bit = ''
                                metadata['name'] = metadata['name'] + suffix_8bit
                                # Update other file references
                                for k, v in metadata.items():
                                    if v == file:
                                        metadata[k] = q8p_file
                                metadata_array.append(copy.deepcopy(metadata))
                    
                    elif file.endswith('_q8p.ckpt'):
                        # Handle additional quantization levels
                        base_name = file[:-len('_q8p.ckpt')]
                        quantization_variants = [
                            ('_q5p.ckpt', ' (5-bit)'),
                            ('_q5p_svd.ckpt', ' (5-bit, SVDQuant)'),
                            ('_q6p.ckpt', ' (6-bit)'),
                            ('_q6p_svd.ckpt', ' (6-bit, SVDQuant)')
                        ]
                        
                        for suffix, name_suffix in quantization_variants:
                            variant_file = base_name + suffix
                            if variant_file in converted:
                                metadata['file'] = variant_file
                                metadata['name'] = metadata['name'] + name_suffix
                                if 'svd' in suffix:
                                    metadata['builtin_lora'] = True
                                # Update other file references
                                for k, v in metadata.items():
                                    if v == file:
                                        metadata[k] = variant_file
                                metadata_array.append(copy.deepcopy(metadata))
                                break  # Only add the first available variant
                else:
                    # No converted files yet, but still add the model with original metadata
                    print(f"No converted files found for {directory_path} (will be added to output)")
                    metadata_array.append(copy.deepcopy(metadata))
            else:
                print(f"Warning: metadata.json not found in {directory_path}")
    
    return metadata_array, sha256_dict

def main():
    """Main function to process uncurated models"""
    # File paths
    models_file_path = 'uncurated_models.txt'
    models_output = 'uncurated_models.json'
    sha256_output = 'uncurated_models_sha256.json'
    
    print("Starting uncurated models processing...")
    print(f"Reading model list from: {models_file_path}")
    
    # Collect metadata
    metadata_array, sha256_dict = collect_metadata_from_list(models_file_path)
    
    # Write SHA256 checksums
    with open(sha256_output, 'w') as file:
        sha256_string = json.dumps(sha256_dict, indent=2)
        file.write(sha256_string)
    print(f"SHA256 checksums written to: {sha256_output}")
    
    # Write models metadata
    with open(models_output, 'w') as file:
        metadata_json_string = json.dumps(metadata_array, indent=2)
        file.write(metadata_json_string)
    print(f"Models metadata written to: {models_output}")
    
    print(f"Processing complete!")
    print(f"Total models processed: {len(metadata_array)}")
    print(f"Total converted files: {len(sha256_dict)}")

if __name__ == "__main__":
    main()