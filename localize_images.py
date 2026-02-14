
import json
import re
import os
import requests
import time
from urllib.parse import urlparse

PRODUCTS_FILE = 'products.js'
DOWNLOAD_DIR = 'FOTOS/Downloaded'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def get_filename_from_url(url):
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    # Sanitize
    basename = re.sub(r'[\\/*?:"<>|]', "", basename)
    if not basename:
        basename = "image.png"
    # Ensure extension
    if not os.path.splitext(basename)[1]:
        basename += '.jpg'
    return basename

def main():
    print("Reading products.js...")
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        content = f.readlines()

    new_content = []
    
    # We need to process line by line to preserve formatting easily
    # Regex to capture fully: img: "HTTP..."
    # Warning: this simple line processing assumes 'img:' key and value are on same line.
    # Based on file view, this seems true.
    
    downloaded_count = 0
    failed_count = 0
    skipped_count = 0
    
    # Track unique URLs to avoid redownloading same image multiple times for different products
    url_map = {} # url -> local_filename

    print(f"Scanning {len(content)} lines...")
    
    for line in content:
        # Check if line has external image
        match = re.search(r'(["\']?img["\']?\s*:\s*)(["\'])(http.+?)(["\'])', line)
        if match:
            prefix = match.group(1)
            quote = match.group(2)
            url = match.group(3)
            # end_quote = match.group(4) # same as quote usually
            
            # Check if we already processed this URL
            if url in url_map:
                local_path = f"{DOWNLOAD_DIR}/{url_map[url]}"
                new_line = line.replace(f"{quote}{url}{quote}", f"'{local_path}'")
                new_content.append(new_line)
                skipped_count += 1
                continue
            
            # Generate local filename
            filename = get_filename_from_url(url)
            # Handle duplicates names
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(DOWNLOAD_DIR, filename)):
                 # If file exists, check if it's the same image (skip check for speed, assume name collision means different image effectively or same)
                 # Better: append hash or counter
                 filename = f"{base}_{counter}{ext}"
                 counter += 1
            
            print(f"Downloading: {filename}")
            try:
                # Download
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    with open(os.path.join(DOWNLOAD_DIR, filename), 'wb') as f:
                        f.write(response.content)
                    
                    local_path = f"{DOWNLOAD_DIR}/{filename}"
                    url_map[url] = filename
                    
                    # Update line
                    # Use ' for new string to be consistent
                    new_line = line.replace(f"{quote}{url}{quote}", f"'{local_path}'")
                    new_content.append(new_line)
                    downloaded_count += 1
                else:
                    print(f"Failed to download (status {response.status_code}): {url}")
                    new_content.append(line) # Keep original
                    failed_count += 1
            except Exception as e:
                print(f"Error downloading {url}: {e}")
                new_content.append(line) # Keep original
                failed_count += 1
            
            # Be nice to servers
            # time.sleep(0.1) 
        else:
            new_content.append(line)

    print("-" * 30)
    print(f"Downloaded: {downloaded_count}")
    print(f"Skipped (Duplicate URL): {skipped_count}")
    print(f"Failed: {failed_count}")
    
    # Backup original
    if downloaded_count > 0:
        os.replace(PRODUCTS_FILE, PRODUCTS_FILE + '.bak_external_fix')
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
        print(f"Updated {PRODUCTS_FILE}")
    else:
        print("No changes made.")

if __name__ == '__main__':
    main()
