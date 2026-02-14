
import os
import re
import json

# Path setup
PROJECT_DIR = r"c:/Users/ramon/OneDrive/Desktop/Proyecto de pagina para la compañia"
PHOTOS_DIR = os.path.join(PROJECT_DIR, "FOTOS/Dynarex")
PRODUCTS_FILE = os.path.join(PROJECT_DIR, "products.js")

def load_products():
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        # Extract the JSON array part
        match = re.search(r'const products = (\[.*\]);', content, re.DOTALL)
        if match:
            # Need to be careful with trailing commas or comments which might break standard JSON parsing
            # But the previous tool output showed pretty standard JSON structure. 
            # Let's try flexible parsing or `eval` if trusted (safe here as it's local file I'm managing)
            # Actually, standard json.loads might fail if there are comments //
            # Let's try to remove comments
            json_str = match.group(1)
            json_str = re.sub(r'//.*', '', json_str)
            return json.loads(json_str) 
    return []

def get_unused_photos(products):
    used_images = set()
    for p in products:
        if p.get('img'):
            # Normalize path separators
            path = p['img'].replace('\\', '/').split('/')[-1]
            used_images.add(path.lower())

    all_photos = []
    if os.path.exists(PHOTOS_DIR):
        for f in os.listdir(PHOTOS_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                all_photos.append(f)
    
    unused = []
    for photo in all_photos:
        if photo.lower() not in used_images:
            unused.append(photo)
    return unused

def find_product_matches(unused_photos, products):
    matches = []    # (Photo, Product)
    new_products = [] # (Photo, Suggested Title)
    
    product_map = {} # Map SKU -> Product, Map ID -> Product
    # Create lookup maps
    for p in products:
        # SKU is often in specs or desc
        ids = [str(p['id'])]
        sku = None
        if 'specs' in p:
            for s in p['specs']:
                if 'SKU:' in s:
                    sku = s.replace('SKU:', '').strip()
                    ids.append(sku)
        
        # Also try to extract SKU from description if not in specs
        if not sku and 'desc' in p:
             m = re.search(r'SKU:\s*([^)]+)', p['desc'])
             if m:
                 sku = m.group(1).strip()
                 ids.append(sku)

        for i in ids:
            product_map[i] = p

    for photo in unused_photos:
        # Strategy 1: Exact SKU match from filename
        # Remove extension
        name_no_ext = os.path.splitext(photo)[0]
        
        # Check simple SKU (e.g. 12510)
        found = False
        
        # 1. Try whole name as SKU
        if name_no_ext in product_map:
            matches.append((photo, product_map[name_no_ext]))
            found = True
        
        # 2. Try splitting by dash/underscore (e.g. 12510-CH -> 12510)
        if not found:
            parts = re.split(r'[-_]', name_no_ext)
            if len(parts) > 0 and parts[0] in product_map:
                 matches.append((photo, product_map[parts[0]]))
                 found = True
        
        # 3. If z- file, treat as generic product line
        if not found and name_no_ext.startswith('z-'):
            # These are "Category" or "Line" images. 
            # If not used, suggest creating a new "Featured" product for them
            title = name_no_ext[2:].replace('-', ' ')
            new_products.append((photo, title))
            
    return matches, new_products

products = load_products()
unused = get_unused_photos(products)
matches, new_prods = find_product_matches(unused, products)

print(f"Found {len(unused)} unused photos.")
print("--- Matches (Update existing product) ---")
for photo, prod in matches[:20]:
    print(f"Photo: {photo} -> ID: {prod['id']} ({prod['title']})")

print("\n--- No Match (Create new product) ---")
for photo, title in new_prods[:20]:
    print(f"Photo: {photo} -> Title: {title}")
