import os, sys, subprocess
from pathlib import Path

def get_installed_versions():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                                capture_output=True, text=True, check=True)
        return {name.lower(): ver.strip() for line in result.stdout.splitlines() if "==" in line
                for name, ver in [line.split("==", 1)]}
    except subprocess.SubprocessError as e:
        print(f"Error getting installed packages: {e}")
        return {}

def parse_requirements_file(file_path):
    try:
        with open(file_path) as f:
            return {
                (parts[0].lower() if "==" in l else l.lower()):
                (parts[1] if "==" in l else None)
                for orig in f if (l := orig.strip()) and not l.startswith("#")
                for parts in ([list(map(str.strip, l.split("==", 1)))] if "==" in l else [[l]])
            }
    except Exception as e:
        print(f"Error reading requirements file: {e}")
        return {}

def show_difference(reqs, installed):
    diff, updates = False, {}
    print("\nComparing requirements.txt with installed packages:")
    print("-" * 84)
    print(f"{'Package':<40} {'Required':<15} {'Installed':<15} {'Status'}")
    print("-" * 84)
    for pkg, req_ver in reqs.items():
        if pkg in installed:
            inst_ver = installed[pkg]
            if req_ver is None:
                status, updates[pkg] = "No version specified", inst_ver
                diff = True
            elif req_ver != inst_ver:
                status, updates[pkg] = "Different version", inst_ver
                diff = True
            else:
                status = "Up to date"
            print(f"{pkg:<40} {(req_ver or 'Not specified'):<15} {inst_ver:<15} {status}")
        else:
            print(f"{pkg:<40} {(req_ver or 'Not specified'):<15} {'Not installed':<15} {'Missing'}")
    return diff, updates

def update_requirements_file(file_path, _, updates):
    try:
        with open(file_path) as f:
            lines = f.read().splitlines()
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                new_lines.append(line)
                continue
            if "==" in stripped:
                parts = [p.strip() for p in stripped.split("==", 1)]
                name = parts[0].lower()
                new_lines.append(f"{parts[0]}=={updates.get(name, parts[1])}" if name in updates else line)
            else:
                name = stripped.lower()
                new_lines.append(f"{line}=={updates[name]}" if name in updates else line)
        with open(file_path, "w") as f:
            f.write("\n".join(new_lines) + "\n")
        print(f"\nRequirements file updated successfully: {file_path}")
        return True
    except Exception as e:
        print(f"Error updating requirements file: {e}")
        return False

def find_requirements_file(directory):
    req = os.path.join(directory, "requirements.txt")
    return req if os.path.isfile(req) else None

def find_all_requirements_files(directory):
    return [os.path.join(root, "requirements.txt") for root, _, files in os.walk(directory) if "requirements.txt" in files]

def select_requirements_file(files):
    if not files:
        return None
    if len(files) == 1:
        return files[0]
    print("\nMultiple requirements.txt files found:")
    for i, path in enumerate(files, 1):
        print(f"{i}. {path}")
    while True:
        try:
            choice = int(input("\nSelect which requirements.txt to use (enter number): "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            print(f"Please enter a number between 1 and {len(files)}")
        except ValueError:
            print("Please enter a valid number")

def main():
    path = Path(input("Enter the path to requirements.txt file or directory containing requirements.txt: "))
    if path.is_dir():
        files = find_all_requirements_files(path)
        if not files:
            print(f"No requirements.txt found in directory: {path} (or any subdirectories)")
            return 1
        req_file = select_requirements_file(files)
        if not req_file:
            print("No requirements.txt file selected. Exiting.")
            return 1
    elif path.is_file():
        req_file = path
    else:
        print(f"Path not found: {path}")
        return 1
    print(f"Using requirements file: {req_file}")
    installed = get_installed_versions()
    if not installed:
        print("Failed to get installed packages. Exiting.")
        return 1
    reqs = parse_requirements_file(req_file)
    if not reqs:
        print("Failed to parse requirements file or file is empty. Exiting.")
        return 1
    diff, updates = show_difference(reqs, installed)
    if diff and input("\nDifferences found. Update requirements.txt with installed versions? (y/n): ").lower() == 'y':
        return 0 if update_requirements_file(req_file, reqs, updates) else 1
    if diff:
        print("Update cancelled.")
    else:
        print("\nNo differences found. All packages are up to date.")
    return 0

if __name__ == "__main__":
    sys.exit(main())