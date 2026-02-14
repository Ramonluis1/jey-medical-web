import re

FILE_PATH = 'products.js'

print(f"Adding Jey Medical product to {FILE_PATH}...")

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the highest ID
ids = re.findall(r'["\']?id["\']?:\s*(\d+)', content)
max_id = 0
if ids:
    max_id = max(map(int, ids))

new_id = max_id + 1

# Jey Medical product entry
new_entry = f"""    {{
        id: {new_id},
        category: 'medical-supply',
        brand: 'Jey Medical',
        title: 'Medical Supply Catalog',
        price: 0.00,
        desc: 'Comprehensive range of medical supplies distributed by Jey Medical.',
        specs: ['Distributor', 'Medical Equipment', 'Supplies'],
        img: 'FOTOS/LOGO JEY MEDICAL.png'
    }}"""

# Append to array
last_bracket_index = content.rfind(']')
if last_bracket_index != -1:
    pre_content = content[:last_bracket_index].rstrip()
    separator = ",\n" if not pre_content.endswith(',') else "\n"
    
    final_content = content[:last_bracket_index] + separator + new_entry + "\n" + content[last_bracket_index:]
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("Success.")
else:
    print("Error: Could not find array end.")
