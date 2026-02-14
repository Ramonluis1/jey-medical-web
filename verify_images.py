import re
import os
import json

# Define the base directory (assuming script runs in project root)
BASE_DIR = os.getcwd()

def check_images():
    products_file = os.path.join(BASE_DIR, 'products.js')
    
    with open(products_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the array content using regex as it's a JS file, not pure JSON
    # Looking for objects { ... img: 'path' ... }
    # This regex is a bit simplistic but should work for the uniform format seen
    
    missing_images = []
    
    # regex to find img properties: img:\s*['"](.*?)['"]
    pattern = re.compile(r"['\"]?img['\"]?:\s*['\"](.*?)['\"]")
    matches = pattern.findall(content)
    
    print(f"Found {len(matches)} image references.")
    
    for img_path in matches:
        # Full absolute path
        # Fix potential path separator issues
        normalized_path = img_path.replace('/', os.sep).replace('\\', os.sep)
        if img_path.startswith('http') or img_path.startswith('https'):
            continue
            
        full_path = os.path.join(BASE_DIR, normalized_path)
        
        if not os.path.exists(full_path):
            missing_images.append(img_path)
            # print(f"Missing: {img_path}")
        else:
            # Check if it looks like a placeholder even if it exists
            filename = os.path.basename(img_path)
            if filename.startswith('z-') or 'placeholder' in filename.lower():
                 missing_images.append(img_path)
                 # print(f"Placeholder/Suspicious: {img_path}")

    # Remove duplicates
    unique_missing = list(set(missing_images))
    print(f"Total specific unique missing/suspicious images: {len(unique_missing)}")
    
    with open('missing_images.txt', 'w') as f:
        for m in unique_missing:
            f.write(m + '\n')
    print(f"COUNT_MISSING: {len(unique_missing)}")

if __name__ == "__main__":
    check_images()
