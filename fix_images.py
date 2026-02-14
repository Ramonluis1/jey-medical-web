import re
import random
import time
import json
from duckduckgo_search import DDGS

PRODUCTS_FILE = 'products.js'
OUTPUT_FILE = 'products.js'
PLACEHOLDER = 'FOTOS/logo.png'
MAX_RETRIES = 3

print("Reading products.js...")
with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse JS array to Python list
# We assume the file is "const products = [ ... ];"
# We'll use a regex to extract the JSON-like content part between [ and ];
match = re.search(r'const products = \[\s*(.*)\s*\];', content, re.DOTALL)
if not match:
    print("Could not parse products array.")
    exit(1)

array_content = match.group(1)

# Because the JS object keys are not quoted (id: 1, etc.), standard json.loads won't work easily.
# However, the previous scripts generated valid JSON-like structure (quoted keys) for the new items.
# The OLD items might have unquoted keys.
# Strategy: 
# 1. We will NOT fully parse to objects if we can avoid it, to preserve formatting.
# 2. OR we can use the `check_url` approach: iterate line by line or object blocks?
# 3. Best robust way: simple string replacement on the lines that match the placeholder. 
#    We need the SKU/Name for the context.

# Let's iterate through the file line by line to build context.
lines = content.split('\n')
new_lines = []
current_product = {}
in_product = False
buffer_lines = [] # To hold lines of current product until we decide how to write them

updated_count = 0
limit = 50 # Batch limit to avoid getting blocked by DDG in one go
processed = 0

ddgs = DDGS()

def get_image_url(query):
    try:
        results = list(ddgs.images(
            keywords=query,
            region="wt-wt",
            safesearch="off",
            size="medium",
            max_results=1
        ))
        if results:
            return results[0]['image']
    except Exception as e:
        print(f"Error searching '{query}': {e}")
    return None

print("Scanning for missing images...")

# Regex to capture field values (robust for quoted/unquoted keys)
title_re = re.compile(r'["\']?title["\']?:\s*["\'](.+?)["\']')
sku_re = re.compile(r'SKU:\s*([\w\-\.]+)') 

print("Scanning for missing images...")

for i, line in enumerate(lines):
    line_stripped = line.strip()
    
    # Check if this line has the placeholder (handling various quote styles)
    # The view showed: "img": "FOTOS/logo.png"
    if PLACEHOLDER in line and ('img' in line or '"img"' in line):
        
        found_title = None
        found_sku = None
        
        # Look backwards from i for title and sku.
        for j in range(i-1, max(0, i-20), -1):
            prev_line = lines[j]
            if not found_title:
                t_match = title_re.search(prev_line)
                if t_match:
                    found_title = t_match.group(1)
            
            if not found_sku:
                # SKU is usually in desc or specs
                s_match = sku_re.search(prev_line)
                if s_match:
                    found_sku = s_match.group(1)
            
            if '"id":' in prev_line or 'id:' in prev_line: 
                break
        
        if found_title:
            # Construct query
            query = f"Dynarex {found_sku if found_sku else ''} {found_title}"
            print(f"[{processed+1}] Missing image for: {query}")
            
            if processed < limit:
                new_url = get_image_url(query)
                if new_url:
                    print(f"   -> Found: {new_url}")
                    # Replace the line
                    # Preserve indentation robustly
                    indent = line[:len(line) - len(line.lstrip())]
                    
                    # Check if we need a comma
                    comma = ',' if line.strip().endswith(',') else ''
                    
                    # Construct new line (using double quotes to match file style better, though JS allows single)
                    # The file uses "img": "..."
                    # We should stick to that pattern if possible, or just be valid JS.
                    # Using "key": "value" is safest.
                    new_line = f'{indent}"img": "{new_url}"{comma}'
                    
                    lines[i] = new_line # Update the list in place
                    updated_count += 1
                else:
                    print("   -> No image found.")
                
                processed += 1
                time.sleep(random.uniform(1.0, 2.5)) # Polite delay
            else:
                 print("   -> Batch limit reached. Run again for more.")
                 break
        else:
             print(f"Found placeholder but couldn't parse title at line {i+1}")

if updated_count > 0:
    print(f"Updating {updated_count} images in {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Done.")
else:
    print("No updates made.")
