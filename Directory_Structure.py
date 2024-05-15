import os
import fnmatch

def read_gitignore(root_dir):
    ignore_patterns = []
    gitignore_path = os.path.join(root_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
    return ignore_patterns

def should_ignore(path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def print_directory_contents(root_dir, ignore_patterns):
    for root, dirs, files in os.walk(root_dir):
        # Apply .gitignore rules to directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns)]
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_path = os.path.join(root, f)
            if not should_ignore(file_path, ignore_patterns):
                print(f"{subindent}{f}")

def print_file_contents(file_path):
    print(f"\nContents of {file_path}:")
    with open(file_path, 'r') as file:
        print(file.read())

def main():
    project_root = input("Enter the path to your project directory: ")
    ignore_patterns = read_gitignore(project_root)

    print("\nDirectory Structure:")
    print_directory_contents(project_root, ignore_patterns)

    # Optionally, print specific file contents
    docker_files = ['Dockerfile', 'docker-compose.yml']
    for root, dirs, files in os.walk(project_root):
        for file in files:
            file_path = os.path.join(root, file)
            if file in docker_files and not should_ignore(file_path, ignore_patterns):
                print_file_contents(file_path)

if __name__ == "__main__":
    main()
