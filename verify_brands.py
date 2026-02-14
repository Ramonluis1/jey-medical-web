import re

# Read products.js
with open('products.js', 'r', encoding='utf-8') as f:
    p_content = f.read()

# Extract brands keys using re.findall (relaxed spaces)
p_brands = set(re.findall(r'brand\s*:\s*[\'"](.+?)[\'"]', p_content))

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    h_content = f.read()

# Extract logo keys
start_marker = "const brandLogos = {"
end_marker = "};"
start = h_content.find(start_marker)
h_brands = set()
if start != -1:
    # Find matching closing brace technically, but simple substring search for first }; might be enough if no nested objects
    # But brandLogos likely doesn't have nested objects
    end = h_content.find(end_marker, start)
    if end != -1:
        block = h_content[start:end]
        # Extract keys: 'Key': 'Value'
        h_brands = set(re.findall(r"['\"](.+?)['\"]\s*:", block))

print(f"Brands in Products ({len(p_brands)}): {sorted(list(p_brands))}")
print(f"Brands with Logos ({len(h_brands)}): {sorted(list(h_brands))}")

missing = p_brands - h_brands
if missing:
    print("\nMISSING LOGOS FOR:")
    for m in missing:
        print(f" - {m}")
else:
    print("\nAll brands have logos!")
