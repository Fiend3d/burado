import requests
import os
from urllib.parse import unquote

# Configuration
CATEGORY_NAME = "Character_Item_Icons"
API_ENDPOINT = "https://genshin-impact.fandom.com/api.php"
DOWNLOAD_FOLDER = "genshin_icons"
BATCH_SIZE = 50

def get_all_files_in_category():
    """Get all file pages in the category using MediaWiki API"""
    print(f"Fetching list of files in Category:{CATEGORY_NAME}...")
    
    files = []
    continue_token = None
    
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{CATEGORY_NAME}",
            "cmlimit": 500,
            "format": "json",
            "cmnamespace": 6
        }
        
        if continue_token:
            params["cmcontinue"] = continue_token
        
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract file page titles
        for member in data["query"]["categorymembers"]:
            files.append(member["title"])
        
        # Check for continuation
        if "continue" in data:
            continue_token = data["continue"]["cmcontinue"]
            print(f"  Found {len(files)} files so far...")
        else:
            break
    
    print(f"Total files found: {len(files)}")
    return files

def get_image_url(file_title):
    """Get full image URL from file page title"""
    # Remove "File:" prefix and URL decode
    filename = unquote(file_title.replace("File:", ""))
    
    params = {
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    
    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()
    data = response.json()
    
    # Extract image URL from response
    pages = data["query"]["pages"]
    for page_id, page_info in pages.items():
        if "imageinfo" in page_info:
            return page_info["imageinfo"][0]["url"]
    
    return None

def download_image(url, filename):
    """Download and save image"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Clean filename for filesystem
        safe_filename = filename.replace(":", "_").replace("/", "_")
        filepath = os.path.join(DOWNLOAD_FOLDER, safe_filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"  Error downloading {filename}: {e}")
        return False

def main():
    """Main execution"""
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    print(f"Icons will be saved to: {os.path.abspath(DOWNLOAD_FOLDER)}\n")
    
    # Step 1: Get all file titles
    file_titles = get_all_files_in_category()
    
    if not file_titles:
        print("No files found in category!")
        return
    
    # Step 2: Download each image
    print(f"\nStarting download...")
    downloaded = 0
    failed = 0
    
    for i, file_title in enumerate(file_titles, 1):
        if i % BATCH_SIZE == 0 or i == len(file_titles):
            print(f"  Progress: {i}/{len(file_titles)} files processed")
        
        # Get image URL
        image_url = get_image_url(file_title)
        if not image_url:
            print(f"  Failed to get URL for {file_title}")
            failed += 1
            continue
        
        # Extract filename from File: page title
        filename = file_title.replace("File:", "")
        
        # Skip if already downloaded
        safe_filepath = os.path.join(DOWNLOAD_FOLDER, filename.replace(":", "_").replace("/", "_"))
        if os.path.exists(safe_filepath):
            print(f"  Skipping {filename} (already exists)")
            downloaded += 1
            continue
        
        # Download
        if download_image(image_url, filename):
            downloaded += 1
        else:
            failed += 1
    
    # Summary
    print(f"\nDownload complete!")
    print(f"✓ Successfully downloaded: {downloaded}")
    print(f"✗ Failed: {failed}")
    print(f"Total saved to: {os.path.abspath(DOWNLOAD_FOLDER)}")

if __name__ == "__main__":
    main()