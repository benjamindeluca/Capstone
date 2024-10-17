import os

def rename_files_with_prefix(target_folder, prefix):
    # Walk through all subfolders in the target folder
    for root, _, files in os.walk(target_folder):
        for file in files:
            # Construct the full file path
            old_file_path = os.path.join(root, file)
            
            # Create the new file name with the prefix
            new_file_name = f"{prefix}_{file}"
            new_file_path = os.path.join(root, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            # print(f"Renamed: {old_file_path} to {new_file_path}")

# Example usage
if __name__ == "__main__":
    target_folder = "C:\\Users\\Ben\\Desktop\\Uni\\Capstone\\Code\\NonUnity\\Capstone\\datasets\\middayNotRip1"  # Replace with your target folder path
    prefix = "middayNotRip1"  # Replace with your desired prefix
    rename_files_with_prefix(target_folder, prefix)
