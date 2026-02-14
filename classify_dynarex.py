import re
import json

file_path = r'c:\Users\ramon\OneDrive\Desktop\Proyecto de pagina para la compañia\products.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the array content. It starts with "const products = [" and ends with "];"
# We'll use a regex to capture the list content
match = re.search(r'const products = \[\s*(.*)\s*\];', content, re.DOTALL)
if not match:
    print("Could not find products array")
    exit(1)

items_str = match.group(1)

# To parse this as JSON, we need to quote the keys and single quotes to double quotes
# However, the file might use single quotes for strings.
# Because it's a JS file, not JSON, we have to be careful.
# A safer way might be to iterate line by line or use a more robust parser.
# Given the simple structure seen in view_file:
# {
#    id: 1,
#    ...
# },
# We can regex replace keys to be quoted.

def fix_json(js_obj_str):
    # Remove comments
    js_obj_str = re.sub(r'//.*', '', js_obj_str)
    # Quote keys
    js_obj_str = re.sub(r'(\w+):', r'"\1":', js_obj_str)
    # Replace single quotes with double quotes for string values
    # careful not to break apostrophes inside words. 
    # The file seems to use single quotes for values: 'diagnostic'
    # strict JSON requires double quotes.
    
    # Let's simple string replace widely used keys
    # But wait, specs: [...] is an array.
    return js_obj_str

# Since parsing fully via partial regex is risky, let's just loop through the file lines
# and modify the "category" line if we detect it's a Dynarex product.

new_lines = []
lines = content.split('\n')
current_product = {}
in_product = False
product_buffer = []

def get_category_for_dynarex(title, desc):
    t = title.lower()
    d = desc.lower()
    
    # Priority Categories
    if "resp-o2" in t or "laryngeal" in t or "suction" in t or "oxygen" in t or "airway" in t or "lma" in t:
        return "Resp-O2"
    
    if "labchoice" in t or "microscope" in t or "slide" in t:
        return "LabChoice"
        
    if "bariatric" in t:
        return "Bari+Max"
        
    if "crutch" in t or "cane" in t or "walker" in t or "rollator" in t or "wheelchair" in t or "commode" in t:
        return "Durable Medical Equipment"
        
    if "cup" in t or "syringe" in t or "needle" in t or "gauze" in t or "bandage" in t or "gloves" in t:
        return "Disposable Medical Supplies"
        
    if "surgical" in t or "scalpel" in t or "blade" in t:
        return "Surgical"
        
    if "safety" in t:
        return "Dispo Safety"

    return "Disposable Medical Supplies" # Default fallback for Dynarex misc

# We will iterate and build a new file content
final_lines = []
current_brand = ""
current_title = ""
current_desc = ""
current_cat_line_index = -1

for i, line in enumerate(lines):
    clean_line = line.strip()
    
    # Detect start of object
    if clean_line.startswith('{'):
        current_brand = ""
        current_title = ""
        current_desc = ""
        current_cat_line_index = -1
    
    # Extract data
    # Relaxed key detection
    if "brand" in clean_line and ":" in clean_line:
         m = re.search(r'[\'"]?brand[\'"]?\s*:\s*[\'"](.*?)[\'"]', clean_line)
         if m: current_brand = m.group(1)
         
    if "title" in clean_line and ":" in clean_line:
         m = re.search(r'[\'"]?title[\'"]?\s*:\s*[\'"](.*?)[\'"]', clean_line)
         if m: current_title = m.group(1)
         
    if "desc" in clean_line and ":" in clean_line:
         m = re.search(r'[\'"]?desc[\'"]?\s*:\s*[\'"](.*?)[\'"]', clean_line)
         if m: current_desc = m.group(1)
         
    if "category" in clean_line and ":" in clean_line:
        current_cat_line_index = len(final_lines) # Mark where the category line will be
        
    final_lines.append(line)
    
    # Detect end of object (or strictly, we process when we have enough info? 
    # No, we can process at the end of the object '},'. 
    # But finding the exact closing brace can be tricky with formatting.)
    # Actually, as soon as we have Brand, Title, and Category line index, we can make a decision?
    # No, we need title to make the decision.
    
    if "Dynarex" in current_brand and current_cat_line_index != -1 and current_title:
        # Determine new category
        new_cat = get_category_for_dynarex(current_title, current_desc)
        
        # Replace the category line in final_lines
        # The line looks like: category: 'medical-supply',
        # We want: category: 'Resp-O2',
        
        old_line = final_lines[current_cat_line_index]
        # preserve indentation
        indent = old_line[:old_line.find(old_line.strip())]
        
        # Check if key is quoted in old_line
        key_part = "category"
        if '"category"' in old_line:
            key_part = '"category"'
        elif "'category'" in old_line:
            key_part = "'category'"
            
        new_line = f"{indent}{key_part}: '{new_cat}',"
        
        final_lines[current_cat_line_index] = new_line
        
        # Reset to avoid double processing
        current_cat_line_index = -1

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print("Dynarex categories updated.")
