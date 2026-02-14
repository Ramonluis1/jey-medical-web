import openpyxl
import os
import requests
import json
import mimetypes

# Configuration
EXCEL_FILE = 'Productos de Dynarex.xlsx'
IMAGE_DIR = os.path.join('FOTOS', 'Dynarex')
START_ID = 46

# Create image directory
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Load Workbook
wb = openpyxl.load_workbook(EXCEL_FILE)
sheet = wb.active

products = []
current_id = START_ID

print(f"Reading {EXCEL_FILE}...")
print(f"Downloading images to {IMAGE_DIR}...")

# Iterate rows (skip header if present - checking row 1 to see if it's header)
for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
    sku = str(row[0]).strip() if row[0] else None
    name = row[1]
    image_url = row[2]

    if not sku or not name:
        continue

    # Clean Name
    name = str(name).strip()

    # Determine filename to check existence
    # We need to guess extension or assume it from URL to check if it exists
    # If we saved it as SKU.ext, we need to know ext.
    # To be safe, we'll check common extensions or just re-download if we can't be sure.
    # BUT, to be safer and faster, let's try to infer extension from URL string first.
    ext = '.jpg' # Default
    if image_url and isinstance(image_url, str):
        _, ext_from_url = os.path.splitext(image_url)
        if ext_from_url:
            ext = ext_from_url
    
    filename = f"{sku}{ext}"
    file_path = os.path.join(IMAGE_DIR, filename)

    local_image_path = ""
    
    if os.path.exists(file_path):
        # File exists, skip download
        # print(f"Skipping download (exists): {filename}")
        local_image_path = f"FOTOS/Dynarex/{filename}"
    else:
        # File doesn't exist, download
        if image_url and isinstance(image_url, str) and image_url.startswith('http'):
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    # Update extension based on content if needed, but for skipping logic consistency we stick to URL ext if possible?
                    # Actually, if we download, we might find a different extension. 
                    # For this 'resume' feature, it's best to stick to what we likely saved.
                    
                    # Re-eval extension for saving
                    content_type = response.headers.get('content-type')
                    guessed_ext = mimetypes.guess_extension(content_type)
                    if guessed_ext:
                         ext = guessed_ext
                    
                    filename = f"{sku}{ext}"
                    file_path = os.path.join(IMAGE_DIR, filename)

                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    local_image_path = f"FOTOS/Dynarex/{filename}"
                    print(f"Downloaded: {sku} -> {filename}")
                else:
                    print(f"Failed to download image for {sku}: Status {response.status_code}")
                    local_image_path = "FOTOS/logo.png" 
            except Exception as e:
                print(f"Error downloading image for {sku}: {e}")
                local_image_path = "FOTOS/logo.png"
        else:
            # print(f"No valid URL for {sku}")
            local_image_path = "FOTOS/logo.png"

    # Create Product Object
    product = {
        "id": current_id,
        "category": "medical-supply",
        "brand": "Dynarex",
        "title": name,
        "price": 0.00,
        "desc": f"{name} (SKU: {sku}). High quality medical supply from Dynarex.",
        "specs": ["Manufacturer: Dynarex", f"SKU: {sku}", "Professional Grade"],
        "img": local_image_path
    }
    
    products.append(product)
    current_id += 1

# Output JSON to a file for easy reading
output_file = 'dynarex_products.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=4)

print(f"Successfully processed {len(products)} products.")
print(f"Data saved to {output_file}")
