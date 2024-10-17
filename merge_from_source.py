import os
import shutil
from tqdm import tqdm

def merge_folders(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Get the top-level subfolder name to use for renaming files
    top_folder_name = os.path.basename(source_folder)
    print(f"Top folder name: {top_folder_name}")

    # Walk through all files in the source_folder, ignoring the first subfolder level
    for root, subdirs, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        
        # Skip the first level subfolder (relative path should be one level deep)
        if relative_path == "." or relative_path.count(os.sep) == 1:
            continue  # Skip the first level subfolder
        
        print(f"Working on: {root}")
        
        # Create target subfolder path, maintaining the structure from the second level
        target_subfolder = os.path.join(target_folder, relative_path)
        
        # Make sure the target subfolder exists
        os.makedirs(target_subfolder, exist_ok=True)

        # Copy each file to the target_folder, renaming with the top-level subfolder name
        for file in files:
            source_file_path = os.path.join(root, file)
            new_file_name = f"{top_folder_name}_{file}"
            target_file_path = os.path.join(target_subfolder, new_file_name)

            shutil.copy(source_file_path, target_file_path)
            # print(f"Copied and renamed {source_file_path} to {target_file_path}")

if __name__ == "__main__":
    # Example usage
    source_folder = "C:\\Users\Ben\Desktop\\Uni\\Capstone\\Code\\NonUnity\\Capstone\datasets"  # Folder containing subfolders
    target_folder = "E:\\finalDataset"  # Target folder for merged files

    merge_folders(source_folder, target_folder)