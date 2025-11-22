from pathlib import Path
import shutil

def copy_and_rename_png_files(source_folder, destination_folder):
    source = Path(source_folder)
    print(source)
    dest = Path(destination_folder)
    
    # Create destination folder if it doesn't exist
    dest.mkdir(exist_ok=True)
    
    copied_count = 0
    
    for file_path in source.glob("* Item.png"):
        print(file_path)
        if "Aether" in file_path.name or "Lumine" in file_path.name:
            print(f"  Skipping {file_path.name} (Aether/Lumine)")
            continue
        
        new_name = file_path.name.replace(" Item.png", ".png")
        new_name = new_name.replace(" ", "_")
        dest_path = dest / new_name
        
        if dest_path.exists():
            print(f"  Skipping {file_path.name} - {new_name} already exists in destination")
            continue
        
        shutil.copy2(file_path, dest_path)
        print(f"  Copied: {file_path.name} -> {dest_path}")
        copied_count += 1
    
    print(f"\nDone! Copied {copied_count} files to {dest.absolute()}")

if __name__ == "__main__":
    source_folder = "./genshin_icons"
    destination_folder = "./genshin_icons_renamed"
    
    copy_and_rename_png_files(source_folder, destination_folder)