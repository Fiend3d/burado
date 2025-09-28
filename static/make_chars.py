import json
from pathlib import Path

def remove_all_extensions(name):
    path_obj = Path(name)
    while path_obj.suffix:
        path_obj = path_obj.with_suffix('')
    return path_obj.name

def save_file_list_to_json(directory_path, output_file):
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory_path}' is not a directory")
        return
    
    files = [remove_all_extensions(f.name) for f in directory.iterdir() if f.is_file()]
    files.sort()
    
    file_list = {
        "directory": "static/chars",
        "chars": files
    }
    
    with open(output_file, "w") as f:
        json.dump(file_list, f, indent=2)
    
    print(f"Saved list of {len(files)} files to {output_file}")

if __name__ == "__main__":
    save_file_list_to_json("./chars", "chars.json")
