import os
import shutil

def clear_directory(dest_repo):
    """
    Empties the destination repository by removing all its contents.
    
    :param dest_repo: Path to the destination repository to clear.
    """
    if os.path.exists(dest_repo):
        # Remove all contents of the destination directory
        for root, dirs, files in os.walk(dest_repo):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        print(f"Emptied destination repository: {dest_repo}")
    else:
        os.makedirs(dest_repo)
        print(f"Created destination directory: {dest_repo}")

def copy_repo_with_prefix(src_repo, dest_repo, prefix):
    """
    Copies the files and folders from the source repository to the destination repository,
    while adding a prefix to the filenames to avoid conflicts.
    
    :param src_repo: Path to the source repository.
    :param dest_repo: Path to the destination repository.
    :param prefix: The prefix to add to filenames from the source repository.
    """
    # Walk through the source repository directory
    for root, dirs, files in os.walk(src_repo):
        # Get the relative path from the source repo root
        relative_path = os.path.relpath(root, src_repo)
        
        # Construct the corresponding destination directory
        dest_dir = os.path.join(dest_repo, relative_path)
        
        # Create the directory if it doesn't exist
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy all the files in the current directory
        for file in files:
            src_file_path = os.path.join(root, file)
            dest_file_name = f"{prefix}_{file}"  # Add prefix to the filename
            dest_file_path = os.path.join(dest_dir, dest_file_name)
            
            # Copy the file to the destination
            shutil.copy(src_file_path, dest_file_path)
            # print(f"Copied {src_file_path} to {dest_file_path}")

def merge_repos(repo1, repo2, dest_repo, prefix1="repo1", prefix2="repo2"):
    """
    Merges two repositories into a third, maintaining folder structure and adding prefixes to filenames.
    
    :param repo1: Path to the first repository.
    :param repo2: Path to the second repository.
    :param dest_repo: Path to the destination repository where both repos will be merged.
    :param prefix1: Prefix for files from the first repository.
    :param prefix2: Prefix for files from the second repository.
    """
    # Ensure destination directory exists and is empty
    clear_directory(dest_repo)
    
    # Copy the first repository with prefix
    print(f"Copying files from {repo1} to {dest_repo} with prefix '{prefix1}'")
    copy_repo_with_prefix(repo1, dest_repo, prefix1)
    
    # Copy the second repository with prefix
    print(f"Copying files from {repo2} to {dest_repo} with prefix '{prefix2}'")
    copy_repo_with_prefix(repo2, dest_repo, prefix2)

if __name__ == "__main__":
    # Define paths to the repositories
    repo1_path = r"C:\Users\Ben\Desktop\Uni\Capstone\Code\NonUnity\Capstone\datasets\both_rips"
    repo2_path = r"C:\Users\Ben\Desktop\Uni\Capstone\Code\NonUnity\Capstone\datasets\new_beach_sweep"
    dest_repo_path = r"C:\Users\Ben\Desktop\Uni\Capstone\Code\NonUnity\Capstone\datasets\combined_new_beach_and_rand_rips"
    
    # Merge the repositories
    merge_repos(repo1_path, repo2_path, dest_repo_path, prefix1="rand", prefix2="sweep")
