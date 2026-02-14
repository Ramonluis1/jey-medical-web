import openpyxl
import os
import json
import mimetypes

# Configuration
EXCEL_FILE = 'Productos de Dynarex.xlsx'
IMAGE_DIR = os.path.join('FOTOS', 'Dynarex')
START_ID = 46

# Load Workbook
wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
sheet = wb.active

products = []
current_id = START_ID

print(f"Reading {EXCEL_FILE}...")

# Iterate rows
for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
    sku = str(row[0]).strip() if row[0] else None
    name = row[1]
    image_url = row[2]

    if not sku or not name:
        continue

    # Clean Name
    name = str(name).strip()

    # Image Handling
    local_image_path = "FOTOS/logo.png" # Default fallback
    
    if image_url and isinstance(image_url, str):
        # Check if we have it locally with common extensions
        # We try to strict match the filename we would have created
        # We guess extension from URL
        ext = '.jpg'
        _, ext_from_url = os.path.splitext(image_url)
        if ext_from_url:
            ext = ext_from_url
            
        filename = f"{sku}{ext}"
        local_path_check = os.path.join(IMAGE_DIR, filename)
        
        if os.path.exists(local_path_check):
            local_image_path = f"FOTOS/Dynarex/{filename}"
        else:
            # Use remote URL
            local_image_path = image_url
            # Check for other extensions just in case? e.g. .png vs .jpg
            # If we missed it, it falls back to remote. That's acceptable.

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

# Output JSON
output_file = 'dynarex_products.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=4)

print(f"Successfully processed {len(products)} products.")
print(f"Data saved to {output_file}")
