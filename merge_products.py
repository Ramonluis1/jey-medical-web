import json
import os

existing_file = 'existing_products_raw.txt'
new_file = 'dynarex_products.json'
output_js = 'products.js'

if not os.path.exists(existing_file):
    print(f"Error: {existing_file} not found")
    exit(1)

if not os.path.exists(new_file):
    print(f"Error: {new_file} not found (Script might still be running)")
    exit(1)

with open(existing_file, 'r', encoding='utf-8') as f:
    existing_raw = f.read().strip()

# Strip outer brackets [ ]
if existing_raw.startswith('[') and existing_raw.endswith(']'):
    existing_content = existing_raw[1:-1].strip()
else:
    # Use as is or fail?
    print("Warning: Existing content format unexpected, using as is")
    existing_content = existing_raw

with open(new_file, 'r', encoding='utf-8') as f:
    new_products = json.load(f)

# Format new products as JS strings (keys unquoted if we want perfect match, but JSON is valid JS too)
# JSON is valid JS, so we can just dump it and strip the outer brackets.
new_content_json = json.dumps(new_products, indent=4)
new_content = new_content_json[1:-1].strip() # Strip [ ]

final_js = f"const products = [\n{existing_content},\n{new_content}\n];"

with open(output_js, 'w', encoding='utf-8') as f:
    f.write(final_js)

print(f"Successfully created {output_js} with merged content.")
