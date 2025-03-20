import os, sys, subprocess
from pathlib import Path

def get_installed_versions():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        installed_packages = {}
        for line in result.stdout.strip().split('\n'):
            if '==' in line:
                name, version = line.split('==', 1)
                installed_packages[name.lower()] = version
        return installed_packages
    except subprocess.SubprocessError as e:
        print(f"Error getting installed packages: {e}")
        return {}

def parse_requirements_file(file_path):
    requirements = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' in line:
                        name, version = line.split('==', 1)
                        requirements[name.lower()] = version
                    else:
                        requirements[line.lower()] = None
        return requirements
    except Exception as e:
        print(f"Error reading requirements file: {e}")
        return {}

def show_difference(requirements, installed):
    diff_found = False
    updates = {}
    
    print("\nComparing requirements.txt with installed packages:")
    print("-" * 60)
    print(f"{'Package':<30} {'Required':<15} {'Installed':<15} {'Status'}")
    print("-" * 60)
    
    for package, req_version in requirements.items():
        if package in installed:
            inst_version = installed[package]
            
            if req_version is None:
                status = "No version specified"
                updates[package] = inst_version
                diff_found = True
            elif req_version != inst_version:
                status = "Different version"
                updates[package] = inst_version
                diff_found = True
            else:
                status = "Up to date"
                
            print(f"{package:<30} {req_version or 'Not specified':<15} {inst_version:<15} {status}")
        else:
            print(f"{package:<30} {req_version or 'Not specified':<15} {'Not installed':<15} {'Missing'}")
    
    return diff_found, updates

def update_requirements_file(file_path, _, updates):
    updated_lines = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                original = line.strip()
                
                if not original or original.startswith('#'):
                    updated_lines.append(original)
                    continue
                
                if '==' in original:
                    name = original.split('==', 1)[0].lower()
                    if name in updates:
                        updated_lines.append(f"{name}=={updates[name]}")
                    else:
                        updated_lines.append(original)
                else:
                    name = original.lower()
                    if name in updates:
                        updated_lines.append(f"{name}=={updates[name]}")
                    else:
                        updated_lines.append(original)
        
        with open(file_path, 'w') as f:
            f.write('\n'.join(updated_lines) + '\n')
        
        print(f"\nRequirements file updated successfully: {file_path}")
        return True
    except Exception as e:
        print(f"Error updating requirements file: {e}")
        return False

def find_requirements_file(directory):
    req_path = os.path.join(directory, "requirements.txt")
    if os.path.isfile(req_path):
        return req_path
    return None

def find_all_requirements_files(directory):
    requirements_files = []
    
    for root, _, files in os.walk(directory):
        if "requirements.txt" in files:
            requirements_files.append(os.path.join(root, "requirements.txt"))
    
    return requirements_files

def select_requirements_file(req_files):
    if len(req_files) == 0:
        return None
    
    if len(req_files) == 1:
        return req_files[0]
    
    print("\nMultiple requirements.txt files found:")
    for i, file_path in enumerate(req_files, 1):
        print(f"{i}. {file_path}")
    
    while True:
        try:
            choice = int(input("\nSelect which requirements.txt to use (enter number): "))
            if 1 <= choice <= len(req_files):
                return req_files[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(req_files)}")
        except ValueError:
            print("Please enter a valid number")

def main():
    path = Path(input("Enter the path to requirements.txt file or directory containing requirements.txt: "))
    
    if os.path.isdir(path):
        requirements_files = find_all_requirements_files(path)
        
        if not requirements_files:
            print(f"No requirements.txt found in directory: {path} (or any subdirectories)")
            return 1
        
        requirements_path = select_requirements_file(requirements_files)
        if not requirements_path:
            print("No requirements.txt file selected. Exiting.")
            return 1
    elif os.path.isfile(path):
        requirements_path = path
    else:
        print(f"Path not found: {path}")
        return 1
    
    print(f"Using requirements file: {requirements_path}")
    
    installed_packages = get_installed_versions()
    if not installed_packages:
        print("Failed to get installed packages. Exiting.")
        return 1
    
    requirements = parse_requirements_file(requirements_path)
    if not requirements:
        print("Failed to parse requirements file or file is empty. Exiting.")
        return 1
    
    diff_found, updates = show_difference(requirements, installed_packages)
    
    if diff_found:
        choice = input("\nDifferences found. Update requirements.txt with installed versions? (y/n): ")
        if choice.lower() == 'y':
            if update_requirements_file(requirements_path, requirements, updates):
                return 0
            else:
                return 1
        else:
            print("Update cancelled.")
    else:
        print("\nNo differences found. All packages are up to date.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())